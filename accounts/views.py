from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'accounts/register.html')


# def user_login(request):

#     if request.method == "POST":

#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user:

#             login(request, user)

#             return redirect('/')

#     return render(request, 'accounts/login.html')


def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            messages.success(request, "Login successful 🎉")
            return redirect('/')

        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, 'accounts/login.html')


def user_logout(request):

    logout(request)

    return redirect('home')
