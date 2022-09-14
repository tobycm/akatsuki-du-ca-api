"""
Auto add menber to Discord server with a token received from Discord API
"""

import json
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# ----------------------------------------------------------

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)

CLIENT_ID = settings["CLIENT_ID"]
CLIENT_SECRET = settings["CLIENT_SECRET"]
DISCORD_TOKEN = settings["DISCORD_TOKEN"]
REDIRECT_URI = settings["REDIRECT_URI"]
API_VERSION = settings["API_VERSION"]

ENDPOINT = "https://discord.com/api/" + API_VERSION

# ---------------------------------------------------------

def exchange_code(code):
    """
    Exchange code for access token
    """

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(f'{ENDPOINT}/oauth2/token', data = data, headers = headers)
    return response.json()

# ---------------------------------------------------------

def get_user(access_token):
    """
    Get user ID and name from access token
    """

    url = f"{ENDPOINT}/oauth2/@me"
    headers = {
    "Authorization" : f"Bearer {access_token}"
    }
    response = requests.get(url = url, headers = headers)
    data = response.json()
    return (data["user"]['id'], f"{data['user']['username']}#{data['user']['discriminator']}")

# ------------------------------------------------------------

def add_to_guild(access_token, user_id, bot_token):
    """
    Add user to guild
    """

    url = f"{ENDPOINT}/guilds/912563175919083571/members/{user_id}"
    data = {
    "access_token" : access_token
    }
    headers = {
    "Authorization" : f"Bot {bot_token}",
    'Content-Type': 'application/json'
    }

    response = requests.put(url = url, headers = headers, json = data)
    return response.status_code
# ----------------------------------------------------------

@app.route('/join', methods = ['GET'])
def api_join():
    """
    Add a member to the server
    """

    if 'code' in request.args:

        code = request.args['code']
        access_token = exchange_code(code)["access_token"]
        user_id, user_name = get_user(access_token)

        add_to_guild(access_token, user_id, DISCORD_TOKEN)
        print(f"Added {user_name} to the server")

    return redirect("https://youtube.com/watch?v=dQw4w9WgXcQ", code = 302)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000) # run server on port 5000
