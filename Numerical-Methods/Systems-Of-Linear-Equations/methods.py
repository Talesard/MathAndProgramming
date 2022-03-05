import numpy as np
import copy as cp
import math

def specialSystem(n):
    Matrix = np.zeros((n,n))
    b = np.zeros(n)
    k = 2
    d = 1
    for i in range(n):
        for j in range(n):
            if i == j:
                Matrix[i, j] = d
                d+=1
            else:
                Matrix[i, j] = k
                k+=1
        b[i] = np.sum(Matrix[i])
    return Matrix, b

def randomSystem(n):
    M = np.random.randint(1, 10, (n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i][j] += n * 11
    b = np.random.randint(1, 10, (n))
    return M, b

# ======================== Cramer ======================== #
def determinant(Matrix):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    elif n == 1:
        return Matrix
    else:
        if n == 2:
            return Matrix[0][0]*Matrix[1][1]-Matrix[0][1]*Matrix[1][0]
        else:
            det = 0
            for i in range(n):
                submatrix = Matrix[1:, :]
                submatrix = np.delete(submatrix, i, 1)
                det += ((-1)**i)*Matrix[0][i]*determinant(submatrix)
    return det

def Cramer(Matrix, b):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    delta = determinant(Matrix)
    if delta == 0:
        print("Det = 0 in Cramer!")
        return None
    else:
        res = list()
        for i in range(n):
            tmp_matr = cp.copy(Matrix)
            tmp_matr[:, i] = b
            delta_i = determinant(tmp_matr)
            x = delta_i / delta
            res.append(x)
    return res
# ======================== ====== ======================== #


# ======================== Gauss ========================= #
def Gauss(Matrix, b):
    
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None

    Matrix = Matrix.tolist()
    b = b.tolist()
    column = 0
    while(column < len(b)):
   
        current_row = None
        for r in range(column, len(Matrix)):
            if current_row is None or abs(Matrix[r][column]) > abs(Matrix[current_row][column]):
                current_row = r
        if current_row is None:
            return None
   
        if current_row != column:
            # меняем местами
            Matrix[current_row], Matrix[column] = Matrix[column], Matrix[current_row]
            b[current_row], b[column] = b[column], b[current_row]
        
        # делим строку на число
        b[column] /= Matrix[column][column]
        Matrix[column] = [a / Matrix[column][column] for a in Matrix[column]]
       
        for r in range(column+1, len(Matrix)):
            # остальные строки + строка*коэфф
            b[r] += b[column] * (-Matrix[r][column])
            Matrix[r] = [(a + k * (-Matrix[r][column])) for a,k in zip(Matrix[r], Matrix[column])]
       
        column += 1
    res = [0 for b in b]
    #res = np.zeros(n)
    # ОБРАТНЫЙ ХОД
    for i in range(len(b)-1, -1, -1):
        res[i] = b[i] - sum(x*a for x,a in zip(res[(i+1):], Matrix[i][(i+1):]))

    return res
# ======================== ====== ======================== #


# ================== Simple Iterations =================== #
def CheckDiagonalDominance(Matrix):
    n = Matrix.shape[0]
    for i in range(0, n):
        sm = 0
        for j in range(0, n):
            if i != j:
                sm+=abs(Matrix[i][j])
        if abs(Matrix[i][i]) < sm:
            return False
    return True

def CheckWithEpsilon(x_prev, x_curr, eps):
    # расстояние межу векторами < эпсилон
    n = x_prev.shape[0]
    sm = 0.0
    for i in range(0, n):
        sm += (x_prev[i] - x_curr[i]) ** 2
    sm = math.sqrt(sm)
    if sm < eps:
        return True
    else:
        return False

def SimpleIterations(Matrix, b, epsilon, maxiter, checkdiag=True):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    if checkdiag:
        if (not CheckDiagonalDominance(Matrix)):
            print("The matrix does not have diagonal predominance. This method doesn't work")
            return None
    
    M = np.zeros((n,n))
    x_curr = np.zeros(n)
    x_next = np.zeros(n)
    iter_counter = 0

    for i in range(0, n):
        for j in range(0, n):
            if i!=j:
                M[i][j] = -Matrix[i][j] / Matrix[i][i]
            else:
                M[i][j] = 0
        x_next[i] = b[i] / Matrix[i][i]
    
    beta = x_next
    x_next = cp.copy(b)
    while True:
        x_curr = x_next
        x_next = np.dot(M, x_curr) + beta
        iter_counter+=1
        if CheckWithEpsilon(x_curr, x_next, epsilon) or iter_counter > maxiter-1:
            break
    return x_next
# ================== ====== ========== =================== #


# ======================== Seidel ======================== #
def Seidel(Matrix, b, epsilon, maxiter, checkdiag=True):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    if checkdiag:
        if (not CheckDiagonalDominance(Matrix)):
            print("The matrix does not have diagonal predominance. This method doesn't work")
            return None
    
    M = np.zeros((n,n))
    x_curr = np.zeros(n)
    x_next = np.zeros(n)
    iter_counter = 0

    for i in range(0, n):
        for j in range(0, n):
            if i!=j:
                M[i][j] = -Matrix[i][j] / Matrix[i][i]
            else:
                M[i][j] = 0
        x_next[i] = b[i] / Matrix[i][i]
    
    beta = cp.copy(x_next)
    x_next = np.zeros(n)
    while True:
        x_curr = cp.copy(x_next)
        for i in range(0, n):
            sm = 0
            if i > 0:
                x_curr[i] = x_next[i]
            for j in range(0, n):
                sm += M[i][j] * x_curr[j]
            x_next[i] = sm + beta[i]
        iter_counter+=1
        if CheckWithEpsilon(x_curr, x_next, epsilon) or iter_counter > maxiter-1:
            break
    return x_next
# ======================== ====== ======================== #


# ======================== Relax ======================== #
def UpperRelaxations(Matrix, b, omega, epsilon, maxiter, checkdiag=True):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    if checkdiag:
        if (not CheckDiagonalDominance(Matrix)):
            print("The matrix does not have diagonal predominance. This method doesn't work")
            return None

    step = 0
    first = np.zeros(b.shape)
    res = first[:]
    delta = np.linalg.norm(np.matmul(Matrix, res) - b)
    while delta > epsilon and step <= maxiter:
        for i in range(Matrix.shape[0]):
            tmp = 0.0
            for j in range(Matrix.shape[1]):
                if j != i:
                    tmp += Matrix[i, j] * res[j]
            res[i] = (1 - omega) * res[i] + (omega / Matrix[i, i]) * (b[i] - tmp)
        delta = np.linalg.norm(np.matmul(Matrix, res) - b)
        step += 1
    return res
# ======================== ===== ======================== #

# ======================== Gauss-Jordan ======================== #
def GaussJordan(Matrix, b):
    n, m = Matrix.shape
    if n != m:
        print('The matrix is not square!')
        return None
    m,n=Matrix.shape
    tmpMatr=np.zeros((m,n+1))
    tmpMatr[:m,:n]=Matrix
    tmpMatr[:,m]=b
    for i in range(0,m-1):
        for j in range(i+1,m):
            k=(-1)*tmpMatr[j,i]/tmpMatr[i,i]
            tmp=tmpMatr[i,:]*k
            tmpMatr[j,:]=tmpMatr[j,:]+tmp
    for i in range(m-1,0,-1):
        for j in range(i-1,-1,-1):
            k=(-1)*tmpMatr[j,i]/tmpMatr[i,i]
            tmp=tmpMatr[i,:]*k
            tmpMatr[j,:]=tmpMatr[j,:]+tmp
    for i in range(0,m):
        tmpMatr[i,:]=tmpMatr[i,:]/tmpMatr[i,i]
    return tmpMatr[:,n]
# ======================== ============ ======================== #
