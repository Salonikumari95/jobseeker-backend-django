import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data['sender']
        receiver_id = data['receiver']
        message_text = data.get('message', '')
        image_data = data.get('image', None)
        file_data = data.get('file', None)
        file_name = data.get('file_name', None)

        sender = await self.get_user(sender_id)
        receiver = await self.get_user(receiver_id)

        message_obj = await self.save_message(sender, receiver, message_text, image_data, file_data, file_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.username,
                'message': message_text,
                'image_url': message_obj.image.url if message_obj.image else None,
                'file_url': message_obj.file.url if message_obj.file else None,
                'file_name': file_name,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'message': event['message'],
            'image_url': event.get('image_url'),
            'file_url': event.get('file_url'),
            'file_name': event.get('file_name'),
        }))

    @staticmethod
    async def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    async def save_message(sender, receiver, message, image_data, file_data, file_name):
        msg = Message(sender=sender, receiver=receiver, message=message)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            msg.image.save(f"chat_{sender.id}_{receiver.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

        if file_data:
            file_content = ContentFile(base64.b64decode(file_data))
            msg.file.save(file_name, file_content, save=False)

        msg.save()
        return msg
