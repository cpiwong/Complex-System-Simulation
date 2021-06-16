from circulargrid import CircularGrid
from scheduler import Scheduler
from visualise import Visualise
import matplotlib.pyplot as plt
import random
import copy
from tqdm import tqdm
import pandas as pd


REGEN_TIME = 50

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

    for ring in grid.rings:
        for cell in ring.children:
            current_age = cell.current_age

            if current_age > 0:
                cell.next_age = current_age - 1
                continue

            neighbours = grid.get_neighbours(cell)
            check = False

            for neighbour in neighbours:
                if neighbour.current_age == REGEN_TIME:

                    # x is the formation probability, has to be determined yet
                    x = random.random()
                    if x < 1:
                        cell.next_age = REGEN_TIME
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


grid = CircularGrid(50, 20, beforestep=propagation, step=step)

# Initialize random stars first
for i in range(200):
    ring = random.choice(grid.rings)
    cell = random.choice(ring.children)

    while cell.current_age > 0:
        ring = random.choice(grid.rings)
        cell = random.choice(ring.children)

    cell.current_age = REGEN_TIME

dataclass = Scheduler(grid)
dataclass.start(1, 30)

df = pd.DataFrame(dataclass.history.tolist())
plotter = Visualise(grid)
plotter.animate(df)
#df.to_csv("test.csv")
