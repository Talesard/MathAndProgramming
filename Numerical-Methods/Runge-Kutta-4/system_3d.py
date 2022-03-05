import matplotlib.pyplot as plt
from numpy import arange
from mpl_toolkits.mplot3d import Axes3D


offset_x = 30
offset_y = 20
offset_z = 30

def dxdt(x, y, z, t): # input
    return x - y + z

def dydt(x, y, z, t): # input
    return -4 * x + y

def dzdt(x, y, z, t): # input
    return -4 * x + z


def runge_kutta_3d(x0, y0, z0, t0, t, h):
    n = int(abs(t - t0) / h)
    if t < t0: h *= -1 # !!!
    x_n = x0
    y_n = y0
    z_n = z0
    t_n = t0
    for i in range(1, n + 1):
        k1 = h * dxdt(x_n, y_n, z_n, t_n)
        m1 = h * dydt(x_n, y_n, z_n, t_n)
        p1 = h * dzdt(x_n, y_n, z_n, t_n)

        k2 = h * dxdt(x_n + k1 / 2, y_n + m1 / 2, z_n + p1 / 2, t_n + h / 2)
        m2 = h * dydt(x_n + k1 / 2, y_n + m1 / 2, z_n + p1 / 2, t_n + h / 2)
        p2 = h * dzdt(x_n + k1 / 2, y_n + m1 / 2, z_n + p1 / 2, t_n + h / 2)

        k3 = h * dxdt(x_n + k2 / 2, y_n + m2 / 2, z_n + p2 / 2, t_n + h / 2)
        m3 = h * dydt(x_n + k2 / 2, y_n + m2 / 2, z_n + p2 / 2, t_n + h / 2)
        p3 = h * dzdt(x_n + k2 / 2, y_n + m2 / 2, z_n + p2 / 2, t_n + h / 2)

        k4 = h * dxdt(x_n + k3, y_n + m3, z_n + p3, t_n + h)
        m4 = h * dydt(x_n + k3, y_n + m3, z_n + p3, t_n + h)
        p4 = h * dzdt(x_n + k3, y_n + m3, z_n + p3, t_n + h)

        x_n = x_n + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y_n = y_n + (m1 + 2 * m2 + 2 * m3 + m4) / 6
        z_n = z_n + (p1 + 2 * p2 + 2 * p3 + p4) / 6

        t_n += h
    return x_n, y_n, z_n


def phase_trajectory(koshi_x0, koshi_y0, koshi_z0, koshi_t0, runge_h, min_t, max_t, plot_step, ax):
    # must return or plot [x], [y], [z]
    x = []
    y = []
    z = []
    for t in arange(min_t, max_t, plot_step):
        rk_res = runge_kutta_3d(koshi_x0, koshi_y0, koshi_z0, koshi_t0, t, runge_h)
        # print(rk_res)
        x.append(rk_res[0])
        y.append(rk_res[1])
        z.append(rk_res[2])
    ax.plot(x, y, z)

def phase_portrait(offset_x, offset_y, offset_z, koshi_x0, koshi_y0, koshi_z0, koshi_t0, runge_h, min_t, max_t, plot_step):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x1 = koshi_x0
    y1 = koshi_y0
    z1 = koshi_z0 + offset_z

    x2 = koshi_x0
    y2 = koshi_y0
    z2 = koshi_z0 - offset_z

    x3 = koshi_x0 + offset_x
    y3 = koshi_y0
    z3 = koshi_z0

    x4 = koshi_x0 - offset_x
    y4 = koshi_y0
    z4 = koshi_z0

    x5 = koshi_x0
    y5 = koshi_y0 + offset_y
    z5 = koshi_z0

    x6 = koshi_x0
    y6 = koshi_y0 - offset_y
    z6 = koshi_z0

    phase_trajectory(x1, y1, z1, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    phase_trajectory(x2, y2, z2, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    phase_trajectory(x3, y3, z3, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    phase_trajectory(x4, y4, z4, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    phase_trajectory(x5, y5, z5, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    phase_trajectory(x6, y6, z6, koshi_t0, runge_h, min_t, max_t, plot_step, ax)
    plt.show()

# работает
if __name__ == '__main__':
    res = runge_kutta_3d(2, 7, 5, 0, 4, 0.001)
    print(res)
    phase_portrait(10, 10, 10, 2, 7, 5, 0, 0.001, -1, 1, 0.01 )
