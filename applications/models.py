from django.db import models
from django.contrib.auth.models import User
from job.models import Job


class Application(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Shortlisted", "Shortlisted"),
        ("Interview", "Interview"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.TextField(blank=True)

    certifications = models.TextField(blank=True)

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)

    resume = models.FileField(upload_to="resumes/")

    status = models.CharField(
    max_length=20,
    choices=STATUS,
    default="Pending"
    )
    education = models.CharField(
    max_length=200,
    blank=True
    )

    experience = models.CharField(
    max_length=200,
    blank=True
    )
    skills = models.TextField(
    blank=True
    )

    ai_summary = models.TextField(
    blank=True
    )

    recruiter_notes = models.TextField(
    blank=True
        )

    match_score = models.IntegerField(default=85)

    applied_at = models.DateTimeField(auto_now_add=True)

    interview_date = models.DateField(
    null=True,
    blank=True
    )

    interview_time = models.TimeField(
    null=True,
    blank=True
    )

    interview_mode = models.CharField(
    max_length=50,
    blank=True
    )

    meeting_link = models.URLField(
    blank=True
    )


def __str__(self):
    return f"{self.user.username} - {self.job.title}"
