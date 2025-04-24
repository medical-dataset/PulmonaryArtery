# # Interactive pulmonary artery extraction tool
# # Allows user to click on the mesh, adjust a slicing plane, and extract geometric features

# import pyvista as pv
# import numpy as np
# import json
# from scipy.spatial import ConvexHull
# import os
# import sys
# import atexit
# import warnings

# def on_exit():
#     print(" \n Visualization closed successfully. Goodbye!")

# atexit.register(on_exit)

# # Suppress PyVista deprecation warnings and shutdown errors
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # === Setup project path ===
# base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, base_path)

# # Debug info
# print("Working directory:", os.getcwd())
# print("Base path added to sys.path:", base_path)

# # === Import project modules ===
# from utils.mesh_utils import load_mesh
# from src.plane_intersection import intersect_mesh_with_plane

# # === Configuration ===
# TEMPLATE_PATH = os.path.join(base_path, "data", "template", "vtks", "RV_ED.vtk")
# #TEMPLATE_PATH = r'\\isd_netapp\cardiac$\UKBB_40616\4D_Segmented_2.0_2nd_batch_18k\1000213\vtks\RV_ED.vtk'

# OUTPUT_JSON = os.path.join(base_path, "output", "pa_plane_features.json")

# # Load the 3D mesh (right heart at end-diastole)
# mesh = load_mesh(TEMPLATE_PATH)
# print("Mesh center:", mesh.center)

# # Create a PyVista plotter for interactive visualization
# plotter = pv.Plotter()
# plotter.add_mesh(mesh, color="lightgray", opacity=0.3, smooth_shading=True)

# # Shared storage for current plane parameters
# chosen_plane = {"origin": None, "normal": [0, 0, 1]}

# # --- Compute geometric features from intersection points ---
# def compute_geometry_features(points):
#     if len(points) < 3:
#         return {"area": 0.0, "major_diameter": 0.0, "minor_diameter": 0.0}

#     # Center and project to 2D for area and diameter estimation
#     center = points.mean(axis=0)
#     _, _, Vt = np.linalg.svd(points - center)
#     projected = (points - center) @ Vt[:2].T

#     # Estimate area via convex hull
#     hull = ConvexHull(projected)
#     area = hull.volume

#     # Estimate diameters via bounding box
#     x_span = projected[:, 0].ptp()
#     y_span = projected[:, 1].ptp()
#     major = max(x_span, y_span)
#     minor = min(x_span, y_span)

#     return {"area": area, "major_diameter": major, "minor_diameter": minor}

# # --- Callback after clicking on mesh ---
# def on_pick(point, picker=None):
#     # Extract actual coordinates from PolyData
#     if hasattr(point, 'points'):
#         point = point.points[0]
#     else:
#         print("Could not extract point coordinates.")
#         return

#     print("Picked point (coords):", point.tolist())
#     chosen_plane["origin"] = point

#     plotter.add_plane_widget(
#         callback=on_plane_update,
#         normal=chosen_plane["normal"],
#         origin=point,
#         color="cyan",
#         implicit=True,
#         outline_translation=True,
#         assign_to_axis=None,
#         tubing=False,
#         factor=1.0
#     )

# # --- Callback whenever the slicing plane is updated ---
# def on_plane_update(normal, origin):
#     print("Plane updated | origin:", origin, "| normal:", normal)
#     chosen_plane["origin"] = origin
#     chosen_plane["normal"] = normal

#     points, ids = intersect_mesh_with_plane(mesh, origin, normal)

#     if "slice_points" in plotter.actors:
#         plotter.remove_actor("slice_points")

#     plotter.add_points(points, color='red', point_size=8, render_points_as_spheres=True, name="slice_points")

#     # Optional: show normal vector as red arrow
#     arrow = pv.Arrow(start=origin, direction=normal, scale=5.0)
#     if "normal_arrow" in plotter.actors:
#         plotter.remove_actor("normal_arrow")
#     plotter.add_mesh(arrow, color="red", name="normal_arrow")

# # --- Finalize selection and save output ---
# def finalize_selection():
#     origin = chosen_plane["origin"]
#     normal = chosen_plane["normal"]

#     if origin is None or normal is None:
#         print("Please click on the mesh and adjust the slicing plane before finalizing.")
#         return

#     points, ids = intersect_mesh_with_plane(mesh, origin, normal)
#     features = compute_geometry_features(np.array(points))

#     print("\nFINAL SELECTION")
#     print(f"→ Origin: {origin}")
#     print(f"→ Normal: {normal}")
#     print(f"→ {len(points)} points | Area ≈ {features['area']:.2f} | Major ≈ {features['major_diameter']:.2f}")

#     with open(OUTPUT_JSON, 'w') as f:
#         json.dump({
#             "origin": list(map(float, origin)),
#             "normal": list(map(float, normal)),
#             "point_ids": list(map(int, ids)),
#             "intersection_count": int(len(points)),
#             "template_point_count": int(mesh.n_points),
#             "point_hash": float(np.sum(mesh.points)),
#             "first_5_points": mesh.points[:5].tolist(),
#             "area": float(features['area']),
#             "major_diameter": float(features['major_diameter']),
#             "minor_diameter": float(features['minor_diameter'])
#         }, f, indent=2)

#     print(f"→ Saved to: {OUTPUT_JSON}")

#     try:
#         plotter.remove_text("success_message")
#     except:
#         pass

#     plotter.add_text(
#         "PA features saved successfully!",
#         position="lower_left",
#         font_size=14,
#         color="lightgreen",
#         name="success_message"
#     )

# # --- Set up visualization ---
# plotter.add_text(
#     "Left-click on the mesh to place slicing plane\n"
#     "Drag to rotate/translate the plane\n"
#     "Press SPACE to finalize and compute PA features",
#     font_size=12,
#     position="lower_right",
#     color="black" #     #00ccff = bright cyan-blue
# )

# # Enable picking and key event
# plotter.enable_point_picking(callback=on_pick, use_mesh=True, show_message=True)
# plotter.add_key_event("space", finalize_selection)

# # Show the interactive viewer
# plotter.show()
# # Ensure proper shutdown
# def safe_close_plotter():
#     try:
#         plotter.close()
#     except:
#         pass

# atexit.register(safe_close_plotter)








# import pyvista as pv
# import numpy as np
# import json
# from scipy.spatial import ConvexHull
# import os
# import sys
# import atexit
# import warnings

# # === Shutdown message ===
# def on_exit():
#     print("\n Visualization closed successfully. Goodbye!")
# atexit.register(on_exit)

# # === Suppress warnings ===
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # === Setup paths ===
# base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, base_path)
# print("Working directory:", os.getcwd())
# print("Base path added to sys.path:", base_path)

# # === Imports ===
# from utils.mesh_utils import load_mesh

# # === Plane intersection (float64 guaranteed) ===
# def intersect_mesh_with_plane(mesh, origin, normal, tolerance=0.1):  #1e-5
#     origin = np.asarray(origin, dtype=np.float64)
#     normal = np.asarray(normal, dtype=np.float64)
#     diff = mesh.points.astype(np.float64) - origin
#     distances = np.dot(diff, normal)
#     mask = np.abs(distances) < tolerance
#     ids = np.where(mask)[0]
#     points = mesh.points[ids].astype(np.float64)
#     return points, ids

# # === Geometry features ===
# def compute_geometry_features(points):
#     if len(points) < 3:
#         return {"area": 0.0, "major_diameter": 0.0, "minor_diameter": 0.0}
#     center = points.mean(axis=0)
#     _, _, Vt = np.linalg.svd(points - center)
#     projected = (points - center) @ Vt[:2].T
#     hull = ConvexHull(projected)
#     area = hull.volume
#     x_span = projected[:, 0].ptp()
#     y_span = projected[:, 1].ptp()
#     return {"area": area, "major_diameter": max(x_span, y_span), "minor_diameter": min(x_span, y_span)}

# # === Load mesh ===
# TEMPLATE_PATH = os.path.join(base_path, "data", "template", "vtks", "RV_ED.vtk")
# OUTPUT_JSON = os.path.join(base_path, "output", "pa_plane_features.json")
# mesh = load_mesh(TEMPLATE_PATH)
# print("Mesh center:", mesh.center)

# # === Plotter setup ===
# plotter = pv.Plotter()
# plotter.add_mesh(mesh, color="lightgray", opacity=0.3, smooth_shading=True)
# chosen_plane = {"origin": None, "normal": [0, 0, 1]}

# # === Picking ===
# def on_pick(point, picker=None):
#     if hasattr(point, 'points'):
#         point = point.points[0]
#     print("Picked point:", point.tolist())
#     chosen_plane["origin"] = point
#     plotter.add_plane_widget(
#         callback=on_plane_update,
#         normal=chosen_plane["normal"],
#         origin=point,
#         color="cyan",
#         implicit=True,
#         outline_translation=True,
#         assign_to_axis=None,
#         tubing=False,
#         factor=1.0
#     )

# # === Plane update ===
# def on_plane_update(normal, origin):
#     chosen_plane["origin"] = origin
#     chosen_plane["normal"] = normal
#     points, ids = intersect_mesh_with_plane(mesh, origin, normal)
#     if "slice_points" in plotter.actors:
#         plotter.remove_actor("slice_points")
#     plotter.add_points(points, color='red', point_size=8, render_points_as_spheres=True, name="slice_points")
#     arrow = pv.Arrow(start=origin, direction=normal, scale=5.0)
#     if "normal_arrow" in plotter.actors:
#         plotter.remove_actor("normal_arrow")
#     plotter.add_mesh(arrow, color="red", name="normal_arrow")

# # === Finalize and Save ===
# def finalize_selection():
#     origin = chosen_plane["origin"]
#     normal = chosen_plane["normal"]
#     if origin is None or normal is None:
#         print("Please define the slicing plane first.")
#         return
#     points, ids = intersect_mesh_with_plane(mesh, origin, normal)
#     features = compute_geometry_features(np.array(points, dtype=np.float64))
#     output = {
#         "origin": list(map(float, origin)),
#         "normal": list(map(float, normal)),
#         "point_ids": list(map(int, ids)),
#         "intersection_count": int(len(points)),
#         "template_point_count": int(mesh.n_points),
#         "point_hash": float(np.sum(mesh.points.astype(np.float64))),
#         "first_5_points": mesh.points[:5].astype(np.float64).tolist(),
#         "area": float(features['area']),
#         "major_diameter": float(features['major_diameter']),
#         "minor_diameter": float(features['minor_diameter'])
#     }
#     with open(OUTPUT_JSON, 'w') as f:
#         json.dump(output, f, indent=2)
#     print("\nFINAL SELECTION")
#     print(f"→ Origin: {origin}")
#     print(f"→ Normal: {normal}")
#     print(f"→ {len(points)} points | Area ≈ {features['area']:.2f} | Major ≈ {features['major_diameter']:.2f}")
#     print(f"→ Saved to: {OUTPUT_JSON}")
#     try: plotter.remove_text("success_message")
#     except: pass
#     plotter.add_text("PA features saved successfully!", position="lower_left", font_size=14, color="lightgreen", name="success_message")

# # === UI text ===
# plotter.add_text(
#     " Left-click to place slicing plane\n Drag to adjust plane\n Press SPACE to finalize",
#     position="upper_left", font_size=12, color="#00ccff")

# # === Bind events ===
# plotter.enable_point_picking(callback=on_pick, use_mesh=True, show_message=True)
# plotter.add_key_event("space", finalize_selection)

# # === Show ===
# plotter.show()

# # === Graceful close ===
# def safe_close_plotter():
#     try:
#         plotter.close()
#     except:
#         pass
# atexit.register(safe_close_plotter)







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
plotter.add_mesh(mesh, color="lightgray", opacity=0.3, smooth_shading=True, lighting=True)
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
    arrow = pv.Arrow(start=origin, direction=normal, scale=5.0)
    if "normal_arrow" in plotter.actors:
        plotter.remove_actor("normal_arrow")
    plotter.add_mesh(arrow, color="red", name="normal_arrow")

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








