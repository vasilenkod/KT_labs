import numpy as np


class Mesh:
    def __init__(self, file):
        self.vertices, self.faces, self.all_vertices, self.group = self.load_mesh(file)
        self.s_ij = self.calculate_sij()
        self.s_i = self.calculate_si()

    def load_mesh(self, file):
        vertices = [[]]
        faces = [[]]
        all_vertices = []
        group = 0
        with open(file, 'r') as file:
            for line in file:
                strs = line.split(" ")
                if strs[0] == "g":
                    group += 1
                    faces.append([])
                    vertices.append([])
                elif strs[0] == "f":
                    faces[group - 1].append(tuple(map(int, strs[1:-1])))
                elif strs[0] == "v":
                    vertices[group].append(tuple(map(float, strs[2:])))
                    all_vertices.append(tuple(map(float, strs[2:])))

        return vertices, faces, all_vertices, group

    def distance(self, p1, p2):
        return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

    def area(self, p1, p2, p3):
        a = self.distance(p1, p2)
        b = self.distance(p2, p3)
        c = self.distance(p3, p1)

        s = (a + b + c) / 2
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))

        return area

    def calculate_sij(self):
        s_ij = np.zeros((self.group, self.group))

        for i in range(self.group-1):
            y = []
            for vertex in self.vertices[i]:
                y.append(vertex[1])

            curr_area = 0
            max_y = np.max(y)

            for face in self.faces[i]:
                if np.min([self.all_vertices[face[0] - 1][1],
                           self.all_vertices[face[1] - 1][1],
                           self.all_vertices[face[2] - 1][1]]) == max_y:

                    curr_area += self.area(
                        self.all_vertices[face[0] - 1],
                        self.all_vertices[face[1] - 1],
                        self.all_vertices[face[2] - 1])

            s_ij[i][i + 1] = s_ij[i + 1][i] = curr_area

        return s_ij

    def calculate_si(self):
        s_i = np.zeros(self.group)

        for i in range(self.group):
            for face in (self.faces[i]):
                s_i[i] = s_i[i] + self.area(
                    self.all_vertices[face[0] - 1],
                    self.all_vertices[face[1] - 1],
                    self.all_vertices[face[2] - 1])

            if i == 0:
                s_i[i] = s_i[i] - self.s_ij[i][i + 1]
            elif i == self.group - 1:
                s_i[i] = s_i[i] - self.s_ij[i - 1][i]
            else:
                s_i[i] = s_i[i] - self.s_ij[i - 1][i] - self.s_ij[i][i + 1]
        return s_i
