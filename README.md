# ⚡ 电动汽车充电负荷拟合系统
*(Charging Load Fitting)*

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Matplotlib](https://img.shields.io/badge/Library-Matplotlib%20%7C%20SciPy-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 项目概述

本项目是一个用于模拟不同类型电动汽车（EV）充电负荷特征的 Python 程序。系统内置了多种典型车辆的充电行为模型，能够基于**蒙特卡洛模拟**生成原始充电数据，并提供基于 **B样条曲线** 和 **高斯核函数** 的负荷拟合算法，最终支持数据的可视化分析与结构化导出。

---

## ✨ 核心功能模块

### 1. 🚗 多场景车辆充电模型
系统内置了多种电动汽车的负荷模型，可精准模拟不同群体的充电规律：
* 🚌 **电动公交车** (`bus_load.py`)
* 🚕 **电动出租车** (`taxi_load.py`)
* 🚙 **电动公务车** (`gongwu_load.py`)
* 🚚 **电动物流与环卫车** (`wuliu_load.py`)
* 🚗 **电动私家车**（提供三种场景策略）：
  * 无序无快充 (`self1_load.py`)
  * 无序有快充 (`self2_load.py`)
  * 有序无快充 (`self3_load.py`)

### 2. 📈 智能拟合与模拟
* **原始数据生成**：基于蒙特卡洛方法模拟车辆充电时间的随机性。
* **拟合算法选择**：支持 **B样条拟合 (B-Spline)** 与 **高斯核函数拟合 (Gaussian Kernel)**，以应对不同的电网负荷分析需求。

### 3. 💾 结果导出与存储
自动将计算结果保存为标准的 `JSON` 格式文件，便于后续跨平台调用与分析：
```json
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
```

---

## 📂 项目结构

```text
project/
├── main.py                    # 🚀 主程序入口
├── charging_choose.py         # 🎛️ 车辆类型选择模块
├── charging_plot.py           # 📊 数据可视化与结果保存模块
├── bus_load.py                # 🚌 电动公交车充电模型
├── gongwu_load.py             # 🚙 电动公务车充电模型
├── self1_load.py              # 🚗 电动私家车（无序无快充）模型
├── self2_load.py              # 🚗 电动私家车（无序有快充）模型
├── self3_load.py              # 🚗 电动私家车（有序无快充）模型
├── taxi_load.py               # 🚕 电动出租车充电模型
├── wuliu_load.py              # 🚚 电动物流环卫车充电模型
└── README.md                  # 📖 项目说明文档
```

---

## 🚀 快速开始

### 1. 安装依赖
请确保您的 Python 环境中安装了以下核心科学计算库：
```bash
pip install numpy matplotlib scipy
```

### 2. 参数配置
您可以在 `main.py` 中灵活调整以下核心平滑参数：
* `bspline_param`：B样条平滑参数（默认值：`1`）
* `kernel_param`：高斯核平滑参数（默认值：`10`）

---

## 📊 输出结果与对比分析

**案例演示参数：**
> - 车辆类型: 电动公交车
> - 车辆数量: 10000 辆
> - 对比函数: B样条拟合 vs 高斯核函数拟合

### 📌 原始负荷分布
<img width="430" height="246" alt="电动公交车一天内充电负荷预测" src="https://github.com/user-attachments/assets/3f8731eb-a7aa-4263-b719-37583e7e7948" />

### 📌 算法对比结论

| 拟合方法 | 效果图例 | 优势与适用场景 |
| :---: | :---: | :--- |
| **B样条拟合** | <img width="428" height="246" alt="B样条拟合曲线" src="https://github.com/user-attachments/assets/c4286f68-0826-4a79-a311-b058a26eef14" /> | **优势**：能在平滑的同时更好地保留原始数据的局部极值信息。<br>**适用**：需要精确捕捉负荷峰值大小和出现时间的场景（如：电网裕度分析、削峰填谷策略制定）。 |
| **高斯核拟合** | <img width="427" height="246" alt="高斯核拟合曲线" src="https://github.com/user-attachments/assets/d65ad98b-a0ad-44ff-a7d6-c01f3e27b0ed" /> | **优势**：具备极度简洁、直观的全局平滑效果。<br>**适用**：侧重于分析负荷长期宏观趋势、识别主要充电大时段的应用。 |

> ⏱️ **计算效率**：对于本系统每天的 1440 个时间粒度（分钟级）数据点，两种方法均能实现**近乎实时的计算响应**，完美满足交互式分析工具的效率要求。
