
% MATLAB代码实现

% 参数设置
r = 0.1;  % 基础生长率
K = 1000;  % 环境承载量
d = 0.05;  % 自然死亡率
beta = 0.01;  % 资源对种群增长的影响系数
alpha = 0.02;  % 资源对性别比例调整的灵敏度
c = 0.001;  % 资源消耗率
s = 10;  % 资源自然增长率

% 初始条件
L0 = 500;  % 初始种群数量
M0 = 0.5;  % 初始雄性比例
R0 = 100;  % 初始资源量

% 时间步
T = 100;  % 模拟时间长度

% 初始化数组
L = zeros(1, T);
M = zeros(1, T);
R = zeros(1, T);
L(1) = L0;
M(1) = M0;
R(1) = R0;

% 模型迭代
for t = 1:T-1
    L(t+1) = L(t) + r*L(t)*(1 - L(t)/K) - d*L(t) + beta*R(t);
    M(t+1) = M(t) + alpha*(R(t) - M(t));
    R(t+1) = R(t) - c*L(t)*R(t) + s;
end

% 绘图
figure;
subplot(1, 3, 1);
plot(L, 'DisplayName', 'Total Population');
title('Total Population Over Time');
xlabel('Time');
ylabel('Population');
legend;

subplot(1, 3, 2);
plot(M, 'DisplayName', 'Male Ratio');
title('Male Ratio Over Time');
xlabel('Time');
ylabel('Male Ratio');
legend;

subplot(1, 3, 3);
plot(R, 'DisplayName', 'Resource Availability');
title('Resource Availability Over Time');
xlabel('Time');
ylabel('Resources');
legend;