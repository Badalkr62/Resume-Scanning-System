from django.db import models


class Resume(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    resume = models.FileField(upload_to='resumes/')

    skills = models.TextField()

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
