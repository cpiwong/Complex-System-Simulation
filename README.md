# Self-propagating star formation of spiral galaxies

## Demo & introduction

## Requirements

This python code uses some common python packages. Make sure you install these or install with pip by running `pip install -r requirements.txt`
  
  * numy
  * matplotlib
  * tqdm
  * pandas

## Sample code

To run a simulation you need to follow 3 steps:
1. Create model
2. Bind a grid to the model
3. Bind a scheduler
```
from model import Model
model = Model(
        REGEN_TIME, propagation_probability, MAX_RANDOM_STARS, PROPAGATION_SPEED
    )
model.bind_grid(NUM_OF_RINGS, CELLS_PER_RING)
model.bind_scheduler()

model.scheduler.start(TIMESTEP, SIMDURATION)
df = pd.DataFrame(model.scheduler.history.tolist())
```

To create a visualistion as the gif on the top of this reamde you can run

```
from visualise import Visualise

plotter = Visualise(model.grid)
plotter.animate(df, probability)
