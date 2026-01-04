clc
close all
%电动物流环卫车建模
N=input('请输入物流环卫车数量:');
socpublic=normrnd(0.4,0.1,[1 N]);%抽取soc，正态分布函数 normrnd 生成均值 0.4 和标准差 0.1 的随机数，表示每辆公务车的剩余电量
pbus=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存，数组用于存储每辆公务车的充电开始时间
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴，创建一个大小为 1x1440 的数组 t，表示一天中的分钟数，用作时间轴
%time=1:24;
%电动公务车白天抽取
for j=1:N
    startt=unifrnd(1140,1440);%抽取充电初始时刻，下午七点到早上七点均匀     
    start(j)=startt;
end

for i=1:N
T(i)=2700*(1-socpublic(i))/6.3;%充电时间
  if (start(i)+T(i))<=1440
    for m=fix(start(i)):fix(start(i)+T(i))
    pbus(m)=7+pbus(m);
    end
  else
    for n=fix(start(i)):1440
    pbus(n)=7+pbus(n); 
    end
    for j=1:((start(i)+T(i))-1440)
        pbus(j)=7+pbus(j);
    end
  end

end    
pbus_60 = pbus(1:60:end);
pbus_sum = sum(pbus); % 对整个 pbus 数组求和
pbus_sum_str = [num2str(pbus_sum) ' kw'];
disp(['N 辆物流电动汽车一天总负荷为: ' num2str(pbus_sum)]);
figure; 
plot (t,pbus)%输出图像
title('电动物流环卫车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['68辆物流环卫电动汽车一天总负荷为: ' pbus_sum_str]);
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后