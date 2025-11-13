import os
import django
from django.core.asgi import get_asgi_application

# 1️⃣ Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobseeker.settings')

# 2️⃣ Setup Django


# 3️⃣ Import Channels stuff AFTER setup
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# 4️⃣ Define ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
