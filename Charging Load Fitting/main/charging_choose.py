from bus_load import electric_bus_model_with_spline_and_kernel
from gongwu_load import gongwu_load_model_with_spline_and_kernel
from self1_load import self1_load_model_with_spline_and_kernel
from self2_load import self2_load_model_with_spline_and_kernel
from self3_load import self3_load_model_with_spline_and_kernel
from taxi_load import taxi_load_model_with_spline_and_kernel
from wuliu_load import wuliu_load_model_with_spline_and_kernel


def choose(N, k1, bspline_param, kernel_param):
    if k1 == 1:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = electric_bus_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动公交车'

    elif k1 == 2:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = gongwu_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动公务车'

    elif k1 == 3:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = self1_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动私家车（无序无快充）'

    elif k1 == 4:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = self2_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动私家车（无序有快充）'

    elif k1 == 5:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = self3_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动私家车（有序无快充）'

    elif k1 == 6:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = taxi_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动出租车'

    elif k1 == 7:
        t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str = wuliu_load_model_with_spline_and_kernel(N, bspline_param, kernel_param)
        c = '电动物流环卫车'

    return t, p, p_smooth_bspline, p_smooth_kernel, p_sum_str, c

