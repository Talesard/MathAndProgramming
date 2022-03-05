from methods import *
import time

def hello():
    print("""
    В этой программе сравниваются численные методы решения СЛАУ:
        1. Метод Крамера
        2. Метод Гаусса
        3. Метод простых итераций
        4. Метод Зейделя
        5. Метод верхних релаксаций
        6. Метод Жордана-Гаусса
    """)

def userInput():
    print('Ax=b')
    n = int(input('Введите число неизвестных\n'))
    print('Введите матрицу (A) (без правой части)')
    tmpM = []
    for i in range(0, n):
        tmpM.append(list(map(float,input(f'Введите строку #{i+1}\n').split())))
    Matrix = np.array(tmpM)
    b = np.array(list(map(float,input(f'Введите свободные члены (b) (через пробел)\n').split())))
    return Matrix, b

if __name__ == '__main__':
    np.seterr(all='ignore')
    hello()
    while True:
        print("""\n
        0. Выход
        1. Запустить встроенные тесты   
        2. Ввести с клавиатуры
        """)

        num = int(input('пункт->'))

        if num == 2:
            Matrix, b = userInput()

            print('A:\n', Matrix)
            print('b:\n', b)

            t0 = time.time()
            resCramer = Cramer(Matrix, b)
            timeCramer = time.time() - t0
            t0 = time.time()
            resGauss = Gauss(Matrix, b)
            timeGauss = time.time() - t0
            t0 = time.time()
            resSimpleIter = SimpleIterations(Matrix, b, 0.0001, 100)
            timeSimpleIter = time.time() - t0
            t0 = time.time()
            resSeidel = Seidel(Matrix, b, 0.0001, 100)
            timeSeidel = time.time() - t0
            t0 = time.time()
            resUpRelax = UpperRelaxations(Matrix, b, 1.5, 0.0001, 100)
            timeUpRelax = time.time() - t0
            t0 = time.time()
            resGaussJordan = GaussJordan(Matrix, b)
            timeGaussJordan = time.time() - t0

            print('\n\nРезультаты:')
            print(f'Метод Крамера, time: {timeCramer}\n', resCramer)
            print(f'Метод Гаусса, time: {timeGauss}\n', resGauss)
            print(f'Метод простых итераций, time: {timeSimpleIter}\n', resSimpleIter)
            print(f'Метод Зейделя, time: {timeSeidel}\n', resSeidel)
            print(f'Метод верхних релаксаций, time: {timeUpRelax}\n', resUpRelax)
            print(f'Метод Жордана-Гаусса, time: {timeGaussJordan}\n', resGaussJordan)
        
        elif num == 1:
            N = int(input('Введите размерность системы: '))
            Matrix, b = randomSystem(N)
            if N <= 9:
                t0 = time.time()
                resCramer = Cramer(Matrix, b)
                timeCramer = time.time() - t0
            else:
                print('При N > 9 Крамер работает крайне медленно')
                resCramer = None
                timeCramer = '> 60 секунд'
            t0 = time.time()
            resGauss = Gauss(Matrix, b)
            timeGauss = time.time() - t0
            t0 = time.time()
            resSimpleIter = SimpleIterations(Matrix, b, 0.0001, 100, checkdiag=False)
            timeSimpleIter = time.time() - t0
            t0 = time.time()
            resSeidel = Seidel(Matrix, b, 0.0001, 100, checkdiag=False)
            timeSeidel = time.time() - t0
            t0 = time.time()
            resUpRelax = UpperRelaxations(Matrix, b, 1.5, 0.0001, 100, checkdiag=False)
            timeUpRelax = time.time() - t0
            t0 = time.time()
            resGaussJordan = GaussJordan(Matrix, b)
            timeGaussJordan = time.time() - t0
            print('\n\nРезультаты:')
            # print(f'Метод Крамера, time: {timeCramer}\n', resCramer)
            # print(f'Метод Гаусса, time: {timeGauss}\n', resGauss)
            # print(f'Метод простых итераций, time: {timeSimpleIter}\n', resSimpleIter)
            # print(f'Метод Зейделя, time: {timeSeidel}\n', resSeidel)
            # print(f'Метод верхних релаксаций, time: {timeUpRelax}\n', resUpRelax)
            # print(f'Метод Жордана-Гаусса, time: {timeGaussJordan}\n', resGaussJordan)
            print(f'Метод Крамера, time: {timeCramer}\n')
            print(f'Метод Гаусса, time: {timeGauss}\n')
            print(f'Метод простых итераций, time: {timeSimpleIter}\n')
            print(f'Метод Зейделя, time: {timeSeidel}\n')
            print(f'Метод верхних релаксаций, time: {timeUpRelax}\n')
            print(f'Метод Жордана-Гаусса, time: {timeGaussJordan}\n')
        
        elif num == 0:
            break
