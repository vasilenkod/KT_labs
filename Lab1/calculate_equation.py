import scipy.integrate

from Lab1.mesh import Mesh
import json
from scipy.integrate import odeint

class EquationSolver:
    def __init__(self, filename):
        self.mesh = Mesh(filename)

        with open('coeff.json') as coeff:
            data = json.load(coeff)
            self.eps = data['eps']
            self.c = data['c']
            self.lamb = data['lambda']

        self.C0 = 5.67
        self.A = 0.1
        self.QTC = self.mesh.s_ij * self.lamb
        self.QE = self.C0 * self.eps * self.mesh.s_i
        self.QR = [0, self.A, 0, 0, 0]

        self.T = None

    def solve(self):
        odeint()

