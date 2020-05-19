# Import modules

import time

# Uncomment for when you want to time the script
#start_time = time.time()
##

import random
import requests

# Uncomment for when you want to time the script
#print("---requests loaded %s seconds ---" % round((time.time() - start_time),2))
import sys
import json
import csv

# Uncomment for when you want to time the script
#print("---modules loaded %s seconds ---" % round((time.time() - start_time),2))

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
    #print(chosen_art_id)
    # preview item found by keyword on device 8292
    preview_item(token, chosen_art_id)
    return(author_artwork[chosen_art_id],chosen_author)


# time it
# Uncomment for when you want to time the script
#print("---functions loaded %s seconds ---" % round((time.time() - start_time),2))

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
# Uncomment for when you want to time the script
#print("---authenticated %s seconds ---" % round((time.time() - start_time),2))

# Importing required libraries
import urllib.request

# Adding information about user agent
# chance otherwise is that website block when they see python trying to access
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# setting filename and image URL
filename = 'image_now.jpg'
image_url = 'https://ichef.bbci.co.uk/onesport/cps/800/cpsprodpb/1384/production/_111769940_whatsubject.jpg'

# calling urlretrieve function to get resource
urllib.request.urlretrieve(image_url, filename)

from PIL import Image

meural_res = [1920,1080]
image = Image.open('image_now.jpg')
w, h = image.size
aspect_ratio = w/h
resize_ratios = [meural_res[0]/w, meural_res[1]/h]
for i,j in enumerate(resize_ratios):
    print(j == max(resize_ratios))
    if j == max(resize_ratios):
        resize_ratio[i]=1 * meural_res[i]
    else:
        resize_ratio[i]=aspect_ratio * meural_res[i]
try:
    resized_image = image.resize((resize_ratio[0], resize_ratio[1]))
except ValueError:
    print("Invalid input to resizing")

###########################################################

artwork_name, author = preview_author(sys.argv[1])
print("Showing {} made by {}".format(artwork_name, author))


# time it
# Uncomment for when you want to time the script
#print("---finished %s seconds ---" % round((time.time() - start_time),2))
