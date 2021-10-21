# to get playlist id for a channel:
# GET https://www.googleapis.com/youtube/v3/channels?id={config['channel_id'}&part=contentDetails&&key={config['api_key']}
# playlist id is at ["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

import requests
import yaml
import json

with open("config.yml") as f:
    config = yaml.safe_load(f)

YT_PARAMS = {
    "key": config["key"],
    "maxResults": 50,
    "part": "snippet",
    "playlistId": config["playlist"]
}

def get_new(new_data) -> list:
    with open("data.json", "r") as f:
        old_data = json.load(f)

    return [i for i in new_data["items"][:5] if i not in old_data]

def get_videos():
    req = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=YT_PARAMS)
    return req.json()

def post_webhook(title, url):
    data = {
        "content": f"@everyone\nNew YouTube video out: {title} -> {url}",
        "username": "YouTube Notifications",
        "avatar_url": "https://www.logo.wine/a/logo/YouTube/YouTube-Icon-Full-Color-Logo.wine.svg"
    }

    requests.post(config["webhook"], json=data)

    print(f"Posted Webhook: {title} - {url}")

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data["items"], f, indent=4)

def main():
    data = get_videos()
    new = get_new(data)
    for video in new:
        post_webhook(video["snippet"]["title"], "https://www.youtube.com/watch?v=" + video["id"])
    save_data(data)

if __name__ == "__main__":
    main()