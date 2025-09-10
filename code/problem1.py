import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# Define the model
def model(y, t, params):
    Nprey, Npred, At = y
    Rt, rprey, K, rpred, alpha_prey, beta_prey, rA, KA, h, k = params

    # The equations
    # dRt_dt = gamma * (At - Athreshold) * (Rt / Rmax)
    dNprey_dt = rprey * Nprey * (1 - Nprey / K) - alpha_prey * Nprey * Npred
    dNpred_dt = -rpred * Npred + beta_prey * Nprey * Npred
    dAt_dt = rA * At * (1 - At / KA) - At * (1 / (1 + np.exp(k * (Rt - 1)))) * Npred



    return [dNprey_dt, dNpred_dt, dAt_dt]


# Initial conditions
Nprey0 = 50  # Initial prey population
Npred0 = 10  # Initial predator population
At0 = 20     # Initial human activity level


# Parameters (these are arbitrary example values)
rprey = 1.1  # Prey growth rate
K = 500      # Carrying capacity for prey
alpha_prey = 0.02  # Predation coefficient
rpred = 0.5       # Predator decay rate
beta_prey = 0.02  # Predator growth coefficient due to prey
rA = 0.1          # Resource availability growth rate
KA = 100          # Carrying capacity for resources
h = 0.1           # Human activity impact factor
Rt = 2          # Gender ratio coefficient, assumed constant
theta = 2
k = 10


params = [Rt, rprey, K, rpred, alpha_prey, beta_prey, rA, KA, h, k]

# Time vector
t = np.linspace(0, 40, 10000)  # From time 0 to 100 with 1000 points

# Solve ODE
solution = odeint(model, [Nprey0, Npred0, At0], t, args=(params,))

# Plot results
plt.figure(figsize=(12, 8))
plt.plot(t, solution[:, 0], label='Prey population (Nprey)')
plt.plot(t, solution[:, 1], label='Predator population (Npred)')
plt.plot(t, solution[:, 2], label='Resource availability (At)')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Population / Resource Availability')
plt.title('Ecosystem Dynamics')
plt.show()