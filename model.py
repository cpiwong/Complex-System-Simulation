from circulargrid import CircularGrid
from scheduler import Scheduler
import numpy as np
import random


class Model:
    def __init__(
        self, REGEN_TIME, PROPAGATION_PROBABILITY, MAX_RANDOM_STARS, PROPAGATION_SPEED
    ):
        self.REGEN_TIME = REGEN_TIME
        self.PROPAGATION_PROBABILITY = PROPAGATION_PROBABILITY
        self.PROPAGATION_SPEED = PROPAGATION_SPEED
        self.MAX_RANDOM_STARS = MAX_RANDOM_STARS
        self.grid = None
        self.scheduler = None

    def bind_grid(self, num_of_rings, cells_per_ring):
        self.grid = CircularGrid(
            num_of_rings, cells_per_ring, self.propagation, self.step, self.randomStars
        )

    def bind_scheduler(self):
        if not self.grid:
            print("Needs to bind a grid before binding a scheduler!")
            return
        self.scheduler = Scheduler(self.grid)

    def step(self, grid):
        for ring in grid.rings:
            offset = np.longdouble(ring.offset)
            r = ring.id + 1
            offset += 1 / np.longdouble(r)  # temporary
            ring.offset = offset

        return grid

    def propagation(self, grid):

        for ring in grid.rings:
            for cell in ring.children:
                current_age = cell.current_age

                if current_age > 0:
                    cell.next_age = current_age - 1

                    continue

                neighbours = grid.get_neighbours(cell)

                for neighbour in neighbours:
                    if neighbour.current_age == (
                        self.REGEN_TIME + 1 - self.PROPAGATION_SPEED
                    ):

                        # x is the formation probability, has to be determined yet
                        x = random.random()
                        if x < self.PROPAGATION_PROBABILITY:
                            cell.next_age = self.REGEN_TIME

                        break

        updated_grid = self.updateGrid(grid)

        return updated_grid

    def updateGrid(self, grid):
        for ring in grid.rings:
            for cell in ring.children:
                cell.current_age = cell.next_age

        return grid

    def randomStars(self, grid):
        rings = len(grid.rings)
        number = random.randint(0, self.MAX_RANDOM_STARS)

        for _ in range(number):

            r = random.randint(0, rings) - 1

            theta_max = len(grid.rings[r].children)
            theta = random.randint(0, theta_max) - 1
            grid.rings[r].children[theta].current_age = self.REGEN_TIME

        return grid
