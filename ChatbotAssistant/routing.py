
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from ChatbotAssistant import consumers

websocket_urlpatterns = [
    path('ws/model/', consumers.ModelConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})