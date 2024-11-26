import requests
import json


BASEURL = "https://thingsboard.cloud/api"

LOGIN_URL = f"{BASEURL}/auth/login"
USER_URL = f"{BASEURL}/auth/user"
DEVICES = {
    "1": f"{BASEURL}/device/95cf0970-a5b2-11ef-af8e-935e87032cca",
    "2": f"{BASEURL}/device/cd3c12f0-a69c-11ef-9126-e7e15310409e",
    "3": f"{BASEURL}/device/ea345690-a6fd-11ef-8300-7376affecafe",
    "4": f"{BASEURL}/device/e03eb710-a730-11ef-af8e-935e87032cca",
}

def login(username, password):

    payload = json.dumps({"username": username, "password": password})
    headers = {'Content-Type': 'application/json'}

    response = requests.post(LOGIN_URL, headers=headers, data=payload)

    if response.status_code != 200:
        print("Login failed:", response.text)
        return None, None

    response_json = response.json()
    token = response_json.get("token")
    refresh_token = response_json.get("refreshToken")

    return token, refresh_token


def get_user_info(token):

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(USER_URL, headers=headers)


    if response.status_code != 200:
        print("Failed to fetch user info:", response.text)
        return None

    return response.json()


def fetch_device_data(device_key, token):

    device_url = DEVICES.get(device_key)
    if not device_url:
        print("Invalid device key. Please choose a number between 1 and 4.")
        return

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(device_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for device {device_key}:", response.text)
        return

    print(f"Device {device_key} data:\n", response.text)


def main():

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Login
    token, refresh_token = login(username, password)
    if not token:
        return

    print("Login successful!")
    print("Token value:", token)
    print("Refresh token value:", refresh_token)


    user_info = get_user_info(token)
    if user_info:
        print("User info:", json.dumps(user_info, indent=4))

    key = input("Which device would you like to choose (1-4)? ")
    fetch_device_data(key, token)


if __name__ == "__main__":
    main()
