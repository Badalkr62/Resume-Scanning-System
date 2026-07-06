from django.urls import path
from . import views

urlpatterns = [

    path("jobs/", views.job_list, name="candidate_jobs"),

    path(
        "jobs/<int:pk>/",
        views.job_detail,
        name="job_detail"
    ),

    path(
        "candidate/dashboard/",
        views.dashboard,
        name="candidate_dashboard"
    ),

    path(
        "my-applications/",
        views.my_applications,
        name="my_applications"
    ),
    path(
        "jobs/<int:pk>/apply/",
        views.apply_job,
        name="apply_job"
    ),
    

]
