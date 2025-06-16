import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatbot import urls as chatbot_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_chatbot.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatbot_urls.websocket_urlpatterns
        )
    ),
})