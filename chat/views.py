from rest_framework import generics, permissions,status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count


class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all().order_by('-updated_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# List all messages in a conversation
class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    
class ConversationCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        participant_ids = request.data.get('participant_ids', [])
        if len(participant_ids) != 1:
            return Response({'error': 'You must provide exactly one other user.'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = request.user.id
        user2 = participant_ids[0]
        if user1 == user2:
            return Response({'error': 'Cannot create conversation with yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing conversation between these two users
        conversations = Conversation.objects.annotate(num_participants=Count('participants')).filter(num_participants=2)
        for convo in conversations:
            ids = set(convo.participants.values_list('id', flat=True))
            if ids == set([user1, user2]):
                serializer = ConversationSerializer(convo, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new conversation
        users = User.objects.filter(id__in=[user1, user2])
        if users.count() != 2:
            return Response({'error': 'One or both users do not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)