import os

head_path = '../model'

for classification in os.listdir(head_path):
    classification_path = os.path.join(head_path, classification)

    if os.path.isdir(classification_path):
        for furniture_piece in os.listdir(classification_path):
            furniture_path = os.path.join(classification_path, furniture_piece)

            if os.path.isdir(furniture_path):
                for file in os.listdir(furniture_path):
                    if (file.endswith('.mtl')):
                        old_path = os.path.join(furniture_path, file)
                        new_path = os.path.join(furniture_path, 'model.mtl')

                        os.rename(old_path, new_path)
                        print(f'Renamed {old_path} to {new_path}')