import numpy as np
from scipy.integrate import solve_ivp

# Define the Lorenz system
def lorenz(t, xyz, sigma=10, rho=28, beta=8/3):
    x, y, z = xyz
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

## Solve the Lorenz system
initial_conditions = [1.0, 1.0, 1.0]

t_span = (0, 100)
t_eval = np.linspace(*t_span, num=10000)
sol = solve_ivp(lorenz, t_span, initial_conditions, t_eval=t_eval)

# Use the solution as seeds for generating random numbers
random_seeds = sol.y[:, ::100].flatten()  # Extract every 100th value
np.random.seed(int(random_seeds[0]))

## Generate random integers within a specified range -3
lower_bound = 0
upper_bound = 509

## 1 letter = 6 numbers/ 3 pixels
sample_letters = "h"

num_random_numbers = len(sample_letters) * 6
random_numbers = np.random.randint(lower_bound, upper_bound, size=num_random_numbers)

paired_numbers = random_numbers.reshape(-1,2)
random_number_pairs = [tuple(row) for row in paired_numbers]
print(random_number_pairs)

def duplicates_test(random_number_pairs):
    counts = {}
    # Count occurrences of each tuple in the list
    for pair in random_number_pairs:
        if pair in counts:
            counts[pair] += 1
        else:
            counts[pair] = 1

    # Filter tuples with counts greater than 1 (i.e., duplicates)
    duplicates = {key: value for key, value in counts.items() if value > 1}
    print("Duplicates:", duplicates)