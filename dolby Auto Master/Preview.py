import os
import requests

# Set or replace these values
body = {
    "inputs": [
        {"source": "dlb://in/example.wav", "segment": {"start": 10, "duration": 30}}
    ],
    "outputs": [
        {
            "destination": "dlb://out/example-master-preview-a.mp4",
            "master": {"dynamic_eq": {"preset": "a"}},
        },
        {
            "destination": "dlb://out/example-master-preview-b.mp4",
            "master": {"dynamic_eq": {"preset": "b"}},
        },
        {
            "destination": "dlb://out/example-master-preview-c.mp4",
            "master": {"dynamic_eq": {"preset": "c"}},
        },
    ],
}

url = "https://api.dolby.com/media/master/preview"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(url, json=body, headers=headers)
response.raise_for_status()
print(response.json())
