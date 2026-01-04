clc
close all
%电动私家车车建模，全天都可能充电
%1.无序无快充时
N=input('请输入无快充时电动私家车车数量:');
length=normrnd(3.2,0.88,[1 N]);%抽取路程
pself=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴

%电动私家充电抽取 生成初始充电时刻
p1 = normspec([336,1440],1056,204,'outside'); %均值1056，标准差204，五点三十六到全天
p2=normspec([0,336],-384,204,'outside'); %零点到五点三十六
cishu=0; %次数，避免陷入循环
while cishu<1000
    cishu=cishu+1;
for j=1:fix(N*p2)
for i=1:5000  %循环次数
    startt=normrnd(1056,204,[1 1]);%抽取充电初始时刻，上午五点三十六到晚上二十四点正态分布    
if startt>=336&&startt<=1440 
    start(j)=startt;
break
end
end
end
for j=(fix(N*p2)+1):N
for i=1:5000
    startt=normrnd(-384,204,[1 1]);%抽取充电初始时刻，0点到5.6点    
if startt>=1&&startt<=336 
    start(j)=startt;
break
end
end
end

for i=1:N    
T(i)=2700*length(i)/445.5;%充电时间 电池容量 充电功率*充电效率
if (start(i)+T(i))<1440
    for m=fix(start(i)):fix(start(i)+T(i))
    pself(m)=3.3+pself(m); %慢充充电功率
    end
else  
    for n=fix(start(i)):1440
    pself(n)=3.3+pself(n); 
    end
     for j=1:((start(i)+T(i))-1440)
        pself(j)=3.3+pself(j);
    end
end
end  
end
%pself=pself/100;
pself_60 = pself(1:60:end);
pself_sum = sum(pself); % 对整个 pbus 数组求和
pself_sum_str = [num2str(pself_sum) ' kw'];
disp(['N辆私家电动汽车一天总负荷为: ' num2str(pself_sum)]);
figure
plot (t,pself)%输出图像
title('电动私家车车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['3388辆电动私家车无序无快充一天总负荷为: ' pself_sum_str]);
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后





