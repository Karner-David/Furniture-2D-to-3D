import json
import os
import trimesh
import pymeshlab

# Load the pix3d.json metadata
with open('pix3d.json', 'r') as f:
    metadata = json.load(f)

def normalize_mesh(mesh):
    if isinstance(mesh, trimesh.Scene):
        geometries = list(mesh.geometry.values())
        mesh = geometries[0]
    mesh.vertices -= mesh.centroid
    scale = max(mesh.extents)
    mesh.vertices /= scale
    return mesh

def simplify_mesh(mesh, target_faces=1000):
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(mesh.vertices, mesh.faces))
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target_faces)
    simplified_mesh = ms.current_mesh()
    return trimesh.Trimesh(vertices=simplified_mesh.vertex_matrix(), faces=simplified_mesh.face_matrix())

# Iterate over the pix3d metadata
for item in metadata:
    model_rel_path = item['model']  # Get the relative path to the 3D model
    model_full_path = model_rel_path.replace('model', '../model', 1)  # Modify the base path as needed

    # Check if the model exists
    if os.path.exists(model_full_path):
        print(f"Processing model: {model_full_path}")
        
        # Load the mesh
        mesh = trimesh.load(model_full_path)

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