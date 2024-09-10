import os
import json

def extract_materials(mtl_file):
    materials = {}
    cur_material = None

    with open(mtl_file, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('newmtl'):
                cur_material = line.split()[1]
                materials[cur_material] = {}

            # Diffuse Color
            elif line.startswith('Kd'):
                diffuse_color = list(map(float, line.split()[1:]))
                materials[cur_material]['diffuse'] = diffuse_color

            # Shininess
            elif line.startswith('Ns'):
                shininess = float(line.split()[1])
                materials[cur_material]['shininess'] = shininess

            # Ambient Color
            elif line.startswith('Ka'):
                ambient_color = list(map(float, line.split()[1:]))
                materials[cur_material]['ambient'] = ambient_color

            # Specular Color
            elif line.startswith('Ks'):
                specular_color = list(map(float, line.split()[1:]))
                materials[cur_material]['specular'] = specular_color
            
            # Transparency
            elif line.startswith('d'):
                transparency = float(line.split()[1])
                materials[cur_material]['transparency'] = transparency

    return materials

def process_through_directory(directory):
    material_map = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mtl'):
                mtl_file_path = os.path.join(root, file)

                material_properties = extract_materials(mtl_file_path)

                relative_path = os.path.relpath(mtl_file_path, directory)
                material_map[relative_path] = material_properties

    return material_map

mtl_dir = '../model'

material_properties_map = process_through_directory(mtl_dir)

with open('material_properties.json', 'w') as json_file:
    json.dump(material_properties_map, json_file, indent=4)

print('Material properties saved to material_properties.json')
            