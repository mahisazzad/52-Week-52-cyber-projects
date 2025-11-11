import requests
url = "http://localhost:8080"
data = {
    "username": "admin",
    "password": "hunter2"
}

for i in range(3):
    try:
        response = requests.post(url, data=data)
        print(f"Login attempt {i+1} status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")