# to run right click on code and click "open in interactive window"

import numpy as np
import matplotlib.pyplot as plt

def lorenz (xyz, s=10, r=28, b=2.667):
    x,y,z = xyz
    return np.array([
        s * (y - x),
        r * x - y - x * z,
        x * y - b * z,
    ])

steps = 10000
xyz = np.zeros((steps, 3))
xyz[0] = [0, 1, 1.05]
dt = 0.01

for i in range(1, steps):
    xyz[i] = (
        xyz[i - 1] + lorenz (xyz[i - 1]) * dt
    )

plt.figure(figsize=(8,8)).add_subplot(projection="3d").plot(*xyz.T)
