%3.有序无快充时
clc
close all
N=input('请输入有序无快充时电动私家车车数量:');
length=normrnd(3.2,0.88,[1 N]);%抽取路程
pself=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴

% --- Matlab: 打印 pself 初始化后的状态 ---
fprintf('\n--- Matlab: pself 初始化后的状态 ---\n');
fprintf('pself 数组前10个值: %s\n', mat2str(pself(1:10)));
fprintf('pself 数组后10个值: %s\n', mat2str(pself(end-9:end)));
fprintf('pself 数组总和: %.2f\n', sum(pself));
fprintf('------------------------------------\n\n');

%电动私家充电抽取
p1 = 0.5*normspec([336,1440],1056,204,'outside');
p2=0.5*normspec([0,336],-384,204,'outside');
cishu=0; %次数，避免陷入循环

% 计算各分组数量 (在while循环外只计算一次)
num_group1_matlab = fix(N * p2);
num_group2_matlab = fix(0.5 * N) - num_group1_matlab;
num_group3_matlab = fix(0.5 * N + 1.5 * N / 11) - fix(0.5 * N);
num_group4_matlab = N - (num_group1_matlab + num_group2_matlab + num_group3_matlab);

fprintf('Matlab 分组数量：G1=%d, G2=%d, G3=%d, G4=%d\n', num_group1_matlab, num_group2_matlab, num_group3_matlab, num_group4_matlab);
fprintf('Matlab 总分组数量: %d\n', num_group1_matlab + num_group2_matlab + num_group3_matlab + num_group4_matlab);


% --- MATLAB: 确保所有车辆的start时间被分配 ---
while cishu<1000
    cishu=cishu+1;

    % 找到所有未分配的车辆索引 (Matlab使用1-based索引)
    unassigned_indices = find(start == 1); 
    if isempty(unassigned_indices)
        fprintf('Matlab: 所有车辆已在 %d 次尝试中分配成功。\n', cishu);
        break; % 所有车辆都已分配
    end

    % 根据分组重新尝试分配start时间，只针对未分配的车辆
    for k = unassigned_indices % 遍历未分配的车辆索引
        % 根据 k (当前车辆索引) 判断它属于哪个分组
        if k <= num_group1_matlab
            % Group 1 logic
            for i_inner = 1:5000
                startt = normrnd(1056, 204, [1 1]);
                if startt >= 336 && startt <= 1440
                    start(k) = startt;
                    break;
                end
            end
        elseif k <= (num_group1_matlab + num_group2_matlab)
            % Group 2 logic
            for i_inner = 1:5000
                startt = normrnd(-384, 204, [1 1]);
                if startt >= 1 && startt <= 336
                    start(k) = startt;
                    break;
                end
            end
        elseif k <= (num_group1_matlab + num_group2_matlab + num_group3_matlab)
            % Group 3 logic
            for i_inner = 1:5000
                startt = unifrnd(1260, 1920);
                if startt >= 1260 && startt <= 1440
                    start(k) = startt;
                    break;
                end
            end
        else % Group 4 logic
            for i_inner = 1:5000
                startt = unifrnd(1260, 1920);
                if (startt - 1440) >= 1 && (startt - 1440) <= 480
                    start(k) = startt - 1440;
                    break;
                end
            end
        end
    end % End of for k = unassigned_indices

    % 每次外层循环结束后再次检查，如果还是有未分配的，则继续尝试
    current_unassigned_count_matlab = sum(start == 1);
    if current_unassigned_count_matlab == 0
        fprintf('Matlab: 所有车辆已在 %d 次尝试中分配成功。\n', cishu);
        break; % 确保循环结束
    end
end % End of while cishu loop

final_assigned_count_matlab = sum(start ~= 1);
fprintf('Matlab: 最终成功分配充电开始时间的车辆数量: %d/%d\n', final_assigned_count_matlab, N);
if final_assigned_count_matlab < N
    fprintf('警告：部分车辆未能成功分配充电开始时间！这可能会导致总负荷降低。\n');
    unassigned_indices_final = find(start == 1);
    fprintf('未分配的车辆索引（前10个）: %s...\n', mat2str(unassigned_indices_final(1:min(10, end))));
end


% --- MATLAB: 将 pself 累加逻辑移到 while 循环之外 ---
% 确保只有在所有 start 时间都确定后才进行负荷累加
for i=1:N    
    % 仅对成功分配了 start time 的车辆进行计算
    if start(i) == 1 % 如果 start(i) 仍为初始值 1，则跳过
        continue;
    end
    
    T(i)=2700*length(i)/445.5;%充电时间

    if (start(i)+T(i))<1440
        for m=fix(start(i)):fix(start(i)+T(i))
            pself(m)=3.3+pself(m);
        end
    else  
        for n=fix(start(i)):1440
            pself(n)=3.3+pself(n); 
        end
        % Matlab `j` loop is 1-based, and it means the number of iterations
        % Use fix for integer part of the duration
        num_overflow_minutes = (start(i)+T(i))-1440;
        for j_inner=1:fix(num_overflow_minutes) 
            % 注意：Matlab数组是1-indexed，所以这里访问 pself(1), pself(2) ...
            pself(j_inner)=3.3+pself(j_inner);
        end
    end
end  

% --- Matlab: 打印 pself 最终状态和总和 ---
fprintf('\n--- Matlab: pself 充电累加后的最终状态 ---\n');
fprintf('pself 数组前10个值: %s\n', mat2str(pself(1:10)));
fprintf('pself 数组后10个值: %s\n', mat2str(pself(end-9:end)));
pself_sum = sum(pself);
fprintf('pself 数组总和: %.2f\n', pself_sum);
fprintf('N辆私家电动汽车一天总负荷为: %.2f\n', pself_sum);
fprintf('------------------------------------------\n\n');

%plot (t,pself)%输出图像
% pself_60 = pself(1:60:end); % 这行不用于求和
% pself_sum = sum(pself); % 这行已经在上面执行
pself_sum_str = [num2str(pself_sum) ' kw'];
disp(['N辆私家电动汽车一天总负荷为: ' num2str(pself_sum)]);
figure
plot (t,pself)%输出图像
title('电动私家车车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['3388辆电动私家车有序无快充一天总负荷为: ' pself_sum_str]); % 这里'3388'是硬编码，应为N
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后