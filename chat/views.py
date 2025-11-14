from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# List all conversations of the logged-in user
class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all().order_by('-updated_at')


# List all messages in a conversation
class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')


# Chat room view with login required
@login_required
def room(request, conversation_id):
    """
    Renders the chat room template.
    Passes the conversation id to template as 'room_name'.
    Only logged-in users can access.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Optional: check if the user is part of this conversation
    if request.user not in conversation.participants.all():
        return render(request, "chat/room.html")  # You can create this template

    return render(request, "chat/room.html", {"room_name": conversation.id})
