import random
import matplotlib.pyplot as plt

class Lamprey:
    def __init__(self, gender, age, reproduction_status, resource_need):
        self.gender = gender
        self.age = age
        self.reproduction_status = reproduction_status
        self.resource_need = resource_need

def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        gender = random.choice(['M', 'F'])
        age = random.randint(1, 5)  # Age is now set between 1 and 5
        reproduction_status = random.choice([True, False])
        resource_need = random.uniform(0.5, 1.5)
        population.append(Lamprey(gender, age, reproduction_status, resource_need))
    return population  # Randomly match the features to the lampreys

def find_neighbors(agent, population, max_neighbors=5):
    differences = [(abs(agent.resource_need - other.resource_need), other) for other in population if other is not agent]
    sorted_differences = sorted(differences, key=lambda x: x[0])
    neighbors = [agent[1] for agent in sorted_differences[:max_neighbors]]
    return neighbors

def calculate_resource_acquisition(agent, environment_availability, competition_factor, neighbors):
    total_neighbor_resource = sum(neighbor.resource_need for neighbor in neighbors)
    acquired_resource = agent.resource_need * environment_availability - competition_factor * total_neighbor_resource
    return acquired_resource

def calculate_reproduction_success(agent, base_reproduction_rate, reproduction_competition_factor, acquired_resource):
    # 确保reproduction_success_rate的值在0到1之间
    reproduction_success_rate = base_reproduction_rate * reproduction_competition_factor * acquired_resource
    reproduction_success_rate = max(0, min(1, reproduction_success_rate))  # 限制在0到1之间
    return random.random() < reproduction_success_rate


def adjust_gender_ratio(base_male_ratio, gender_adjust_factor, environment_availability, base_threshold):
    new_male_ratio = base_male_ratio + gender_adjust_factor * (environment_availability - base_threshold)
    return max(0, min(1, new_male_ratio))

def simulate_one_time_step(population, environment_availability, competition_factor,
                           base_reproduction_rate, reproduction_competition_factor,
                           base_male_ratio, gender_adjust_factor, base_threshold):
    new_population = []
    for agent in population:
        neighbors = find_neighbors(agent, population)
        acquired_resource = calculate_resource_acquisition(agent, environment_availability, competition_factor, neighbors)

        if agent.reproduction_status and calculate_reproduction_success(agent, base_reproduction_rate,
                                                                        reproduction_competition_factor, acquired_resource):
            gender = 'M' if random.random() < adjust_gender_ratio(base_male_ratio, gender_adjust_factor,
                                                                  environment_availability, base_threshold) else 'F'
            new_population.append(Lamprey(gender, 0, True, random.uniform(0.5, 1.5)))  # Allow new borns to reproduce in future generations

        # Update agent's age and possibly reproduction status
        agent.age += 1
        if agent.age >= 3:  # Assuming Lampreys become capable of reproduction at age 3
            agent.reproduction_status = True

    population.extend(new_population)

    # Optional: Remove agents that have surpassed their lifespan
    population[:] = [agent for agent in population if agent.age <= 5]  # Assuming a lifespan of 5 years

    return population

def plot_gender_ratio_over_time(gender_ratios):
    time_steps = range(len(gender_ratios))
    plt.plot(time_steps, gender_ratios, label='Male Ratio')
    plt.xlabel('Time Steps')
    plt.ylabel('Male Ratio')
    plt.title('Male Ratio Over Time')
    plt.legend()
    plt.show()

# Simulation parameters
initial_population_size = 200
environment_availability = 1.5
competition_factor = 0.1
base_reproduction_rate = 0.5
reproduction_competition_factor = 0.3
base_male_ratio = 0.5
gender_adjust_factor = 0.4
base_threshold = 0.8

# Initialize population
population = initialize_population(initial_population_size)

# Run simulation for multiple time steps
male_ratios_over_time = []
for _ in range(10):
    population = simulate_one_time_step(population, environment_availability, competition_factor,
                                        base_reproduction_rate, reproduction_competition_factor,
                                        base_male_ratio, gender_adjust_factor, base_threshold)
    if len(population) > 0:
        male_ratio = sum(1 for agent in population if agent.gender == 'M') / len(population)
        male_ratios_over_time.append(male_ratio)
    else:
        print("Population has become extinct.")
        break

# Visualize the results (Sex Ratio)
plot_gender_ratio_over_time(male_ratios_over_time)

# Reproduction success rates Box Plot
reproduction_success_data = {age: [] for age in range(1, 6)}  # Initialize a dictionary for ages 1 to 5

for agent in population:
    # Ensure the agent is capable of reproduction
    if agent.age >= 3:
        # Simulate the acquisition of resources and reproduction success
        neighbors = find_neighbors(agent, population, max_neighbors=5)  # Assuming you have a defined max_neighbors
        acquired_resource = calculate_resource_acquisition(agent, environment_availability, competition_factor, neighbors)
        reproduction_success_rate = base_reproduction_rate * reproduction_competition_factor * acquired_resource
        reproduction_success_rate = max(0, min(1, reproduction_success_rate))

        # Append the reproduction success rate to the appropriate age group in the dictionary
        if agent.age not in reproduction_success_data:
            reproduction_success_data[agent.age] = []
        reproduction_success_data[agent.age].append(reproduction_success_rate)

# Filter out age groups with no data
reproduction_success_data = {age: rates for age, rates in reproduction_success_data.items() if rates}

# Prepare the data for the boxplot
ages = sorted(reproduction_success_data.keys())
reproduction_rates = [reproduction_success_data[age] for age in ages]

# Plot the boxplot
plt.boxplot(reproduction_rates, labels=[str(age) for age in ages])
plt.xlabel('Age')
plt.ylabel('Reproduction Success Rate')
plt.title('Boxplot of Reproduction Success Rate by Age')
plt.savefig('Reproduction_Success_Rate_by_Age.pdf')
plt.show()

# barchart
resource_needs = [agent.resource_need for agent in population]
plt.hist(resource_needs, bins=20, alpha=0.5,edgecolor='black')
plt.xlabel('Resource Needs')
plt.ylabel('Frequency')
plt.title('Histogram of Resource Needs')
plt.savefig('Resource_Needs.pdf')
plt.show()

# boxplot
male_ages = [agent.age for agent in population if agent.gender == 'M']
female_ages = [agent.age for agent in population if agent.gender == 'F']
plt.boxplot([male_ages, female_ages], labels=['Male', 'Female'])
plt.ylabel('Age')
plt.title('Boxplot of Age by Gender')
plt.savefig('Age_by_Gender.pdf')
plt.show()