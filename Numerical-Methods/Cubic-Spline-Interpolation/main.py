from interpolationLib import *
from random import randint, shuffle
import json

def load_settings():
    with open('settings.json', 'r', encoding='utf-8') as fh:
        data_r = json.load(fh)
    fh.close()
    return data_r

def read_data_from_keyboard():
    flag = True
    x = list()
    y = list()
    params = [0.0, 0.0, 0.0]
    while (flag):
        flag = False
        x = list(map(float,input('Введите значения x через пробел\n').split()))
        if sorted(x) != x:
            print('ОШИБКА! Значения должны быть отсортированы по возрастанию!')
            flag = True
            continue
        y = list(map(float,input('Введите значения y через пробел\n').split()))
        if len(x) != len(y):
            print('ОШИБКА! Размеры списков x и y должны совпадать!')
            flag = True
            continue
        params = list(map(float,input('Введите левую и правую границы для графика, шаг построения(рекомм. <= 0.1) через пробел \n').split()))
        if params[0] > params[1] or params[2] <= 0:
            print('ОШИБКА! неверные параметры построения')
            flag = True
            continue
    return x, y, params[0], params[1], params[2]
    
def random_data():
    x_data = list(range(-10, 10+1))
    y_data = [randint(-10, 10) for _ in range(-10, 10+1)]
    return x_data, y_data

def menu():
    x = """
        0. Выход
        1. Ввести с клавиатуры
        2. Случайные значения
        3. Пример: sin(x) -10 <= x <= 10 с шагом 0.1
        4. Пример: x^2 -10 <= x <= 10 с шагом 0.1
        """
    print(x)
    pos = 0
    while True:
        pos = int(input('num-> '))
        if pos >= 0 and pos <= 4:
            break
    return pos


if __name__ == '__main__':
    settings = load_settings()
    pos = -1
    x_data = list()
    y_data = list()
    left_x = 0
    right_x = 0
    step = 1
    while (True):
        pos = menu()
        if pos == 0:
            break
        elif pos == 1:
            x_data, y_data, left_x, right_x, step = read_data_from_keyboard()
        elif pos == 2:
            x_data, y_data = random_data()
            left_x = -10
            right_x = 10
            step = 0.05
        elif pos == 3:
            x_data = list(range(-10, 10 + 1))
            y_data = [math.sin(x) for x in range(-10, 10 + 1)]
            left_x = -10
            right_x = 10
            step = 0.1
        elif pos == 4:
            x_data = list(range(-10, 10 + 1))
            y_data = [x ** 2 for x in range(-10, 10 + 1)]
            left_x = -10
            right_x = 10
            step = 0.1

        spline = make_spline(x_data, y_data)

        new_x = list(np.arange(left_x, right_x + step, step))
        new_y = list()
    
        for x in new_x:
            new_y.append(calc_new_point(spline, x))

        if settings['PRINT_DATA']: print_data(x_data, y_data)
        if settings['PRINT_SPLINE']: print_spline(spline)
        if settings['PRINT_CALC']: print_calc_points(new_x, new_y)
        calc_legend = plot_new_points(new_x, new_y, settings['PLOT_CALC_DOTS'])
        if settings['PLOT_DATA']: data_legend = plot_data(x_data, y_data)
        if settings['PLOT_CALC_DOTS'] and settings['PLOT_DATA']: plt.legend((data_legend, calc_legend), ('data', 'calc'))

        plt.gcf().canvas.set_window_title('Cubic Spline Interpolation')
        if settings['CENTRAL_AXES']:
            ax = plt.gca()
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('center')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        plt.grid()
        plt.show()
