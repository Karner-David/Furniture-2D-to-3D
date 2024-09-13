import os
import json

def extract_materials(mtl_file):
    materials = {}
    cur_material = None

    default_materials = {
        'diffuse': [1.0, 1.0, 1.0],  
        'shininess': 96.078431,       
        'ambient': [0.0, 0.0, 0.0],  
        'specular': [0.0, 0.0, 0.0], 
        'transparency': 1.0,      
        'illumination': 2 
    }

    with open(mtl_file, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('newmtl'):
                cur_material = line.split()[1]
                materials[cur_material] = default_materials.copy()

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

            elif line.startswith('map_Kd'):
                texture_map = line.split()[1]
                materials[cur_material]['texture_map'] = texture_map

            elif line.startswith('illum'):
                illumination = int(line.split()[1])
                materials[cur_material]['illumination'] = illumination

    return materials

def process_through_directory(directory):
    material_map = {}

    for root, dirs, files in os.walk(directory):
        mtl_file_path = None

        # Skip directories with "SS" prefix in file names
        if any('SS' in file for file in files):
            print(f"Skipping {root} due to missing or SS-prefixed models.")
            continue

        for file in files:
            if file.endswith('.mtl'):
                mtl_file_path = os.path.join(root, file)
                break

        if mtl_file_path:
            material_properties = extract_materials(mtl_file_path)

            for file in files:
                if file.endswith('_simple_normal.obj'):
                    obj_file_path = os.path.join(root, file)
                    
                    rel_path = os.path.relpath(obj_file_path, directory)
                    material_map[rel_path] = material_properties

    return material_map

mtl_dir = '../model'

material_properties_map = process_through_directory(mtl_dir)

with open('material_properties.json', 'w') as json_file:
    json.dump(material_properties_map, json_file, indent=4)

print('Material properties saved to material_properties.json')
            