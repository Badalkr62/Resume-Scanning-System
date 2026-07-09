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


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # User Create
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Profile Create
        profile = UserProfile.objects.create(
            user=user
        )

        # Generate OTP
        otp = generateOTP()

        profile.otp = otp
        profile.save()

        # Send Email
        send_mail(
            "Verification OTP",
            f"Your OTP is {otp}",
            None,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "OTP has been sent to your email.")
        return redirect("verify_otp")

    return render(request, "accounts/register.html")

# Login
# ==========================


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

                return redirect("recruiter_dashboard")

            return redirect("user_dashboard")

        messages.error(request, "Invalid Credentials")

    return render(request, "accounts/login.html")


@login_required
def choose_role(request):

    profile = UserProfile.objects.get(user=request.user)

    return render(request, "accounts/choose_role.html", {
        "profile": profile
    })


# ==========================
# Logout
# ==========================
def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect("login")


def forgot_password(request):

    form = PasswordResetForm()

    if request.method == "POST":

        form = PasswordResetForm(request.POST)

        if form.is_valid():

            form.save(
                request=request,
                use_https=False
            )

            messages.success(
                request,
                "Password reset link sent."
            )

            return redirect("login")

    return render(
        request,
        "accounts/forgot_password.html",
        {"form": form}
    )
