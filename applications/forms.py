from django import forms
from .models import Application


class InterviewForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            "interview_date",
            "interview_time",
            "interview_mode",
            "meeting_link",
        ]

        widgets = {

            "interview_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "interview_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "interview_mode": forms.Select(
                choices=[
                    ("Google Meet", "Google Meet"),
                    ("Zoom", "Zoom"),
                    ("Offline", "Offline")
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://meet.google.com/..."
                }
            )

        }
