from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from job.models import Job
from applications.models import Application


# ===========================
# Candidate Dashboard
# ===========================

@login_required(login_url="login")
def dashboard(request):

    return render(
        request,
        "candidate/dashboard.html"
    )


@login_required(login_url="login")
def job_list(request):

    jobs = Job.objects.filter(
        status="Active"
    ).order_by("-created_at")

    search = request.GET.get("search")

    if search:
        jobs = jobs.filter(title__icontains=search)

    return render(
        request,
        "candidate/job_list.html",
        {
            "jobs": jobs,
            "search": search,
        },
    )

@login_required(login_url="login")
def job_detail(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        status="Active",
    )

    return render(
        request,
        "candidate/job_detail.html",
        {
            "job": job,
        },
    )


@login_required(login_url="login")
def apply_job(request, id):

    job = get_object_or_404(Job, id=id)

    # Already Applied
    if Application.objects.filter(
        user=request.user,
        job=job
    ).exists():

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect("job_detail", pk=id)

    if request.method == "POST":

        resume = request.FILES.get("resume")

        if not resume:

            messages.error(
                request,
                "Please upload your resume."
            )

            return redirect("apply_job", id=id)

        Application.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            status="Pending",
        )

        messages.success(
            request,
            "Job Applied Successfully."
        )

        return redirect("my_applications")

    return render(
        request,
        "candidate/apply_job.html",
        {
            "job": job,
        },
    )

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
            "applications": applications,
        },
    )