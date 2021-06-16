import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

REGEN_TIME = 50


class Visualise:
    def __init__(self, grid):
        self.grid = grid

        # plot settings
        self.PRINT_GRID = True  # boolean to print each cell borders
        self.BG_COLOR = "lightgray"  # background color of cell borders
        self.FIG_SIZE = (15, 15)  # size of visualisation
        self.RING_RES = 0.01  # stepsize in radians of plot

        # basic pyplot settins
        self.fig = plt.figure(figsize=self.FIG_SIZE)
        self.ax = self.fig.add_subplot(projection="polar")
        self.ax.grid(False)  # don't plot default grid lines
        plt.axis("off")
        self.ax.set_ylim([0, grid.NUM_OF_RINGS])
        self.df = None

        # usefull variables that are used multiple times
        self.rads = np.arange(0, (2 * np.pi), self.RING_RES)
        self.constant = np.ones(len(self.rads))

    def update(self, timestep):
        self.ax.clear()
        self.ax.set_ylim([0, self.grid.NUM_OF_RINGS])
        for index, row in self.df[
            (self.df.t == timestep) & (self.df.age == 50)
        ].iterrows():
            age = row["age"]
            color = (
                255 / REGEN_TIME * (REGEN_TIME - age),
                255 / REGEN_TIME * (REGEN_TIME - age),
                255 / REGEN_TIME * (REGEN_TIME - age),
            )
            # print(color)
            self.fill_cell(row["theta1"], row["theta2"], row["parent_ring"], color)

    def animate(self, df):
        self.df = df
        frames = df["t"].max()
        print("TEST!")
        ani = FuncAnimation(self.fig, self.update, frames)
        ani.save("animation.gif", writer="PillowWriter", fps=10)

    def print_grid(self):
        # print out custom grid lines if enables
        for i in range(self.grid.NUM_OF_RINGS + 2):
            self.ax.plot(self.rads, i * self.constant, self.BG_COLOR)

            # plot cell deviders, except for the last ring
            if i == self.grid.NUM_OF_RINGS + 1:
                continue

            for j in range(i * self.grid.CELLS_PER_RING):
                theta = j * 2 * np.pi / (i * self.grid.CELLS_PER_RING)
                self.ax.plot([theta, theta], [i, i + 1], self.BG_COLOR)

    def fill_cell(self, theta1, theta2, r, color):
        # plt.fill_between([cell.theta1, cell.theta2], [cell.level, cell.level + 1], color)
        self.ax.fill_between(
            x=np.arange(theta1, theta2, self.RING_RES), y1=r, y2=r + 1, color=color,
        )

    def show(self):
        plt.show()
