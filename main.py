from circulargrid import CircularGrid
from visualise import Visualise
import matplotlib.pyplot as plt
import random
import copy

grid = CircularGrid(10, 6)


def step(grid):
    for ring in grid.rings:
        offset = ring.offset
        offset += 1  # temporary
        ring.offset = offset

        for cell in ring.children:
            cell.theta1 += offset
            cell.theta2 += offset

    return grid


def propagation(grid):
    temp_grid = copy.deepcopy(grid)

    for ring, temp_ring in zip(grid.rings, temp_grid.rings):
        for cell, temp_cell in zip(ring.children, temp_ring.children):
            cell_age = cell.age

            if cell_age > 0:
                temp_cell.age -= 1
                continue

            neighbours = grid.get_neighbours(cell)
            check = False

            for neighbour in neighbours:
                if neighbour.age > 0:

                    # x is the formation probability, has to be determined yet
                    x = random.random()
                    if x < 0.5:
                        temp_cell.age = 7
                        check = True

                    break
    return temp_grid


# Initialize random stars first
for i in range(10):
    ring = random.choice(grid.rings)
    cell = random.choice(ring.children)

    while cell.age > 0:
        ring = random.choice(grid.rings)
        cell = random.choice(ring.children)

    cell.age = 7


# Plot before 20 steps
plotter = Visualise(grid)
for ring in grid.rings:
    for cell in ring.children:
        if cell.age > 0:
            plotter.fill_cell(cell, "b")

# Propagate and rotate
for i in range(20):
    new_grid = propagation(grid)
    new_grid = step(new_grid)

# Plot after 20 steps
plotter = Visualise(new_grid)
for ring in new_grid.rings:
    for cell in ring.children:
        if cell.age > 0:
            plotter.fill_cell(cell, "b")

plt.show()
