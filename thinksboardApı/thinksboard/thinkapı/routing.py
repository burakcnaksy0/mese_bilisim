from django.urls import path
from thinksboard.thinkapı.consumers import TelemetryConsumer

websocket_urlpatterns = [
    path('ws/telemetry/<uuid:device_uuid>/', TelemetryConsumer.as_asgi()),
]
