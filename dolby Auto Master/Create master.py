import os
import requests

# Set or replace these values
body = {
    "inputs": [{"source": "dlb://in/example.wav"}],
    "outputs": [
        {
            "destination": "dlb://out/example-mastered.wav",
            "master": {"dynamic_eq": {"preset": "c"}},
        }
    ],
}

url = "https://api.dolby.com/media/master"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(url, json=body, headers=headers)
response.raise_for_status()
print(response.json())
