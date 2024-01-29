import numpy as np
import matplotlib.pyplot as plt

def lorenz(xyz, sigma=10, rho=28, beta=2.667):
    x,y,z = xyz
    return np.array([
        sigma * (y - x),
        rho * x - y - x * z,
        x * y - beta * z,
    ])

# num of rows
steps = 10000
# make 1000 blank tuple with 3 columns
xyz = np.zeros((steps, 3))
# initial conditions
xyz[0] = [0, 1, 1.05]
# time step
dt = 0.01

for i in range(1, steps):
    xyz[i] = (
        xyz[i - 1] + lorenz(xyz[i - 1]) * dt
    )

for value in xyz:
    print(value.astype(int))