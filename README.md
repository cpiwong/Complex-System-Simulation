# Self-propagating star formation of spiral galaxies

## Demo & introduction

This project is a python implemtation of the self-propagating star formation model. It uses a circular grid where every disk rotates with a velocity of 1/r. This code is use to study under which propagation probabilities spiral formation takes place. 

<img src="spiral.gif">

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

To create a visualistion as the gif on the top of this readme you can run

```
from visualise import Visualise

plotter = Visualise(model.grid)
plotter.animate(df, probability)

1. varying_prob.py
