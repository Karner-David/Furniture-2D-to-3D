import json
import os

# Load the metadata JSON file from the Pix3D dataset
with open("pix3d.json", 'r') as f:
    data = json.load(f)

img_model_pairs = {}

for item in data:
    img_path = item['img']
    model_path = item['model']

    img_model_pairs[img_path] = model_path

for img, model in list(img_model_pairs.items()):
    print(f"Image: {img} -> Model: {model}")