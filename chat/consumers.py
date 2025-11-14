import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get("text", "")
        image_data = data.get("image", None)
        file_data = data.get("file", None)
        file_name = data.get("file_name", None)

        conversation = await self.get_conversation(self.conversation_id)
        if not conversation:
            await self.send(text_data=json.dumps({"error": "Conversation not found"}))
            return

        message = await self.save_message(conversation, self.user, text, image_data, file_data, file_name)

        # Broadcast message to all participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "id": message.id,
                    "sender": self.user.username,
                    "text": message.text,
                    "image_url": message.image.url if message.image else None,
                    "file_url": message.file.url if message.file else None,
                    "timestamp": str(message.timestamp),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, conversation, sender, text, image_data, file_data, file_name):
        msg = Message(conversation=conversation, sender=sender, text=text)
        if image_data:
            fmt, imgstr = image_data.split(";base64,")
            ext = fmt.split("/")[-1]
            msg.image.save(f"{sender.id}_{conversation.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)
        if file_data and file_name:
            msg.file.save(file_name, ContentFile(base64.b64decode(file_data)), save=False)
        msg.save()
        return msg
