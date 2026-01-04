import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import splrep, splev
from scipy.stats import norm
from scipy.ndimage import gaussian_filter1d
def normspec_equivalent(limits, mu, sigma, spec_type='outside'):
    lower, upper = limits[0], limits[1]

    if spec_type == 'outside':
        # 计算P(X< lower)
        prob_less_than_lower = norm.cdf(lower, loc=mu, scale=sigma)
        # 计算P(X> upper)
        prob_greater_than_upper = 1 - norm.cdf(upper, loc=mu, scale=sigma)
        # 落在区间之外的概率 P(X < lower) + P(X > upper)
        prob_outside = prob_less_than_lower + prob_greater_than_upper

        return prob_outside

def self2_load_model_with_spline_and_kernel(N, bspline_param, kernel_param):

    length = np.random.normal(3.2, 0.88, N)

    p = np.ones(1440)
    start_time = np.ones(N)
    charge_duration = np.ones(N)
    t = np.arange(1, 1441)
    p2_original = normspec_equivalent([0, 336], -384, 204, 'outside')

    slow_charge_evening_group_count = int(N * p2_original * 0.8)

    fast_charge_evening_group_count = int(N * p2_original * 0.2)

    num = 0
    while num < 1000:
        num += 1

        for j in range(slow_charge_evening_group_count):
            for i_inner in range(5000):
                startt = np.random.normal(1056, 204)
                if 336 <= startt <= 1440:
                    start_time[j] = startt
                    break

        for j in range(slow_charge_evening_group_count, int(N * 0.8)):
            for i_inner in range(5000):
                startt = np.random.normal(-384, 204)
                if 1 <= startt <= 336:
                    start_time[j] = startt
                    break

        for i in range(int(N * 0.8)):
            charge_duration[i] = 2700 * length[i] / 445.5
            if (start_time[i] + charge_duration[i]) < 1440:
                for m in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                    p[m] += 0.33
            else:
                for n in range(int(start_time[i]), 1440):
                    p[n] += 0.33
                overflow_duration = (start_time[i] + charge_duration[i]) - 1440
                for j_inner in range(int(overflow_duration)):
                    if j_inner < 1440:
                        p[j_inner] += 0.33

        start_index_fast_charge = int(N * 0.8)
        for j in range(start_index_fast_charge, start_index_fast_charge + fast_charge_evening_group_count):
            for i_inner in range(5000):
                startt = np.random.normal(1056, 204)
                if 336 <= startt <= 1440:
                    start_time[j] = startt
                    break

        for j in range(start_index_fast_charge + fast_charge_evening_group_count, N):
            for i_inner in range(5000):
                startt = np.random.normal(-384, 204)
                if 1 <= startt <= 336:
                    start_time[j] = startt
                    break

        assigned_count = np.sum(start_time != 1)
        if assigned_count == N:
            break

    for i in range(int(N * 0.8), N):
        charge_duration[i] = 2700 * length[i] / 3780
        if (start_time[i] + charge_duration[i]) < 1440:
            for m in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                p[m] += 2.8
        else:
            for n in range(int(start_time[i]), 1440):
                p[n] += 2.8
            overflow_duration = (start_time[i] + charge_duration[i]) - 1440
            for j_inner in range(int(overflow_duration)):
                if j_inner < 1440:
                    p[j_inner] += 2.8

    p_sum = np.sum(p)
    p_sum_str = f"{p_sum:.2f} kw"

    # --- 加入B样条曲线拟合 ---
    s_param = bspline_param * len(p)
    tck = splrep(t, p, k=3, s=s_param)
    p_smooth_bspline = splev(t, tck)

    # --- 加入核函数拟合 (高斯核平滑) ---
    p_smooth_kernel = gaussian_filter1d(p, sigma=kernel_param)

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str
