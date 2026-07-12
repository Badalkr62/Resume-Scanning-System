from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="candidate_dashboard",
    ),

    # Jobs
    path(
        "jobs/",
        views.job_list,
        name="candidate_job_list",
    ),

    path(
        "jobs/<int:pk>/",
        views.job_detail,
        name="job_detail",
    ),

    # Apply Job
    path(
        "apply/<int:id>/",
        views.apply_job,
        name="apply_job",
    ),

    # My Applications
    path(
        "my-applications/",
        views.my_applications,
        name="my_applications",
    ),

]