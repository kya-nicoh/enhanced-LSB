import numpy as np
from scipy.integrate import solve_ivp

# Define the Lorenz system
def lorenz(t, xyz, sigma=10, rho=28, beta=8/3):
    x, y, z = xyz
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Solve the Lorenz system
initial_conditions = [1.0, 1.0, 1.0]
t_span = (0, 100)
t_eval = np.linspace(*t_span, num=10000)
sol = solve_ivp(lorenz, t_span, initial_conditions, t_eval=t_eval)

# Use the solution as seeds for generating random numbers
random_seeds = sol.y[:, ::100].flatten()  # Extract every 100th value
np.random.seed(int(random_seeds[0]))

# Generate random integers within a specified range
lower_bound = 0
upper_bound = 100
num_random_numbers = 10
random_numbers = np.random.randint(lower_bound, upper_bound, size=num_random_numbers)
print("Random numbers within the range:", random_numbers)