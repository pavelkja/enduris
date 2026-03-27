import requests

url = "http://127.0.0.1:8000/api/dashboard/health"
params = {
    "user_id": "b506b832-76f2-48f2-b1a1-e00ccef8b988"
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.text)