from django.shortcuts import render, redirect
from .models import Resume
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def upload_resume(request):

    if request.method == "POST":

        Resume.objects.create(

            name=request.POST['name'],

            email=request.POST['email'],

            phone=request.POST['phone'],

            resume=request.FILES['resume']

        )

        return redirect('resume_list')

    return render(
        request,
        'resumes/upload_resume.html'
    )


def resume_list(request):

    resumes = Resume.objects.all()

    return render(
        request,
        'resumes/resume_list.html',
        {'resumes': resumes}
    )
