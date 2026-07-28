# from datetime import timedelta
# import os
# import random
# import traceback
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models import Q
# from django.shortcuts import redirect, render
# from django.utils import timezone
# import resend
# from .models import UserProfile
# from .utils import generateOTP

# # Environment variable se key read karein (Hardcode mat karein)
# resend.api_key = os.getenv("RESEND_API_KEY")


# def register(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         role = request.POST.get("role", "candidate")
#         phone = request.POST.get("phone")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect("register")

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#             return redirect("register")

#         if phone and UserProfile.objects.filter(phone=phone).exists():
#             messages.error(request, "Phone number already exists.")
#             return redirect("register")

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#         )

#         otp = generateOTP()

#         profile = UserProfile.objects.create(
#             user=user,
#             role=role,
#             phone=phone,
#             otp=otp,
#             otp_created=timezone.now(),
#             is_verified=False,
#             email_verified=False,
#             phone_verified=False,
#         )

#         # Send OTP via Resend API
#         try:
#             resend.Emails.send(
#                 {
#                     "from": "Job Portal <otp@myjobportal.online>",
#                     "to": [email],
#                     "subject": "Verification OTP",
#                     "html": f"<p>Hello <strong>{username}</strong>,</p><p>Your OTP for verification is: <strong>{otp}</strong></p><p>Valid for 10 minutes.</p>",
#                 }
#             )
#             print("✅ EMAIL SENT SUCCESSFULLY VIA RESEND")

#         except Exception as e:
#             print("❌ EMAIL ERROR:", str(e))
#             profile.delete()
#             user.delete()
#             messages.error(
#                 request, "Unable to send OTP email. Please try again later."
#             )
#             return redirect("register")

#         request.session["user_id"] = user.id
#         messages.success(request, "OTP sent successfully.")
#         return redirect("verify_otp")

#     return render(request, "accounts/register.html")


# def user_login(request):

#     if request.method == "POST":

#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         remember = request.POST.get("remember")

#         user = None

#         if User.objects.filter(username=username).exists():
#             user_obj = User.objects.get(username=username)

#         elif User.objects.filter(email=username).exists():
#             user_obj = User.objects.get(email=username)

#         elif UserProfile.objects.filter(phone=username).exists():
#             profile = UserProfile.objects.get(phone=username)
#             user_obj = profile.user

#         else:
#             user_obj = None

#         if user_obj:
#             user = authenticate(
#                 username=user_obj.username,
#                 password=password
#             )

#         if user:

#             login(request, user)

#             profile = UserProfile.objects.get(user=user)
#             profile.last_seen = timezone.now()
#             profile.save()

#             if not remember:
#                 request.session.set_expiry(0)

#             # ✅ Success Message
#             messages.success(request, "Login Successfully")

#             if profile.role == "recruiter":
#                 return redirect("choose_role")

#             return redirect("home")

#         messages.error(request, "Invalid Credentials")

#     return render(request, "accounts/login.html")


# @login_required
# def choose_role(request):
#     profile = UserProfile.objects.get(user=request.user)

#     return render(request, "accounts/choose_role.html", {
#         "profile": profile
#     })


# def user_logout(request):
#     logout(request)
#     messages.success(request, "Logout Successfully")
#     return redirect("home")


# def forgot_password(request):

#     if request.method == "POST":

#         email = request.POST.get("email")

#         if User.objects.filter(email=email).exists():

#             # Generate 6 digit OTP
#             otp = random.randint(100000, 999999)

#             # Save OTP in session
#             request.session["reset_email"] = email
#             request.session["reset_otp"] = str(otp)

#             # Send Email
#             send_mail(
#                 subject="Password Reset OTP",
#                 message=f"Your OTP is {otp}. Do not share it with anyone.",
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#             messages.success(request, "OTP sent successfully.")
#             return redirect("verify_reset_otp")

#         else:
#             messages.error(request, "Email not registered.")

#     return render(request, "accounts/forgot_password.html")


# def verify_otp(request):

#     if request.method == "POST":

#         otp = request.POST.get("otp")

#         if "user_id" not in request.session:
#             messages.error(request, "Session expired. Please register again.")
#             return redirect("register")

#         try:
#             user = User.objects.get(id=request.session["user_id"])
#             profile = UserProfile.objects.get(user=user)

#         except (User.DoesNotExist, UserProfile.DoesNotExist):
#             messages.error(request, "User not found.")
#             return redirect("register")

#         # OTP Validation
#         if profile.otp == otp:

#             profile.is_verified = True
#             profile.email_verified = True
#             profile.phone_verified = True
#             profile.otp = ""
#             profile.save()

#             login(
#                 request,
#                 user,
#                 backend="django.contrib.auth.backends.ModelBackend"
#             )

#             # Remove session
#             request.session.pop("user_id", None)

#             messages.success(
#                 request,
#                 "Account Verified Successfully."
#             )

#             # Always go to Choose Role page
#             return redirect("choose_role")

#         else:
#             messages.error(request, "Invalid OTP.")

#     return render(request, "accounts/otp_verify.html")


# def verify_reset_otp(request):

#     if "reset_email" not in request.session:
#         messages.error(request, "Session expired.")
#         return redirect("forgot_password")

#     if request.method == "POST":

#         entered_otp = request.POST.get("otp")

#         saved_otp = request.session.get("reset_otp")

#         if entered_otp == saved_otp:

#             messages.success(request, "OTP verified successfully.")
#             return redirect("reset_password")

#         messages.error(request, "Invalid OTP")

#     return render(request, "accounts/otp_verify.html")


# def reset_password(request):

#     if "reset_email" not in request.session:
#         messages.error(request, "Session expired.")
#         return redirect("forgot_password")

#     if request.method == "POST":

#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect("reset_password")

#         email = request.session.get("reset_email")

#         user = User.objects.get(email=email)

#         user.set_password(password1)
#         user.save()

#         request.session.pop("reset_email", None)
#         request.session.pop("reset_otp", None)

#         messages.success(request, "Password updated successfully.")
#         return redirect("login")

#     return render(request, "accounts/reset_password.html")


# def resend_otp(request):

#     if "user_id" not in request.session:

#         return redirect("register")

#     user = User.objects.get(
#         id=request.session["user_id"]
#     )

#     profile = UserProfile.objects.get(
#         user=user
#     )

#     otp = generateOTP()

#     profile.otp = otp

#     profile.otp_created = timezone.now()

#     profile.save()

#     send_mail(

#         "New Verification OTP",

#         f"Your new OTP is {otp}",

#         None,

#         [user.email],

#         fail_silently=False,

#     )

#     messages.success(
#         request,
#         "New OTP sent successfully."
#     )

#     return redirect("verify_otp")


from datetime import timedelta
import os
import random
import logging
import traceback
import resend

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import UserProfile
from .utils import generateOTP

logger = logging.getLogger(__name__)

# Initialize Resend API key
resend.api_key = os.getenv("RESEND_API_KEY")


def send_otp_email(to_email, username, otp_code, subject="Smart Recruiter Access Code"):
    """
    Anti-Spam Optimized OTP Email Function
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 20px; margin: 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 32px;">
            <tr>
                <td>
                    <h2 style="color: #111827; font-size: 20px; margin-top: 0;">Smart Recruiter</h2>
                    <p style="font-size: 15px; color: #374151;">Hi {username},</p>
                    <p style="font-size: 14px; color: #4b5563;">Use the code below to complete your login or registration:</p>
                    
                    <div style="background-color: #f3f4f6; border-radius: 6px; padding: 16px; text-align: center; margin: 20px 0;">
                        <span style="font-size: 32px; font-weight: 700; letter-spacing: 6px; color: #1d4ed8;">{otp_code}</span>
                    </div>
                    
                    <p style="font-size: 13px; color: #6b7280;">This security code is valid for 10 minutes.</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    plain_text = f"Hi {username},\n\nYour Smart Recruiter code is: {otp_code}\nValid for 10 minutes."

    try:
        response = resend.Emails.send({
            "from": "Smart Recruiter <otp@myjobportal.online>",
            "to": [to_email],
            "subject": subject,
            "html": html_content,
            "text": plain_text,
            "headers": {
                "X-Entity-Ref-ID": f"sec-{otp_code}"
            }
        })
        logger.info(f"✅ User OTP Sent: {response}")
        return True
    except Exception as e:
        logger.error(f"❌ User OTP Error: {e}")
        return False


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "candidate")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        if phone and UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        otp = generateOTP()

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

        # Send OTP Email using Clean Helper
        sent = send_otp_email(
            to_email=email,
            username=username,
            otp_code=otp,
            subject="Your Account Verification Code"
        )

        if not sent:
            profile.delete()
            user.delete()
            messages.error(
                request, "Unable to send OTP email. Please try again later."
            )
            return redirect("register")

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

            messages.success(request, "Login Successfully")

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
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)

            request.session["reset_email"] = email
            request.session["reset_otp"] = str(otp)

            # Send OTP using Resend API instead of old send_mail
            send_otp_email(
                to_email=email,
                username=user.username,
                otp_code=otp,
                subject="Password Reset Code"
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

        if str(profile.otp).strip() == str(otp).strip():
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

            request.session.pop("user_id", None)
            messages.success(
                request,
                "Account Verified Successfully."
            )
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

        if str(entered_otp).strip() == str(saved_otp).strip():
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

    user = User.objects.get(id=request.session["user_id"])
    profile = UserProfile.objects.get(user=user)

    otp = generateOTP()
    profile.otp = otp
    profile.otp_created = timezone.now()
    profile.save()

    # Replaced send_mail with Resend API Helper
    send_otp_email(
        to_email=user.email,
        username=user.username,
        otp_code=otp,
        subject="Your New Verification OTP"
    )

    messages.success(request, "New OTP sent successfully.")
    return redirect("verify_otp")
