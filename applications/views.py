from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

from .models import Application
from .forms import InterviewForm
from .ai_parser import extract_resume_data
from .ai_match import calculate_match_score


def application_list(request):
    applications = Application.objects.select_related(
        "user", "job").order_by("-applied_at")
    return render(request, "recruiter/application_list.html", {"applications": applications})


def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.resume and not application.skills:
        try:
            data = extract_resume_data(application.resume.path)
            if data.get("skills"):
                application.skills = data["skills"]
                score, matched_skills, missing_skills = calculate_match_score(
                    application.job.skills, application.skills
                )
                application.match_score = score
                application.save(update_fields=['skills', 'match_score'])
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(
                f"Resume Parsing Error for App {pk}: {e}")

    matched_skills, missing_skills = [], []
    if application.skills:
        _, matched_skills, missing_skills = calculate_match_score(
            application.job.skills, application.skills
        )

    return render(
        request,
        "recruiter/application_detail.html",
        {
            "application": application,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }
    )


def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)

    if application.status != status:
        application.status = status
        application.save(update_fields=['status'])

        # Context Data (आप अपनी ज़रूरत के अनुसार लिंक्स और कंपनी का नाम बदल सकते हैं)
        context = {
            "candidate": application.user.username,
            "job": application.job.title,
            "company": "Smart Resume Corp",
            "dashboard_link": "https://youratspreferedlink.com/dashboard",
            "careers_link": "https://youratspreferedlink.com/careers"
        }

        if status == "Shortlisted":
            html_content = render_to_string(
                "emails/shortlisted_email.html", context)
            text_content = f"Hello {context['candidate']},\n\nCongratulations! You have been shortlisted for the position of {context['job']}."

            email = EmailMultiAlternatives(
                subject="🎉 Great News! Profile Shortlisted",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[application.user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)
            messages.success(
                request, "Application updated to Shortlisted. Premium Email sent.")

        elif status == "Rejected":
            html_content = render_to_string(
                "emails/rejected_email.html", context)
            text_content = f"Dear {context['candidate']},\n\nThank you for applying for the position of {context['job']}."

            email = EmailMultiAlternatives(
                subject="💼 Application Update",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[application.user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)
            messages.info(
                request, "Application updated to Rejected. Premium Email sent.")

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
