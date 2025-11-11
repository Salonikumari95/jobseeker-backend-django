from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from users.views import seeker_dashboard, recruiter_dashboard  # aapke views yahan se import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('jobs/', include('jobs.urls')),

    path('dashboard/seeker/', login_required(seeker_dashboard), name='seeker_dashboard'),
    path('dashboard/recruiter/', login_required(recruiter_dashboard), name='recruiter_dashboard'),

    # Root URL redirect to seeker dashboard
    path('', RedirectView.as_view(url='/dashboard/seeker/', permanent=False)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
