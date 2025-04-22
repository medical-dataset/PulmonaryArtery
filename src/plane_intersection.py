import numpy as np
import pyvista as pv

def intersect_mesh_with_plane(mesh, origin, normal):
    """
    Intersects a 3D mesh with a plane and returns the intersection points and their closest point IDs on the mesh.

    Parameters:
    - mesh: pyvista.PolyData object
    - origin: list or array-like, [x, y, z] point on the plane
    - normal: list or array-like, [nx, ny, nz] normal vector of the plane

    Returns:
    - intersected_points: numpy array of intersected coordinates
    - intersected_ids: Indexes of points in the mesh near the intersection
    """

    # Create a slicing plane and perform intersection
    plane = pv.Plane(center=origin, direction=normal, i_size=100, j_size=100)
    sliced = mesh.slice(normal=normal, origin=origin)

    # Debug: check how many points were found
    print(f"Sliced points shape: {sliced.points.shape}")
    if sliced.n_points == 0:
        print("⚠️ No intersection points found. Check the plane position and orientation.")

    intersected_ids = []
    for i, p in enumerate(sliced.points):
        # Check if point is valid and has 3 coordinates
        if not isinstance(p, (np.ndarray, list)) or len(p) != 3:
            print(f"⚠️ Skipping invalid point at index {i}: {p}")
            continue
        try:
            closest_id = mesh.find_closest_point(p)
            intersected_ids.append(closest_id)
        except Exception as e:
            print(f"❌ Error finding closest point for {p} at index {i}: {e}")

    return sliced.points, intersected_ids
