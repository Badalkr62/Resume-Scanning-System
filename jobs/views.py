from django.shortcuts import render, redirect, get_object_or_404
from .models import Job


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def add_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST['title'],
            company=request.POST['company'],
            location=request.POST['location'],
            experience=request.POST['experience'],
            salary=request.POST['salary'],
            skills=request.POST['skills'],
            description=request.POST['description']
        )
        return redirect('job_list')

    return render(request, 'jobs/add_job.html')


def edit_job(request, id):
    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        job.title = request.POST['title']
        job.company = request.POST['company']
        job.location = request.POST['location']
        job.experience = request.POST['experience']
        job.salary = request.POST['salary']
        job.skills = request.POST['skills']
        job.description = request.POST['description']
        job.save()

        return redirect('job_list')

    return render(request, 'jobs/edit_job.html', {'job': job})


def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    job.delete()

    return redirect('job_list')
