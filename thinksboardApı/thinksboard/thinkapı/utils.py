import requests

def make_api_request(method, url, headers=None, data=None):
    try:
        if method.lower() == "get":
            response = requests.get(url, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url, headers=headers, json=data)
        else:
            return None, "Unsupported HTTP method."

        if response.status_code != 200:
            return None, f"API call failed: {response.status_code} - {response.text}"
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
