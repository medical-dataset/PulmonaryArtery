# ----------------------
# utils/mesh_utils.py
# ----------------------
import pyvista as pv

def load_mesh(path):
    """
    Loads a 3D mesh from a .vtk or .vtp file.
    
    Parameters:
    - path: Path to the mesh file

    Returns:
    - mesh: pyvista.PolyData object
    """
    return pv.read(path)
