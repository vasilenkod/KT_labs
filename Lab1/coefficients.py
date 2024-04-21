import json
class Coefficients:
    def __init__(self, filename):
        with open(filename, 'r') as coefficients:
            data = json.load(coefficients)
            self.eps = data['eps']
            self.c = data['c']
            self.lamb = data['lambda']

        self.C0 = 5.67
        self.A = 20