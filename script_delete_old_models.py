import os

# Set the base directory
base_dir = "../model/"

# Walk through the directory tree
for root, dirs, files in os.walk(base_dir):
    for file in files:
        # Check if the file ends with 'simple_normal_model.obj'
        if file.endswith("simple_normal_model.obj"):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
