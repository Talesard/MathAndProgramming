import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import math
def f(x, x_points, y_points):
    tck = interpolate.splrep(x_points, y_points)
    return interpolate.splev(x, tck)

def interpolate_and_plot(x_points, y_points, step=1):
    new_y = list()
    new_x = list()
    left = min(x_points)
    right = max(x_points) + step
    for i in np.arange(left, right, step):
        new_x.append(i)
        new_y.append(f(i, x_points, y_points))
        calc = plt.scatter(i, f(i, x_points, y_points), c='deeppink')
    for i in range(len(x_points)):
        data = plt.scatter(x_points[i], y_points[i], c='green')
    plt.plot(new_x, new_y)
    plt.legend((data, calc), ('data', 'calc'))
    plt.gcf().canvas.set_window_title("Cubic Spline Interpolation")
    plt.show()

        

x_points = [-19, -18, -17, -12, -4, -2, 4, 19]
# x_points = range(-10, 10)
y_points = [3, 7, -1, 5, 6, 3, 6, 0]
# y_points = list()
# for x in x_points :
#     y_points.append(math.sin(x))


interpolate_and_plot(x_points, y_points, step=0.1)
