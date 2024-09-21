import json
import os
import trimesh
import pymeshlab
import numpy as np

# Load the pix3d.json metadata
with open('pix3d.json', 'r') as f:
    metadata = json.load(f)

def normalize_mesh(mesh):
    if isinstance(mesh, trimesh.Scene):
        geometries = list(mesh.geometry.values())
        mesh = geometries[0]
    print(f"Original vertex count before normalization: {len(mesh.vertices)}")
    mesh.vertices -= mesh.centroid
    scale = max(mesh.extents)
    mesh.vertices /= scale
    print(f"Vertex count after normalization: {len(mesh.vertices)}")
    return mesh

def simplify_mesh(mesh, target_faces=4000):
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(mesh.vertices, mesh.faces))
    print(f"Original face count before simplification: {len(mesh.faces)}")

    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target_faces)
    simplified_mesh = ms.current_mesh()

    print(f"Face count after simplification: {simplified_mesh.face_number()}")

    return trimesh.Trimesh(vertices=simplified_mesh.vertex_matrix(), faces=simplified_mesh.face_matrix())

def load_complete_mesh(path):
    # Load the mesh
    loaded_mesh = trimesh.load(path)
    
    # If the mesh is a scene (multiple parts), concatenate all the parts
    if isinstance(loaded_mesh, trimesh.Scene):
        combined_vertices = []
        combined_faces = []
        current_vertex_offset = 0
        
        for geom in loaded_mesh.geometry.values():
            vertices = geom.vertices
            faces = geom.faces + current_vertex_offset
            combined_vertices.append(vertices)
            combined_faces.append(faces)
            current_vertex_offset += len(vertices)
        
        # Create a single mesh from the concatenated parts
        combined_vertices = np.vstack(combined_vertices)
        combined_faces = np.vstack(combined_faces)
        full_mesh = trimesh.Trimesh(vertices=combined_vertices, faces=combined_faces)
    else:
        full_mesh = loaded_mesh
    
    print(f"Loaded complete mesh with {len(full_mesh.vertices)} vertices and {len(full_mesh.faces)} faces.")
    return full_mesh

# Iterate over the pix3d metadata
for item in metadata:
    model_rel_path = item['model']  # Get the relative path to the 3D model
    model_full_path = model_rel_path.replace('model', '../model', 1)  # Modify the base path as needed

    # Check if the model exists
    if os.path.exists(model_full_path):
        print(f"Processing model: {model_full_path}")
        
        # Load the mesh
        mesh = load_complete_mesh(model_full_path)

        # Normalize the mesh
        normal_mesh = normalize_mesh(mesh)

        # Simplify the mesh
        simple_mesh = simplify_mesh(normal_mesh)

        # Define output path for the simplified model
        output_path = model_full_path.replace('.obj', '_simple_normal.obj')
        simple_mesh.export(output_path)
        print(f"Simplified model saved to: {output_path}")
    else:
        print(f"Model not found: {model_full_path}")

# model_to_fix = '../model/chair/IKEA_SOLSTA_OLARP/model.obj'

# if os.path.exists(model_to_fix):
#     print(f"Processing model: {model_to_fix}")
    
#     # Load the mesh
#     mesh = load_complete_mesh(model_to_fix)

#     # Normalize the mesh
#     normal_mesh = normalize_mesh(mesh)

#     # Simplify the mesh
#     simple_mesh = simplify_mesh(normal_mesh)

#     # Define output path for the simplified model
#     output_path = model_to_fix.replace('.obj', '_simple_normal.obj')
#     simple_mesh.export(output_path)
#     print(f"Simplified model saved to: {output_path}")
# else:
#     print(f"Model not found: {model_to_fix}")