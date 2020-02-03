# Import modules
import pandas as pd 
import stringdist
import random
import requests
import sys
import json

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


def preview_item(token, art_id, path="/devices/8292/preview/"):
    headers = {"Authorization": "Token " + token}
    preview = requests.post(base_url + path + str(art_id), headers=headers).json()


authors = []
names = []
descriptions = []
art_ids = []
token = authenticate()
items = get_uploads(token)

# number of items uploaded in items['count']
for i in range(items["count"]):
    authors.append(items["data"][i]["author"])
    names.append(items["data"][i]["name"])
    descriptions.append(items["data"][i]["description"])
    art_ids.append(items["data"][i]["id"])

uploads = pd.DataFrame(
    {"author": authors, "name": names, "description": descriptions, "art_id": art_ids}
)

# Preview smalles levenshtein distance author
def preview_author(author="rembrandt"):
    distance = {}
    for n in filter(None, uploads.author):
        lh = stringdist.levenshtein_norm(author, n)
        distance[n] = lh

    chosen_author = min(distance, key=distance.get)
    art_ids = uploads[uploads['author']==chosen_author]['art_id']
    chosen_art_id = random.choice(list(art_ids))
    print(chosen_art_id)
    # preview item found by keyword on device 8292
    preview_item(token, chosen_art_id)


preview_author(sys.argv[1])
