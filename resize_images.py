from PIL import Image
import os

def resize_images(image_dir, output_dir, size=(256, 256)):
    os.makedirs(output_dir, exist_ok=True)
    for img_name in os.listdir(image_dir):
        print(img_name)
        img_path = os.path.join(image_dir, img_name)
        img = Image.open(img_path)
        img_resized = img.resize(size)

        if img_resized.mode == 'RGBA':
            img_resized = img_resized.convert('RGB')
        img_resized.save(os.path.join(output_dir, img_name))

input_dir = 'img'

output_dir = 'resized_images'

for folder in os.listdir(input_dir):
    print(folder)
    input_path = os.path.join(input_dir, folder)
    output_path = os.path.join(output_dir, folder)

    # Skip any non-directory items
    if not os.path.isdir(input_path):
        continue

    print(input_path)
    resize_images(input_path, output_path)