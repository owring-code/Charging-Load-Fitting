%3.有序无快充时
clc
close all
N=input('请输入有序无快充时电动私家车车数量:');
length=normrnd(3.2,0.88,[1 N]);%抽取路程
pself=ones(1,1440);%负荷储存
start=ones(1,N);%开始充电时间储存
T=ones(1,N);%充电时长储存
t=1:1440;%时间轴

%电动私家充电抽取
p1 = 0.5*normspec([336,1440],1056,204,'outside');
p2=0.5*normspec([0,336],-384,204,'outside');
disp(['Matlab p1: ' num2str(p1)]);
disp(['Matlab p2: ' num2str(p2)]);
cishu=0; %次数，避免陷入循环
while cishu<1000
    cishu=cishu+1;
for j=1:fix(N*p2)
  for i=1:5000
    startt=normrnd(1056,204,[1 1]);%抽取充电初始时刻，上午五点三十六到晚上二十四点正态分布    
    if startt>=336&&startt<=1440 
    start(j)=startt;
     break
    end
  end
end

for j=(fix(N*p2)+1):(0.5*N)
  for i=1:5000
    startt=normrnd(-384,204,[1 1]);%抽取充电初始时刻，0点到5.6点    
    if startt>=1&&startt<=336 
    start(j)=startt;
     break
    end
  end
end

for j=((0.5*N)+1):(fix(0.5*N+1.5*N/11))
 for i=1:5000
    startt=unifrnd(1260,1920);%抽取充电初始时刻，晚上九点到上午八点   
  if startt>=1260&&startt<=1440
        start(j)=startt;
     break
  end
 end
end

for j=(fix(0.5*N+1.5*N/11)+1):N
 for i=1:5000
    startt=unifrnd(1260,1920);%抽取充电初始时刻，晚上九点到上午八点  
   if (startt-1440)>=1&&(startt-1440)<=480
    start(j)=startt-1440;
     break
   end
 end
end

for i=1:N    
T(i)=2700*length(i)/445.5;%充电时间
  if (start(i)+T(i))<1440
      for m=fix(start(i)):fix(start(i)+T(i))
    pself(m)=3.3+pself(m);
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
%plot (t,pself)%输出图像
pself_60 = pself(1:60:end);
pself_sum = sum(pself); % 对整个 pbus 数组求和
pself_sum_str = [num2str(pself_sum) ' kw'];
disp(['N辆私家电动汽车一天总负荷为: ' num2str(pself_sum)]);
figure
plot (t,pself)%输出图像
title('电动私家车车建模'); %添加图标题
xlabel('时间段');
ylabel('充电功率/kw'); %标注横纵坐标轴
legend(['3388辆电动私家车有序无快充一天总负荷为: ' pself_sum_str]);
grid on; %在所画出的图形坐标中添加栅格，注意用在plot之后



