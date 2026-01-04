import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import splrep, splev
from scipy.ndimage import gaussian_filter1d

def electric_bus_model_with_spline_and_kernel(N, bspline_param, kernel_param):

    socbus = np.random.normal(0.5, 0.1, N)

    p = np.ones(1440)
    start_time = np.ones(N)
    charge_duration = np.ones(N)
    t = np.arange(1, 1441)

    for j in range(N):
        while True:
            startt = np.random.normal(840, 30)
            if 540 <= startt <= 990:
                start_time[j] = startt
                break

    for i in range(N):
        charge_duration[i] = 10800 * (1 - socbus[i]) / 81

        if (start_time[i] + charge_duration[i]) <= 990:
            for m in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                p[m] += 0.9
        else:
            for n in range(int(start_time[i]), 990):
                p[n] += 0.9

    # 电动公交车晚上充电模拟
    for j in range(N):
        while True:
            startt = np.random.uniform(1380, 1440)
            if 1380 <= startt <= 1440:
                start_time[j] = startt
                break

    for i in range(N):
        charge_duration[i] = 10800 * (1 - socbus[i]) / 18.9

        for n in range(int(start_time[i]), 1440):
            p[n] += 0.21
        if charge_duration[i] - (1440 - start_time[i]) > 0:
            for m in range(int(charge_duration[i] - (1440 - start_time[i]))):
                if m < 1440:
                    p[m] += 0.21

    pbus_sum = np.sum(p)
    p_sum_str = f"{pbus_sum:.2f} kw"


    # --- 加入B样条曲线拟合 ---
    s_param = bspline_param * len(p)
    tck = splrep(t, p, k=3, s=s_param)
    # 使用拟合的B样条参数来评估新点（或原始点）上的值
    p_smooth_bspline = splev(t, tck)

    # --- 加入核函数拟合 (高斯核平滑) ---
    p_smooth_kernel = gaussian_filter1d(p, sigma=kernel_param)

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str
