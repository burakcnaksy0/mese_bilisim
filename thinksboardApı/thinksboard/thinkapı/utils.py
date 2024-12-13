import json
import random
import time
import requests
import logging
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

def send_random_telemetry(device_key, device_data):
    """
    Belirtilen cihaz için ThingsBoard'a rastgele telemetri verileri gönderir ve
    WebSocket aracılığıyla yayınlar.
    """
    access_token = device_data.get("Erişim şifresi")
    telemetry_keys = device_data.get("telemetry", "").split(",")
    telemetry_url = f"http://thingsboard.cloud/api/v1/{access_token}/telemetry"
    headers = {"Content-Type": "application/json"}
    channel_layer = get_channel_layer()
    group_name = f"device_{device_key}"

    if not access_token or not telemetry_keys:
        logger.error(f"[Device {device_key}] Invalid device data: {device_data}")
        return

    successful_sends = 0
    stop_flag = False  # Bu değişken harici bir mekanizma ile durdurulabilir.

    while not stop_flag:
        # Telemetri verilerini rastgele oluştur
        telemetry_payload = {
            key: round(random.uniform(20, 100), 2) for key in telemetry_keys
        }
        telemetry_payload["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ThingsBoard API'ye gönder
        try:
            response = requests.post(
                telemetry_url, headers=headers, json=telemetry_payload, timeout=5
            )
            if response.status_code == 200:
                successful_sends += 1
                logger.info(f"[Device {device_key}] Telemetry sent to ThingsBoard: {telemetry_payload}")
            else:
                logger.warning(f"[Device {device_key}] ThingsBoard Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"[Device {device_key}] Exception while sending to ThingsBoard: {e}")

        # WebSocket üzerinden yayınla
        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "telemetry_message",
                    "message": telemetry_payload,
                }
            )
            logger.info(f"[Device {device_key}] Telemetry sent via WebSocket: {telemetry_payload}")
        except Exception as e:
            logger.error(f"[Device {device_key}] Exception while sending via WebSocket: {e}")

        logger.info(f"Total Successful Sends for Device {device_key}: {successful_sends}")

        # 5 saniye bekle
        time.sleep(5)
