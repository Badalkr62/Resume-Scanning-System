from job.models import Job
from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def features(request):
    return render(request, 'home/features.html')


def how_it_works(request):
    return render(request, 'home/howitworks.html')


def contact(request):
    return render(request, 'home/contact.html')


def user_section(request):

    trending_jobs = Job.objects.filter(
        status="Active"
    ).order_by("-id")[:5]

    return render(
        request,
        "user/user_section.html",
        {
            "trending_jobs": trending_jobs
        }
    )
