% 设置模型参数
rf = 0.1; % 雌性出生率
rm = 0.1; % 雄性出生率
df = 0.05; % 雌性死亡率
dm = 0.05; % 雄性死亡率
k = 1; % 资源影响性别转换的敏感度
R0 = 100; % 资源量的阈值
rR = 0.1; % 资源的再生率
K = 250; % 资源的承载能力
cf = 0.02; % 雌性资源消耗率
cm = 0.02; % 雄性资源消耗率
N0 = 100; % 初始种群大小
R = 150; % 初始资源量

% 定义逻辑斯蒂函数来计算Pf(R)
Pf = @(R) 1 / (1 + exp(-k*(R-R0)));

% 定义种群动态的微分方程
dPop = @(t, y) [rf * Pf(y(2)) * y(1) - df * y(1); % dNf/dt
                 rm * (1 - Pf(y(2))) * y(1) - dm * y(3); % dNm/dt
                 rR * y(2) * (1 - y(2)/K) - cf * y(1) - cm * y(3)]; % dR/dt

% 设置初始条件
initial_conditions = [N0/2; R; N0/2];

% 设置模拟时间范围
tspan = [0 70]; % 比如从0到70天

% 使用ode45求解微分方程
[t, y] = ode45(dPop, tspan, initial_conditions);

% 绘制资源量并设置左侧Y轴颜色
figure(1);
yyaxis left; % 激活左侧Y轴
plot(t, y(:,2), 'r'); % 绘制资源量
ylabel('Resource Amount (thousand)');
xlabel('Time (day)');
set(gca, 'YColor', 'r'); % 设置左侧Y轴和标签颜色为红色

% 计算并绘制Female Quantity与Male Quantity的比值，设置右侧Y轴颜色
yyaxis right; % 切换到右侧Y轴
gender_ratio = y(:,1) ./ y(:,3);
plot(t, gender_ratio, 'b-'); % 绘制性别比值曲线
ylabel('Ratio');
set(gca, 'YColor', 'b'); % 设置右侧Y轴和标签颜色为蓝色

% 设置图例和标题
legend('Resource Amount', 'Female/Male Ratio', 'Location', 'best');
title('Sea Lamprey Population and Resource Dynamics Model');

% 设置图形保存参数并保存为PDF
fig = gcf;
fig.PaperPositionMode = 'auto';
fig_pos = fig.PaperPosition;
fig.PaperSize = [fig_pos(3) fig_pos(4)];
filename = '海洋七鳃鳗种群与资源动态模型';
print(filename, '-dpdf', '-bestfit');


% 计算性别比
gender_ratio = y(:,1) ./ y(:,3);

% 绘制性别比与资源量的关系图
figure(2);
plot(gender_ratio, y(:,2), 'b-');
xlabel('性别比 Nf/Nm');
ylabel('资源量 R');
title('性别比与资源量的关系');
grid on;

fig = gcf;
fig.PaperPositionMode = 'auto';
fig_pos = fig.PaperPosition;
fig.PaperSize = [fig_pos(3) fig_pos(4)];
filename = '海洋七鳃鳗种群与资源动态模型';
print(filename, '-dpdf', '-bestfit');

print('Gender_Ratio_vs_Resource', '-dpdf');
