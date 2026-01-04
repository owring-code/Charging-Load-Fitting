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

def self1_load_model_with_spline_and_kernel(N, bspline_param, kernel_param):


    length = np.random.normal(3.2, 0.88, N)

    p = np.ones(1440)
    start_time = np.ones(N)
    charge_duration = np.ones(N)
    t = np.arange(1, 1441)


    p2 = normspec_equivalent([0, 336], -384, 204, 'outside')
    num_group1 = int(N * p2)

    num = 0
    while num < 1000:
        num += 1

        for j in range(num_group1):
            for i_inner in range(5000):
                startt = np.random.normal(1056, 204)
                if 336 <= startt <= 1440:
                    start_time[j] = startt
                    break

        for j in range(num_group1, N):
            for i_inner in range(5000):
                startt = np.random.normal(-384, 204)
                if 1 <= startt <= 336:
                    start_time[j] = startt
                    break

        if np.all(start_time != 1):
            break

    for i in range(N):
        charge_duration[i] = 2700 * length[i] / 445.5

        if (start_time[i] + charge_duration[i]) < 1440:
            for m in range(int(start_time[i]), int(start_time[i] + charge_duration[i])):
                p[m] += 0.33
        else:
            for n in range(int(start_time[i]), 1440):
                p[n] += 0.33
            overflow_duration = (start_time[i] + charge_duration[i]) - 1440
            for j in range(int(overflow_duration)):
                if j < 1440:
                    p[j] += 0.33

    p_sum = np.sum(p)
    p_sum_str = f"{p_sum:.2f} kw"

    # --- 加入B样条曲线拟合 ---
    s_param = bspline_param * len(p)
    tck = splrep(t, p, k=3, s=s_param)
    p_smooth_bspline = splev(t, tck)

    # --- 加入核函数拟合 (高斯核平滑) ---
    p_smooth_kernel = gaussian_filter1d(p, sigma=kernel_param)

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str
