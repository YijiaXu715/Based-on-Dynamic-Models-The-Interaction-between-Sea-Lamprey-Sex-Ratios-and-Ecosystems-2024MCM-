clc; clear;

% 初始化参数
num_age_groups = 2;  % 年龄组数量
L = [12/17,0.55];  % 每个年龄组的生存率
A = [0 1.2];  % 每个年龄组的繁殖率

% 初始种群分布（每个年龄组的初始数量）
N_0 = [800 50];  % 假设的初始数量

% 模拟的时间步长和总步数
time_step = 5;
total_steps = 40;

% 初始化种群矩阵
N = zeros(num_age_groups, total_steps);
N(:, 1) = N_0';

for t = 2:total_steps
    % 对于两个年龄组，我们需要特别处理，因为第二组分为a和b两部分
    N(1, t) = L(1) * N(1, t-1);  % 第一年龄组
    N(2, t) = L(2) * N(2, t-1) + A(2) * N(1, t-1);  % 第二年龄组，考虑繁殖
end

% 细分第二组为a部分和b部分
Na = 0.7 * N(2, :);  % 第二组a部分
Nb = 0.3 * N(2, :);  % 第二组b部分

% 绘制结果
figure(1);
hold on;
plot(1:total_steps, N(1, :), 'o-', 'DisplayName', 'Age Group 1');
plot(1:total_steps, N(2, :), 'x-', 'DisplayName', 'Age Group 2');
plot(1:total_steps, Na, '*-', 'DisplayName', 'Group 2a');
plot(1:total_steps, Nb, 's-', 'DisplayName', 'Group 2b');
xlabel('Time Steps');
ylabel('Population');
legend;
title('Modified Leslie Population Model');
grid on;