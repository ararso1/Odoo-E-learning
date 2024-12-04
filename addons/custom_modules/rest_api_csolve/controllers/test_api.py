import requests
import json

# Define the URL for the Odoo endpoint
url = "http://127.0.0.1:8069/csolve_create_user"

# Payload with user data
payload = {
    "name": "alisho",
    "login": "alisho",
    "password": "alisho",
    "email": "alisho.doe@example.com"
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check response status
    if response.status_code == 200:
        print("Request was successful.")
        print("Response:", response.json())  # Assuming the response is in JSON format
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Error message:", response.text)

except Exception as e:
    print("An error occurred:", str(e))
