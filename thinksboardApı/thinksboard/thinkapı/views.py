from django.shortcuts import render, redirect
from .forms import UserLogInForm, DevicesListForm
import requests
import json

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


DEVICES = {
    "1": "95cf0970-a5b2-11ef-af8e-935e87032cca",
    "2": "cd3c12f0-a69c-11ef-9126-e7e15310409e",
    "3": "ea345690-a6fd-11ef-8300-7376affecafe",
    "4": "e03eb710-a730-11ef-af8e-935e87032cca",
    "5": "87a23920-abe9-11ef-ba27-0bc777b49120",
}


def devicePrefer(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')  # Giriş yapmadıysa yönlendir

    if request.method == "POST":
        deviceform = DevicesListForm(request.POST)
        if deviceform.is_valid():
            device_key = deviceform.cleaned_data["device"]  # "1", "2" gibi bir anahtar alıyoruz
            device_uuid = DEVICES.get(device_key)  # UUID'yi alıyoruz
            if not device_uuid:
                return render(request, "deviceInfo.html", {"error": "Invalid device selected!"})

            headers = {'Authorization': f'Bearer {token}'}
            device_url = f"{BASEURL}/device/{device_uuid}"  # UUID kullanarak URL oluştur

            # Loglama
            print(f"URL: {device_url}")
            print(f"Headers: {headers}")

            response = requests.get(device_url, headers=headers)

            # Yanıt kontrolü
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

            if response.status_code != 200:
                return render(request, "deviceInfo.html",
                              {"error": f"Device fetch failed! Status: {response.status_code}, Error: {response.text}"})

            device_info = response.json()
            return render(request, "deviceİnformation.html", {"device_info": device_info})
        else:
            return render(request, "deviceInfo.html", {"error": "Invalid form submission!"})
    else:
        deviceform = DevicesListForm()
        return render(request, "deviceInfo.html", {"deviceform": deviceform})
