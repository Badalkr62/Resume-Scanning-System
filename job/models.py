from django.db import models
from django.utils import timezone


class Job(models.Model):

    JOB_TYPES = (
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
        ("Remote", "Remote"),
    )

    WORK_MODE = (
        ("Onsite", "Onsite"),
        ("Remote", "Remote"),
        ("Hybrid", "Hybrid"),
    )

    STATUS = (
        ("Active", "Active"),
        ("Closed", "Closed"),
    )

    EXPERIENCE = (
        ("Fresher", "Fresher"),
        ("0-1 Years", "0-1 Years"),
        ("1-3 Years", "1-3 Years"),
        ("3-5 Years", "3-5 Years"),
        ("5+ Years", "5+ Years"),
    )

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    work_mode = models.CharField(
        max_length=20,
        choices=WORK_MODE,
        default="Onsite"
    )

    job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPES,
        default="Full Time"
    )

    experience = models.CharField(
        max_length=30,
        choices=EXPERIENCE,
        default="Fresher"
    )

    education = models.CharField(max_length=200)

    salary = models.CharField(max_length=100)

    openings = models.PositiveIntegerField(default=1)

    applicants = models.PositiveIntegerField(default=0)

    skills = models.TextField(
        help_text="Example: Python, Django, SQL, REST API"
    )

    responsibilities = models.TextField()

    requirements = models.TextField()

    benefits = models.TextField(blank=True)

    description = models.TextField()

    deadline = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
