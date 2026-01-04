from charging_choose import choose
from charging_plot import plot

# 设置基本参数
bspline_param = 1  # B样条平滑参数 越大越平滑
kernel_param = 10   # 高斯核函数平滑参数 越大越平滑
print("车辆类型:1.电动公交车 2.电动公务车 3.电动私家车（无序无快充） 4.电动私家车（无序有快充） 5.电动私家车（有序无快充） 6.电动出租车 7.电动物流环卫车")
k1 = int(input('请输入车辆类型(1-7):'))
N = int(input('请输入车辆数量:'))
print("函数类型:a. B样条拟合 b. 高斯核函数拟合")
k2 = input('请输入函数类型(a/b):')

if __name__ == '__main__':
    # 选择车辆类型
    t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str, c = choose(N, k1, bspline_param, kernel_param)
    # 拟合曲线
    plot(N, k2, t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str, c)
