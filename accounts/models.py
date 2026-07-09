from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE = (
        ("candidate", "Candidate"),
        ("recruiter", "Recruiter"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE,
        default="candidate"
    )
    profile_image = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )
    is_verified = models.BooleanField(default=False)

    profile_completed = models.BooleanField(default=False)
    last_seen = models.DateTimeField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True
    )
    otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )
    otp_created = models.DateTimeField(
        blank=True,
        null=True
    )
    email_verified = models.BooleanField(
        default=False
    )
    phone_verified = models.BooleanField(
        default=False
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        default="profiles/default.png"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
