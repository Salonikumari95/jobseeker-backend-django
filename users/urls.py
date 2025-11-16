from django.urls import path,include
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
    ,login_view,
    change_application_status,
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    path('logout/', LogoutView.as_view(), name='logout'),
     path('application/<int:app_id>/change-status/', change_application_status, name='change_application_status'),
     
    


]
