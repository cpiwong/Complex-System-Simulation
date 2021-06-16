from circulargrid import CircularGrid
from scheduler import Scheduler
from visualise import Visualise
import matplotlib.pyplot as plt
import random
import copy
from tqdm import tqdm
import pandas as pd
import numpy as np

REGEN_TIME = 20
PROPAGATION_PROBABILITY = 0.8
MAX_RANDOM_STARS = 10


def step(grid):
    for ring in grid.rings:
        offset = ring.offset
        r = ring.id + 1
        offset += 1 / r  # temporary
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

            for neighbour in neighbours:
                if neighbour.current_age == REGEN_TIME:

                    # x is the formation probability, has to be determined yet
                    x = random.random()
                    if x < PROPAGATION_PROBABILITY:
                        cell.next_age = REGEN_TIME

                    break

    updated_grid = updateGrid(grid)

    return updated_grid


def updateGrid(grid):
    for ring in grid.rings:
        for cell in ring.children:
            cell.current_age = cell.next_age

    return grid


def randomStars(grid):
    rings = len(grid.rings)
    number = random.randint(0, MAX_RANDOM_STARS)

    for _ in range(number):

        r = random.randint(0, rings) - 1

        theta_max = len(grid.rings[r].children)
        theta = random.randint(0, theta_max) - 1
        grid.rings[r].children[theta].current_age = REGEN_TIME

    return grid


grid = CircularGrid(50, 20, beforestep=propagation, step=step, afterstep=randomStars)

# Initialize random stars first
for i in range(200):
    ring = random.choice(grid.rings)
    cell = random.choice(ring.children)

    while cell.current_age > 0:
        ring = random.choice(grid.rings)
        cell = random.choice(ring.children)

    cell.current_age = REGEN_TIME

dataclass = Scheduler(grid)
dataclass.start(1, 100)

df = pd.DataFrame(dataclass.history.tolist())
plotter = Visualise(grid)
plotter.animate(df)
# df.to_csv("test.csv")
