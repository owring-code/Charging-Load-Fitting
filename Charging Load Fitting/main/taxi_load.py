import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import splrep, splev
from scipy.ndimage import gaussian_filter1d
def taxi_load_model_with_spline_and_kernel(N, bspline_param, kernel_param):

    soctaxi = np.random.normal(0.3, 0.1, N)

    p = np.ones(1440)
    start_time = np.ones(N)
    charge_duration = np.ones(N)
    t = np.arange(1, 1441)

    # 电动出租车白天抽取
    for j in range(N):
        startt = np.random.uniform(660, 840)
        start_time[j] = startt

    for i in range(N):
        charge_duration[i] = 2700 * (1 - soctaxi[i]) / 40.5
        if (start_time[i] + charge_duration[i]) <= 840:
            for m in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                p[m] += 4.5
        else:
            for n in range(int(start_time[i]), 840):
                p[n] += 4.5

    for j in range(N):
        startt = np.random.uniform(120, 240)
        start_time[j] = startt

    for i in range(N):
        charge_duration[i] = 2700 * (1 - soctaxi[i]) / 40.5
        if (start_time[i] + charge_duration[i]) <= 240:
            for n in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                p[n] += 4.5
        else:
            for m in range(int(start_time[i]), 240):
                p[m] += 4.5


    p_sum = np.sum(p)
    p_sum_str = f"{p_sum:.2f} kw"

    # --- 加入B样条曲线拟合 ---
    s_param = bspline_param * len(p)
    tck = splrep(t, p, k=3, s=s_param)
    p_smooth_bspline = splev(t, tck)

    # --- 加入核函数拟合 (高斯核平滑) ---
    p_smooth_kernel = gaussian_filter1d(p, sigma=kernel_param)

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str
