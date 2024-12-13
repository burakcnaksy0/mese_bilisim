from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_uuid = self.scope['url_route']['kwargs']['device_uuid']
        await self.channel_layer.group_add(self.device_uuid, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.device_uuid, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Gelen veriyi işleyin
        await self.send(text_data=json.dumps({
            'message': 'Data received',
            'data': data
        }))
