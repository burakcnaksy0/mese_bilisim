import json
import random
import time
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.sites import requests


def send_random_telemetry(device_key, device_data):
    """
    Generate random telemetry data every 5 seconds and send it via WebSocket and ThingsBoard API.
    """
    # ThingsBoard API setup
    access_token = device_data["Erişim şifresi"]
    telemetry_keys = device_data["telemetry"].split(",")  # Split telemetry keys
    telemetry_url = f"http://thingsboard.cloud/api/v1/{access_token}/telemetry"
    headers = {"Content-Type": "application/json"}

    # WebSocket setup
    channel_layer = get_channel_layer()
    group_name = f"device_{device_key}"

    # Infinite loop to send telemetry data
    while True:
        telemetry_payload = {}
        for key in telemetry_keys:
            telemetry_payload[key] = round(random.uniform(20, 100), 2)  # Generate random values

        # Add timestamp to telemetry data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        telemetry_payload["timestamp"] = timestamp

        # Send data to ThingsBoard API
        try:
            response = requests.post(telemetry_url, headers=headers, json=telemetry_payload)
            if response.status_code == 200:
                print(f"[Device {device_key}] Telemetry sent to ThingsBoard: {telemetry_payload}")
            else:
                print(f"[Device {device_key}] ThingsBoard Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[Device {device_key}] Exception while sending to ThingsBoard: {e}")

        # Send data via WebSocket
        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "telemetry_message",
                    "message": telemetry_payload,
                }
            )
            print(f"[Device {device_key}] Telemetry sent via WebSocket: {telemetry_payload}")
        except Exception as e:
            print(f"[Device {device_key}] Exception while sending via WebSocket: {e}")

        # Wait 5 seconds before sending the next telemetry data
        time.sleep(5)
