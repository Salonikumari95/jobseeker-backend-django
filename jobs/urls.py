from django.urls import path
from .views import (
    JobPostCreateView,
    JobPostListView,
    JobApplicationCreateView,
    JobApplicationUpdateView,
    JobPostUpdateView,
    JobPostDeleteView,
    JobApplicationDeleteView,
  RecruiterJobApplicationsView
)

urlpatterns = [
    path('post/', JobPostListView.as_view(), name='job-list'),
    path('post/create/', JobPostCreateView.as_view(), name='job-create'),
    path('applications/', JobApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/', JobApplicationUpdateView.as_view(), name='application-update'),
       path('post/<int:pk>/update/', JobPostUpdateView.as_view(), name='job-update'),
     path('post/<int:pk>/delete/', JobPostDeleteView.as_view(), name='job-delete'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='application-delete'),
  path('post/<int:job_id>/applied-applications/', RecruiterJobApplicationsView.as_view(), name='job-applications-for-job'),
]