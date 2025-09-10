% 温度参数
T_min = 0;  % 最低温度
T_max = 40;  % 最高温度
T_step = 0.1;  % 温度步长
T_range = T_min:T_step:T_max;  % 温度范围

% 温度影响函数（高斯函数）
A = 1.2;
mu = 16;
sigma = 5;
g = @(T) A * exp(-(T - mu).^2 / (2 * sigma^2));

% 初始化性别比数组
sex_ratio = zeros(size(T_range));

% 假设性别比与温度的关系
% 注意：这是一个假设的关系。在实际应用中，这种关系可能更为复杂。
for i = 1:length(T_range)
    T_current = T_range(i);
    growth_rate = g(T_current);  % 当前温度下的增长率
    sex_ratio(i) = growth_rate / (1 + growth_rate);  % 假设性别比与增长率相关
end

% 绘图
plot(T_range, sex_ratio, 'LineWidth', 2);
xlabel('Temperature (°C)');
ylabel('Sex Ratio (proportion of males)');
title('Sex Ratio vs. Temperature');
grid on;
