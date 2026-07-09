from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Jobs
    path('job_list', views.job_list, name='job_list'),
    path('job/add/', views.add_job, name='add_job'),
    path('job/<int:id>/', views.job_detail, name='job_detail'),
    path('job/edit/<int:id>/', views.edit_job, name='edit_job'),
    path('job/delete/<int:id>/', views.delete_job, name='delete_job'),

    # Applications
    path('', views.application_list, name='application_list'),
    path('<int:id>/', views.application_detail, name='application_detail'),

    # Shortlisted
    path('shortlisted/', views.shortlisted_candidates,
         name='shortlisted_candidates'),

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



    # Offers Lettters
    path(
        "<int:pk>/offer/",
        views.send_offer_letter,
        name="send_offer_letter",
    ),


    # Messages
    path('recruiter_messages/', views.recruiter_messages,
         name='recruiter_messages'),

    # Reports
    path('reports/', views.reports, name='reports'),

    # Settings
    path('settings_page/', views.settings_page, name='settings_page'),
]
