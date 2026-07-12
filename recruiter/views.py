import os
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile
from job.models import Job
from applications.models import Application
from recruiter.offer_letter import generate_offer_letter
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .forms import InterviewForm
from .models import RecruiterSettings
from .forms import RecruiterSettingsForm
from django.contrib.auth.decorators import login_required
from job.forms import JobForm


def recruiter_dashboard(request):

    total_jobs = Job.objects.count()

    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(
        status="Shortlisted"
    ).count()

    rejected = Application.objects.filter(
        status="Rejected"
    ).count()

    selected = Application.objects.filter(
        status="Selected"
    ).count()

    live_users = User.objects.filter(
        is_active=True
    ).count()

    applications_per_job = (
        Application.objects
        .values("job__title")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    monthly_applications = (
        Application.objects
        .annotate(month=TruncMonth("applied_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    status_distribution = (
        Application.objects
        .values("status")
        .annotate(total=Count("id"))
    )

    top_candidates = (
        Application.objects
        .order_by("-match_score")[:5]
    )

    online_users = UserProfile.objects.filter(
        last_seen__gte=timezone.now() - timedelta(minutes=5)
    ).count()

    selected = Application.objects.filter(
        status="Selected"
    ).count()

    latest_resume = (
        Application.objects
        .select_related("user")
        .order_by("-applied_at")
        .first()
    )

    latest_job = (
        Job.objects
        .order_by("-id")
        .first()
    )

    latest_interview = (
        Application.objects
        .filter(interview_date__isnull=False)
        .order_by("-interview_date", "-interview_time")
        .first()
    )

    # Latest Resume Uploaded
    latest_resume = (
        Application.objects
        .select_related("user")
        .order_by("-applied_at")
        .first()
    )

    # Latest Candidate Applied
    latest_application = (
        Application.objects
        .select_related("user", "job")
        .order_by("-applied_at")
        .first()
    )

    # Latest Interview
    latest_interview = (
        Application.objects
        .filter(
            interview_date__isnull=False,
            status="Interview"
        )
        .select_related("user", "job")
        .order_by("-interview_date", "-interview_time")
        .first()
    )

    # Latest Job
    latest_job = Job.objects.order_by("-created_at").first()

    context = {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "selected": selected,
        "live_users": live_users,
        "top_candidates": top_candidates,
        "online_users": online_users,
        "applications_per_job": applications_per_job,
        "monthly_applications": monthly_applications,
        "status_distribution": status_distribution,
        "latest_resume": latest_resume,
        "latest_job": latest_job,
        "latest_interview": latest_interview,
        "latest_resume": latest_resume,
        "latest_application": latest_application,
        "latest_interview": latest_interview,
        "latest_job": latest_job,
    }

    return render(
        request,
        "recruiter/dashboard.html",
        context
    )


def recruiter_job_list(request):

    jobs = Job.objects.all().order_by("-created_at")

    return render(
        request,
        "recruiter/job_list.html",
        {
            "jobs": jobs
        }
    )


def add_job(request):
    return render(request, "recruiter/add_job.html")


def edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        form = JobForm(
            request.POST,
            request.FILES,
            instance=job,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Job Updated Successfully")
            return redirect("recruiter_job_list")

    else:
        form = JobForm(instance=job)

    return render(
        request,
        "recruiter/edit_job.html",
        {
            "form": form,
            "job": job,
        },
    )


def delete_job(request, id):
    return render(request, "recruiter/delete_job.html")


def recruiter_job_detail(request, id):

    job = get_object_or_404(Job, id=id)

    return render(
        request,
        "recruiter/job_detail.html",
        {
            "job": job
        }
    )


def application_list(request):

    applications = (
        Application.objects
        .select_related("user", "job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "recruiter/application_list.html",
        {
            "applications": applications
        }
    )


def application_detail(request, id):
    return render(request, "recruiter/application_detail.html")


def shortlisted_candidates(request):
    return render(request, "recruiter/shortlisted.html")


def interviews(request):

    interviews = (
        Application.objects
        .filter(interview_date__isnull=False)
        .select_related("user", "job")
        .order_by("interview_date", "interview_time")
    )

    return render(
        request,
        "recruiter/interviews.html",
        {
            "interviews": interviews
        }
    )


def schedule_interview(request, pk):

    application = get_object_or_404(
        Application,
        pk=pk
    )

    if request.method == "POST":

        form = InterviewForm(
            request.POST,
            instance=application
        )

        if form.is_valid():

            interview = form.save(commit=False)

            interview.status = "Interview"

            interview.save()

            messages.success(
                request,
                "Interview Scheduled Successfully."
            )

            return redirect("interviews")

    else:

        form = InterviewForm(
            instance=application
        )

    return render(
        request,
        "recruiter/schedule_interview.html",
        {
            "form": form,
            "application": application,
        }
    )


def send_offer_letter(request, pk):

    application = get_object_or_404(
        Application,
        pk=pk
    )

    html = render_to_string(
        "emails/offer_letter.html",
        {
            "candidate": application.user.get_full_name() or application.user.username,
            "company": application.job.company,
            "job": application.job.title,
            "department": "Software Development",
            "salary": application.job.salary,
            "joining_date": "15 July 2026",
            "location": application.job.location,
            "offer_letter": "#",
        }
    )

    email = EmailMultiAlternatives(
        subject=f"Offer of Employment | {application.job.company}",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[application.user.email]
    )

    email.attach_alternative(html, "text/html")

    pdf_path = generate_offer_letter(application)

    if os.path.exists(pdf_path):
        email.attach_file(pdf_path)

    email.send()

    application.status = "Selected"
    application.save()

    messages.success(
        request,
        "Offer Letter sent successfully."
    )

    return redirect("application_detail", pk=pk)


def recruiter_messages(request):
    return render(request, "recruiter/messages.html")


def reports(request):
    return render(request, "recruiter/reports.html")


@login_required
def settings_page(request):

    settings_obj, created = RecruiterSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = RecruiterSettingsForm(
            request.POST,
            request.FILES,
            instance=settings_obj
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Settings Updated Successfully."
            )

            return redirect("settings_page")

    else:

        form = RecruiterSettingsForm(
            instance=settings_obj
        )

    return render(
        request,
        "recruiter/settings.html",
        {
            "form": form,
            "settings": settings_obj,
        }
    )
