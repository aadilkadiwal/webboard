from django.urls import path
from django.contrib.auth import views as auth_views
from .import views as account_views

urlpatterns = [
    path('signup/', account_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password-reset'),
    path('reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password-reset-done'),
    path('reset-password/confirm/(<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password-reset-confirm'),
    path('reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html'
        ),
        name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
        ),
        name='change-password-done'),    
]    