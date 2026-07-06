from django.urls import path
from . import views

urlpatterns = [
    path("", views.application_list, name="application_list"),
    path("<int:pk>/", views.application_detail, name="application_detail"),
    path("<int:pk>/status/<str:status>/", views.update_application_status,
         name="update_application_status"),
    path("<int:pk>/interview/", views.schedule_interview,
         name="schedule_interview"),
]
