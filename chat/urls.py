from django.urls import path, re_path
from .views import MessageListAPIView, room, ConversationListAPIView
from . import consumers

urlpatterns = [
    path('conversations/', ConversationListAPIView.as_view(), name='conversation-list'),
    path('messages/<int:conversation_id>/', MessageListAPIView.as_view(), name='message-list'),
    path('room/<int:conversation_id>/', room, name='room'),  # Pass conversation_id
]

# WebSocket routing
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
