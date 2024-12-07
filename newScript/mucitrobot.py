import requests
import time  # time modülünü import ediyoruz

# ThingsBoard Sunucusu ve Token Bilgileri
thingsboard_url = "https://thingsboard.cloud/api/v1/"

# Cihaz bilgileri
devices = [
    {"device_token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJha3NveWJ1cmFrODA4QGdtYWlsLmNvbSIsInVzZXJJZCI6ImE5ODJhMDkwLWE1YTItMTFlZi05MTI2LWU3ZTE1MzEwNDA5ZSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiMmE4NzYxYjgtMTlhNi00N2I5LTkwZjMtM2E2YzI2MTk2OWJhIiwiZXhwIjoxNzMzNTE3NzMxLCJpc3MiOiJ0aGluZ3Nib2FyZC5jbG91ZCIsImlhdCI6MTczMzQ4ODkzMSwiZmlyc3ROYW1lIjoiYnVyYWsiLCJsYXN0TmFtZSI6ImFrc295IiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJpc0JpbGxpbmdTZXJ2aWNlIjpmYWxzZSwicHJpdmFjeVBvbGljeUFjY2VwdGVkIjp0cnVlLCJ0ZXJtc09mVXNlQWNjZXB0ZWQiOnRydWUsInRlbmFudElkIjoiYTk0MzRkYTAtYTVhMi0xMWVmLTkxMjYtZTdlMTUzMTA0MDllIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.sQn8DS5k3_vSPU2OPi7Rlb9MBxl72Duq_0PCLcft831IE9djqVZAFs7cnqO6SUcTpflCATqJWDeODZvyI1omPQ", "attribute_key": "url_check_result", "check_url": "https://mucitrobot.com/"},
]


# URL durum kontrol fonksiyonu
def check_url_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 1
        else:
            return response.status_code
    except Exception:
        return "error"


# ThingsBoard cihazını güncelleyen fonksiyon
def update_thingsboard_telemetry(thingsboard_url, device_token, key, value):
    headers = {"Content-Type": "application/json"}
    payload = {
        key: value,
        "ts": int(time.time() * 1000)  # Zaman damgası (milisaniye cinsinden)
    }
    api_url = f"{thingsboard_url}{device_token}/telemetry"
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"{key} başarıyla güncellendi: {value}")
        else:
            print(f"Güncelleme başarısız: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Hata oluştu: {e}")


# Cihazları işle
for device in devices:
    device_token = device["device_token"]
    attribute_key = device["attribute_key"]
    check_url = device["check_url"]

    # URL kontrolü
    url_check_result = check_url_status(check_url)

    # Sonucu gönder
    update_thingsboard_telemetry(thingsboard_url, device_token, attribute_key, url_check_result)
