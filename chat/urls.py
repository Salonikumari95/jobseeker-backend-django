from django.urls import path
from .views import MessageListAPIView

urlpatterns = [
    path('messages/<int:user_id>/', MessageListAPIView.as_view(), name='message-list'),
]
