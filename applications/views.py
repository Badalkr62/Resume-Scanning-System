from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
import logging
from .models import Application
from .forms import InterviewForm
from .ai_parser import extract_resume_data
from .ai_match import calculate_match_score


logger = logging.getLogger(__name__)


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


logger = logging.getLogger(__name__)


def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    matched_skills = []
    missing_skills = []
    skills_list = []

    if application.resume:
        try:
            # Resume Parse
            data = extract_resume_data(application.resume.path)

            application.skills = data.get("skills", "")

            if application.skills:
                skills_list = [
                    s.strip()
                    for s in application.skills.split(",")
                    if s.strip()
                ]

            score, matched_skills, missing_skills = calculate_match_score(
                application.job.skills,
                application.skills
            )

            application.match_score = score

            application.education = data.get(
                "education",
                application.education
            )

            application.experience = data.get(
                "experience",
                application.experience
            )

            total_skills = len([
                s.strip()
                for s in application.job.skills.split(",")
                if s.strip()
            ])

            recommendation = (
                "Highly Recommended ✅"
                if score >= 80 else
                "Recommended 👍"
                if score >= 60 else
                "Needs Improvement ⚠️"
            )

            application.ai_summary = f"""
📊 Resume Analysis Report

👤 Candidate
{application.user.get_full_name() or application.user.username}

💼 Job Role
{application.job.title}

🏢 Company
{application.job.company}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Total Required Skills : {total_skills}

✅ Matched Skills : {len(matched_skills)}

❌ Missing Skills : {len(missing_skills)}

📈 AI Match Score : {score}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Matched Skills

{", ".join(matched_skills) if matched_skills else "None"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Missing Skills

{", ".join(missing_skills) if missing_skills else "None"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Recommendation

{recommendation}
"""

            application.save()

        except Exception as e:
            logger.exception(f"Resume Parsing Error: {e}")

    if request.method == "POST":
        application.recruiter_notes = request.POST.get("notes", "")
        application.save(update_fields=["recruiter_notes"])

        messages.success(
            request,
            "Recruiter notes saved successfully."
        )

        return redirect("application_detail", pk=pk)

    context = {
        "application": application,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skills_list": skills_list,
    }

    return render(
        request,
        "recruiter/application_detail.html",
        context,
    )


def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)

    if application.status != status:

        application.status = status
        application.save(update_fields=["status"])

        context = {
            "candidate": application.user.username,
            "job": application.job.title,
            "company": application.job.company,
            "dashboard_link": "https://your-domain.com/dashboard",
            "careers_link": "https://your-domain.com/careers",
        }

        if status == "Shortlisted":

            html = render_to_string(
                "emails/shortlisted_email.html",
                context
            )

            email = EmailMultiAlternatives(
                subject="🎉 Congratulations! You are Shortlisted",
                body="Congratulations!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[application.user.email],
            )

            email.attach_alternative(html, "text/html")
            email.send(fail_silently=True)

            messages.success(request, "Candidate shortlisted successfully.")

        elif status == "Rejected":

            html = render_to_string(
                "emails/rejected_email.html",
                context
            )

            email = EmailMultiAlternatives(
                subject="Application Status",
                body="Application Update",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[application.user.email],
            )

            email.attach_alternative(html, "text/html")
            email.send(fail_silently=True)

            messages.success(request, "Candidate rejected successfully.")

    return redirect("application_detail", pk=pk)


def schedule_interview(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == "POST":
        form = InterviewForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = "Interview"
            application.save()

            html = render_to_string(
                "emails/interview_email.html",
                {
                    "candidate": application.user.username,
                    "job": application.job.title,
                    "date": application.interview_date,
                    "time": application.interview_time,
                    "mode": application.interview_mode,
                    "link": application.meeting_link,
                }
            )

            email = EmailMultiAlternatives(
                subject="🗓️ Interview Invitation",
                body=f"Hi {application.user.username}, your interview has been scheduled.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[application.user.email]
            )
            email.attach_alternative(html, "text/html")

            try:
                email.send()
                messages.success(
                    request, "Interview scheduled and email invitation sent successfully!")
            except Exception:
                messages.warning(
                    request, "Interview scheduled locally, but email failed to send.")

            return redirect("application_detail", pk=pk)
    else:
        form = InterviewForm(instance=application)

    return render(request, "recruiter/schedule_interview.html", {"form": form, "application": application})
