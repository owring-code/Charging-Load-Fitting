clc
%电动出租车建模
N=input('请输入电动出租车数量:');
soctaxi=normrnd(0.3,0.1,[1 N]);%抽取soc
pbus=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴

%电动出租车白天抽取
for j=1:N
    startt=unifrnd(660,840);%抽取充电初始时刻，上午11点到下午14点正态分布    
    start(j)=startt;
end

for i=1:N
T(i)=2700*(1-soctaxi(i))/40.5;%白天快速充电时间
if (start(i)+T(i))<=840
    for m=fix(start(i)):fix(start(i)+T(i))
    pbus(m)=45+pbus(m);
    end
else  
    for n=fix(start(i)):840
    pbus(n)=45+pbus(n); 
    end
end
end

%电动出租车车晚上抽取
for j=1:N
    startt=unifrnd(120,240);%抽取充电初始时刻，凌晨2点到4点    
    start(j)=startt;
end

for i=1:N
T(i)=2700*(1-soctaxi(i))/40.5;%晚上常规充电时间
if (start(i)+T(i))<=240
    for n=fix(start(i)):fix(start(i)+T(i))
    pbus(n)=45+pbus(n);
    end
else
for m=fix(start(i)):240
    pbus(m)=45+pbus(m);
end
end
end


%plot (t,pbus)%输出图像
 pbus_60 =  pbus(1:60:end);
 pbus_sum = sum( pbus); % 对整个 pbus 数组求和
 pbus_sum_str = [num2str( pbus_sum) ' kw'];
disp(['N辆出租电动汽车一天总负荷为: ' num2str( pbus_sum)]);
figure
plot (t, pbus)%输出图像

title('电动出租车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['421辆电动出租车有序无快充一天总负荷为: '  pbus_sum_str]);
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后






























