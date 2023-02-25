import os
import requests

# Set or replace these values

file_path = os.environ["INPUT_MEDIA_LOCAL_PATH"]

# Declare your dlb:// location

url = "https://api.dolby.com/media/input"
headers = {
    "Authorization": "Bearer {0}".format( API Key),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

body = {"url": "dlb://in/Beat.wav"}

response = requests.post(url, json=body, headers=headers)
response.raise_for_status()
data = response.json()
presigned_url = data["url"]

# Upload your media to the pre-signed url response

print("Uploading {0} to {1}".format(file_path, presigned_url))
with open(file_path, "rb") as input_file:
    requests.put(presigned_url, data=input_file)