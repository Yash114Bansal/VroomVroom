import requests
from django.conf import settings
from celery import shared_task

@shared_task
def send_push_notification(title, body, users):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={settings.FCM_API_KEY}"
    }
    
    for user in users:
        title_formatted = title.replace("{name}", user.name)
        body_formatted = body.replace("{name}", user.name)
        if user.fcm_token:
            data = {
                "to": user.fcm_token,
                "notification": {
                    "title": title_formatted,
                    "body": body_formatted,
                }
            }
        
            try:
                requests.post("https://fcm.googleapis.com/fcm/send", json=data, headers=headers)
                
            except requests.RequestException as e:
                
                print(f"Error sending notification to {user.name}: {e}")
