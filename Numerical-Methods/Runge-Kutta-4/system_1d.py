# src 1: https://www.youtube.com/watch?v=tbfmdC3arec
# src 2: https://cf.ppt-online.org/files/slide/x/xAiL34CKButWojbmz6qO8UsZQTF1SaEX9JepGc/slide-23.jpg

# it's input (diff equation)
def derivative(x, y):
    return y * (x + 1)


def runge_kutta(x0, y0, x, h):
    n = int(abs(x - x0) / h)
    if x < x0: h *= -1
    x_n = x0
    y_n = y0
    for i in range(1, n + 1):
        k1 = h * derivative(x_n, y_n)

        k2 = h * derivative(x_n + h / 2, y_n + k1 / 2)

        k3 = h * derivative(x_n + h / 2, y_n + k2 / 2)

        k4 = h * derivative(x_n + h, y_n + k3)

        y_n = y_n + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        
        x_n += h
    return y_n

if __name__ == '__main__':
    res = runge_kutta(0, 1, 1, 0.1)
    print(res)