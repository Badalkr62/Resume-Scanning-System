from django.db import models
from applications.models import Application
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.application.user.username} - {self.interview_date}"


from django.db import models
from django.contrib.auth.models import User


class RecruiterSettings(models.Model):

    THEME = (
        ("Light", "Light"),
        ("Dark", "Dark"),
        ("Blue", "Blue"),
        ("Green", "Green"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Profile
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

    # Company
    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    company_logo = models.ImageField(
        upload_to="company/logo/",
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    # Notifications
    email_notification = models.BooleanField(default=True)

    resume_notification = models.BooleanField(default=True)

    interview_notification = models.BooleanField(default=True)

    offer_notification = models.BooleanField(default=True)

    # AI
    ai_enabled = models.BooleanField(default=True)

    minimum_score = models.IntegerField(default=70)

    default_skills = models.TextField(
        blank=True
    )

    # Theme
    theme = models.CharField(
        max_length=20,
        choices=THEME,
        default="Light"
    )

    

    def __str__(self):
        return self.user.username