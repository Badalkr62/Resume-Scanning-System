from django.db import models


class Job(models.Model):

    JOB_TYPE = (

        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),

    )

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    salary = models.CharField(max_length=100)

    job_type = models.CharField(max_length=50, choices=JOB_TYPE)

    skills = models.TextField()

    description = models.TextField()

    deadline = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title
