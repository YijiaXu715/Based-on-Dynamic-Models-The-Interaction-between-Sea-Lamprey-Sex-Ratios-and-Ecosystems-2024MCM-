% 时间参数
T0 = 30;  % 总时间
dt = 0.01;  % 时间步长
N_t = T0 / dt + 1;  % 时间点数，确保包括最后一个时间点;  % 时间点数

% 模型参数
r0 = 0.1;  % 基础增长率
K = 1000;  % 环境承载量
d = 0.01;  % 寄生虫引起的死亡率常数
alpha = 0.02;  % 性比例调整速度
beta = 0.01;  % 寄生虫对性比例影响的强度

% 环境因素函数
F_max = 1.2;  % 食物对增长率的最大可能影响
F_half = 0.5;  % 达到最大影响一半时的食物量
k_F = 10;  % 形状参数
f = @(F) F_max / (1 + exp(-k_F * (F - F_half)));

% 修改温度影响函数为高斯函数
A = 1.2;  % 最大增长率影响
mu = 16;  % 最适宜的温度点
sigma = 5;  % 控制曲线宽度，需要根据实际情况调整

g = @(T) A * exp(-(T - mu).^2 / (2 * sigma^2));
h = @(P) 1 - 0.1 * P;
p = @(P) 1 + 0.1 * P;
s_opt = @(F, T) 0.5 + 0.05 * (F - T);

% 初始化
N = zeros(1, N_t);
s = zeros(1, N_t);
N(1) = 100;  % 初始种群数量
s(1) = 0.5;  % 初始性比例

% 假设环境因素是常数（实际应用中可能需要动态模拟或使用实际数据）
P = 0.1;

% 数值解
for t = 1:(N_t - 1)
    r = r0 * f(F) * g(T) * h(P);
    N(t + 1) = N(t) + (r * N(t) * (1 - N(t) / K) - d * N(t) * p(P)) * dt;
    s(t + 1) = s(t) + (alpha * (s_opt(F, T) - s(t)) - beta * s(t) * p(P)) * dt;
end

% 绘图
t = 0:dt:T0;
figure(1)
plot(t, N);
title('Population over time');
xlabel('Time');
ylabel('Population size');
figure(2)
plot(t, s);
title('Sex ratio over time');
xlabel('Time');
ylabel('Sex ratio (proportion of males)');
figure(3)
plot(T,s,'r',F,s,'b');
title('Sex ratio over time');
xlabel('Time');
ylabel('Sex ratio (proportion of males)');
