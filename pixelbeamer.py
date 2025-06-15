from PIL import Image
import time
import os
import json
import requests

# Step 1: open config file

with open("config.json", "r") as f:
    CONFIG = json.load(f)

# Step 2: download current status

IMAGE_URL = CONFIG['PIXELEBBE_IMAGE_URL'] + f'?d={int(time.time())}'
RESIZE_FACTOR = CONFIG['RESIZE_FACTOR']

img_data = requests.get(IMAGE_URL).content
with open('output/image.png', 'wb') as handler:
    handler.write(img_data)

status_image = Image.open('output/image.png')
si_newsize = (
    RESIZE_FACTOR * status_image.size[0],
    RESIZE_FACTOR * status_image.size[1]
)
status_image = status_image.resize(si_newsize, resample=Image.NEAREST)

# Step 3: find all templates and generate output for each

TPL_X, TPL_Y = CONFIG['TPL_X'], CONFIG['TPL_Y']

for file in os.listdir("templates/"):
    tpl_im = Image.open(f'templates/{file}')
    tpl_im.paste(status_image, (TPL_X, TPL_Y))
    tpl_im.save('output/' + file)