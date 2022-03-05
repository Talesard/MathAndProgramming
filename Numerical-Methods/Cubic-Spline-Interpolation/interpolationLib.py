import matplotlib.pyplot as plt
import numpy as np
import math


class SplineDoesntExistYet(Exception):
    pass
      
def plot_data(x_data, y_data):
    data_leg = plt.scatter(x_data, y_data, c='green')
    return data_leg

def plot_new_points(x_points, y_points, flag):
    if flag: calc_leg = plt.scatter(x_points, y_points, c='deeppink')
    else: calc_leg = None
    # the calculated values are connected by a line
    plt.plot(x_points, y_points)
    return calc_leg

def print_data(x_data, y_data):
    print('============= DATA =============')
    for i in range(len(x_data)):
        print(x_data[i], y_data[i], sep='\t')
    print('================================')

def print_spline(spline):
    print('\n\n============ SPLINE =============')
    for i in range(1, len(spline)):
        print(spline[i])
    print('=================================')

def print_calc_points(calc_x, calc_y):
    print('\n\n============= CALC =============')
    for i in range(len(calc_x)):
        print(calc_x[i], calc_y[i], sep='\t')
    print('================================')   

# returns coeffs for all spline - list of dictionaries(a,b,c,d,x), 
# where x is needed to select the spline
def make_spline(x_data, y_data):
    n = len(x_data)

    spline = [{'a': y_data[i], 'b': 0, 'c': 0, 'd': 0, 'x': x_data[i]} for i in range(0, n)]

    # forward 
    alpha = [0] * (n - 1)
    beta  = [0] * (n - 1)

    for i in range(1, n - 1):
        hi  = x_data[i] - x_data[i - 1]
        hi_next = x_data[i + 1] - x_data[i]
        A = hi
        C = 2.0 * (hi + hi_next)
        B = hi_next
        F = 6.0 * ((y_data[i + 1] - y_data[i]) / hi_next - (y_data[i] - y_data[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z

    # reverse
    for i in range(n - 2, 0, -1):
        spline[i]['c'] = alpha[i] * spline[i + 1]['c'] + beta[i]

    for i in range(n - 1, 0, -1):
        hi = x_data[i] - x_data[i - 1]
        spline[i]['d'] = (spline[i]['c'] - spline[i - 1]['c']) / hi
        spline[i]['b'] = hi * (2.0 * spline[i]['c'] + spline[i - 1]['c']) / 6.0 + (y_data[i] - y_data[i - 1]) / hi

    # fix coeffs
    for i in range(len(spline)):
        spline[i]['c'] /= 2
        spline[i]['d'] /= 6
    return spline

# returns f(x), where f is selected spline
def calc_new_point(spline, x):
    if not spline:
        raise SplineDoesntExistYet('First you need to build a spline!')
    
    n = len(spline)
    spl = None
    
    if x <= spline[0]['x']: spl = spline[1]
    elif x >= spline[n-1]['x']: spl = spline[n-1]
    else:
        for i in range(1, n):
            if x > spline[i - 1]['x'] and x <= spline[i]['x']:
                spl = spline[i]
                break

    f = spl['a'] + spl['b'] * (x - spl['x']) + spl['c'] * ((x - spl['x']) ** 2) + spl['d'] * ((x - spl['x']) ** 3)
    return f
