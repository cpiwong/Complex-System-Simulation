class Scheduler:
    def __init___(self, grid, timestep=0, iteration_callback=None):
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

    def start(self):
        """ Starts the simulation """

        # TODO implement function
        return

    def pause(self):
        """"Pauses the current simulation after finishing current iteration"""
        self.started = False

    def __iteration_callback(self):
        """ Internal callback function. Handles basic scheduler tasks before 
            calling external callback
        """
        # TODO implement function
