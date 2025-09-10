T = 100;
rf = 0.1; % 雌性出生率
rm = 0.1; % 雄性出生率
df = 0.05; % 雌性死亡率
dm = 0.05; % 雄性死亡率
R0 = 100; % 资源量的阈值
rR = 0.1; % 资源的再生率
K = 500; % 资源的承载能力
cf = 0.5; % 雌性资源消耗率
%cm = 0.01; % 雄性资源消耗率
N = zeros(1, T);
R = zeros(1, T);
a = 0.1;
% 初始值设定
N(1) = 100; % 初始种群雌性大小
R(1) = 80; % 初始资源量
for t = 1:T-1
    N(t+1) = N(t) + rf*R(t)*N(t) - df*N(t);
    R(t+1) = R(t) + rR*R(t) - a * cf * R(t) * N(t);
end
t = 1:1:T;
plot(t,R,'b',t,N,'r')
% xlabel('$x$','Interpreter','latex');
% ylabel('$y$','Interpreter','latex');
% title('Flight Path','Interpreter','latex');
% % -------cut saved PDF size---------
% fig = gcf;
% fig.PaperPositionMode='auto';
% fig_pos = fig.PaperPosition;
% fig.PaperSize = [fig_pos(3) fig_pos(4)];
% % -------cut saved PDF size---------
% print('path','-dpdf');
