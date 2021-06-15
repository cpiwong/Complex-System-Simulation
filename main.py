from circulargrid import CircularGrid
from visualise import Visualise
import matplotlib.pyplot as plt

grid = CircularGrid(10, 6)

ring = grid.rings[3]
cell = ring.children[4]

plotter = Visualise(grid)
plotter.print_grid()
plotter.fill_cell(cell, "b")
neighbours = grid.get_neighbours(cell)
for neighbour in neighbours:
    plotter.fill_cell(neighbour, "yellow")
plt.show()
