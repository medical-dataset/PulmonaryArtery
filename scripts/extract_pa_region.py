
# ----------------------
# scripts/extract_pa_region.py
# ----------------------
from utils.mesh_utils import load_mesh
from src.plane_intersection import intersect_mesh_with_plane
from src.io import save_point_ids

origin = [-10, 20, 5]
normal = [0.1, -0.3, 0.9]

mesh = load_mesh('data/template_mesh.vtk')
points, ids = intersect_mesh_with_plane(mesh, origin, normal)
save_point_ids(ids, 'output/pa_point_ids.json')

#with open('output/pa_point_ids.json', 'w') as f:
#    json.dump(ids, f)
