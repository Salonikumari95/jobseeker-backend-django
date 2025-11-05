from django.urls import path
from .views import JobPostListCreateView

urlpatterns = [
    path('', JobPostListCreateView.as_view(), name='job-list-create'),
]