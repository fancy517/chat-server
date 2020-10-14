import json
from django.core import serializers
from django.shortcuts import render
from chat.models import Message
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getMessages(request):
    payload=json.loads(request.body)
    user1 = payload.get('user1')
    user2 = payload.get('user2')
    room_id = payload.get('room_id')
    if (room_id):
    	messages = Message.objects.filter(room_id=room_id)
    else:
    	messages = Message.objects.filter(sender=user1, receiver=user2) | Message.objects.filter(sender=user2, receiver=user1)

    json_response = {
        'messages': json.loads(serializers.serialize('json', messages.order_by('created_at') )),
    }

    return JsonResponse(json_response)
