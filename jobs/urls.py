from django.urls import path
from . import views

urlpatterns = [

    path("", views.job_list, name="job_list"),

    path("add/", views.add_job, name="add_job"),

    path("view/<int:id>/", views.view_job, name="view_job"),

    path("edit/<int:id>/", views.edit_job, name="edit_job"),

    path("delete/<int:id>/", views.delete_job, name="delete_job"),

]
