"""
ASGI config for CinebBE project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CinebBE.settings')
django_asgi_app = get_asgi_application()
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

from channels.routing import ProtocolTypeRouter, URLRouter
from watchpartyapp.routing import url_patterns


# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": URLRouter(url_patterns)
    }
)