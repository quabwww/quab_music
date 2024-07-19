import requests

url = "http://localhost:9000/api/musica/"
data = {
    "guild_id": 1077968892535775262,
    "channel_id": 1100148368996573265,
    "user_id": 1073383604576591974,
    "url": "I'll Do It"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
