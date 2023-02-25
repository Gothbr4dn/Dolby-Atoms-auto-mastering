https://docs.dolby.io/media-apis/docs/quick-start-to-music-mastering
# Music Mastering API

Getting started

To get started you'll follow these steps.

Get your API token
Prepare your media
Make a Music Mastering request
Check the job status
Download and review the output
1. Get your API token

To use the Music Mastering API, you need an API token. To learn more about how to get an API token, see API Authentication.

2. Prepare your media

Make your media available for mastering:

a. Use your own cloud storage provider
b. Use our Dolby Media Input API

a. Use your own cloud storage provider

You will want to consider this option when you move your applications into production. Our services are able to work with many popular cloud storage services such as AWS S3, Azure Blob Storage, GCP Cloud Storage, or your own services with basic or token based authentication.

See the Media Input and Output guide for more detail on various storage options.

b. Use our Dolby Media Input API (optional)

The Media Input API was designed to give you a quick way to upload media while evaluating the Media APIs. We can securely store your media temporarily, any media you upload will be removed regularly so _shouldn't be used for permanent storage.

Call Start Media Input to identify a shortcut url. It must begin with dlb:// but otherwise is your own personal unique identifier. Some valid examples:

dlb://example.mp4
dlb://input/your-favorite-podcast.mp4
dlb://usr/home/me/voice-memo.wav
You can think of this like an object key that is used to identify a file for your account. Once you call POST /media/input you'll be returned a new url in the response. This is a pre-signed URL to a cloud storage location you will use to upload the file. You do that by making a PUT request with your media.

```
import os
import requests

# Set or replace these values

file_path = os.environ["INPUT_MEDIA_LOCAL_PATH"]

# Declare your dlb:// location

url = "https://api.dolby.com/media/input"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

body = {"url": "dlb://in/example.wav"}

response = requests.post(url, json=body, headers=headers)
response.raise_for_status()
data = response.json()
presigned_url = data["url"]
```

# Upload your media to the pre-signed url response
```
print("Uploading {0} to {1}".format(file_path, presigned_url))
with open(file_path, "rb") as input_file:
    requests.put(presigned_url, data=input_file)
Once the upload is complete, you'll be able to refer to this media with the dlb://in/example.wav shortcut.
```

3. Make a Music Mastering request

The following examples include using a sample of your music file to preview 3 different music mastering presets. When the preset samples are complete, you can move on to creating a music master with your preferred preset.

After you start a music mastering request, you use the returned job_id to make job status requests. After a Successful job status is returned, you can download and review your music master preview audio file or music master audio file.

3.1 Preview a section of your audio file using three different presets
```
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
```
Check the job status of the previewed content

You can learn more about this in the How It Works section of the Introduction.

For this GET /media/master/preview request, use the job_id returned from the previous step. In these examples, it is specified as an environment variable that you'll need to set or replace in the code samples.
```
import os
import requests

url = "https://api.dolby.com/media/master/preview"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

params = {"job_id": os.environ["DOLBYIO_JOB_ID"]}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()
print(response.json())
```
While the job is still in progress, you will be able to see the status and progress values returned.
```
JSON

{
  "path": "/media/master/preview",
  "status": "Running",
  "progress": 42
}
```
If you re-run and call again after a period of time you'll see the status changes and the output you originally specified will be ready for download.
```
JSON

{
  "path": "/media/master/preview",
  "progress": 100,
  "result": {},
  "status": "Success"
}
```
Download the completed previews

When the Music Master previews are complete, the files will be PUT in the output location specified when the job was started. If you used the optional Dolby.io temporary storage, you will need to follow a couple steps to download your media. For more information, see the Dolby.io Media Temporary Cloud Storage guide.
```
import os
import shutil
import requests

output_path = os.environ["PREVIEW_A_MEDIA_LOCAL_PATH"]

url = "https://api.dolby.com/media/output"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

preview_url = "dlb://out/example-master-preview-a.mp4"

args = {"url": preview_url}

with requests.get(url, params=args, headers=headers, stream=True) as response:
    response.raise_for_status()
    response.raw.decode_content = True
    print("Downloading from {0} into {1}".format(response.url, output_path))
    with open(output_path, "wb") as output_file:
        shutil.copyfileobj(response.raw, output_file)
```
3.2 Create a music master
```
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
```
Check the job status of the music master

You can learn more about this in the How It Works section of the Introduction.

For this GET /media/master request, use the job_id returned from the previous step. In these examples, it is specified as an environment variable that you'll need to set or replace in the code samples.
```
import os
import requests

url = "https://api.dolby.com/media/master"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

params = {"job_id": os.environ["DOLBYIO_JOB_ID"]}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()
print(response.json())
```
While the job is still in progress, you will be able to see the status and progress values returned.
```
JSON

{
  "path": "/media/master",
  "status": "Running",
  "progress": 42
}
```
If you re-run and call again after a period of time you'll see the status changes and the output you originally specified will be ready for download.
```
JSON

{
  "path": "/media/master",
  "progress": 100,
  "result": {},
  "status": "Success"
}
```
Download the completed music master

When the Music Master is complete, the file will be PUT in the output location specified when the job was started. If you used the optional Dolby.io temporary storage, you will need to follow a couple steps to download your media. For more information, see the Dolby.io Media Temporary Cloud Storage guide.
```
import os
import shutil
import requests

output_path = os.environ["OUTPUT_MEDIA_LOCAL_PATH"]

url = "https://api.dolby.com/media/output"
headers = {
    "Authorization": "Bearer {0}".format(api_token),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

args = {"url": "dlb://out/example-mastered.wav"}

with requests.get(url, params=args, headers=headers, stream=True) as response:
    response.raise_for_status()
    response.raw.decode_content = True
    print("Downloading from {0} into {1}".format(response.url, output_path))
    with open(output_path, "wb") as output_file:
        shutil.copyfileobj(response.raw, output_file)
 ```
