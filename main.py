from scheduler import Scheduler
from visualise import Visualise
from model import Model
from analyse import *
import matplotlib.pyplot as plt
import random
import pandas as pd

REGEN_TIME = 20
PROPAGATION_PROBABILITY = 0.8
MAX_RANDOM_STARS = 10
NUM_OF_RINGS = 50
CELLS_PER_RING = 20
TIMESTEP = 1
SIMDURATION = 100

model = Model(REGEN_TIME, PROPAGATION_PROBABILITY, MAX_RANDOM_STARS)
model.bind_grid(NUM_OF_RINGS, CELLS_PER_RING)
model.bind_scheduler()

# Initialize random stars first
for i in range(200):
    ring = random.choice(model.grid.rings)
    cell = random.choice(ring.children)

    while cell.current_age > 0:
        ring = random.choice(model.grid.rings)
        cell = random.choice(ring.children)

    cell.current_age = REGEN_TIME

model.scheduler.start(TIMESTEP, SIMDURATION)
df = pd.DataFrame(model.scheduler.history.tolist())

starsformed = starFormationRate(df, REGEN_TIME)
plt.plot(range(len(starsformed)), starsformed)
plt.title("Star formation per timestep")
plt.xlabel("Frame")
plt.ylabel("Stars formed")
plt.show()
#plotter = Visualise(grid)
#plotter.animate(df)
# df.to_csv("test.csv")
