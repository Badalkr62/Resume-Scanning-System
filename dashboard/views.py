from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta  # 🔴 YEH IMPORT MISSING THA, ISILTYE CRASH HO RAHA THA!

# Apne saare models import karein
from django.contrib.auth.models import User
from accounts.models import UserProfile
from job.models import Job
from applications.models import Application

@login_required
def dashboard(request):
    # 1. Database se actual counts lein (Safe try-except block ke sath)
    try:
        today_users = User.objects.count()
        total_jobs = Job.objects.count()
        total_recruiters = UserProfile.objects.filter(role="recruiter").count()
        total_applications = Application.objects.count()
        
        # Last 5 minutes mein active users
        live_users = UserProfile.objects.filter(
            last_seen__gte=timezone.now() - timedelta(minutes=5)
        ).count()
    except Exception as e:
        # Agar migration ya database mein koi issue ho toh fallback values
        today_users = 0
        total_jobs = 0
        total_recruiters = 0
        total_applications = 0
        live_users = 0

    # 2. Saara data ek hi context dict mein dalein
    context = {
        "today_users": today_users,
        "total_jobs": total_jobs,
        "total_recruiters": total_recruiters,
        "total_applications": total_applications,
        "live_users": live_users,
        
        # Aapke dusre function ka static data (agar aapko use karna ho template mein)
        "jobs_count_static": 10,
        "resumes": 45,
        "shortlisted": 15,
        "pending": 30
    }

    # 3. 🔴 PATH CHECK KAREIN: Aapka dashboard file kis folder mein hai?
    # Agar 'recruiter' folder mein hai toh niche wali line use karein:
    return render(request, "recruiter/dashboard.html", context)

    # Agar 'dashboard' folder mein hai toh is line ko uncomment karein:
    # return render(request, "dashboard/dashboard.html", context)