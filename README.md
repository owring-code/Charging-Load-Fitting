# 电动汽车充电负荷拟合

这是一个用于模拟不同类型电动汽车充电负荷的Python程序，包含多种车辆类型的充电行为模型、数据拟合和可视化功能。

## 项目结构
~~~text
├── main.py                    # 主程序入口
├── charging_choose.py         # 车辆类型选择模块
├── charging_plot.py           # 数据可视化与结果保存模块
├── bus_load.py                # 电动公交车充电模型
├── gongwu_load.py             # 电动公务车充电模型
├── self1_load.py              # 电动私家车（无序无快充）模型
├── self2_load.py              # 电动私家车（无序有快充）模型
├── self3_load.py              # 电动私家车（有序无快充）模型
├── taxi_load.py               # 电动出租车充电模型
├── wuliu_load.py              # 电动物流环卫车充电模型
└── README.md                  # 项目说明文档
~~~

## 原始数据生成：
基于蒙特卡洛的充电时间模拟

## 拟合函数选择：
B样条拟合和高斯核函数拟合

## 结果导出：
自动保存为JSON格式文件
~~~json
{
  "metadata": {
    "车辆类型": "电动公交车",
    "车辆数量": 100,
    "一天总负荷": "12345.67 kw",
    "拟合方法": "B样条拟合曲线"
  },
  "data": {
    "时间_分钟": [1, 2, 3, ...],
    "原始负荷_kW": [1.0, 1.21, 1.42, ...],
    "拟合负荷_kW": [1.1, 1.2, 1.3, ...]
  }
}
~~~

## 安装依赖
~~~bash
pip install numpy matplotlib scipy
~~~

## 配置参数
在main.py中可以调整

bspline_param：B样条平滑参数（默认：1）

kernel_param：高斯核平滑参数（默认：10）

## 输出结果案例
~~~text
车辆类型: 电动公交车
车辆数量: 10000
函数类型:B样条拟合 & 高斯核函数拟合
~~~
### 电动公交车一天内充电负荷预测
<img width="430" height="246" alt="image" src="https://github.com/user-attachments/assets/3f8731eb-a7aa-4263-b719-37583e7e7948" />

### B样条拟合曲线
<img width="428" height="246" alt="image" src="https://github.com/user-attachments/assets/c4286f68-0826-4a79-a311-b058a26eef14" />

### 高斯核函数拟合曲线
<img width="427" height="246" alt="image" src="https://github.com/user-attachments/assets/d65ad98b-a0ad-44ff-a7d6-c01f3e27b0ed" />

## 结果分析
在对比中可以发现，对于需要精确捕捉负荷峰值大小和出现时间的应用场景，如电网裕度分析或削峰填谷策略制定，B样条拟合可能更具优势，因为它能在平滑的同时更好地保留原始数据的局部极值信息。而对于侧重于分析负荷长期趋势、识别主要充电时段的应用，高斯核函数拟合则以其简洁、直观的平滑效果提供了有力的支持。在计算效率方面，对于本研究中1440个数据点的时间序列，两种方法均能实现近乎实时的计算，满足了软件工具交互式分析的要求。
