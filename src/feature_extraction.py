# ----------------------
# src/feature_extraction.py
# ----------------------
import numpy as np
from scipy.spatial import ConvexHull

def compute_cross_section_area(points):
    """
    Computes the cross-sectional area of a set of points using ConvexHull.
    
    Parameters:
    - points: Numpy array of shape (N, 3)

    Returns:
    - area: Scalar value of the cross-sectional area
    """
    if points.shape[1] == 3:
        points_2d = points[:, :2]
    else:
        points_2d = points

    hull = ConvexHull(points_2d)
    return hull.volume
