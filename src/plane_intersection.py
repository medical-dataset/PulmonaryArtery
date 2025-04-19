
import numpy as np
import pyvista as pv

def intersect_mesh_with_plane(mesh, origin, normal):
    """
    Intersects a 3D mesh with a plane and returns the intersection points.

    Parameters:
    - mesh: pyvista.PolyData object
    - origin: list or array-like, [x, y, z] point on the plane
    - normal: list or array-like, [nx, ny, nz] normal vector of the plane

    Returns:
    - intersected_points: numpy array of intersected coordinates
    - intersected_ids: list of point indices in the original mesh
    """
    plane = pv.Plane(center=origin, direction=normal, i_size=100, j_size=100)
    sliced = mesh.slice(normal=normal, origin=origin)
    intersected_ids = mesh.find_closest_point(sliced.points)
    return sliced.points, intersected_ids



def intersect_mesh_with_plane2(mesh, origin, normal):
    """
    Intersects a 3D mesh with a defined plane.

    Parameters:
    - mesh: pyvista.PolyData object
    - origin: [x, y, z] coordinates of a point on the plane
    - normal: [nx, ny, nz] normal vector of the plane

    Returns:
    - points: Coordinates of the intersection points
    - ids: Indexes of points in the mesh near the intersection
    """
    sliced = mesh.slice(normal=normal, origin=origin)
    ids = [mesh.find_closest_point(p) for p in sliced.points]
    return sliced.points, ids
