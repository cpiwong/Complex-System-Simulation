from model import Model
import random
import numpy as np
import pandas as pd
from analyse import *
import matplotlib.pyplot as plt

# All parameters
REGEN_TIME = 20
PROPAGATION_PROBABILITY = 0.1
MAX_RANDOM_STARS = 10
NUM_OF_RINGS = 50
CELLS_PER_RING = 20
TIMESTEP = 1
SIMDURATION = 100
INITIAL_STARS = 200


propagation_list = [x for x in np.arange(0.15, 0.4, 0.01)]
star_formation_rate = []

for propagation_probability in propagation_list:

    # Model initialization
    model = Model(REGEN_TIME, propagation_probability, MAX_RANDOM_STARS)
    model.bind_grid(NUM_OF_RINGS, CELLS_PER_RING)
    model.bind_scheduler()

    # Initialize random stars first
    for i in range(INITIAL_STARS):
        ring = random.choice(model.grid.rings)
        cell = random.choice(ring.children)

        while cell.current_age > 0:
            ring = random.choice(model.grid.rings)
            cell = random.choice(ring.children)

        cell.current_age = REGEN_TIME

    model.scheduler.start(TIMESTEP, SIMDURATION)
    df = pd.DataFrame(model.scheduler.history.tolist())

    # Star formation rate
    starsformed = starFormationRate(df, REGEN_TIME)
    converged = convergenceCheck(starsformed)
    mean_starformation_rate = converged.mean() - 10
    print(converged)
    if mean_starformation_rate < 0:
        mean_starformation_rate = 0
    star_formation_rate.append(mean_starformation_rate)

plt.plot(propagation_list, star_formation_rate)
plt.xlabel("Pst", fontsize=20)
plt.ylabel("Star formation rate", fontsize=20)
plt.yscale("log")
plt.show()
