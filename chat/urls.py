from django.urls import path
from .views import MessageListAPIView, ConversationListAPIView, ConversationCreateAPIView

urlpatterns = [
    path('conversations/', ConversationListAPIView.as_view(), name='conversation-list'),
    path('messages/<int:conversation_id>/', MessageListAPIView.as_view(), name='message-list'),

     path('conversations/create/', ConversationCreateAPIView.as_view(), name='conversation-create'),
]
