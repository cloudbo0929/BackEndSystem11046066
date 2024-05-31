from CardNotificationConsumer import CardNotificationConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/cards/', CardNotificationConsumer.as_asgi()),
]
