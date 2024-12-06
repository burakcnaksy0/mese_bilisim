import requests

url = input("Entry a URL value : ")  # Hatalı URL

payload = ""
headers = {}

try:
    response = requests.request("GET", url, headers=headers, data=payload)
    print(f"HTTP Status Code: {response.status_code}")
    # Eğer 200 OK ise, içerikleri yazdırabiliriz
    if response.status_code == 200:
        print("Request was successful!")
        print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}")
except requests.exceptions.RequestException as e:
    # URL yanlış olduğunda veya başka bir hata oluştuğunda burada özel bir mesaj verebilirsiniz.
    print("Request error occurred, but I'll handle this in my code. Error details: ")
    print(e)


