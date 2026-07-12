from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("user/", views.user_section, name="user_section"),
    path("companies/", views.companies, name="companies"),
    # path("<str:company_name>/", views.company_detail, name="company_detail"),
]
