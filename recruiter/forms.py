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
        ]