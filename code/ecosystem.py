import random
import matplotlib.pyplot as plt
import numpy as np

class Lamprey:
    def __init__(self, age, resource_need, reproduction_rate, reproduction_competition, gender_ratio_adjustment,
                 gender_threshold):
        self.age = age
        self.resource_need = resource_need
        self.reproduction_rate = reproduction_rate
        self.reproduction_competition = reproduction_competition
        self.gender_ratio_adjustment = gender_ratio_adjustment
        self.gender_threshold = gender_threshold
        self.gender = random.choice(['M', 'F'])
        self.reproduction_status = False
        self.acquired_resource = 0

    def calculate_resource_acquisition(self, environment_availability, competition_factor, neighbor_resources,
                                       male_ratio):
        adjustment_factor = 1.0
        if self.gender == 'M':
            adjustment_factor = 0.8
        else:
            adjustment_factor = 1.2
        competition_effect = competition_factor * sum(neighbor_resources)
        theoretical_resource = self.resource_need * environment_availability * adjustment_factor
        max_competition_effect = theoretical_resource * 0.5
        competition_effect = min(max_competition_effect, competition_effect)
        self.acquired_resource = max(0, theoretical_resource - competition_effect)
        return self.acquired_resource

    def calculate_reproduction_success(self):
        base_success_rate = 0.2
        self.reproduction_success_rate = self.reproduction_rate * self.reproduction_competition * self.acquired_resource + base_success_rate
        self.reproduction_status = random.random() < self.reproduction_success_rate
        return self.reproduction_status

    def calculate_infection_chance(self, male_ratio, neighbor_resources):
        # 基本感染率
        infection_rate = 0.3
        # 考虑性别比的影响
        if self.gender == 'M':
            infection_rate *= (1 + (male_ratio - self.gender_threshold) * self.gender_ratio_adjustment)
        else:
            infection_rate *= (1 - (male_ratio - self.gender_threshold) * self.gender_ratio_adjustment)
        # 考虑资源获取量的影响
        resource_factor = sum(neighbor_resources) / len(neighbor_resources) if neighbor_resources else 1
        infection_rate *= resource_factor
        return infection_rate

def initialize_population(population_size):
    return [Lamprey(random.randint(1, 10), random.uniform(0.5, 1.5), random.uniform(0.1, 0.5), random.uniform(0.1, 0.5),
                    random.uniform(0.01, 0.1), random.uniform(0.5, 1.5)) for _ in range(population_size)]


def adjust_gender_ratio(population):
    target_male_ratio = random.uniform(0.5, 0.8 )
    male_count = sum(1 for lamprey in population if lamprey.gender == 'M')
    total_population = len(population)
    males_needed = int(target_male_ratio * total_population) - male_count

    if males_needed > 0:
        females = [lamprey for lamprey in population if lamprey.gender == 'F']
        change_candidates = random.sample(females, min(abs(males_needed), len(females)))
        for lamprey in change_candidates:
            lamprey.gender = 'M'
    elif males_needed < 0:
        males = [lamprey for lamprey in population if lamprey.gender == 'M']
        change_candidates = random.sample(males, min(abs(males_needed), len(males)))
        for lamprey in change_candidates:
            lamprey.gender = 'F'

    new_male_ratio = sum(1 for lamprey in population if lamprey.gender == 'M') / total_population
    return new_male_ratio

def simulate_one_time_step(population, environment_availability, competition_factor):
    environment_availability += random.uniform(-0.5, 0.5)
    environment_availability = max(0, min(1, environment_availability))
    male_ratio = adjust_gender_ratio(population)
    infection_status_this_step = []
    for lamprey in population:
        neighbor_resources = [neighbor.resource_need for neighbor in population if neighbor != lamprey]
        lamprey.calculate_resource_acquisition(environment_availability, competition_factor, neighbor_resources,
                                               male_ratio)
        lamprey.calculate_reproduction_success()
        # 在这里传递 male_ratio 和 neighbor_resources 给 calculate_infection_chance 方法
        lamprey.infection_status = random.random() < lamprey.calculate_infection_chance(male_ratio, neighbor_resources)
        infection_status_this_step.append((lamprey.infection_status, male_ratio))
    return population, male_ratio, infection_status_this_step


def plot_resource_distribution(population, ax, male_ratio, alpha=0.5, time_step=0):
    resource_acquisitions = [agent.acquired_resource for agent in population]

    # 定义蓝色渐变色系的起始和结束RGB值
    color_start = np.array([0.2, 0.2, 0.8])  # 深蓝色
    color_end = np.array([0.7, 0.7, 1.0])  # 浅蓝色

    # 根据时间步长计算当前颜色
    color_current = color_start + (color_end - color_start) * (time_step / 10)
    color_current = tuple(color_current)  # 将NumPy数组转换为元组

    # 画柱状图，颜色根据时间步长渐变
    ax.hist(resource_acquisitions, bins=20, color=color_current, alpha=alpha, label=f'Male Ratio: {male_ratio:.2f}')
    ax.set_title(f'Time Step {time_step + 1} - Male Ratio: {male_ratio:.2f}')

def plot_resource_distribution_10(population, time_step, rows, cols, max_resource, max_frequency, male_ratio):
    plt.subplot(rows, cols, time_step + 1)
    resource_acquisitions = [agent.acquired_resource for agent in population]
    plt.hist(resource_acquisitions, bins=20, alpha=0.5)
    plt.xlim(0, max(1.0, max(resource_acquisitions)))  # 调整横坐标的上限为数据的最大值或1.5中的较大者
    plt.ylim(0, max(10, max_frequency))  # 调整纵坐标的上限为10或最大频率中的较大者
    plt.xlabel('Resource Acquisition')
    plt.ylabel('Frequency')
    plt.title(f'Male Ratio: {male_ratio:.2f}')

def plot_age_distribution_by_gender(population):
    plt.figure()
    male_ages = [agent.age for agent in population if agent.gender == 'M']
    female_ages = [agent.age for agent in population if agent.gender == 'F']
    plt.boxplot([male_ages, female_ages], labels=['Male', 'Female'])
    plt.ylabel('Age')
    plt.title('Boxplot of Age by Gender')
    plt.show()


def plot_infection_status_by_male_ratios(infection_status_over_time, male_ratios_over_time):
    true_counts = [0] * len(male_ratios_over_time)
    false_counts = [0] * len(male_ratios_over_time)

    # 计算每个时间步长的感染状态的True和False的数量
    for index, infection_data in enumerate(infection_status_over_time):
        for status in infection_data:
            if status[0]:  # 第一个元素是感染状态
                true_counts[index] += 1
            else:
                false_counts[index] += 1

    # 筛选出有感染状态变化的时间步长
    valid_indices = [index for index, (t_count, f_count) in enumerate(zip(true_counts, false_counts)) if
                     t_count > 0 or f_count > 0]
    true_counts = [true_counts[index] for index in valid_indices]
    false_counts = [false_counts[index] for index in valid_indices]
    valid_male_ratios = [male_ratios_over_time[index] for index in valid_indices]

    # 将male_ratios_over_time和对应的true_counts和false_counts进行排序
    sorted_indices = np.argsort(valid_male_ratios)
    sorted_male_ratios = np.array(valid_male_ratios)[sorted_indices]
    sorted_true_counts = np.array(true_counts)[sorted_indices]
    sorted_false_counts = np.array(false_counts)[sorted_indices]

    x = np.arange(len(sorted_male_ratios))  # x 坐标对应于排序后的 valid_male_ratios


    # 绘制柱状图
    plt.figure(figsize=(10,6))
    plt.bar(x - 0.1, sorted_true_counts, width=0.2, label='Infected (True)', color=(1, 0, 0, 0.5))
    plt.bar(x + 0.1, sorted_false_counts, width=0.2, label='Not Infected (False)', color=(0, 0, 1, 0.5))

    # 设置图表标题和标签
    plt.xlabel('Male Ratio')
    plt.ylabel('Frequency of Infection Status')
    plt.title('Infection_Status.pdf')
    plt.xticks(x, [f'{ratio:.2f}' for ratio in sorted_male_ratios])
    plt.legend()

    # 显示图表
    plt.show()

def main():
    initial_population_size = 100
    environment_availability = 1.0
    competition_factor = 0.2
    population = initialize_population(initial_population_size)
    male_ratios_over_time = []
    infection_status_over_time = []
    populations = []

    # 生成资源获取量的分布图
    fig, ax = plt.subplots(figsize=(10, 6))
    for time_step in range(10):
        population, male_ratio, infection_status = simulate_one_time_step(population, environment_availability,
                                                                          competition_factor)
        male_ratios_over_time.append(male_ratio)
        populations.append(population)
        infection_status_over_time.append(infection_status)
        plot_resource_distribution(population, ax, male_ratio=male_ratio, alpha=0.5 / (time_step + 1), time_step=time_step)
        sorted_data = sorted(zip(male_ratios_over_time, populations), key=lambda x: x[0])
        sorted_male_ratios, sorted_populations = zip(*sorted_data)
    ax.legend()
    ax.set_xlabel('Resource Acquisition')
    ax.set_ylabel('Frequency')
    ax.set_title('Overlayed Histogram of Resource Acquisition Over Time Steps')
    plt.savefig('Overlayed_Resource.pdf')
    plt.show()

    # 生成年龄分布图
    plot_age_distribution_by_gender(population)

    # 打印每个lamprey的详细信息
    for agent in population:
        print(f"Gender: {agent.gender}, Age: {agent.age}, Acquired_resources: {format(agent.acquired_resource, '.4f')}, Reproduction Status: {agent.reproduction_status}, Infection Status: {agent.infection_status}")
    print("Male Ratios Over Time:", [format(ratio, '.3f') for ratio in male_ratios_over_time])

    # 生成感染状态的分布图
    plot_infection_status_by_male_ratios(infection_status_over_time, male_ratios_over_time)

    time_steps = 10
    rows = 2
    cols = 5
    max_resource = 2  # 假定的最大资源获取量
    max_frequency = 20  # 假定的最大频率

    plt.figure(figsize=(20, 8))
    for time_step in range(time_steps):
        population, male_ratio, infection_status = simulate_one_time_step(population, environment_availability,
                                                                          competition_factor)
        male_ratios_over_time.append(male_ratio)
        plot_resource_distribution_10(
            sorted_populations[time_step],
            time_step,
            rows,
            cols,
            max_resource,
            max_frequency,
            sorted_male_ratios[time_step]
        )

    plt.tight_layout()
    plt.savefig('Resource_Distribution_Grid.pdf')
    plt.show()



if __name__ == "__main__":
    main()