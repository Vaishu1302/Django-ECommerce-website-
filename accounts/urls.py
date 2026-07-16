from django.urls import path
from . import views

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    # PasswordResetView,
    # PasswordResetDoneView,
    # PasswordResetConfirmView,
    # PasswordResetCompleteView,
)

urlpatterns = [
    path(
    '',
    views.home,
    name='home'
),

    # Authentication
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    # Profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

    # Change Password
    path(
        'change-password/',
        PasswordChangeView.as_view(
            template_name='accounts/change_password.html'
        ),
        name='change_password'
    ),

    path(
        'password-changed/',
        PasswordChangeDoneView.as_view(
            template_name='accounts/password_changed.html'
        ),
        name='password_change_done'
    ),

    # Forgot Password
    # path(
    #     'forgot-password/',
    #     PasswordResetView.as_view(
    #         template_name='accounts/forgot_password.html'
    #     ),
    #     name='password_reset'
    # ),

    # path(
    #     'forgot-password/done/',
    #     PasswordResetDoneView.as_view(
    #         template_name='accounts/password_reset_done.html'
    #     ),
    #     name='password_reset_done'
    # ),

    # path(
    #     'reset/<uidb64>/<token>/',
    #     PasswordResetConfirmView.as_view(
    #         template_name='accounts/password_reset_confirm.html'
    #     ),
    #     name='password_reset_confirm'
    # ),

    # path(
    #     'reset-complete/',
    #     PasswordResetCompleteView.as_view(
    #         template_name='accounts/password_reset_complete.html'
    #     ),
    #     name='password_reset_complete'
    # ),
    # Forgot Password using Email OTP
    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),

    path(
        'verify-otp/',
        views.verify_otp,
        name='verify_otp'
    ),

    path(
        'reset-password/',
        views.reset_password,
        name='reset_password'
    ),
    # path(
    #     '',
    #     views.product_list,
    #     name='products'
    # ),

    # path(
    #     '<int:pk>/',
    #     views.product_detail,
    #     name='product_detail'
    # ),


]