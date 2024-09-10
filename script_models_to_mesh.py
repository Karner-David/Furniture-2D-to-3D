import os
import pymeshlab

def normalize_mesh(mesh):
    if isinstance(mesh, trimesh.Scene):
        geometries = list(mesh.geometry.values())
        mesh = geometries[0]
    mesh.vertices -=mesh.centroid
    scale = max(mesh.extents)
    mesh.vertices /= scale
    return mesh

def simplify_mesh(mesh, target_faces=1000):
    ms = pymeshlab.MeshSet()

    ms.add_mesh(pymeshlab.Mesh(mesh.vertices, mesh.faces))

    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target_faces)

    simplified_mesh = ms.current_mesh()
    return trimesh.Trimesh(vertices=simplified_mesh.vertex_matrix(), faces=simplified_mesh.face_matrix())


from pywavefront import Wavefront

def load_with_texture(obj_file, mtl_file):
    scene = Wavefront(obj_file, create_materials=True)
    return scene

head_dir = '../model'

for classification in os.listdir(head_dir):
    classification_path = os.path.join(head_dir, classification)

    if os.path.isdir(classification_path):
        for furniture_piece in os.listdir(classification_path):
            furniture_path = os.path.join(classification_path, furniture_piece, 'model.obj')

            if os.path.exists(furniture_path):
                mesh = trimesh.load(furniture_path)

                normal_mesh = normalize_mesh(mesh)

                simple_mesh = simplify_mesh(normal_mesh)

                output_path = os.path.join(classification_path, furniture_piece, 'simple_normal_model.obj')
                simple_mesh.export(output_path)