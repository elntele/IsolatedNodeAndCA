import csv

class TopologyLoader:
    @staticmethod
    def load(file_path):
        with open(file_path, newline='') as f:
            return [list(map(int, row)) for row in csv.reader(f)]
