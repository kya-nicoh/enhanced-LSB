# to run right click on code and click "open in interactive window"

import numpy as np
import matplotlib.pyplot as plt

def lorenz(xyz, sigma=10, rho=28, beta=2.667):
    x,y,z = xyz
    return np.array([
        sigma * (y - x),
        rho * x - y - x * z,
        x * y - beta * z,
    ])

steps = 10000
xyz = np.zeros((steps, 3))
xyz[0] = [0, 1, 1.05]
dt = 0.01

for i in range(1, steps):
    xyz[i] = (
        xyz[i - 1] + lorenz(xyz[i - 1]) * dt
    )

plt.figure(figsize=(8,8)).add_subplot(projection="3d").plot(*xyz.T)