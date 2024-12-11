from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_key = self.scope['url_route']['kwargs']['device_key']
        self.group_name = f"device_{self.device_key}"

        # Join WebSocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def telemetry_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

