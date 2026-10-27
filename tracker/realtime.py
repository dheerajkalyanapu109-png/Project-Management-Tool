from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification

def broadcast(project_id):
    """Tell every browser watching this project to refresh."""
    async_to_sync(get_channel_layer().group_send)(f"project_{project_id}", {"type": "changed"})

def notify(user, text, url=""):
    """Save a notification and push it live to that user."""
    Notification.objects.create(user=user, text=text, url=url)
    data = {"text": text, "url": url, "unread": user.notifications.filter(read=False).count()}
    async_to_sync(get_channel_layer().group_send)(f"user_{user.id}", {"type": "notify", "data": data})
