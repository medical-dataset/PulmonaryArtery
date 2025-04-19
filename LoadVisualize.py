import pyvista as pv

# Load the .vtk file
mesh = pv.read(r"\\isd_netapp\mvafaeez$\Projects\PA\PAmesh\data\template\vtks\RV_ED.vtk")  # Make sure this path points to your file

# Create a plotter
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="lightblue", show_edges=True)
plotter.add_axes()
plotter.show_bounds(grid='front', location='outer')
plotter.show()
print(mesh)

