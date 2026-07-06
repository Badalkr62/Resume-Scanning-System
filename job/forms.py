from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = "__all__"

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Python Django Developer"
            }),

            "company": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Company Name"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ranchi, Jharkhand"
            }),

            "salary": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "5 LPA - 8 LPA"
            }),

            "education": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "B.Tech / MCA"
            }),

            "openings": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "skills": forms.Textarea(attrs={
                "class": "form-control",
                "rows":3,
                "placeholder":"Python, Django, SQL, REST API"
            }),

            "description": forms.Textarea(attrs={
                "class":"form-control",
                "rows":5
            }),

            "responsibilities": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),

            "requirements": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),

            "benefits": forms.Textarea(attrs={
                "class":"form-control",
                "rows":3
            }),

            "deadline": forms.DateInput(attrs={
                "class":"form-control",
                "type":"date"
            }),

            "job_type": forms.Select(attrs={
                "class":"form-select"
            }),

            "work_mode": forms.Select(attrs={
                "class":"form-select"
            }),

            "experience": forms.Select(attrs={
                "class":"form-select"
            }),

            "status": forms.Select(attrs={
                "class":"form-select"
            })

        }