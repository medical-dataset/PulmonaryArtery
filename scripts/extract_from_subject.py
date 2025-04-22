import os
import json
import pyvista as pv
import numpy as np
from scipy.spatial import ConvexHull

def compute_features(points):
    if len(points) < 3:
        return dict(area=0.0, major_diameter=0.0, minor_diameter=0.0)

    center = points.mean(axis=0)
    _, _, Vt = np.linalg.svd(points - center)
    projected = (points - center) @ Vt[:2].T

    hull = ConvexHull(projected)
    area = hull.volume
    x_span = projected[:, 0].ptp()
    y_span = projected[:, 1].ptp()

    return dict(
        area=area,
        major_diameter=max(x_span, y_span),
        minor_diameter=min(x_span, y_span)
    )

def extract_features_from_subject(subject_mesh_path, ref_json_path, output_dir):
    subject_mesh = pv.read(subject_mesh_path)

    with open(ref_json_path, 'r') as f:
        ref_data = json.load(f)

    ref_point_ids = ref_data['point_ids']
    expected_n_points = ref_data['template_point_count']
    expected_hash = float(ref_data['point_hash'])  # Ensure float64 comparison
    first_points_ref = np.array(ref_data['first_5_points'], dtype=np.float64)

    if subject_mesh.n_points != expected_n_points:
        print("❌ Mesh point count mismatch.")
        return

    actual_hash = float(np.sum(subject_mesh.points.astype(np.float64)))  # Ensure float64 precision
    if abs(actual_hash - expected_hash) > 1e-2:
        print("❌ Mesh point hash mismatch.")
        return

    actual_first_5 = subject_mesh.points[:5].astype(np.float64)
    if not np.allclose(actual_first_5, first_points_ref, atol=1e-3):
        print("❌ First 5 points do not match. Meshes are not aligned.")
        return

    points = subject_mesh.points[ref_point_ids].astype(np.float64)
    features = compute_features(points)

    subject_id = os.path.normpath(subject_mesh_path).split(os.sep)[-2]
    output_path = os.path.join(output_dir, f"features_{subject_id}.json")

    output = {
        "subject_id": subject_id,
        "point_ids_used": [int(i) for i in ref_point_ids],
        "area": float(features['area']),
        "major_diameter": float(features['major_diameter']),
        "minor_diameter": float(features['minor_diameter'])
    }
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Features for subject {subject_id} saved to {output_path}")

    # Visual confirmation
    plotter = pv.Plotter()
    plotter.add_mesh(subject_mesh, color='lightgray', opacity=0.3, smooth_shading=True)
    plotter.add_points(points, color='red', point_size=10, render_points_as_spheres=True)

    origin = np.array(ref_data["origin"], dtype=np.float64)
    normal = np.array(ref_data["normal"], dtype=np.float64)
    plane_arrow = pv.Arrow(start=origin, direction=normal, scale=5.0)
    plotter.add_mesh(plane_arrow, color='blue')

    plotter.add_text(
        f"Subject: {subject_id}\nArea: {features['area']:.2f}\nMajor: {features['major_diameter']:.2f}",
        position="lower_left", font_size=12, color='cyan'
    )

    plotter.show()

if __name__ == "__main__":
    extract_features_from_subject(
        subject_mesh_path=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\data\template\vtks\RV_ED.vtk",
        ref_json_path=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\output\pa_plane_features.json",
        output_dir=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\output"
    )













# import os
# import json
# import pyvista as pv
# import numpy as np
# from scipy.spatial import ConvexHull

# def compute_features(points):
#     if len(points) < 3:
#         return dict(area=0.0, major_diameter=0.0, minor_diameter=0.0)

#     center = points.mean(axis=0)
#     _, _, Vt = np.linalg.svd(points - center)
#     projected = (points - center) @ Vt[:2].T

#     hull = ConvexHull(projected)
#     area = hull.volume
#     x_span = projected[:, 0].ptp()
#     y_span = projected[:, 1].ptp()

#     return dict(
#         area=area,
#         major_diameter=max(x_span, y_span),
#         minor_diameter=min(x_span, y_span)
#     )

# def extract_features_from_subject(subject_mesh_path, ref_json_path, output_dir):
#     # Load subject mesh
#     subject_mesh = pv.read(subject_mesh_path)

#     # Load reference JSON with point_ids and template metadata
#     with open(ref_json_path, 'r') as f:
#         ref_data = json.load(f)

#     ref_point_ids = ref_data['point_ids']
#     expected_n_points = ref_data['template_point_count']
#     expected_hash = ref_data['point_hash']
#     first_points_ref = np.array(ref_data['first_5_points'])
    
#     # Validate mesh compatibility
#     if subject_mesh.n_points != expected_n_points:
#         print("❌ Mesh point count mismatch.")
#         return

#     actual_hash = float(np.sum(subject_mesh.points))
#     if abs(actual_hash - expected_hash) > 1e-2:
#         print("❌ Mesh point hash mismatch.")
#         return

#     actual_first_5 = subject_mesh.points[:5]
#     if not np.allclose(actual_first_5, first_points_ref, atol=1e-3):
#         print("❌ First 5 points do not match. Meshes are not aligned.")
#         return
    
#     # Extract and compute features
#     points = subject_mesh.points[ref_point_ids]
#     features = compute_features(points)

#     # Derive subject ID from path (e.g., "...\\1000213\\vtks")
#     subject_id = os.path.normpath(subject_mesh_path).split(os.sep)[-2]
#     output_path = os.path.join(output_dir, f"features_{subject_id}.json")

#     # Save output
#     output = {
#     "subject_id": subject_id,
#     "point_ids_used": [int(i) for i in ref_point_ids],
#     "area": float(features['area']),
#     "major_diameter": float(features['major_diameter']),
#     "minor_diameter": float(features['minor_diameter'])
#     }
#     with open(output_path, 'w') as f:
#         json.dump(output, f, indent=2)

#     print(f"✅ Features for subject {subject_id} saved to {output_path}")

#     # Visual confirmation
#     plotter = pv.Plotter()
#     plotter.add_mesh(subject_mesh, color='lightgray', opacity=0.3, smooth_shading=True)
#     plotter.add_points(points, color='red', point_size=10, render_points_as_spheres=True)

#     origin = ref_data["origin"]
#     normal = ref_data["normal"]
#     plane_arrow = pv.Arrow(start=origin, direction=normal, scale=5.0)
#     plotter.add_mesh(plane_arrow, color='blue')

#     plotter.add_text(
#         f"Subject: {subject_id}\nArea: {features['area']:.2f}\nMajor: {features['major_diameter']:.2f}",
#         position="lower_left", font_size=12, color='cyan'
#     )

#     plotter.show()

# # Call for single test subject
# if __name__ == "__main__":
#     extract_features_from_subject(
#         subject_mesh_path=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\data\template\vtks\RV_ED.vtk",
#         ref_json_path=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\output\pa_plane_features.json",
#         output_dir=r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\output"
#     )
# #\\isd_netapp\cardiac$\UKBB_40616\4D_Segmented_2.0_2nd_batch_18k\1000213\vtks\RV_ED.vtk
# #\\isd_netapp\ukb$\jz_ukbb_18k\collection_1\1000213\motion\vtks\frames\template_space\RV
# #\\isd_netapp\ukb$\jz_ukbb_18k\collection_1\1000213\vtks\     #C_RV_ED  F  FC
# #\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\data\template\vtks