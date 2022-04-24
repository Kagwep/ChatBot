from django.urls import re_path
from . import consumer


websocket_urlpatterns = [
    re_path(r'watch/(?P<pk>\w+)', consumer.ChatConsumer.as_asgi()),
]