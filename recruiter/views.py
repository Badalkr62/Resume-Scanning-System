import os
import logging
import resend

from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth

from accounts.models import UserProfile
from job.models import Job
from applications.models import Application
from applications.ai_match import calculate_match_score
from applications.ai_parser import extract_resume_data
from recruiter.offer_letter import generate_offer_letter

from .models import RecruiterSettings
from .forms import InterviewForm, RecruiterSettingsForm
from job.forms import JobForm

# Setup Logger and Resend API Key
logger = logging.getLogger(__name__)
resend.api_key = getattr(settings, "RESEND_API_KEY", "")


def recruiter_dashboard(request):
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(status="Shortlisted").count()
    rejected = Application.objects.filter(status="Rejected").count()
    selected = Application.objects.filter(status="Selected").count()
    live_users = User.objects.filter(is_active=True).count()

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

    latest_resume = (
        Application.objects
        .order_by("-applied_at")
        .first()
    )

    latest_application = (
        Application.objects
        .order_by("-applied_at")
        .first()
    )

    latest_interview = (
        Application.objects
        .filter(interview_date__isnull=False, status="Interview")
        .order_by("-interview_date", "-interview_time")
        .first()
    )

    latest_job = Job.objects.order_by("-id").first()

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
        "latest_application": latest_application,
    }

    return render(request, "recruiter/dashboard.html", context)


def recruiter_job_list(request):
    jobs = Job.objects.all().order_by("-id")
    return render(request, "recruiter/job_list.html", {"jobs": jobs})


@login_required
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            if hasattr(job, "recruiter"):
                job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect("recruiter_job_list")
    else:
        form = JobForm()

    return render(request, "recruiter/add_job.html", {"form": form})


def edit_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("recruiter_job_list")
    else:
        form = JobForm(instance=job)

    return render(request, "recruiter/edit_job.html", {"form": form, "job": job})


@login_required
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("recruiter_job_list")

    return render(request, "recruiter/delete_job.html", {"job": job})


def application_detail(request, id):
    application = get_object_or_404(Application, id=id)

    matched_skills = []
    missing_skills = []

    if application.resume:
        try:
            data = extract_resume_data(application.resume.path)
            application.skills = data.get("skills", [])

            score, matched_skills, missing_skills = calculate_match_score(
                getattr(application.job, "skills", ""),
                application.skills
            )

            application.match_score = score
            application.ai_summary = (
                f"Matched {len(matched_skills)} skills, "
                f"Missing {len(missing_skills)} skills."
            )
            application.save()
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")

    if request.method == "POST":
        application.recruiter_notes = request.POST.get("notes")
        application.save()
        return redirect("application_detail", id=id)

    return render(
        request,
        "recruiter/application_detail.html",
        {
            "application": application,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        },
    )


def application_list(request):
    applications = Application.objects.order_by("-applied_at")
    return render(request, "recruiter/application_list.html", {"applications": applications})


def recruiter_job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    applications = Application.objects.filter(job=job)

    context = {
        "job": job,
        "applications": applications,
        "total_applications": applications.count(),
    }
    return render(request, "recruiter/job_detail.html", context)


def shortlisted_candidates(request):
    return render(request, "recruiter/shortlisted.html")


def interviews(request):
    interviews_qs = (
        Application.objects
        .filter(interview_date__isnull=False)
        .order_by("interview_date", "interview_time")
    )
    return render(request, "recruiter/interviews.html", {"interviews": interviews_qs})


def schedule_interview(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == "POST":
        form = InterviewForm(request.POST, instance=application)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.status = "Interview"
            interview.save()
            messages.success(request, "Interview Scheduled Successfully.")
            return redirect("interviews")
    else:
        form = InterviewForm(instance=application)

    return render(
        request,
        "recruiter/schedule_interview.html",
        {"form": form, "application": application}
    )


def send_offer_letter(request, application_id):
    # Fetch actual application object
    application = get_object_or_404(Application, id=application_id)

    # Safely get candidate object (handles 'user' or 'applicant' model fields)
    candidate = getattr(application, "applicant", None) or getattr(
        application, "user", None)

    if not candidate or not candidate.email:
        messages.error(request, "Candidate email address not found.")
        return redirect("application_detail", id=application_id)

    applicant_name = (
        candidate.first_name if hasattr(candidate, "first_name") and candidate.first_name
        else getattr(candidate, "username", "Candidate")
    )
    job_title = getattr(application.job, "title", "the position")
    applicant_email = candidate.email

    try:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 20px; margin: 0;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 520px; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 32px;">
                <tr>
                    <td>
                        <h2 style="color: #2563eb; font-size: 20px; margin-top: 0;">Smart Recruiter</h2>
                        <p style="font-size: 15px; color: #374151;">Dear <strong>{applicant_name}</strong>,</p>
                        <p style="font-size: 14px; color: #4b5563; line-height: 1.5;">
                            We are pleased to extend an offer for the position of <strong>{job_title}</strong> at our company!
                        </p>
                        <p style="font-size: 14px; color: #4b5563; line-height: 1.5;">
                            Please log in to your candidate portal to review the offer details and complete the next steps.
                        </p>
                        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;" />
                        <p style="font-size: 12px; color: #6b7280; margin-bottom: 0;">Best regards,<br>Smart Recruiter Hiring Team</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        plain_text = f"Dear {applicant_name},\n\nWe are pleased to offer you the position of {job_title}.\nPlease log in to your candidate portal for details.\n\nBest regards,\nSmart Recruiter Hiring Team"

        response = resend.Emails.send({
            "from": "Smart Recruiter <otp@myjobportal.online>",
            "to": [applicant_email],
            "subject": f"Job Offer: {job_title}",
            "html": html_content,
            "text": plain_text,
            "headers": {
                "X-Entity-Ref-ID": f"offer-{application_id}"
            }
        })

        logger.info(f"✅ Offer letter sent via Resend: {response}")
        messages.success(request, "Offer letter sent successfully!")

    except Exception as e:
        logger.error(f"❌ Offer Letter Email Error: {e}")
        messages.error(request, f"Unable to send offer letter. Error: {e}")

    return redirect("application_detail", id=application_id)


def recruiter_messages(request):
    return render(request, "recruiter/messages.html")


@login_required
def settings_page(request):
    settings_obj, created = RecruiterSettings.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = RecruiterSettingsForm(
            request.POST,
            request.FILES,
            instance=settings_obj
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect("settings_page")
    else:
        form = RecruiterSettingsForm(instance=settings_obj)

    return render(
        request,
        "recruiter/settings.html",
        {"form": form, "settings": settings_obj}
    )
