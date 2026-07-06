from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from accounts.models import UserProfile
from django.contrib.auth.models import User
from job.models import Job
from applications.models import Application


def dashboard(request):

    total_jobs = Job.objects.count()

    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(
        status="Shortlisted"
    ).count()

    rejected = Application.objects.filter(
        status="Rejected"
    ).count()

    live_users = User.objects.filter(
        is_active=True
    ).count()

    top_candidates = Application.objects.order_by(
        "-match_score"
    )[:5]
    online_users = UserProfile.objects.filter(
        last_seen__gte=timezone.now() - timedelta(minutes=5)
    ).count()

    return render(
        request,
        "recruiter/dashboard.html",   # ya apna actual template path
        {
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "rejected": rejected,
            "live_users": live_users,
            "top_candidates": top_candidates,
             "online_users": online_users,
        }
    )


def job_list(request):
    return render(request, "recruiter/job_list.html")


def add_job(request):
    return render(request, "recruiter/add_job.html")


def edit_job(request, id):
    return render(request, "recruiter/edit_job.html")


def delete_job(request, id):
    return render(request, "recruiter/delete_job.html")


def job_detail(request, id):
    return render(request, "recruiter/job_detail.html")


def application_list(request):
    return render(request, "recruiter/application_list.html")


def application_detail(request, id):
    return render(request, "recruiter/application_detail.html")


def resume_scanning(request):
    return render(request, "recruiter/resume_scanning.html")


def shortlisted_candidates(request):
    return render(request, "recruiter/shortlisted.html")


def interviews(request):
    return render(request, "recruiter/interviews.html")


def offers(request):
    return render(request, "recruiter/offers.html")


def messages(request):
    return render(request, "recruiter/messages.html")


def reports(request):
    return render(request, "recruiter/reports.html")


def settings_page(request):
    return render(request, "recruiter/settings.html")
