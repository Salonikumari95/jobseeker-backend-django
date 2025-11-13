from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from users.views import seeker_dashboard, recruiter_dashboard, login_view, change_application_status

from users.views import login_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('jobs/', include('jobs.urls')),

    path('dashboard/seeker/', login_required(seeker_dashboard), name='seeker_dashboard'),
    path('dashboard/recruiter/', login_required(recruiter_dashboard), name='recruiter_dashboard'),

   
    path('', RedirectView.as_view(url='/dashboard/seeker/', permanent=False)),
    path('logout/', login_view, name='template_logout'),
    
    path('application/<int:app_id>/change-status/', change_application_status, name='change_application_status'),
    path('login-view/', login_view, name='template_login'),
    path('community/', include('community.urls')),
    path('chat/', include('chat.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
