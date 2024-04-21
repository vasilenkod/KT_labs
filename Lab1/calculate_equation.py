import math
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from Lab1.mesh import Mesh


class EquationSolver:
    def __init__(self, mesh, coefficients, initial_values):
        self.mesh = mesh
        self.coefficients = coefficients
        self.initial_values = initial_values
        self.__read_coefficients()
        self.__read_initial_value()


    def __read_coefficients(self):
        self.eps = self.coefficients.eps
        self.c = self.coefficients.c
        self.lamb = self.coefficients.lamb
        self.C0 = 5.67
        self.A = 20

    def __read_initial_value(self):
        self.initial_value = self.initial_values.values

    def QR2_func(self, t):
        return self.A * (20 + 3 * math.sin(t / 4))

    def __make_system_of_func(self, initial_value, time):
        k_ij = np.zeros((5, 5), dtype=float)
        k_ij[0][1] = self.lamb[0][1] * self.mesh.s_ij[0, 1]
        k_ij[1][2] = self.lamb[1][2] * self.mesh.s_ij[1, 2]
        k_ij[2][3] = self.lamb[2][3] * self.mesh.s_ij[2, 3]
        k_ij[3][4] = self.lamb[3][4] * self.mesh.s_ij[3, 4]

        func = np.zeros(5, dtype=float)

        func[0] = (-k_ij[0, 1] * (initial_value[0] - initial_value[1]) - \
                  self.eps[0] * self.mesh.s_i[0] * self.C0 * ((initial_value[0] / 100) ** 4)) / self.c[0]

        func[1] = (-k_ij[0, 1] * (initial_value[1] - initial_value[0]) - \
                  k_ij[1, 2] * (initial_value[1] - initial_value[2]) - \
                  self.eps[1] * self.mesh.s_i[1] * self.C0 * ((initial_value[1] / 100) ** 4) + \
                  self.QR2_func(time)) / self.c[1]

        func[2] = (-k_ij[1, 2] * (initial_value[2] - initial_value[1]) - \
                  k_ij[2, 3] * (initial_value[2] - initial_value[3]) - \
                  self.eps[2] * self.mesh.s_i[2] * self.C0 * ((initial_value[2] / 100) ** 4)) / self.c[2]

        func[3] = (-k_ij[2, 3] * (initial_value[3] - initial_value[2]) - \
                  k_ij[3, 4] * (initial_value[3] - initial_value[4]) - \
                  self.eps[3] * self.mesh.s_i[3] * self.C0 * ((initial_value[3] / 100) ** 4)) / self.c[3]

        func[4] = (-k_ij[3, 4] * (initial_value[4] - initial_value[3]) - \
                  self.eps[4] * self.mesh.s_i[4] * self.C0 * ((initial_value[4] / 100) ** 4)) / self.c[4]

        return func

    def solve_equatuon(self, end_time, points):
        time = np.linspace(0, end_time, points)
        ode_sol = odeint(self.__make_system_of_func, self.initial_value, time)
        return time, ode_sol

