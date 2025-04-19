# ----------------------
# scripts/compute_pa_features.py
# ----------------------
from src.mesh_utils import load_mesh
from src.io import load_point_ids
from src.feature_extraction import compute_cross_section_area
import pandas as pd
import os

id_list = load_point_ids('output/pa_point_ids.json')
input_dir = 'data/subject_meshes/'
subjects = sorted(os.listdir(input_dir))

records = []
for filename in subjects:
    path = os.path.join(input_dir, filename)
    mesh = load_mesh(path)
    points = mesh.points[id_list]
    area = compute_cross_section_area(points)
    records.append({"subject": filename, "area": area})

pd.DataFrame(records).to_csv('output/subject_measurements.csv', index=False)