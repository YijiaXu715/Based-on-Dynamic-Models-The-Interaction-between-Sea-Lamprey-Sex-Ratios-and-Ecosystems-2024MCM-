syms R A R0 % 声明符号变量
eqn = exp(-R + R0) == exp(-R + R0 + log(A)/2 - log(0.25))/2 - 1; % 定义方程
solR = solve(eqn, R); % 解方程
pretty(solR) % 显示解的美化形式
