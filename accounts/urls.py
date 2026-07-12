from django.urls import path
from . import views

urlpatterns = [

    path("register/", views.register, name="register"),
    # path("UserProfile/", views.UserProfile, name="UserProfile"),


    path("login/", views.user_login, name="login"),

    path("verify-otp/", views.verify_otp, name="verify_otp"),

    path(
        "resend-otp/",
        views.resend_otp,
        name="resend_otp",
    ),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-reset-otp/", views.verify_reset_otp, name="verify_reset_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),


    path("logout/", views.user_logout, name="logout"),

    path("choose-role/", views.choose_role, name="choose_role"),


]
