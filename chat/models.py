from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    text = models.TextField()
    message_type = models.TextField(default="text")
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.TextField()
    receiver = models.TextField()
    room_id = models.TextField(default="p2pchat")
