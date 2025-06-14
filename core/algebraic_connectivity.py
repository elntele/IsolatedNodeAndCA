import numpy as np


class AlgebraicConnectivityCalculator:
    @staticmethod
    def calculate(cromossomo, num_nodes):
        # Converte o cromossomo para binário: 1 se alelo > 0, 0 se alelo == 0
        binary_cromossomo = [1 if gene > 0 else 0 for gene in cromossomo]
        adjacency = np.zeros((num_nodes, num_nodes))
        upper_idx = 0
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                adjacency[i][j] = adjacency[j][i] = binary_cromossomo[upper_idx]
                upper_idx += 1
        degree = np.diag(adjacency.sum(axis=1))
        laplacian = degree - adjacency
        eigenvalues = np.linalg.eigvalsh(laplacian)
        return round(sorted(eigenvalues)[1], 6)
