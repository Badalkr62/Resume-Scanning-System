from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from applications.models import Application


@login_required(login_url="login")
def dashboard(request):

    total_applications = Application.objects.filter(
        user=request.user
    ).count()

    pending = Application.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    shortlisted = Application.objects.filter(
        user=request.user,
        status="Shortlisted"
    ).count()

    interview = Application.objects.filter(
        user=request.user,
        status="Interview"
    ).count()

    context = {
        "total_applications": total_applications,
        "pending": pending,
        "shortlisted": shortlisted,
        "interview": interview,
    }

    return render(
        request,
        "candidate/dashboard.html",
        context
    )


def job_list(request):

    jobs = Job.objects.all().order_by("-created_at")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        jobs = jobs.filter(title__icontains=search)

    if status:
        jobs = jobs.filter(status=status)

    context = {
        "jobs": jobs,
        "total_jobs": Job.objects.count(),
        "active_jobs": Job.objects.filter(status="Active").count(),
        "closed_jobs": Job.objects.filter(status="Closed").count(),
    }

    return render(request, "recruiter/job_list.html", context)
# ----------------------------
# Add Job
# ----------------------------


def add_job(request):

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("job_list")

    else:

        form = JobForm()

    return render(request, "recruiter/add_job.html", {
        "form": form
    })


# ----------------------------
# Edit Job
# ----------------------------
def edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        form = JobForm(request.POST, instance=job)

        if form.is_valid():

            form.save()

            return redirect("job_list")

    else:

        form = JobForm(instance=job)

    return render(request, "recruiter/edit_job.html", {
        "form": form,
        "job": job
    })


# ----------------------------
# Delete Job
# ----------------------------
def delete_job(request, id):

    job = get_object_or_404(Job, id=id)

    job.delete()

    return redirect("job_list")


# ----------------------------
# Job Details
# ----------------------------
def job_details(request, id):

    job = get_object_or_404(Job, id=id)

    return render(
        request,
        "recruiter/job_details.html",
        {
            "job": job
        }
    )


@login_required(login_url="login")
def my_applications(request):

    applications = Application.objects.filter(
        user=request.user
    ).select_related("job").order_by("-applied_at")

    return render(
        request,
        "candidate/my_applications.html",
        {
            "applications": applications
        }
    )
