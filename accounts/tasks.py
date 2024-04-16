import requests
from django.conf import settings
from celery import shared_task


@shared_task
def send_push_notification(title, body, users):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={settings.FCM_API_KEY}",
    }

    # Iterate over users
    for user in users:
        # Format title and body with user's name
        title_formatted = title.replace("{name}", user["name"])
        body_formatted = body.replace("{name}", user["name"])

        # Check if user has FCM token
        if user["fcm_token"]:
            # Prepare data for FCM
            data = {
                "to": user["fcm_token"],
                "notification": {
                    "title": title_formatted,
                    "body": body_formatted,
                },
            }

            # Send POST request to FCM
            try:
                response = requests.post(
                    "https://fcm.googleapis.com/fcm/send", json=data, headers=headers
                )
                response.raise_for_status()  # Raise exception for 4xx or 5xx responses

            except requests.RequestException as e:
                # Handle request exceptions
                print(f"Error sending notification to {user['name']}: {e}")
