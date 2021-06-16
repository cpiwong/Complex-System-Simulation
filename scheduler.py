import numpy as np
from tqdm import tqdm


class Scheduler:
    def __init__(self, grid, timestep=0, iteration_callback=None):
        """" Manages the timesteps on the circular grid
        Args:
            grid: the Circular grid object
            timestep: time to wait between each step, only usefull is visualing data. Should be zero otherwise
            iteration_callback: Function that gets called after a completed iteration.
        """

        self.grid = grid
        self.timestep = timestep
        self.iteration_callback = iteration_callback
        self.started = False

        self.history = []
        self.timestamp = 0

    def start(self, dt, t_end):
        """ Starts the simulation """

        for t in tqdm(np.arange(0, t_end, dt)):
            self.timestamp = t
            self.grid.announce_beforestep()
            self.grid.announce_step()

            # self.iteration_callback()
            self.history.append(self.get_snapshot())

        return

    def get_snapshot(self):
        """" Returns a array of dictionaries with all the cell states"""
        data = []
        for ring in self.grid.rings:
            for cell in ring.children:
                celldata = {
                    "t": self.timestamp,
                    "id": cell.id,
                    "age": cell.current_age,
                    "parent_ring": cell.parent.id,
                    "theta1": cell.theta1,
                    "theta2": cell.theta2,
                }
                data.append(celldata)
        return np.array(data)

    def pause(self):
        """"Pauses the current simulation after finishing current iteration"""
        self.started = False

