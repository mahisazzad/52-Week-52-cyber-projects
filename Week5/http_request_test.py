import requests

for i in range(5):
    try:
        response = requests.get("http://neverssl.com")
        print(f"Request {i+1} status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")