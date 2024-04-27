from sympy import symbols, Symbol, solve, Eq, lambdify, Matrix
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

x, y, z = symbols('x y z')
k1 = Symbol("k1")
k1m = Symbol("k1m")
k2 = Symbol("k2")
k3 = Symbol("k3")
k3m = Symbol("k3m")

z = 1 - x - 2*y
f1 = k1 * z - k1m * x - k2 * z**2 * x
f2 = k3 * z**2 - k3m * y

sols = solve([Eq(f1, 0), Eq(f2, 0)], (x, k1))

x0 = sols[0][0]
k1_sol0 = sols[0][1]
x1 = sols[1][0]
k1_sol1 = sols[1][1]

x0_func = lambdify((y, k3, k3m), x0)
x1_func = lambdify((y, k3, k3m), x1)
k1_sol0_func = lambdify((y, k1m, k2, k3, k3m), k1_sol0)
k1_sol1_func = lambdify((y, k1m, k2, k3, k3m), k1_sol1)


#Пункт 1: зависимость от k1m
k1m_vals = [0.001, 0.005, 0.01, 0.015, 0.02]
k2v = 2.5
k3m_val = 0.001
k3v = 0.0032

plt.figure(figsize=(7, 25))
plt.rc('axes', titlesize=10)

y_k = np.linspace(0.001, 0.5, 100)

for i in range(len(k3m_vals)):
    x_v = x0_func(y_k, k3v, k3m_vals[i])
    k1_v = k1_sol0_func(y_k, k1m_v, k2v, k3v, k3m_vals[i])

    x_v, y_p, k1_v = zip(*[(x, y, z) for x, y, z in zip(x_v, y_k, k1_v) if 0 <= x <= 1])

    plt.subplot(5, 1, i + 1)
    plt.plot(k1_v, x_v, label='x(k1)')
    plt.plot(k1_v, y_p, label='y(k1)')
    plt.title('k_-3 =' + str(k3m_vals[i]))
    plt.legend(['x(k1)', 'y(k1)'])

plt.show()

#Пункт 2: зависимость от k3m
k1m_v = 0.01
k2v = 2.5
k3m_vals = [0.0005, 0.001, 0.002, 0.003, 0.004]
k3v = 0.0032

y_k = np.linspace(0.001, 0.5, 100)


plt.figure(figsize=(7, 25))
plt.rc('axes', titlesize=10)

for i in range(len(k3m_vals)):
    x_v = x0_func(y_k, k3v, k3m_vals[i])
    k1_v = k1_sol0_func(y_k, k1m_v, k2v, k3v, k3m_vals[i])

    x_v, y_p, k1_v = zip(*[(x, y, z) for x, y, z in zip(x_v, y_k, k1_v) if 0 <= x <= 1])

    plt.subplot(5, 1, i + 1)
    plt.plot(k1_v, x_v, label='x(k1)')
    plt.plot(k1_v, y_p, label='y(k1)')
    plt.title('k_-3 =' + str(k3m_vals[i]))
    plt.legend(['x(k1)', 'y(k1)'])

plt.show()


#Пункт 3: матрица Якоби и точки бифуркации
F = Matrix([f1, f2])
A = F.jacobian([x, y])

detA = A.det()
traceA = A.trace()

detA_func = lambdify((x, y, k1, k1m, k2, k3, k3m), detA)
traceA_func = lambdify((x, y, k1, k1m, k2, k3, k3m), traceA)

def get_biff_points(x, y, k1_vals, k1m_val, k2val, k3val, k3m_val):
    saddles = []
    hopf = []

    detA_vals = [detA_func(x[i], y[i], k1_vals[i], k1m_val, k2val, k3val, k3m_val) for i in range(len(x))]
    traceA_vals = [traceA_func(x[i], y[i], k1_vals[i], k1m_val, k2val, k3val, k3m_val) for i in range(len(x))]

    get_saddle_points(detA_vals, k1m_val, k2val, k3m_val, k3val, saddles, y)
    get_andre_hopf_points(traceA_vals, detA_vals, k1m_val, k2val, k3m_val, k3val, hopf, y)

    return saddles, hopf


def get_saddle_points(det_A, k1m_val, k2val, k3m_val, k3val, saddles, y):
    for i in range(len(y) - 1):
        if det_A[i] * det_A[i + 1] < 0 or det_A[i] == 0:
            tmp_y = y[i] - det_A[i] * (y[i + 1] - y[i]) / (det_A[i + 1] - det_A[i])
            k1_tmp = k1_sol0_func(tmp_y, k1m_val, k2val, k3val, k3m_val)
            x_tmp = x0_func(tmp_y, k3val, k3m_val)
            saddles.append((tmp_y, x_tmp, k1_tmp))


def get_andre_hopf_points(trace_A, det_A, k1m_val, k2val, k3m_val, k3val, saddles, y):
    for i in range(len(y) - 1):
        if trace_A[i] * trace_A[i + 1] < 0 or (trace_A[i] == 0 and det_A[i] < 0):
            tmp_y = y[i] - trace_A[i] * (y[i + 1] - y[i]) / (trace_A[i + 1] - trace_A[i])
            k1_tmp = k1_sol0_func(tmp_y, k1m_val, k2val, k3val, k3m_val)
            x_tmp = x0_func(tmp_y, k3val, k3m_val)
            saddles.append((tmp_y, x_tmp, k1_tmp))




k1m_v = 0.01
k2v = 2.5
k3m_vals = [0.0005, 0.001, 0.002, 0.003, 0.004]
k3v = 0.0032
y_k = np.linspace(0.0001, 0.5, 100)

plt.figure(figsize=(7, 25))
plt.rc('axes', titlesize=10)

for j in range(len(k3m_vals)):
    x_v = x0_func(y_k, k3v, k3m_vals[j])
    k1_v = k1_sol0_func(y_k, k1m_v, k2v, k3v, k3m_vals[j])

    x_v, y_p, k1_v = zip(*[(x, y, z) for x, y, z in zip(x_v, y_k, k1_v) if 0 <= x <= 1])
    saddles, hopf = get_biff_points(x_v, y_p, k1_v, k1m_v, k2v, k3v, k3m_vals[j])
    y_saddle = [saddles[i][0] for i in range(len(saddles))]
    x_saddle = [saddles[i][1] for i in range(len(saddles))]
    k1_saddle = [saddles[i][2] for i in range(len(saddles))]

    y_hopf = [hopf[i][0] for i in range(len(hopf))]
    x_hopf = [hopf[i][1] for i in range(len(hopf))]
    k1_hopf = [hopf[i][2] for i in range(len(hopf))]

    plt.subplot(5, 1, j + 1)
    plt.plot(k1_v, x_v, label='x(k1)')
    plt.plot(k1_v, y_p, label='y(k1)')

    plt.plot(k1_saddle, y_saddle, 'rs')
    plt.plot(k1_saddle, x_saddle, 'rs')

    plt.plot(k1_hopf, y_hopf, 'k*')
    plt.plot(k1_hopf, x_hopf, 'k*')

    plt.title('k_-3 =' + str(k3m_vals[j]))
    plt.xlabel('k1')
    plt.legend(['x(k1)', 'y(k1)'])

plt.show()

#решение ОДУ
k1val = 0.12
k1m_v = 0.01
k2v = 2.5
k3m_val = 0.003
k3v = 0.0032

def eval_equation(y, t):
    z = 1 - y[0] - 2 * y[1]
    eq1 = k1val * z - k1m_v * y[0] - k2v * (z ** 2) * y[0]
    eq2 = k3v * z ** 2 - k3m_val * y[1]
    return [eq1, eq2]


t = np.linspace(0, 2500, 100000)
sol = odeint(eval_equation, [0.4, 0.5], t)

plt.figure(figsize=(7, 10))
plt.rc('axes', titlesize=10)

plt.subplot(2, 1, 1)
plt.plot(t, sol[:, 0], color='red', label='x(t)')
plt.plot(t, sol[:, 1], color='green', label='y(t)')
plt.title('Решение ОДУ')
plt.xlabel('t')
plt.legend(['x(t)', 'y(t)'])

plt.subplot(2, 1, 2)
plt.plot(sol[:, 0], sol[:, 1], color='red', label='y(x)')
plt.title('Фазовое пространство')
plt.xlabel('x')
plt.ylabel('y')

plt.show()
