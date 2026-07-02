from django.db import models

# Create your models here.
class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('Resume Screening', 'Resume Screening'),
        ('Technical Support', 'Technical Support'),
        ('Business Inquiry', 'Business Inquiry'),
        ('General Question', 'General Question'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name