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
    # New Field
    last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
