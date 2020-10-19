import json
from django.core import serializers
from django.shortcuts import render
from chat.models import Message
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@csrf_exempt
def getMessages(request):
    payload=json.loads(request.body)
    user1 = payload.get('user1')
    user2 = payload.get('user2')
    room_id = payload.get('room_id')
    page = payload.get('page')
    offset = payload.get('offset')
    if (room_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT chat_message.id, chat_message.text, chat_message.created_at, chat_message.message_type, chat_message.sender, users.username FROM chat_message INNER JOIN users ON (cast(chat_message.sender as uuid) = users.user_id) WHERE chat_message.room_id = %s ORDER BY chat_message.created_at DESC;", [room_id])
            messages = dictfetchall(cursor)
            cursor.close()
            connection.close()
    else:
        with connection.cursor() as cursor:
            queryString = f"SELECT chat_message.id, chat_message.text, chat_message.created_at, chat_message.message_type, chat_message.sender, users.username FROM chat_message INNER JOIN users ON (cast(chat_message.sender as uuid) = users.user_id) WHERE (chat_message.sender = '{user1}' AND chat_message.receiver = '{user2}') OR (chat_message.sender = '{user2}' AND chat_message.receiver = '{user1}') ORDER BY chat_message.created_at DESC;";
            cursor.execute(queryString)
            messages = dictfetchall(cursor)
            cursor.close()
            connection.close()

    json_response = {
        'messages': (messages)[(page - 1) * offset : page * offset],
        'count': len(list(messages))
    }

    return JsonResponse(json_response)
