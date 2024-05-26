from celery import shared_task
from .models import Chat, UserProfile
from django.db import transaction

message_queue = []

@shared_task
def process_chat_messages():
    if message_queue:
        with transaction.atomic():
            batch = message_queue[:]
            message_queue.clear()
            Chat.objects.bulk_create(batch)

@shared_task
def add_message_to_queue(sender, receiver, content):
    chat = Chat(
        sender=UserProfile.objects.get(email=sender),
        receiver=UserProfile.objects.get(email=receiver),
        content=content,
    )
    message_queue.append(chat)