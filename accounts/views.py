from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


# ==========================
# Register
# ==========================
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, "Registration Successful.")
        return redirect("login")

    return render(request, "accounts/register.html")

# ==========================
# Login
# ==========================


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": "candidate"}
            )

            if profile.role == "recruiter":
                return redirect("choose_role")

            return redirect("home")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")
# Choose Role
# ==========================


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
