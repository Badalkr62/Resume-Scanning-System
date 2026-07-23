from applications.models import Application
import os
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Resume
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def upload_resume(request):
    if request.method == "POST":
        Resume.objects.update_or_create(
            user=request.user,
            defaults={
                "name": request.POST["name"],
                "email": request.POST["email"],
                "phone": request.POST["phone"],
                "resume": request.FILES["resume"],
            }
        )

        return redirect("resume_list")

    return render(
        request,
        "resumes/upload_resume.html"
    )


@login_required(login_url="login")
def resume_list(request):

    resumes = Resume.objects.filter(user=request.user)

    return render(
        request,
        "resumes/resume_list.html",
        {
            "resumes": resumes
        }
    )

