from django.urls import path
from . import views

urlpatterns = [

    path("register/", views.register, name="register"),
    # path("UserProfile/", views.UserProfile, name="UserProfile"),


    path("login/", views.user_login, name="login"),
    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path("logout/", views.user_logout, name="logout"),

    path("choose-role/", views.choose_role, name="choose_role"),


]
