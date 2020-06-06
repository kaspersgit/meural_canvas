# Import modules

import time

# Uncomment for when you want to time the script
#start_time = time.time()
##

import random
import requests
import warnings
import urllib.request
from PIL import Image

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

def resize_image(original_image):
    meural_res = [1920,1080]
    aspect_ratio_meural = meural_res[0]/meural_res[1]

    # resolution of image
    w, h = image.size
    if (w < meural_res[0]) | (h < meural_res[1]):
        print(1)
        warnings.warn("Original image has lower resolution than Meural Canvas, may lead to unsharp image")
    # get the w/h ratio (to preserve after scaling down)
    aspect_ratio = w/h

    # How much both width and height have to be resized (ratio)
    resize_ratios = [meural_res[0]/w, meural_res[1]/h]
    resize_size = [None] * 2
    for i,j in enumerate(resize_ratios):
        print('Does dimension {} need to be resized? '.format(i) + str(j == max(resize_ratios)))
        if j == max(resize_ratios):
            resize_size[i]=int(1 * meural_res[i])
        else:
            resize_size[i]=int(max(resize_ratios) * image.size[i])
    try:
        resized_image = image.resize((resize_size[0], resize_size[1]))
    except ValueError:
        print("Invalid input to resizing")

    # Cropping the image to make it fit perfectly
    left_top = (int(resize_size[0]/2 - meural_res[0]/2), int(resize_size[1]/2 - meural_res[1]/2))
    right_bottom = (left_top[0] + meural_res[0], left_top[1] + meural_res[1])
    image_area = (left_top + right_bottom)
    final_image = resized_image.crop(image_area)
    return(final_image)

def preview_item(token, art_id, path="/devices/8292/preview/"):
    headers = {"Authorization": "Token " + token}
    preview = requests.post(base_url + path + str(art_id), headers=headers).json()


def upload_image(token, image_path, path="/items"):
    headers = {"Authorization": "Token " + token}
    files = {'image': open(image_path, 'rb')}
    r = requests.post(base_url + path, headers=headers, files=files).json()
    return(r)

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


# Adding information about user agent
# chance otherwise is that website block when they see python trying to access
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

#%%
# setting filename and image URL
filename = 'image_now.jpg'
image_url = sys.argv[1]

# calling urlretrieve function to get resource
urllib.request.urlretrieve(image_url, filename)

image = Image.open('image_now.jpg')
final_image = resize_image(image)
final_image.save('resized_image.jpg')
response = upload_image(token,"/Users/kasper.de-harder/Downloads/resized_image.jpg")
preview_item(token, art_id = response['data']['id'])

###########################################################

# time it
# Uncomment for when you want to time the script
#print("---finished %s seconds ---" % round((time.time() - start_time),2))
