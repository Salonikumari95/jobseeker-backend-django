from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
import datetime 
from django.core.exceptions import ValidationError
class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='conversations_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='conversations_user2', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_conversation_users_ordered'
            ),
        ]
    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError("A conversation must be between two different users.")

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    file =  CloudinaryField('file', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)