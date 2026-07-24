from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from job.models import Job


def index(request):
    jobs = Job.objects.filter(status="Active")

    search = request.GET.get("search")
    location = request.GET.get("location")
    job_type = request.GET.get("job_type")

    if search:
        jobs = jobs.filter(title=search)

    if location:
        jobs = jobs.filter(location=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        "jobs": jobs,
        "search": search,
        "location": location,
        "job_type": job_type,
        "job_titles": Job.objects.values_list("title", flat=True).distinct(),
        "locations": Job.objects.values_list("location", flat=True).distinct(),
        "job_types": Job.objects.values_list("job_type", flat=True).distinct(),
    }

    return render(request, "home/index.html", context)


@login_required(login_url="login")
def user_section(request):
    return render(request, "home/user_section.html")


def companies(request):
    company_list = Job.objects.values(
        "company",
        "location"
    ).distinct()

    return render(request, "companies.html", {
        "companies": company_list
    })
