from django.db import models
from django.utils import timezone
from django.conf import settings
from django.apps import apps


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
    skills = models.TextField(
        help_text="Example: Python, Django, SQL, REST API"
    )

    responsibilities = models.TextField()

    requirements = models.TextField()

    benefits = models.TextField(blank=True)

    description = models.TextField()

    deadline = models.DateField(default=timezone.now)
    applicants = models.PositiveIntegerField(default=0)
    openings = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Active"
    )

    @property
    def total_applicants(self):
        Application = apps.get_model("applications", "Application")
        return Application.objects.filter(job=self).count()

    @property
    def remaining_openings(self):
        return max(0, self.openings - self.total_applicants)

    @property
    def current_status(self):
        if self.remaining_openings == 0:
            return "Closed"
        return "Active"


    def update_status(self):
        if self.remaining_openings <= 0:
            self.status = "Closed"
        else:
            self.status = "Active"

        self.save(update_fields=["status"])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Job Application Model
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="applications")

    # 2. settings.AUTH_USER_MODEL use karein (Yeh 'user not defined' error permanently khatam kar dega)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} - {self.job.title}"
