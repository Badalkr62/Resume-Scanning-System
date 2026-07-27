from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from applications.models import Application
from django.contrib.auth.decorators import login_required

# Correct Model Imports
from .models import Job, JobApplication
from .forms import JobForm


@login_required(login_url="login")
def dashboard(request):
    total_applications = JobApplication.objects.filter(
        applicant=request.user).count()

    context = {
        "total_applications": total_applications,
    }

    return render(request, "candidate/dashboard.html", context)


# ==========================================
# Job List (With Search & Filter)
# ==========================================
@login_required(login_url="login")
def job_list(request):
    jobs = Job.objects.all().order_by("-id")

    search = request.GET.get("search")
    location = request.GET.get("location")
    job_type = request.GET.get("job_type")

    if search:
        jobs = jobs.filter(title__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Update status and check applied
    for job in jobs:
        if job.remaining_openings <= 0:
            job.status = "Closed"
        else:
            job.status = "Active"

        job.save(update_fields=["status"])

        job.already_applied = Application.objects.filter(
            job=job,
            user=request.user
        ).exists()

    context = {
        "jobs": jobs,
        "search": search,
        "location": location,
        "job_type": job_type,
    }

    return render(request, "candidate/job_list.html", context)


@login_required(login_url="login")
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, status="Active")

    applied = Application.objects.filter(job=job).count()

    remaining = max(job.openings - applied, 0)
    if job.remaining_openings <= 0:
        job.status = "Closed"
    else:
        job.status = "Active"

    job.save(update_fields=["status"])

    already_applied = Application.objects.filter(
        job=job,
        user=request.user
    ).exists()

    return render(
        request,
        "candidate/job_detail.html",
        {
            "job": job,
            "applied": applied,
            "remaining": remaining,
            "already_applied": already_applied,
        },
    )


@login_required(login_url="login")
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)

    # Auto update status
    if job.remaining_openings <= 0:
        job.status = "Closed"
    else:
        job.status = "Active"

    job.save(update_fields=["status"])

    # Job Closed
    if job.status == "Closed":
        messages.error(request, "This job is closed.")
        return redirect("job_detail", pk=job.id)

    # Already Applied
    if Application.objects.filter(
        user=request.user,
        job=job
    ).exists():

        messages.warning(request, "You have already applied.")
        return redirect("job_detail", pk=job.id)

    if request.method == "POST":

        resume = request.FILES.get("resume")

        if not resume:
            messages.error(request, "Please upload your resume.")
            return redirect("apply_job", id=job.id)

        Application.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            status="Pending",
        )

        # Update status again after application
        job.update_status()

        messages.success(request, "Application submitted successfully.")
        return redirect("my_applications")

    return render(request, "candidate/apply_job.html", {
        "job": job,
    })


@login_required(login_url="login")
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Job Added Successfully")
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "recruiter/add_job.html", {"form": form})


@login_required(login_url="login")
def edit_job(request, id):
    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job Updated Successfully")
            return redirect("job_list")
    else:
        form = JobForm(instance=job)

    return render(request, "recruiter/edit_job.html", {"form": form, "job": job})


@login_required(login_url="login")
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    job.delete()
    messages.success(request, "Job Deleted Successfully")
    return redirect("job_list")


@login_required(login_url="login")
def my_applications(request):
    applications = (
        JobApplication.objects
        .filter(applicant=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "candidate/my_applications.html",
        {"applications": applications}
    )
