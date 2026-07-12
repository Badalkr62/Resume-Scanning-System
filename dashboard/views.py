from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# 🔴 YEH IMPORT MISSING THA, ISILTYE CRASH HO RAHA THA!
from datetime import timedelta
from applications.models import Application
# Apne saare models import karein
from django.contrib.auth.models import User
from accounts.models import UserProfile

from applications.models import Application
from job.models import Job
from django.db.models import Count


@login_required
@login_required
def dashboard(request):

    today_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_recruiters = UserProfile.objects.filter(role="recruiter").count()
    total_applications = Application.objects.count()

    live_users = UserProfile.objects.filter(
        last_seen__gte=timezone.now() - timedelta(minutes=5)
    ).count()

    rejected = Application.objects.filter(status="Rejected").count()

    online_users = live_users

    latest_resume = Application.objects.order_by("-applied_at").first()

    latest_application = Application.objects.order_by("-applied_at").first()

    latest_interview = Application.objects.filter(
        interview_date__isnull=False
    ).order_by("-interview_date").first()

    latest_job = Job.objects.order_by("-created_at").first()

    top_candidates = Application.objects.order_by("-match_score")[:10]

    applications_per_job = (
        Application.objects.values("job__title")
        .annotate(total=Count("id"))
    )

    status_distribution = (
        Application.objects.values("status")
        .annotate(total=Count("id"))
    )

    monthly_applications = []

    context = {
        "today_users": today_users,
        "total_jobs": total_jobs,
        "total_recruiters": total_recruiters,
        "total_applications": total_applications,
        "live_users": live_users,
        "online_users": online_users,
        "rejected": rejected,

        "latest_resume": latest_resume,
        "latest_application": latest_application,
        "latest_interview": latest_interview,
        "latest_job": latest_job,

        "top_candidates": top_candidates,
        "applications_per_job": applications_per_job,
        "status_distribution": status_distribution,
        "monthly_applications": monthly_applications,

        "jobs_count_static": 10,
        "resumes": 45,
        "shortlisted": 15,
        "pending": 30,
    }

    return render(request, "recruiter/dashboard.html", context)