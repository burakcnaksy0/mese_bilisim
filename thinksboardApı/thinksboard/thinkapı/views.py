from django.shortcuts import render, redirect
from .forms import UserLogInForm, DevicesListForm
import requests
import json
from datetime import datetime

BASEURL = "https://thingsboard.cloud/api"
LOGIN_URL = f"{BASEURL}/auth/login"
USER_URL = f"{BASEURL}/auth/user"


def userlogın(request):
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            payload = json.dumps({"username": username, "password": password})
            headers = {'Content-Type': 'application/json'}
            response = requests.post(LOGIN_URL, headers=headers, data=payload)
            if response.status_code != 200:
                return render(request, "login.html", {"error": "login failed !!"})
            response_json = response.json()
            token = response_json.get("token")
            refresh_token = response_json.get("refreshToken")
            request.session['token'] = token
            request.session['refresh_token'] = refresh_token
            context = {
                "token": token,
                "refresh_token": refresh_token
            }
            return render(request, "token.html", context)
        else:
            return render(request, "login.html", {"error": "form is not valid !"})
    else:
        form = UserLogInForm()
        return render(request, "login.html", {"form": form})


DEVICE_TELEMETRY = {
    "1": {
        "uuid": "95cf0970-a5b2-11ef-af8e-935e87032cca",
        "telemetry": "values/timeseries?keys=temperature,state,rez"
    },
    "2": {
        "uuid": "cd3c12f0-a69c-11ef-9126-e7e15310409e",
        "telemetry": "values/timeseries?keys=temp,temperature"
    },
    "3": {
        "uuid": "ea345690-a6fd-11ef-8300-7376affecafe",
        "telemetry": "values/timeseries?keys=temperature,machineState"
    },
    "4": {
        "uuid": "e03eb710-a730-11ef-af8e-935e87032cca",
        "telemetry": "values/timeseries?keys=clock,temperature"
    },
    "5": {
        "uuid": "87a23920-abe9-11ef-ba27-0bc777b49120",
        "telemetry": "values/timeseries?keys=quality,temperature"
    }
}


def devicePrefer(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    if request.method == "POST":
        deviceform = DevicesListForm(request.POST)
        if deviceform.is_valid():
            device_key = deviceform.cleaned_data["device"]
            device_data = DEVICE_TELEMETRY.get(device_key)
            if not device_data:
                return render(request, "deviceInfo.html", {"error": "Invalid device selected!"})

            device_uuid = device_data["uuid"]
            telemetry_url = device_data["telemetry"]
            headers = {'Authorization': f'Bearer {token}'}

            # Cihaz bilgilerini al
            device_url = f"{BASEURL}/device/{device_uuid}"
            device_response = requests.get(device_url, headers=headers)

            # Telemetri bilgilerini al
            full_telemetry_url = f"{BASEURL}/plugins/telemetry/DEVICE/{device_uuid}/{telemetry_url}"
            telemetry_response = requests.get(full_telemetry_url, headers=headers)

            if device_response.status_code != 200 or telemetry_response.status_code != 200:
                return render(request, "deviceInfo.html", {
                    "error": f"Error fetching data! Device: {device_response.status_code}, "
                             f"Telemetry: {telemetry_response.status_code}"
                })

            device_info = device_response.json()
            telemetry_info = telemetry_response.json()

            # Telemetri geçmişini saklama
            telemetry_history = request.session.get('telemetry_history', {})

            # Her cihazın telemetri geçmişini ayrı bir anahtar altında sakla
            if device_uuid not in telemetry_history:
                telemetry_history[device_uuid] = {}

            for key, entries in telemetry_info.items():
                if key not in telemetry_history[device_uuid]:
                    telemetry_history[device_uuid][key] = []

                for entry in entries:
                    # Format timestamp to human-readable time
                    timestamp = datetime.utcfromtimestamp(entry['ts'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
                    entry['formatted_ts'] = timestamp

                    # Eğer giriş zaten geçmişte yoksa ekle
                    if entry not in telemetry_history[device_uuid][key]:
                        telemetry_history[device_uuid][key].append(entry)

            # Telemetri geçmişini oturumda güncelle
            request.session['telemetry_history'] = telemetry_history

            # Grafik verilerini hazırlama
            charts_data = {}
            for key, entries in telemetry_history[device_uuid].items():
                chart_labels = [entry['formatted_ts'] for entry in entries]
                chart_data = [entry['value'] for entry in entries]
                charts_data[key] = {
                    "labels": chart_labels,
                    "data": chart_data
                }

            # Cihaz ve telemetri bilgisini gönder
            return render(request, "deviceİnformation.html", {
                "device_info": device_info,
                "telemetry_info": telemetry_info,
                "telemetry_history": telemetry_history[device_uuid],
                "charts_data": charts_data,
            })
        else:
            return render(request, "deviceInfo.html", {"error": "Invalid form submission!"})
    else:
        deviceform = DevicesListForm()
        return render(request, "deviceInfo.html", {"deviceform": deviceform})
