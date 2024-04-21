import sys

import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Lab1.calculate_equation import EquationSolver
from Lab1.initial_values import InitialValues
from Lab1.mesh import Mesh
from Lab1.coefficients import Coefficients


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Read data")
        self.setGeometry(100, 100, 500, 400)

        self.model_filename = None
        self.coefficients_filename = None
        self.initial_value_filename = None

        self.model_filename = None
        self.coefficients_filename = None
        self.initial_value_filename = None

        self.create_toolbar()

        self.plot_button = QPushButton("Draw plot")
        self.plot_button.clicked.connect(self.draw_plot)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_button)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")

        action = QAction("Read coefficients", self)
        action.triggered.connect(self.choose_coefficients)
        toolbar.addAction(action)

        action = QAction("Read model", self)
        action.triggered.connect(self.choose_model)
        toolbar.addAction(action)

        action = QAction("Read initial values", self)
        action.triggered.connect(self.choose_initial_values)
        toolbar.addAction(action)

        action = QAction("Save results", self)
        action.triggered.connect(self.save_results)
        toolbar.addAction(action)


    def choose_coefficients(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select coefficients file', '', 'Coefficients Files (*.json)')

        if filename:
            self.coefficients_filename = filename
            print('Opened coefficients file:', self.coefficients_filename)

        self.coefficients = Coefficients(filename)

    def choose_initial_values(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select initial values file', '', 'Initial Values Files (*.json)')

        if filename:
            self.initial_values_filename = filename
            print('Opened initial values file:', self.initial_values_filename)

        self.initial_values = InitialValues(filename)
        print(self.initial_values.values)


    def choose_model(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select model file', '', 'Model Files (*.obj)')

        if filename:
            self.model_filename = filename
            print('Model file is selected:', self.model_filename)
            self.mesh = Mesh(filename)

    def save_results(self):
        directory_name = QFileDialog.getExistingDirectory(self, 'Select Directory for saving results')

        if directory_name:
            self.directory_path = directory_name

    def draw_plot(self):
        self.time = 100
        self.points = 1001

        solver = EquationSolver(self.mesh, self.coefficients, self.initial_values)
        time, ode_sol = solver.solve_equatuon(self.time, self.points)

        np.savetxt(self.directory_path + '/' + 'results.csv', np.column_stack([time, ode_sol]),
                   delimiter=",", fmt='%10.5f')

        ax = self.figure.add_subplot(111)
        ax.plot(time, ode_sol)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
