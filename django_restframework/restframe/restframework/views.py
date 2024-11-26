import requests
import json
from django.shortcuts import render, redirect
from .forms import *

# ThingsBoard API Base URL
BASEURL = "https://thingsboard.cloud/api"
LOGIN_URL = f"{BASEURL}/auth/login"


# Helper function to retrieve token from session
def get_token_from_session(request):
    return request.session.get('token')


# Login View
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            payload = json.dumps({"username": username, "password": password})
            headers = {'Content-Type': 'application/json'}

            try:
                # Make API request to authenticate user
                response = requests.post(LOGIN_URL, headers=headers, data=payload)
                response.raise_for_status()  # Raise error for bad responses
                response_json = response.json()
            except requests.exceptions.RequestException as e:
                return render(request, "login.html", {"error": f"An error occurred: {str(e)}"})

            # Save tokens in session if login is successful
            token = response_json.get("token")
            refresh_token = response_json.get("refreshToken")
            if token and refresh_token:
                request.session['token'] = token
                request.session['refresh_token'] = refresh_token
                return redirect('device_info')  # Redirect to device info page
            else:
                return render(request, "login.html", {"error": "Invalid credentials!"})

        else:
            return render(request, "login.html", {"error": "Invalid form data!"})

    # Render the login page with an empty form for GET requests
    return render(request, "login.html", {"form": LoginForm()})


# Device Info View
def device_info(request,device_id):
    token = get_token_from_session(request)

    if not token:
        return redirect('login')  # Redirect to login if token is not available

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            device_id = form.cleaned_data['device_id']
            device_url = f"{BASEURL}/device/{device_id}"
            headers = {'Authorization': f'Bearer {token}'}

            try:
                response = requests.get(device_url, headers=headers)
                response.raise_for_status()
                device_data = response.json()
                return render(
                    request,
                    "device_info.html",
                    {"device_data": device_data, "form": form, "success": "Device information retrieved successfully!"}
                )
            except requests.exceptions.RequestException as e:
                return render(request, "device_info.html", {"error": f"Error occurred: {str(e)}", "form": form})
    else:  # Handle GET requests
        default_device_id = "cd3c12f0-a69c-11ef-9126-e7e15310409e"
        device_url = f"{BASEURL}/device/{default_device_id}"
        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = requests.get(device_url, headers=headers)
            response.raise_for_status()
            device_data = response.json()
            return render(
                request,
                "device_info.html",
                {"device_data": device_data, "form": LoginForm(),
                 "success": "Default device information retrieved!"}
            )
        except requests.exceptions.RequestException as e:
            return render(request, "device_info.html",
                          {"error": f"Error retrieving default device information: {str(e)}",
                           "form": LoginForm()})

    return render(request, "device_info.html", {"form": LoginForm()})
