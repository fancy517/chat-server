from .models import Message
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer

import json

class Consumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        if(receiver):
            senderInstance = User.objects.get(pk=sender['pk'])
            receiverInstance = User.objects.get(pk=receiver['pk'])            
            newMessage = Message(sender=senderInstance, receiver = receiverInstance ,text=message)
            newMessage.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender' : sender
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))