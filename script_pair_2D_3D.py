import json
import os

with open('pix3d.json', 'r') as f:
    metadata = json.load(f)

resized_img_head = '../resized_images'
model_head = '../model'

image_to_model_map = {}

for item in metadata:
    orig_img_path = item['img'].replace('img/', '')
    img_full_path = os.path.join(resized_img_head, orig_img_path)

    model_path = item['model'].replace('model/', '')
    model_full_path = os.path.join(model_head, model_path)

    model_dir = os.path.dirname(model_full_path)
    processed_model_path = os.path.join(model_dir, 'simple_normal_model.obj')

    if os.path.exists(img_full_path) and os.path.exists(processed_model_path):
        # save pair into map
        image_to_model_map[img_full_path] = processed_model_path

with open('resized_img_processed_model_mapping.json', 'w') as outfile:
    json.dump(image_to_model_map, outfile, indent=4)

print(f'Mapping saved to resized_image_processed_model_mapping.json')
