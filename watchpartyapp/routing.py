from django.urls import path
from .consumers import ChatConsumer, GroupConsumer

url_patterns = [
    path('chat/', ChatConsumer.as_asgi()),
    path('group/', GroupConsumer.as_asgi())
]