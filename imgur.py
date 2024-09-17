import os
import base64
import requests


def upload(client_id, image_path):
    """Upload image to Imgur and return URL."""
    headers = {"Authorization": f"Client-ID {client_id}"}
    url = "https://api.imgur.com/3/image"

    with open(image_path, "rb") as file:
        data = file.read()
    base64_data = base64.b64encode(data)

    response = requests.post(
        url,
        headers=headers,
        data={
            "image": base64_data,
            "type": "base64",
            "name": os.path.basename(image_path),
            "title": "Image"
        },
    )
    json = response.json()
    url = response.json()["data"]["link"]
    return url
