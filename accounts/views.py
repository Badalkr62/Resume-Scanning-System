import random
from django.shortcuts import redirect, render
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.db import models
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import UserProfile
from .utils import generateOTP
from django.utils import timezone
from django.conf import settings


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "candidate")
        phone = request.POST.get("phone")

        # Username Check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Email Check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Phone Check
        if phone and UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("register")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Generate OTP
        otp = generateOTP()

        # Create Profile
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            otp=otp,
            otp_created=timezone.now(),
            is_verified=False,
            email_verified=False,
            phone_verified=False,
        )

        # Send OTP Email
        send_mail(
            subject="Verification OTP",
            message=f"Hello {username},\n\nYour OTP is: {otp}\n\nValid for 10 minutes.",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        # Store user id in session
        request.session["user_id"] = user.id

        messages.success(request, "OTP sent successfully.")
        return redirect("verify_otp")

    return render(request, "accounts/register.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        remember = request.POST.get("remember")

        user = None

        if User.objects.filter(username=username).exists():

            user_obj = User.objects.get(username=username)

        elif User.objects.filter(email=username).exists():

            user_obj = User.objects.get(email=username)

        elif UserProfile.objects.filter(phone=username).exists():

            profile = UserProfile.objects.get(phone=username)

            user_obj = profile.user

        else:

            user_obj = None

        if user_obj:

            user = authenticate(
                username=user_obj.username,
                password=password
            )

        if user:

            login(request, user)

            profile = UserProfile.objects.get(user=user)

            profile.last_seen = timezone.now()

            profile.save()

            if not remember:

                request.session.set_expiry(0)

            if profile.role == "recruiter":

                return redirect("choose_role")

            return redirect("home")

        messages.error(request, "Invalid Credentials")

    return render(request, "accounts/login.html")


@login_required
def choose_role(request):
    profile = UserProfile.objects.get(user=request.user)

    return render(request, "accounts/choose_role.html", {
        "profile": profile
    })


def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect("home")

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():

            # Generate 6 digit OTP
            otp = random.randint(100000, 999999)

            # Save OTP in session
            request.session["reset_email"] = email
            request.session["reset_otp"] = str(otp)

            # Send Email
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp}. Do not share it with anyone.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent successfully.")
            return redirect("verify_reset_otp")

        else:
            messages.error(request, "Email not registered.")

    return render(request, "accounts/forgot_password.html")


def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")

        if "user_id" not in request.session:
            messages.error(request, "Session expired. Please register again.")
            return redirect("register")

        try:
            user = User.objects.get(id=request.session["user_id"])
            profile = UserProfile.objects.get(user=user)

        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "User not found.")
            return redirect("register")

        # OTP Validation
        if profile.otp == otp:

            profile.is_verified = True
            profile.email_verified = True
            profile.phone_verified = True
            profile.otp = ""
            profile.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )

            # Remove session
            request.session.pop("user_id", None)

            messages.success(
                request,
                "Account Verified Successfully."
            )

            # Always go to Choose Role page
            return redirect("choose_role")

        else:
            messages.error(request, "Invalid OTP.")

    return render(request, "accounts/otp_verify.html")


def verify_reset_otp(request):

    if "reset_email" not in request.session:
        messages.error(request, "Session expired.")
        return redirect("forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:

            messages.success(request, "OTP verified successfully.")
            return redirect("reset_password")

        messages.error(request, "Invalid OTP")

    return render(request, "accounts/otp_verify.html")


def reset_password(request):

    if "reset_email" not in request.session:
        messages.error(request, "Session expired.")
        return redirect("forgot_password")

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        email = request.session.get("reset_email")

        user = User.objects.get(email=email)

        user.set_password(password1)
        user.save()

        request.session.pop("reset_email", None)
        request.session.pop("reset_otp", None)

        messages.success(request, "Password updated successfully.")
        return redirect("login")

    return render(request, "accounts/reset_password.html")


def resend_otp(request):

    if "user_id" not in request.session:

        return redirect("register")

    user = User.objects.get(
        id=request.session["user_id"]
    )

    profile = UserProfile.objects.get(
        user=user
    )

    otp = generateOTP()

    profile.otp = otp

    profile.otp_created = timezone.now()

    profile.save()

    send_mail(

        "New Verification OTP",

        f"Your new OTP is {otp}",

        None,

        [user.email],

        fail_silently=False,

    )

    messages.success(
        request,
        "New OTP sent successfully."
    )

    return redirect("verify_otp")
