# Import modules
import time

start_time = time.time()
import stringdist
import random
import requests

print("---requests loaded %s seconds ---" % (time.time() - start_time))
import sys
import json
import csv

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
    for n in filter(None, favorites.keys()):
        lh = stringdist.levenshtein_norm(author, n)
        distance[n] = lh

    chosen_author = min(distance, key=distance.get)
    art_ids = favorites[chosen_author]
    chosen_art_id = random.choice(art_ids)
    print(chosen_art_id)
    # preview item found by keyword on device 8292
    preview_item(token, chosen_art_id)
    return(chosen_author)


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

with open(
    "/home/pi/Documents/python_scripts/meural_canvas/meural_favorites.csv",
    mode="r",
    encoding="utf-8",
) as infile:
    reader = csv.reader(infile)
    favorites = {}
    for rows in reader:
        if rows[2] not in favorites.keys():
            favorites[rows[2]] = [rows[1]]
        else:
            favorites[rows[2]].append(rows[1])
    del favorites["author"]

author = preview_author(sys.argv[1])
print("Showing creation made by "+author)

# time it
print("---finished %s seconds ---" % (time.time() - start_time))
