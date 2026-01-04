clc 
close all
%电动公交车建模
N=input('请输入电动公交车数量:');
socbus=normrnd(0.5,0.1,[1 N]);%抽取soc，生成N辆电动汽车的剩余电量
a1=ones(1,1440);%一天有1440分钟
pbus=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴
%初始化数组


%电动公交车白天抽取 对每辆公交车进行白天充电模拟
for j=1:N
for i=1:5000   %5000次
    startt=normrnd(840,30,[1 1]);%抽取充电初始时刻  
if startt>=540&&startt<=990  
    start(j)=startt;
break
end
end
end
%计算每辆公交车白天充电时长T
for i=1:N
T(i)=10800*(1-socbus(i))/81;%白天快速充电时间，电池容量180千瓦时*60
if (start(i)+T(i))<=990
    for m=fix(start(i)):fix(start(i)+T(i))
    pbus(m)=90+pbus(m);
    end
else  
    for n=fix(start(i)):990
    pbus(n)=90+pbus(n); 
    end
end
end

%电动公交车晚上抽取
for j=1:N
for i=1:5000
    startt=unifrnd(1380,1440);%抽取充电初始时刻，晚上11点到12点 ,均匀分布   
if startt>=1380&&startt<=1440  
    start(j)=startt;
break
end
end
end

for i=1:N
T(i)=10800*(1-socbus(i))/18.9;%晚上常规充电时间，电池容量180千瓦时*60
    for n=fix(start(i)):1440
    pbus(n)=21+pbus(n);
    end
for m=1:fix(T(i)-1440+start(i))
    pbus(m)=21+pbus(m);
end
end

pbus_60 = pbus(1:60:end);
pbus_sum = sum(pbus); % 对整个 pbus 数组求和
pbus_sum_str = [num2str(pbus_sum) ' kw'];
disp(['N 辆公务电动汽车一天总负荷为: ' num2str(pbus_sum)]);
figure; 
plot (t,pbus)%输出图像
title('电动公交车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['759辆电动公交车一天总负荷为: ' pbus_sum_str]);
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后































