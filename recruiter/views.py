from datetime import datetime
import random
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


def send_offer_letter(request, pk=None, application_id=None):
    app_id = pk or application_id
    application = get_object_or_404(Application, id=app_id)

    # Candidate object safe fetching
    candidate = getattr(application, "applicant", None) or getattr(
        application, "user", None)

    if not candidate or not candidate.email:
        messages.error(request, "Candidate email address not found.")
        return redirect("application_detail", id=app_id)

    # Data Extracting
    applicant_name = candidate.get_full_name() if hasattr(candidate,
                                                          'get_full_name') and candidate.get_full_name() else getattr(candidate, "username", "Candidate")
    applicant_email = candidate.email
    mobile = getattr(candidate, "phone_number",
                     getattr(candidate, "mobile", "N/A"))
    if hasattr(candidate, 'userprofile') and hasattr(candidate.userprofile, 'phone'):
        mobile = candidate.userprofile.phone

    job = getattr(application, "job", None)
    job_title = getattr(job, "title", "Software Developer")
    company_name = getattr(job, "company_name", getattr(
        job, "company", "TechNova Solutions Pvt. Ltd."))
    location = getattr(job, "location", "Ranchi, Jharkhand")
    salary = getattr(job, "salary", getattr(
        job, "salary_range", "5 LPA - 8 LPA"))
    department = getattr(job, "department", "Software Development")

    # Dynamic Dates & IDs
    today_date = datetime.now().strftime("%d %B %Y")
    offer_no = f"ATS-{random.randint(10000, 99999)}"
    candidate_id = f"ATS-{candidate.id if hasattr(candidate, 'id') else app_id}"
    joining_date = (datetime.now() + timedelta(days=15)).strftime("%d %B %Y")

    # EXACT HTML TEMPLATE matching your image
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #111; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 680px; margin: 0 auto; background: #ffffff; padding: 40px; border: 1px solid #ddd; border-radius: 4px; }}
            .header {{ text-align: center; margin-bottom: 25px; }}
            .header h2 {{ font-size: 22px; font-weight: bold; margin: 0 0 5px 0; color: #000; }}
            .header h4 {{ font-size: 15px; font-weight: bold; margin: 0 0 15px 0; color: #333; }}
            .address {{ font-size: 11px; color: #555; line-height: 1.4; border-bottom: 1px solid #ccc; padding-bottom: 15px; }}
            .title {{ text-align: center; font-size: 16px; font-weight: bold; margin: 25px 0; letter-spacing: 1px; text-transform: uppercase; }}
            .content {{ font-size: 13px; line-height: 1.6; color: #222; }}
            .meta-info {{ margin: 15px 0; font-size: 13px; line-height: 1.7; }}
            .meta-info strong {{ width: 140px; display: inline-block; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }}
            table, th, td {{ border: 1px solid #888; }}
            td {{ padding: 8px 12px; }}
            td.label {{ background-color: #eaeaea; font-weight: bold; width: 35%; }}
            .section-title {{ font-size: 15px; font-weight: bold; margin: 25px 0 10px 0; text-align: center; }}
            .terms {{ font-size: 12px; line-height: 1.7; padding-left: 18px; margin-bottom: 30px; }}
            .footer {{ margin-top: 40px; font-size: 13px; }}
            .stamp {{ margin-top: 15px; display: inline-block; padding: 10px 15px; border: 2px dashed #1d4ed8; color: #1d4ed8; font-weight: bold; font-size: 11px; border-radius: 50%; text-align: center; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Global Talent Solutions</h2>
                <h4>Talent Acquisition Team</h4>
                <div class="address">
                    Smart Recruiter Technologies Pvt. Ltd.<br>
                    Hazaribagh, Jharkhand - 825301<br>
                    www.smartresumeats.com
                </div>
            </div>

            <div class="title">OFFICIAL OFFER LETTER</div>

            <div class="content">
                <p><strong>Date :</strong> {today_date}</p>
                <p>Dear <strong>{applicant_name}</strong>,</p>
                <p>Congratulations! We are delighted to offer you employment with <strong>SMART RESUME ATS</strong>. Based on your interview performance, we are pleased to appoint you to the following position.</p>

                <div class="meta-info">
                    <div><strong>Offer No :</strong> {offer_no}</div>
                    <div><strong>Candidate Name :</strong> {applicant_name}</div>
                    <div><strong>Mobile :</strong> {mobile}</div>
                    <div><strong>Email :</strong> {applicant_email}</div>
                    <div><strong>Candidate ID :</strong> {candidate_id}</div>
                </div>

                <table>
                    <tr>
                        <td class="label">Position</td>
                        <td>{job_title}</td>
                    </tr>
                    <tr>
                        <td class="label">Company</td>
                        <td>{company_name}</td>
                    </tr>
                    <tr>
                        <td class="label">Department</td>
                        <td>{department}</td>
                    </tr>
                    <tr>
                        <td class="label">Location</td>
                        <td>{location}</td>
                    </tr>
                    <tr>
                        <td class="label">Salary</td>
                        <td>{salary}</td>
                    </tr>
                    <tr>
                        <td class="label">Joining Date</td>
                        <td>{joining_date}</td>
                    </tr>
                </table>

                <div class="section-title">Terms & Conditions</div>
                <ol class="terms">
                    <li>You will report to the HR Department on your joining date.</li>
                    <li>Bring all original educational documents.</li>
                    <li>Employment is subject to company policies.</li>
                    <li>Company reserves the right to terminate employment as per company policy.</li>
                </ol>

                <p>We look forward to welcoming you to our team.</p>

                <div class="footer">
                    <strong>HR Manager</strong><br>
                    SMART RESUME ATS<br>
                    <div class="stamp">
                        BADAL PRIVATE LIMITED<br>
                        PVT. LTD.
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = f"Dear {applicant_name},\n\nOFFICIAL OFFER LETTER\n\nPosition: {job_title}\nCompany: {company_name}\nLocation: {location}\nSalary: {salary}\nJoining Date: {joining_date}\n\nCongratulations!"

    # Send Email via Resend
    try:
        response = resend.Emails.send({
            "from": "Smart Recruiter <otp@myjobportal.online>",
            "to": [applicant_email],
            "subject": f"OFFICIAL OFFER LETTER - {applicant_name}",
            "html": html_content,
            "text": plain_text,
            "headers": {
                "X-Entity-Ref-ID": f"offer-{app_id}"
            }
        })

        logger.info(f"✅ Offer letter sent successfully: {response}")
        messages.success(
            request, "Official Offer Letter sent successfully to Gmail!")

    except Exception as e:
        logger.error(f"❌ Offer Letter Email Error: {e}")
        messages.error(request, f"Unable to send offer letter. Error: {e}")

    try:
        return redirect("application_detail", id=app_id)
    except Exception:
        return redirect("application_detail", pk=app_id)
    

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
