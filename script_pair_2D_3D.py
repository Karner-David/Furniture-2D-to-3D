import json
import os

# Load the metadata from pix3d.json
with open('pix3d.json', 'r') as f:
    metadata = json.load(f)

resized_img_head = '../resized_images'
model_head = '../model'


image_to_model_map = {}


for item in metadata:

    orig_img_path = item['img'].replace('img/', '')
    img_full_path = os.path.join(resized_img_head, orig_img_path)


    model_rel_path = item['model'].replace('model', '../model', 1)  # Replace only the first 'model'
    model_full_path = model_rel_path.replace('.obj', '_simple_normal.obj')

    if os.path.exists(img_full_path) and os.path.exists(model_full_path):
        image_to_model_map[img_full_path] = model_full_path

# Save the mapping to a new JSON file
with open('resized_img_processed_model_mapping.json', 'w') as outfile:
    json.dump(image_to_model_map, outfile, indent=4)

print(f'Mapping saved to resized_img_processed_model_mapping.json')
