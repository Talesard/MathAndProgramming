import PySimpleGUI as sg
import math
import matplotlib.pyplot as plt
import numpy as np
import time as timelib


# в этой либе гуи распологается по строкам. один список - одна строка
sg.theme('DefaultNoMoreNagging')
layout = [  # graph.png
            [sg.Image(r'clear.png', key='plot_image')], 
            [sg.Text('Длина:', size=(5, 1)), sg.Input('20', size=(8, 1)), sg.Text('Время:', size=(5, 1)), sg.Input('12', size=(8, 1)), sg.Text('', size=(5, 1)),sg.Button('Часть А'), sg.Text('(после В)', size=(10, 1))],
            [sg.Text('Шаг t:', size=(5, 1)), sg.Input('0.01', size=(8, 1)), sg.Text('Шаг x:', size=(5, 1)), sg.Input('0.4', size=(8, 1)), sg.Text('', size=(5, 1)),sg.Button('Часть В')],
            [sg.Text('ф1', size=(5, 1)), sg.Input('0.2', size=(8, 1)), sg.Text('ф2', size=(5, 1)), sg.Input('0.4', size=(8, 1)), sg.Text('', size=(5, 1)),sg.Button('Закрыть')],
            [sg.Text('b0', size=(5, 1)), sg.Input('0.02', size=(8, 1)), sg.Text('b1', size=(5, 1)), sg.Input('0.2', size=(8, 1)), sg.Text('b2', size=(5, 1)), sg.Input('0.3', size=(8, 1)), sg.Text('Время работы:', size=(25, 1), key='work_time')],
            [sg.ProgressBar(1000,orientation='h', size=(55, 20), key='br_bar')]
        ]

window = sg.Window('ЛР4 Напылов Е.И. 381806-2', layout)


# values[0] - длина
# values[1] - время
# values[2] - шаг время
# values[3] - шаг х
# values[4] - ф1
# values[5] - ф2
# values[6] - б0
# values[7] - б1
# values[8] - б2


A_result = []
B_result = []


fig, ax = plt.subplots(figsize=(6, 4))
ax.grid()
ax.plot([0], [0])
fig.savefig('graph.png')


def Source_Function_Phi(x, l, f1, f2):
    return 1/l + f1 * math.cos((math.pi*x)/l) + f2 * math.cos(2*(math.pi*x)/l)

def Source_Function_B(x, l, b0, b1, b2):
    return b0 + b1 * math.cos((math.pi*x)/l) + b2 * math.cos(2*(math.pi*x)/l)

x_list = []
phi_list = []

def Tridiagonal_Matrix_Algorithm(a, b, c, f):
    size = len(f)
    A = np.zeros(size, float)
    B = np.zeros(size, float)
    x = np.zeros(size, float)

    A[0] = -c[0]/b[0]
    B[0] = f[0]/b[0]
    
    for i in range(1, size):
        A[i] = -c[i] / (a[i] * A[i - 1] + b[i])
        B[i] = (f[i] - a[i] * B[i - 1]) / (a[i] * A[i - 1] + b[i])
    x[size-1] = B[size - 1]

    i = size - 2
    while (i > -1):
        x[i] = (A[i] * x[i + 1] + B[i])
        i -= 1
    return x

def Calc_Integral(h, f):
    res = (f[0] + f[len(f) - 1])
    for i in range(1, len(f) - 1, 2):
        res += (4 * f[i] + 2 * f[i + 1])
    return h * res / 3

view_mode = False



while True:
    event, values = window.Read(timeout = 100)
    # print(values)
    if event in (None, 'Закрыть'):
        # print('close')
        break
    if event in (None, 'Часть А'):
        # print('part A')
        if(view_mode == 0):
            ax.plot(x_list, phi_list, 'b')
            ax.plot(x_list, B_result, 'r')
            ax.plot(x_list, A_result, 'g') # linewidth=5.0
            fig.savefig('graph.png')
            window['plot_image'].update(r'graph.png')
            view_mode = 1
        else:
            # print('part A else')
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.grid()
            ax.plot(x_list, phi_list, 'b')
            ax.plot(x_list, B_result, 'r')
            fig.savefig('graph.png')
            window['plot_image'].update(r'graph.png')
            view_mode = 0

    if event in ('Часть В'):
        # print('part b')
        start_time = timelib.time()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.grid()
        fig.savefig('graph.png')
        progress_bar = window['br_bar']
        window['plot_image'].update(r'clear.png')
        try:
            l = float(values[0])
            time = float(values[1])
            tau = float(values[2])
            h = float(values[3])
            f1 = float(values[4])
            f2 = float(values[5])
            b0 = float(values[6])
            b1 = float(values[7])
            b2 = float(values[8])
        except:
            print('value parse error')
            continue
        
        if not tau / (h**2) < 0.25:
            sg.popup_error(f"tau/h^2={round(tau/(h**2), 3)}")
            continue

        count_L_segm = int(l/h) + 1
        count_T_segm = int(time/tau) + 1
        slices1 = np.zeros((count_T_segm,count_L_segm), float)
        slices2 = np.zeros((count_T_segm,count_L_segm), float)
        prbar_step = 1000/count_T_segm
        phi_list = np.zeros(count_L_segm, float)
        b_list = np.zeros(count_L_segm, float)
        
        # Вычисление значений функции и заполнение нулевого слоя сетки
        for i in range(0, count_L_segm):
            phi_list[i] = Source_Function_Phi(i*h, l, f1, f2)
            b_list[i] = Source_Function_B(i*h, l, b0, b1, b2)
            
            slices1[0][i] = phi_list[i]
            slices2[0][i] = phi_list[i]

        # Заполнение матрицы коэффициентов для метода прогонки
        k_a = np.zeros(count_L_segm, float)
        k_b = np.zeros(count_L_segm, float)
        k_c = np.zeros(count_L_segm, float)

        k_b[0] = 1.0
        k_c[0] = -1.0
        for i in range(1, count_L_segm - 1):
            k_a[i] = (tau / (h * h))
            k_b[i] = (-1 - 2*tau / (h * h))
            k_c[i] = (tau / (h * h))
        k_a[count_L_segm - 1] = -1.0
        k_b[count_L_segm - 1] = 1.0
        
        
        # Вычисление последующих слоев сетки
        for i in range(1, count_T_segm):
            
            y_func = np.zeros(count_L_segm, float) 
            
            for j in range(0, count_L_segm):
                y_func[j] = b_list[j] * slices1[i - 1][j]
            
            I = Calc_Integral(h, y_func)
            f = np.zeros(count_L_segm, float)
            right_2 = np.zeros(count_L_segm, float)
            
            
            # Вычисляем правую часть системы для прогонки
            for j in range(1, count_L_segm - 1):
                # тут было tau*tau в двух строках
                f[j] = -slices1[i - 1][j] * ((b_list[j] - I) * tau  + 1.0) #  часть B
                right_2[j] = -slices2[i - 1][j] * (b_list[j] * tau + 1.0) # часть А
        
            # Метод прогонки для системы из B
            res = Tridiagonal_Matrix_Algorithm(k_a, k_b, k_c, f) # it was fu
            for j in range(0, count_L_segm):
                slices1[i][j] = res[j]
            
            # Метод прогонки для системы из A
            res2 = Tridiagonal_Matrix_Algorithm(k_a, k_b, k_c, right_2)
            for j in range(0, count_L_segm):
                slices2[i][j] = res2[j]
            progress_bar.UpdateBar(i * prbar_step)
                
        I = Calc_Integral(h, slices2[count_T_segm - 1])
        
        B_result = np.zeros(count_L_segm, float)
        A_result = np.zeros(count_L_segm, float)
        for j in range(count_L_segm):
            A_result[j] = slices2[count_T_segm - 1][j] / I
            B_result[j] = slices1[count_T_segm - 1][j]
        
        x_list = np.zeros(count_L_segm, float)
        
        for i in range(0, count_L_segm):
            x_list[i] = i * h
        
        ax.plot(x_list, phi_list, 'b')
        ax.plot(x_list, slices1[count_T_segm - 1], 'r')
        fig.savefig('graph.png')
        window['plot_image'].update(r'graph.png')
        progress_bar.UpdateBar(1000)
        view_mode = 0
        end_time = timelib.time()
        window['work_time'].update(f'Время работы: {round(end_time - start_time, 4)} с')