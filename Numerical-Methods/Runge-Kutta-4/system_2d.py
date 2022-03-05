# src: http://codenet.ru/progr/alg/Runge-Kutt-Method/
# check: https://math24.biz/s_differential_equation2

# old test: x - y; -4 * x + y
import matplotlib.pyplot as plt
from numpy import arange
from math import *

xxx = compile('-2 * x -2 * y', '', 'eval')
yyy = compile('-1 * x + 2 * y + cos(t)',' ', 'eval')

def dxdt(x, y, t): # input
    return eval(xxx)

def dydt(x, y, t): # input
    return eval(yyy)

# x(t0) = x0; y(t0) = y0

# setup plt
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.grid(True, which='both')
ax.set_ylim(-100, 100)
ax.set_xlim(-100, 100)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.text (50, 110, u"dx/dt=-2 * x -2 * y\ndy/dt=-1 * x + 2*y")


def runge_kutta_2d(x0, y0, t0, t, h):
    n = int(abs(t - t0) / h)
    if t < t0: h *= -1 # !!!
    x_n = x0
    y_n = y0
    t_n = t0
    for i in range(1, n + 1):
        k1 = h * dxdt(x_n, y_n, t_n)
        m1 = h * dydt(x_n, y_n, t_n)

        k2 = h * dxdt(x_n + k1 / 2, y_n + m1 / 2, t_n + h / 2)
        m2 = h * dydt(x_n + k1 / 2, y_n + m1 / 2, t_n + h / 2)

        k3 = h * dxdt(x_n + k2 / 2, y_n + m2 / 2, t_n + h / 2)
        m3 = h * dydt(x_n + k2 / 2, y_n + m2 / 2, t_n + h / 2)

        k4 = h * dxdt(x_n + k3, y_n + m3, t_n + h)
        m4 = h * dydt(x_n + k3, y_n + m3, t_n + h)

        x_n = x_n + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y_n = y_n + (m1 + 2 * m2 + 2 * m3 + m4) / 6
        
        t_n += h
    return x_n, y_n

def phase_trajectory(koshi_x0, koshi_y0, koshi_t0, runge_h, min_t, max_t, plot_step):
    # must return or plot [x], [y]
    x = []
    y = []
    for t in arange(min_t, max_t, plot_step):
        rk_res = runge_kutta_2d(koshi_x0, koshi_y0, koshi_t0, t, runge_h)
        # print(rk_res)
        x.append(rk_res[0])
        y.append(rk_res[1])
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)

def phase_portrait(offset_x, offset_y, koshi_x0, koshi_y0, koshi_t0, runge_h, min_t, max_t, plot_step):
    x_up = koshi_x0 + 2 * offset_x
    y_up = koshi_y0

    x_down = koshi_x0
    y_down = koshi_y0 - 2 * offset_y

    x_left = koshi_x0 - offset_x
    y_left = koshi_y0 + offset_y

    x_right = koshi_x0 + offset_x
    y_right = koshi_y0 + offset_y

    phase_trajectory(x_up, y_up, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x_down, y_down, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x_left, y_left, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x_right, y_right, koshi_t0, runge_h, min_t, max_t, plot_step)


# ОНО РАБОТАЕТ
if __name__ == '__main__':
    res = runge_kutta_2d(2, 7, 0, -0.91, 0.001)
    print(res)
    # phase_trajectory(2, 7, 0, 0.001, -0.91, 0.91, 0.01)
    phase_portrait(30, 20, 2, 7, 0, 0.001, -2, 2, 0.1)
    plt.show()



'''
def phase_portrait(offset_x, offset_y, koshi_x0, koshi_y0, koshi_t0, runge_h, min_t, max_t, plot_step):
    x1 = koshi_x0 - 1.7*offset_x
    y1 = koshi_y0 + 1.7*offset_y

    x2 = koshi_x0 + 1.7*offset_x
    y2 = koshi_y0 + 1.7*offset_y

    x3 = koshi_x0 + 1.7*offset_x
    y3 = koshi_y0 - 1.7*offset_y

    x4 = koshi_x0 - 1.7*offset_x
    y4 = koshi_y0 - 1.7*offset_y

    phase_trajectory(x1, y1, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x2, y2, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x3, y3, koshi_t0, runge_h, min_t, max_t, plot_step)
    phase_trajectory(x4, y4, koshi_t0, runge_h, min_t, max_t, plot_step)
'''
