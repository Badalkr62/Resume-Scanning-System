from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('upload/', views.upload_resume, name='upload_resume'),
   
]
