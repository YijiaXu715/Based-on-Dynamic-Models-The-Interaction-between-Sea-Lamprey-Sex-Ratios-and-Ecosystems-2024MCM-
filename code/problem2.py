import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters and initial conditions
r = 0.1  # Basic growth rate
alpha = 0.05  # Reproduction success rate coefficient
beta = 100  # Resource utilization efficiency coefficient
R = 150  # Resource
A = np.linspace(0.3, 2, 20)  # Sex ratio range
R0 = 100  # Initialize resource
gamma = 100 # The influence coefficient of sex ratio on resource utilization efficiency
S_values = [alpha *(R0-math.log(2/(math.exp((math.log(A)+3)/2)-2)))* A / (A+1) ** 2 for A in A]
E_values = [beta * (R0-math.log(2/(math.exp((math.log(A)+3)/2)-2)) - gamma * (A - 1) ** 2) * A for A in A]
mu = 0.56  # Mean of the distribution
sigma = 0.5  # Standard deviation of the distribution
Abundance_values = [(1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((A - mu) ** 2) / (2 * sigma ** 2)) for A in A]

# Plot the reproduction success rate and resource utilization efficiency as a function of sex ratio
plt.figure(figsize=(14, 6))

# Plot and save the reproduction success rate graph
plt.plot(A, S_values, '-o', color='blue')
plt.title('Reproduction Success Rate vs. Sex Ratio')
plt.xlabel('Sex Ratio (A)')
plt.ylabel('Reproduction Success Rate (S)')
plt.savefig('reproduction_success_rate.pdf')
plt.show()

# Plot and save the resource utilization efficiency graph
plt.plot(A, E_values, '-o', color='green')
plt.title('Resource Utilization Efficiency vs. Sex Ratio')
plt.xlabel('Sex Ratio (A)')
plt.ylabel('Resource Utilization Efficiency (E)')
plt.savefig('resource_utilization_efficiency.pdf')
plt.show()

# Plot and save the relative abundance graph
plt.plot(A, Abundance_values, '-o', color='red')
plt.title('Relative Abundance vs. Sex Ratio')
plt.xlabel('Sex Ratio (A)')
plt.ylabel('Relative Abundance (RA)')
plt.tight_layout()
plt.savefig('relative_abundance.pdf')
plt.show()