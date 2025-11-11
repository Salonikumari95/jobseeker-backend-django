from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    EmailLoginView,
    UserProfileView,
    LogoutView,
    RequestPasswordResetOTPView,
    PasswordResetView,
    seeker_dashboard,
    recruiter_dashboard,
    template_logout
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', template_logout, name='logout'), 
    path('password-reset/request-otp/', RequestPasswordResetOTPView.as_view(), name='request-password-otp'),
    path('password-reset/confirm/', PasswordResetView.as_view(), name='password-reset'),
    path('dashboard/seeker/', seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/recruiter/', recruiter_dashboard, name='recruiter_dashboard'),
]
