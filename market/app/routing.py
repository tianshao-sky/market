from django.urls import re_path, path
from app.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/test', ChatConsumer),
]
