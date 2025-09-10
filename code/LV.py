import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# 模型参数
r_F = 0.1  # 雌性出生率
r_M = 0.1  # 雄性出生率
alpha = 0.2  # 雌性竞争和捕食影响系数
beta = 0.1  # 雄性竞争和捕食影响系数
gamma = 0.2  # 雄性竞争和捕食影响系数
delta = 0.1  # 雄性竞争和捕食影响系数
lambda_ = 0.05  # 食物的自然减少速率
mu = 0.02  # 外部的食物补给速率
eta1 = 0.1  # 雌性数量对性别比例的影响系数
eta2 = 0.1  # 雄性数量对性别比例的影响系数
eta3 = 0.1  # 食物供应对性别比例的影响系数

# 初值
F0 = 100  # 初始雌性数量
M0 = 100  # 初始雄性数量
S0 = 50  # 初始食物供应


# 模型函数
def model(y, t):
    F, M, S = y
    dFdt = r_F * F * (1 - alpha * F - beta * M)
    dMdt = r_M * M * (1 - gamma * F - delta * M)
    dSdt = -lambda_ * S + mu
    dSexRatiodt = eta1 * dFdt + eta2 * dMdt + eta3 * dSdt
    return [dFdt, dMdt, dSdt, dSexRatiodt]


# 求解ODE
t = np.linspace(0, 100, 1000)
y0 = [F0, M0, S0, M0 / (F0 + M0)]  # 初始条件包括性别比例
solution = odeint(model, y0, t)

# 提取结果
F = solution[:, 0]
M = solution[:, 1]
S = solution[:, 2]
SexRatio = solution[:, 3]

# 绘图
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, F, 'b', label='雌性')
plt.plot(t, M, 'r', label='雄性')
plt.xlabel('时间')
plt.ylabel('数量')
plt.legend()
plt.title('灯鱼种群数量随时间变化')

plt.subplot(2, 1, 2)
plt.plot(t, SexRatio, 'g')
plt.xlabel('时间')
plt.ylabel('性别比例')
plt.title('性别比例随时间变化')

plt.tight_layout()
plt.show()