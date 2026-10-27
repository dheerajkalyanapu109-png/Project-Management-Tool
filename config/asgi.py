import os
from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_asgi = get_asgi_application()  # must run before importing app code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from tracker.routing import websocket_urlpatterns
application = ProtocolTypeRouter({"http": django_asgi, "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))})
