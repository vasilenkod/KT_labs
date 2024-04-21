import sys

import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel
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

        self.setWindowTitle("Equation solution")
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

        self.time_input_label = QLabel("Enter a time:")

        self.time_input_field = QLineEdit()

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.time_input)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()

        layout.addWidget(self.time_input_label)
        layout.addWidget(self.time_input_field)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.plot_button)


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

    def time_input(self):
        self.figure.clear()
        time_str = self.time_input_field.text()
        try:
            time = int(time_str)
            self.time = time
        except ValueError:
            print("Error: Unable to convert text into int")


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
        points = self.time * 10 + 1

        solver = EquationSolver(self.mesh, self.coefficients, self.initial_values)
        time, ode_sol = solver.solve_equatuon(self.time, points)

        np.savetxt(self.directory_path + '/' + 'results.csv', np.column_stack([time, ode_sol]),
                   delimiter=",", fmt='%10.5f')

        ax = self.figure.add_subplot(111)
        self.figure.xla

        ax.plot(time, ode_sol[:, 0], color='brown', label="T_1(t)")
        ax.plot(time, ode_sol[:, 1], color='red', label="T_2(t)")
        ax.plot(time, ode_sol[:, 2], color='orange', label="T_3(t)")
        ax.plot(time, ode_sol[:, 3], color='green', label="T_4(t)")
        ax.plot(time, ode_sol[:, 4], color='blue', label="T_5(t)")
        ax.legend()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
