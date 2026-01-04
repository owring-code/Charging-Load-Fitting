# charging_plot.py

import matplotlib.pyplot as plt
import numpy as np
import json  # <-- 1. 导入json库

# 设置全局字体及大小
plt.rcParams['font.sans-serif'] = ['SimHei', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 20  # 全局字体大小


def plot(N, k2, t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str, c):
    # --- 绘图部分 (与原来保持一致) ---
    plt.figure(figsize=(14, 7))

    plt.plot(t, p, label='原始充电负荷数据', alpha=0.7, linewidth=2)

    # 为了保存，定义变量来存储选择的拟合结果
    fitted_data = None
    c2_for_filename = ''

    if k2 == 'a':
        plt.plot(t, p_smooth_bspline, label='B样条拟合曲线', color='red', linestyle='--', linewidth=2)
        c2 = 'B样条拟合曲线'
        c2_for_filename = 'B样条拟合' # 用于文件名
        fitted_data = p_smooth_bspline
    elif k2 == 'b':
        plt.plot(t, p_smooth_kernel, label='高斯核函数拟合曲线', color='green', linestyle='--', linewidth=2)
        c2 = '高斯核函数拟合曲线'
        c2_for_filename = '高斯核函数拟合' # 用于文件名
        fitted_data = p_smooth_kernel

    print(f'{N} 辆{c}一天总负荷为: {p_sum_str}')

    plt.title(f'{c}充电负荷建模与{c2}', fontsize=22)
    plt.xlabel('时间段/min', fontsize=20, labelpad=10)
    plt.ylabel('充电功率/kW', fontsize=20)
    plt.legend([f'总负荷为: {p_sum_str}', f'{c2}'], fontsize=20)
    plt.grid(True)
    plt.show()

    if fitted_data is not None:
        results_to_save = {
            "metadata": {
                "车辆类型": c,
                "车辆数量": N,
                "一天总负荷": p_sum_str,
                "拟合方法": c2
            },
            "data": {
                "时间_分钟": t.tolist() if isinstance(t, np.ndarray) else t,
                "原始负荷_kW": p.tolist() if isinstance(p, np.ndarray) else p,
                "拟合负荷_kW": fitted_data.tolist() if isinstance(fitted_data, np.ndarray) else fitted_data
            }
        }

        filename = f"{N}辆{c}_{c2_for_filename}_结果.json"

        # 写入JSON文件
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_to_save, f, ensure_ascii=False, indent=4)

            print(f"✅ 拟合结果已成功保存到文件: {filename}")
        except Exception as e:
            print(f"❌ 保存文件时出错: {e}")