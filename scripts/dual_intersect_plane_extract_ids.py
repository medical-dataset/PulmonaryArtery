"""
Interactive tool for exploring and selecting pulmonary artery slicing planes on a 3D right ventricle (RV) mesh.
This version includes:
- Standard coordinate XYZ axes next to the selected plane
- A normal vector with reduced length and a distinct color (orange)
- Visual slicing and geometric measurement
- Saves intersected point IDs and derived geometry features to JSON
"""

import pyvista as pv
import numpy as np
import json
from scipy.spatial import ConvexHull
import os
import sys
import atexit
import warnings

# === Shutdown message ===
def on_exit():
    print("\n Visualization closed successfully. Goodbye!")
atexit.register(on_exit)

# === Suppress warnings ===
warnings.filterwarnings("ignore", category=DeprecationWarning)

# === Setup paths ===
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)
print("Working directory:", os.getcwd())
print("Base path added to sys.path:", base_path)

# === Imports ===
from utils.mesh_utils import load_mesh

# === Plane intersection using slicing (accurate ring) ===
def intersect_mesh_with_plane(mesh, origin, normal):
    origin = np.asarray(origin, dtype=np.float64)
    normal = np.asarray(normal, dtype=np.float64)
    sliced = mesh.slice(normal=normal, origin=origin)

    if sliced.n_points == 0:
        print(" No intersection points found. Check the plane position and orientation.")

    intersected_ids = []
    for i, p in enumerate(sliced.points):
        try:
            closest_id = mesh.find_closest_point(p)
            intersected_ids.append(closest_id)
        except Exception as e:
            print(f" Error finding closest point for {p} at index {i}: {e}")

    return sliced.points, intersected_ids

# === Geometry features ===
def compute_geometry_features(points):
    if len(points) < 3:
        return {"area": 0.0, "major_diameter": 0.0, "minor_diameter": 0.0}
    center = points.mean(axis=0)
    _, _, Vt = np.linalg.svd(points - center)
    projected = (points - center) @ Vt[:2].T
    hull = ConvexHull(projected)
    area = hull.volume
    x_span = projected[:, 0].ptp()
    y_span = projected[:, 1].ptp()
    return {"area": area, "major_diameter": max(x_span, y_span), "minor_diameter": min(x_span, y_span)}

# === Load mesh ===
TEMPLATE_PATH = os.path.join(base_path, "data", "template", "vtks", "RV_ED.vtk")
OUTPUT_JSON = os.path.join(base_path, "output", "pa_plane_features.json")
mesh = load_mesh(TEMPLATE_PATH)
print("Mesh center:", mesh.center)

# === Plotter setup ===
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="lightgray", opacity=0.3, smooth_shading=True)
plotter.add_axes(line_width=2, color='black', x_color='red', y_color='green', z_color='blue')
chosen_plane = {"origin": None, "normal": [0, 0, 1]}

# === Picking ===
def on_pick(point, picker=None):
    if hasattr(point, 'points'):
        point = point.points[0]
    print("Picked point:", point.tolist())
    chosen_plane["origin"] = point
    plotter.add_plane_widget(
        callback=on_plane_update,
        normal=chosen_plane["normal"],
        origin=point,
        color="cyan",
        implicit=True,
        outline_translation=True,
        assign_to_axis=None,
        tubing=False,
        factor=1.0
    )



# === Plane update ===
def on_plane_update(normal, origin):
    chosen_plane["origin"] = origin
    chosen_plane["normal"] = normal
    points, ids = intersect_mesh_with_plane(mesh, origin, normal)

    if "slice_points" in plotter.actors:
        plotter.remove_actor("slice_points")
    plotter.add_points(points, color='red', point_size=8, render_points_as_spheres=True, name="slice_points")

    # Normal vector arrow (dark green)
    if "normal_arrow" in plotter.actors:
        plotter.remove_actor("normal_arrow")
    normal_arrow = pv.Arrow(start=origin, direction=normal, scale=2.5)
    # Normal vector arrow (dark purple)
    if "normal_arrow" in plotter.actors:
        plotter.remove_actor("normal_arrow")
    normal_arrow = pv.Arrow(start=origin, direction=normal, scale=2.5)
    plotter.add_mesh(normal_arrow, color="indigo", name="normal_arrow")

    # Local coordinate axes at origin
    for axis_name in ["x_axis_local", "y_axis_local", "z_axis_local"]:
        if axis_name in plotter.actors:
            plotter.remove_actor(axis_name)

    axis_len = 2.0
    x_axis = pv.Arrow(start=origin, direction=[1, 0, 0], scale=axis_len)
    y_axis = pv.Arrow(start=origin, direction=[0, 1, 0], scale=axis_len)
    z_axis = pv.Arrow(start=origin, direction=[0, 0, 1], scale=axis_len)

    plotter.add_mesh(x_axis, color="red", name="x_axis_local")
    plotter.add_mesh(y_axis, color="green", name="y_axis_local")
    plotter.add_mesh(z_axis, color="blue", name="z_axis_local")


# === Finalize and Save ===
def finalize_selection():
    origin = chosen_plane["origin"]
    normal = chosen_plane["normal"]
    if origin is None or normal is None:
        print("Please define the slicing plane first.")
        return
    points, ids = intersect_mesh_with_plane(mesh, origin, normal)
    features = compute_geometry_features(np.array(points, dtype=np.float64))
    output = {
        "origin": list(map(float, origin)),
        "normal": list(map(float, normal)),
        "point_ids": list(map(int, ids)),
        "intersection_count": int(len(points)),
        "template_point_count": int(mesh.n_points),
        "point_hash": float(np.sum(mesh.points.astype(np.float64))),
        "first_5_points": mesh.points[:5].astype(np.float64).tolist(),
        "area": float(features['area']),
        "major_diameter": float(features['major_diameter']),
        "minor_diameter": float(features['minor_diameter'])
    }
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f, indent=2)
    print("\nFINAL SELECTION")
    print(f"→ Origin: {origin}")
    print(f"→ Normal: {normal}")
    print(f"→ {len(points)} points | Area ≈ {features['area']:.2f} | Major ≈ {features['major_diameter']:.2f}")
    print(f"→ Saved to: {OUTPUT_JSON}")
    try: plotter.remove_text("success_message")
    except: pass
    plotter.add_text("PA features saved successfully!", position="lower_left", font_size=14, color="lightgreen", name="success_message")

# === UI text ===
plotter.add_text(
    " Left-click to place slicing plane\n Drag to adjust plane\n Press SPACE to finalize",
    position="upper_left", font_size=12, color="#00ccff")

# === Bind events ===
plotter.enable_point_picking(callback=on_pick, use_mesh=True, show_message=True)
plotter.add_key_event("space", finalize_selection)

# === Show ===
plotter.show()

# === Graceful close ===
def safe_close_plotter():
    try:
        plotter.close()
    except:
        pass
atexit.register(safe_close_plotter)
