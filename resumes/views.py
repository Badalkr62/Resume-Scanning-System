from django.shortcuts import render, redirect
from .models import Resume
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

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



