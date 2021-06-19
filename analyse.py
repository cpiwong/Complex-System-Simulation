import numpy as np

def starFormationRate(df, regenTime):
    """" Returrns the amount of new formed stars per timestep"""

    frames = df["t"].max()
    formationRate = np.zeros(frames)
    for i in range(frames):
        for index, row in df[
            (df.t == i) & (df.age == regenTime)
        ].iterrows():
            formationRate[int(row["t"])] += 1

    return formationRate

