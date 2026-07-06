from django.shortcuts import render, get_object_or_404
from job.models import Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from applications.models import Application
from resumes.models import Resume


def job_list(request):

    jobs = Job.objects.filter(status="Active").order_by("-created_at")

    search = request.GET.get("search")

    if search:
        jobs = jobs.filter(title__icontains=search)

    return render(
        request,
        "candidate/job_list.html",
        {
            "jobs": jobs,
            "search": search,
        }
    )


def job_detail(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        status="Active"
    )

    return render(
        request,
        "candidate/job_detail.html",
        {
            "job": job
        }
    )


@login_required(login_url="login")
def apply_job(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        status="Active"
    )

    # Duplicate Apply Check
    if Application.objects.filter(
        user=request.user,
        job=job
    ).exists():

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect("job_detail", pk=pk)

    # Resume Check
    resume = Resume.objects.filter(
        user=request.user
    ).first()

    if not resume:
        messages.error(
            request,
            "Please upload your resume first."
        )
        return redirect("upload_resume")   # <-- if ke andar hona chahiye

    # Create Application
    Application.objects.create(

        user=request.user,
        job=job,
        resume=resume.resume,
        skills=resume.skills,
        status="Pending"

    )

    # Update Applicant Count
    job.applicants += 1
    job.save()

    messages.success(
        request,
        "Application Submitted Successfully."
    )

    return redirect("my_applications")


def dashboard(request):
    return render(request, "candidate/dashboard.html")


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
