from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs['user_id']
        return Message.objects.filter(
            sender__in=[user.id, other_user_id],
            receiver__in=[user.id, other_user_id]
        ).order_by('timestamp')
