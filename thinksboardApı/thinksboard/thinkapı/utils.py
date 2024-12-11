import requests
import random
import time
from datetime import datetime, timedelta

def send_random_telemetry(request, device_key, device_dataz):
    """
    Generate 100 random telemetry data points for each key and send them to the ThingsBoard API.
    """
    access_token = device_data["Erişim şifresi"]
    telemetry_keys = device_data["telemetry"].split(",")  # Split telemetry keys

    # ThingsBoard URL
    telemetry_url = f"http://thingsboard.cloud/api/v1/{access_token}/telemetry"
    headers = {"Content-Type": "application/json"}

    # Retrieve the start time from the session or set it if not present
    if 'start_time' not in request.session:
        request.session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.strptime(request.session['start_time'], "%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.strptime(request.session['start_time'], "%Y-%m-%d %H:%M:%S")

    now = datetime.now()
    elapsed_time = now - start_time

    # Generate 100 random data points for each second
    for seconds in range(elapsed_time.seconds + 1):  # Include current second
        for i in range(100):  # Generate 100 random data points
            telemetry_payload = {}
            for key in telemetry_keys:
                value = round(random.uniform(20, 100), 2)
                telemetry_payload[key] = value

            # Update the timestamp for each data point with milliseconds precision
            timestamp = (start_time + timedelta(seconds=seconds) + timedelta(milliseconds=i)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            telemetry_payload["ts"] = timestamp

            try:
                response = requests.post(telemetry_url, headers=headers, json=telemetry_payload)
                if response.status_code == 200:
                    print(f"[Device {device_key}] Telemetry sent: {telemetry_payload}")
                else:
                    print(f"[Device {device_key}] Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"[Device {device_key}] Exception: {e}")

            print(f"Telemetry Payload: {telemetry_payload}")

    request.session['start_time'] = now.strftime("%Y-%m-%d %H:%M:%S")

# Example usage:
# send_random_telemetry(request, "your_device_key", {"Erişim şifresi": "your_access_token", "telemetry": "temperature,humidity"})
