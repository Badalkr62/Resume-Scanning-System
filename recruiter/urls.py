from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        views.recruiter_dashboard,
        name="recruiter_dashboard",
    ),

    # Jobs
    path(
        "jobs/",
        views.recruiter_job_list,
        name="recruiter_job_list",
    ),

    path(
        "job/add/",
        views.add_job,
        name="add_job",
    ),

    path(
        "job/<int:id>/",
        views.recruiter_job_detail,
        name="recruiter_job_detail",
    ),

    path(
        "job/edit/<int:id>/",
        views.edit_job,
        name="edit_job",
    ),

    path(
        "job/delete/<int:id>/",
        views.delete_job,
        name="delete_job",
    ),

    # Applications
    path(
        "applications/",
        views.application_list,
        name="application_list",
    ),

    path(
        "applications/<int:id>/",
        views.application_detail,
        name="application_detail",
    ),

    # Shortlisted
    path(
        "shortlisted/",
        views.shortlisted_candidates,
        name="shortlisted_candidates",
    ),

    # Interviews
    path(
        "interviews/",
        views.interviews,
        name="interviews",
    ),

    path(
        "interview/<int:pk>/schedule/",
        views.schedule_interview,
        name="schedule_interview",
    ),

    # Offer Letter
    path(
        "offer/<int:pk>/",
        views.send_offer_letter,
        name="send_offer_letter",
    ),

    # Messages
    path(
        "messages/",
        views.recruiter_messages,
        name="recruiter_messages",
    ),

    # Reports
    path(
        "reports/",
        views.reports,
        name="reports",
    ),

    # Settings
    path(
        "settings/",
        views.settings_page,
        name="settings_page",
    ),
]
