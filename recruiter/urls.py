from django.urls import path
from . import views

urlpatterns = [
    path(
        "dashboard/",
        views.recruiter_dashboard,
        name="recruiter_dashboard",
    ),
    path(
        "send_offer_letter/<int:pk>/",  # <-- Yahan <int:pk>/ add kiya
        views.send_offer_letter,
        name="send_offer_letter",
    ),

    path(
        "settings/",
        views.settings_page,
        name="settings_page",
    ),
    path(
        "jobs/",
        views.recruiter_job_list,
        name="recruiter_job_list",
    ),
    path(
        "applications/<int:id>/",
        views.application_detail,
        name="application_detail"
    ),
    path(
        "job/add/",
        views.add_job,
        name="recruiter_add_job",
    ),

    path(
        "job/edit/<int:id>/",
        views.edit_job,
        name="recruiter_edit_job",
    ),

    path(
        "job/delete/<int:id>/",
        views.delete_job,
        name="recruiter_delete_job",
    ),
]
