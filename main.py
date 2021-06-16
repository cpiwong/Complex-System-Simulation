from circulargrid import CircularGrid
from visualise import Visualise
import matplotlib.pyplot as plt
import random
import copy
from tqdm import tqdm

grid = CircularGrid(50, 20)


def step(grid):
    for ring in grid.rings:
        offset = ring.offset
        offset += 1  # temporary
        ring.offset = offset

        for cell in ring.children:
            cell.theta1 += offset
            cell.theta2 += offset

    return grid


# def propagation(grid):
#     temp_grid = copy.deepcopy(grid)

#     for ring, temp_ring in zip(grid.rings, temp_grid.rings):
#         for cell, temp_cell in zip(ring.children, temp_ring.children):
#             cell_age = cell.current_age

#             if cell_age > 0:
#                 temp_cell.current_age -= 1
#                 continue

#             neighbours = grid.get_neighbours(cell)
#             check = False

#             for neighbour in neighbours:
#                 if neighbour.current_age > 0:

#                     # x is the formation probability, has to be determined yet
#                     x = random.random()
#                     if x < 0.1:
#                         temp_cell.current_age = 7
#                         check = True

#                     break
#     return temp_grid


def propagation(grid):

    for ring in grid.rings:
        for cell in ring.children:
            current_age = cell.current_age

            if current_age > 0:
                cell.next_age = current_age - 1
                continue

            neighbours = grid.get_neighbours(cell)
            check = False

            for neighbour in neighbours:
                if neighbour.current_age > 0:

                    # x is the formation probability, has to be determined yet
                    x = random.random()
                    if x < 0.1:
                        cell.next_age = 7
                        check = True

                    break

    updated_grid = updateGrid(grid)

    return updated_grid


def updateGrid(grid):
    for ring in grid.rings:
        for cell in ring.children:
            cell.current_age = cell.next_age
            cell.next_age = 0

    return grid


# Initialize random stars first
for i in range(10):
    ring = random.choice(grid.rings)
    cell = random.choice(ring.children)

    while cell.current_age > 0:
        ring = random.choice(grid.rings)
        cell = random.choice(ring.children)

    cell.current_age = 7


# Plot before 20 steps
plotter = Visualise(grid)
for ring in grid.rings:
    for cell in ring.children:
        if cell.current_age > 0:
            plotter.fill_cell(cell, "b")

# Propagate and rotate
new_grid = grid
for i in tqdm(range(100)):
    temp_grid = propagation(new_grid)
    new_grid = step(temp_grid)

# Plot after 20 steps
plotter = Visualise(new_grid)
for ring in new_grid.rings:
    for cell in ring.children:
        if cell.current_age > 0:
            plotter.fill_cell(cell, "b")

plt.show()
