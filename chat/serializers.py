from rest_framework import serializers
from .models import Conversation, Message

from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth.models import User
from users.models import UserProfile

class MessageSerializer(serializers.ModelSerializer):
    sender_first_name = serializers.CharField(source='sender.first_name', read_only=True)
    sender_last_name = serializers.CharField(source='sender.last_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'content', 'timestamp',
            'sender_first_name', 'sender_last_name'
        ]

class ParticipantProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [ 'profile_image']

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None

class ParticipantSerializer(serializers.ModelSerializer):
    profile = ParticipantProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile','first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(source='id', read_only=True)
    last_message = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'other_participant', 'updated_at', 'last_message']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            others = obj.participants.exclude(id=request.user.id)
            if others.exists():
                return ParticipantSerializer(others.first()).data
        return None