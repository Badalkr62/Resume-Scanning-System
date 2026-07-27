from django.db import models
from django.contrib.auth.models import User
from applications.models import Application


class Interview(models.Model):

    MODE_CHOICES = (
        ("Online", "Online"),
        ("Offline", "Offline"),
    )

    STATUS_CHOICES = (
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Rescheduled", "Rescheduled"),
        ("No Show", "No Show"),
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    interview_date = models.DateField()
    interview_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        default="Online"
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-interview_date', '-interview_time']

    def __str__(self):
        # Safer string formatting in case application or user is None
        user_name = getattr(self.application.user, 'username',
                            'Unknown Candidate') if self.application else "No Application"
        return f"Interview with {user_name} on {self.interview_date}"


class RecruiterSettings(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="recruiter_settings"
    )

    profile_image = models.ImageField(
        upload_to="recruiter/profile/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    company_logo = models.ImageField(
        upload_to="company/logo/",
        blank=True,
        null=True
    )

    website = models.URLField(blank=True)
    address = models.TextField(blank=True)

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    profile_completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings - {self.user.username}"
