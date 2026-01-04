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


def self3_load_model_with_spline_and_kernel(N, bspline_param, kernel_param):

    length = np.random.normal(3.2, 0.88, N)  # 抽取路程

    p = np.ones(1440)
    start_time = np.ones(N)
    charge_duration = np.ones(N)
    t = np.arange(1, 1441)

    p1_val = 0.5 * normspec_equivalent([336, 1440], 1056, 204, 'outside')
    p2_val = 0.5 * normspec_equivalent([0, 336], -384, 204, 'outside')

    num_group1 = int(N * p2_val)
    num_group2 = int(0.5 * N) - num_group1
    num_group3 = int(0.5 * N + 1.5 * N / 11) - int(0.5 * N)
    num_group4 = N - (num_group1 + num_group2 + num_group3)

    num = 0
    while num < 1000:
        num += 1

        for j in range(num_group1):
            for i_inner in range(5000):
                startt = np.random.normal(1056, 204)
                if 336 <= startt <= 1440:
                    start_time[j] = startt
                    break

        for j in range(num_group1, num_group1 + num_group2):
            for i_inner in range(5000):
                startt = np.random.normal(-384, 204)
                if 1 <= startt <= 336:
                    start_time[j] = startt
                    break

        current_idx = num_group1 + num_group2
        for j in range(current_idx, current_idx + num_group3):
            for i_inner in range(5000):
                startt = np.random.uniform(1260, 1920)  # 均匀分布
                if 1260 <= startt <= 1440:
                    start_time[j] = startt
                    break

        current_idx += num_group3
        for j in range(current_idx, current_idx + num_group4):
            for i_inner in range(5000):
                startt = np.random.uniform(1260, 1920)  # 均匀分布
                if 1 <= (startt - 1440) <= 480:
                    start_time[j] = startt - 1440
                    break

        assigned_count = np.sum(start_time != 1)
        if assigned_count == N:
            break

    for i in range(N):
        charge_duration[i] = 2700 * length[i] / 445.5  # 慢充充电时间
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

    p_sum = np.sum(p)
    p_sum_str = f"{p_sum:.2f} kw"

    # --- 加入B样条曲线拟合 ---
    s_param = bspline_param * len(p)
    tck = splrep(t, p, k=3, s=s_param)
    p_smooth_bspline = splev(t, tck)

    # --- 加入核函数拟合 (高斯核平滑) ---
    p_smooth_kernel = gaussian_filter1d(p, sigma=kernel_param)

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str

