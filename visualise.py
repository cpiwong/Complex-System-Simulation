import matplotlib.pyplot as plt
import numpy as np

class Visualise:

    def __init__(self, grid, PRINT_GRID=True, BG_COLOR='lightgray', FIG_SIZE=(15,15), RING_RES=0.01):
        self.grid = grid

        # plot settings
        self.PRINT_GRID = PRINT_GRID    # boolean to print each cell borders
        self.BG_COLOR = BG_COLOR        # background color of cell borders
        self.FIG_SIZE = FIG_SIZE        # size of visualisation
        self.RING_RES = RING_RES        # stepsize in radians of plot

        # basic pyplot settins
        self.fig = plt.figure(figsize=self.FIG_SIZE)
        self.ax = self.fig.add_subplot(111, polar=True)
        self.ax.grid(False)              # don't plot default grid lines
        plt.axis('off') 

        # usefull variables that are used multiple times
        self.rads = np.arange(0, (2 * np.pi), self.RING_RES)
        self.constant = np.ones(len(self.rads))

    def print_grid(self):
        # print out custom grid lines if enables
        for i in range(self.grid.NUM_OF_RINGS + 2): 
            plt.polar(self.rads, i * self.constant, self.BG_COLOR)

            # plot cell deviders, except for the last ring
            if i == self.grid.NUM_OF_RINGS + 1:
                continue

            for j in range(i * self.grid.CELLS_PER_RING):
                theta = j * 2 * np.pi / (i * self.grid.CELLS_PER_RING) 
                plt.polar([theta, theta],[i, i + 1], self.BG_COLOR);

    def fill_cell(self, cell, color):
        #plt.fill_between([cell.theta1, cell.theta2], [cell.level, cell.level + 1], color)
        plt.fill_between(np.arange(cell.theta1, cell.theta2, self.RING_RES),
                        cell.level, cell.level + 1, color=color)

    def show():
        plt.show()
