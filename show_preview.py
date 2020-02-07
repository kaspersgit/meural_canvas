# Import modules
import time

start_time = time.time()
import stringdist
import random
import requests
import sys
import json
import pandas as pd

print("---modules loaded %s seconds ---" % (time.time() - start_time))

# Meural api base url
base_url = "https://api.meural.com/v0"

# Meural api functions
def authenticate(path="/authenticate"):
    req = requests.post(
        base_url + path, data={"username": username, "password": password}
    ).json()
    token = req["token"]
    token_time = time.time()
    return token, token_time


def preview_item(token, art_id, path="/devices/8292/preview/"):
    headers = {"Authorization": "Token " + token}
    preview = requests.post(base_url + path + str(art_id), headers=headers).json()


# Preview smalles levenshtein distance author
def preview_author(author="rembrandt"):
    distance = {}
    for n in filter(None, favorites.author):
        lh = stringdist.levenshtein_norm(author, n)
        distance[n] = lh

    chosen_author = min(distance, key=distance.get)
    art_ids = favorites[favorites["author"] == chosen_author]["art_id"]
    chosen_art_id = random.choice(list(art_ids))
    print(chosen_art_id)
    # preview item found by keyword on device 8292
    preview_item(token, chosen_art_id)


# time it
print("---functions loaded %s seconds ---" % (time.time() - start_time))

# Check if token time exist otherwise authenticate
if "token_time" not in globals():
    # set variables
    path_to_json = "/home/pi/Documents/trusted/meural_cred.json"

    with open(path_to_json, "r") as handler:
        info = json.load(handler)

    username = info["username"]
    password = info["password"]

    # authenticate
    token, token_time = authenticate()
# If token is older than 300 seconds than re-authenticate
elif (token_time - time.time()) > 300:
    token, token_time = authenticate()

# time it
print("---authenticated %s seconds ---" % (time.time() - start_time))

favorites = pd.read_csv(
    "/home/pi/Documents/python_scripts/meural_canvas/meural_favorites.csv"
)

preview_author(sys.argv[1])

# time it
print("---finished %s seconds ---" % (time.time() - start_time))
