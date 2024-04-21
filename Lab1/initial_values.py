import json


class InitialValues:
    def __init__(self, filename):
        with open(filename, 'r') as values:
            data = json.load(values)
            self.values = data["values"]