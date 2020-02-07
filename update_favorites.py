# Import modules
import pandas as pd
import stringdist
import random
import requests
import sys
import json
import pandas as pd

# set variables
path_to_json = "/home/pi/Documents/trusted/meural_cred.json"

with open(path_to_json, "r") as handler:
    info = json.load(handler)

username = info["username"]
password = info["password"]

base_url = "https://api.meural.com/v0"

# Meural api functions
def authenticate(path="/authenticate"):
    req = requests.post(
        base_url + path, data={"username": username, "password": password}
    ).json()
    token = req["token"]
    return token


def get_uploads(token, path="/user/items?count=50&page=1"):
    headers = {"Authorization": "Token " + token}
    items = requests.get(base_url + path, headers=headers).json()
    return items


def get_favorites(token, path="/favorites/items?count=50&page=1"):
    headers = {"Authorization": "Token " + token}
    items = requests.get(base_url + path, headers=headers).json()
    return items


authors = []
names = []
descriptions = []
art_ids = []
token = authenticate()
items = get_favorites(token)

# number of items uploaded in items['count']
for i in range(items["count"]):
    authors.append(items["data"][i]["author"])
    names.append(items["data"][i]["name"])
    descriptions.append(items["data"][i]["description"])
    art_ids.append(items["data"][i]["id"])

favorites = pd.DataFrame(
    {"author": authors, "name": names, "description": descriptions, "art_id": art_ids}
)

favorites.to_csv(r'/home/pi/Documents/python_scripts/meural_canvas/meural_favorites.csv')
