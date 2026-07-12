from django.contrib import messages
from job.models import Job
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm
from applications.models import Application
from accounts.models import UserProfile


# ==========================================
# Candidate Dashboard
# ==========================================
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

    return render(request, "candidate/dashboard.html", context)

@login_required(login_url="login")
def job_list(request):

    jobs = Job.objects.filter(status="Active").order_by("-created_at")

    search = request.GET.get("search")
    location = request.GET.get("location")
    job_type = request.GET.get("job_type")

    if search:
        jobs = jobs.filter(title__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        "jobs": jobs,
        "search": search,
        "location": location,
        "job_type": job_type,
    }

    return render(request, "candidate/job_list.html", context)

@login_required(login_url="login")
def job_details(request, id):

    job = get_object_or_404(Job, id=id)

    return render(
        request,
        "candidate/job_detail.html",
        {
            "job": job
        }
    )

@login_required(login_url="login")
def add_job(request):

    if request.method == "POST":

        form = JobForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Job Added Successfully")

            return redirect("job_list")

    else:

        form = JobForm()

    return render(
        request,
        "recruiter/add_job.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
def edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        form = JobForm(
            request.POST,
            request.FILES,
            instance=job
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Job Updated Successfully")

            return redirect("job_list")

    else:

        form = JobForm(instance=job)

    return render(
        request,
        "recruiter/edit_job.html",
        {
            "form": form,
            "job": job
        }
    )

@login_required(login_url="login")
def delete_job(request, id):

    job = get_object_or_404(Job, id=id)

    job.delete()

    return redirect("job_list")

@login_required(login_url="login")
def my_applications(request):

    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "candidate/my_applications.html",
        {
            "applications": applications
        }
    )
