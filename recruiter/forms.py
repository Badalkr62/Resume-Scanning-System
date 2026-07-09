from applications.models import Application
from django import forms
from .models import RecruiterSettings


class InterviewForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            "interview_date",
            "interview_time",
            "interview_mode",
            "meeting_link",
            "status",
        ]

        widgets = {

            "interview_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "interview_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "interview_mode": forms.Select(
                choices=[
                    ("Online", "Online"),
                    ("Offline", "Offline"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),

            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://meet.google.com/xxxxx",
                }
            ),

            "status": forms.Select(
                choices=[
                    ("Interview", "Interview Scheduled"),
                    ("Selected", "Selected"),
                    ("Rejected", "Rejected"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "interview_date": "Interview Date",
            "interview_time": "Interview Time",
            "interview_mode": "Interview Mode",
            "meeting_link": "Meeting Link",
            "status": "Application Status",
        }


class RecruiterSettingsForm(forms.ModelForm):

    class Meta:
        model = RecruiterSettings

        fields = [
            "profile_image",
            "phone",
            "designation",

            "company_name",
            "company_logo",
            "website",
            "address",
            "city",
            "state",
            "country",

            "email_notification",
            "resume_notification",
            "interview_notification",
            "offer_notification",

            "ai_enabled",
            "minimum_score",
            "default_skills",

            "theme",
        ]

        widgets = {

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number"
                }
            ),

            "designation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Designation"
                }
            ),

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name"
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "minimum_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "default_skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Python, Django, SQL"
                }
            ),

            "theme": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "gemini_api_key": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "openai_api_key": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "profile_image": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "company_logo": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }
