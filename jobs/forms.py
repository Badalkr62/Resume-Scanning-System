from django import forms

from .models import Job

class JobForm(forms.ModelForm):

    class Meta:

        model=Job

        fields="__all__"

        widgets={

            "title":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Python Developer"
            }),

            "company":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Google"
            }),

            "location":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Bangalore"
            }),

            "salary":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"₹8 LPA"
            }),

            "job_type":forms.Select(attrs={
                "class":"form-select"
            }),

            "skills":forms.Textarea(attrs={
                "class":"form-control",
                "rows":3
            }),

            "description":forms.Textarea(attrs={
                "class":"form-control",
                "rows":5
            }),

            "deadline":forms.DateInput(attrs={
                "class":"form-control",
                "type":"date"
            }),

        }