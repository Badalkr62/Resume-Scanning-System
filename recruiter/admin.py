from .models import Interview
from django.contrib import admin


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "interview_date",
        "interview_time",
        "mode",
        "status",
    )

    list_filter = (
        "status",
        "mode",
    )

    search_fields = (
        "application__user__username",
        "application__job__title",
    )
