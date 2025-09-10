% 假设值 - 需要根据实际情况调整
N = 100; % 初始种群数量
E = 50; % 初始能量
C = 0.1; % 能量消耗系数
BMR = 0.5; % 基础成熟率
GAR = 0.2; % 生长率调整因子
BT = 10; % 基础阈值

% 初始化种群
population = struct();
sexratio = zeros(N,1);
for i = 1:N
    population(i).gender = randi([0, 1]) == 1; % 随机性别分配
    population(i).age = randi([1, 5]); % 随机年龄分配
    population(i).energy = E; % 初始能量
    sexratio(i) = 0.1 + (2 - 0.1) * rand; 
end
% Simulation Steps
for t = 1:100   
    % Useable Resource
    Ra = N * E - C * sum([population.energy]);
    for i = 1:N
        % 计算再生产资源和条件
        Rr = E * Ra;% 根据模型定义
        Rc = calculate_reproduction_condition(population(i), sexratio); % 根据模型定义
        Rs = Rr * Rc * Ra;

 % 决定是否繁殖
        if rand < Rs
            % 繁殖成功，创建新个体
            new_gender = rand < sexratio;
            new_agent = struct('gender', new_gender, 'age', 0, 'energy', E);
            population = [population new_agent];
            N = N + 1;
        end

        % 更新能量和状态
        population(i).energy = population(i).energy - C; % 根据模型调整
        population(i).age = population(i).age + 1; % 增加年龄
    end
    
    % 更新种群数量和性别比例，根据新生个体更新
    num_males = sum([population.gender] == 1);
    num_females = N - num_males;
    male_ratio = num_males / N;
    female_ratio = num_females / N;
end

% 结果分析
% 分析种群大小的变化
population_sizes = arrayfun(@(t) length(population(t)), 1:100);
plot(population_sizes);
title('Population Size Over Time');
xlabel('Time Step');
ylabel('Population Size');

% 分析性别比例的变化
gender_ratios = arrayfun(@(t) sum([population(t).gender] == 1) / length(population(t)), 1:100);
plot(gender_ratios);
title('Male Gender Ratio Over Time');
xlabel('Time Step');
ylabel('Male Gender Ratio');
