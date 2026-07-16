from django.urls import path
from . import views

urlpatterns = [

    path("", views.job_list, name="job_list"),

    path("detail/<int:id>/", views.job_details, name="job_details"),

    path("add/", views.add_job, name="add_job"),

    path("edit/<int:id>/", views.edit_job, name="edit_job"),

    path("delete/<int:id>/", views.delete_job, name="delete_job"),

    path("my-applications/", views.my_applications, name="my_applications"),

    path("candidate/dashboard/", views.dashboard, name="candidate_dashboard"),
]
