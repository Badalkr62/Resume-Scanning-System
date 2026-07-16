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


class RecruiterSettings(models.Model):

    THEME_CHOICES = (
        ("Light", "Light"),
        ("Dark", "Dark"),
        ("Blue", "Blue"),
        ("Green", "Green"),
    )

    FONT_CHOICES = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
    )

    SIDEBAR_CHOICES = (
        ("Primary", "Primary"),
        ("Dark", "Dark"),
        ("Success", "Success"),
        ("Danger", "Danger"),
    )

    DASHBOARD_CHOICES = (
        ("Default", "Default"),
        ("Blue", "Blue"),
        ("Purple", "Purple"),
        ("Green", "Green"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # =====================
    # Profile
    # =====================

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

    # =====================
    # Company
    # =====================

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

    # =====================
    # Notifications
    # =====================

    email_notification = models.BooleanField(default=True)

    resume_notification = models.BooleanField(default=True)

    interview_notification = models.BooleanField(default=True)

    offer_notification = models.BooleanField(default=True)

    # =====================
    # AI Settings
    # =====================

    ai_enabled = models.BooleanField(default=True)

    minimum_score = models.PositiveIntegerField(default=70)

    default_skills = models.TextField(blank=True)

    gemini_api_key = models.TextField(
        blank=True
    )

    openai_api_key = models.TextField(
        blank=True
    )

    # =====================
    # Appearance
    # =====================

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="Light"
    )

    sidebar_color = models.CharField(
        max_length=20,
        choices=SIDEBAR_CHOICES,
        default="Primary"
    )

    dashboard_color = models.CharField(
        max_length=20,
        choices=DASHBOARD_CHOICES,
        default="Default"
    )

    font_size = models.CharField(
        max_length=20,
        choices=FONT_CHOICES,
        default="Medium"
    )

    # =====================
    # Account
    # =====================

    profile_completed = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username
