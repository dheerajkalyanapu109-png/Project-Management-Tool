from django.urls import path
from . import consumers
websocket_urlpatterns = [
    path("ws/project/<int:pid>/", consumers.ProjectConsumer.as_asgi()),
    path("ws/notifications/", consumers.NotifyConsumer.as_asgi()),
]
