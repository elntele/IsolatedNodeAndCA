# ------------------------------------------------------------------------------
# obs.: essa abordagem é muito lenta e foi abandonada
# PARA GERAR O EXECUTÁVEL .EXE
#
# 1. Abra o terminal na pasta:
#    use o terminal da própria ide na pasta .\core
#
# 2. Execute o comando:
#    pyinstaller --onefile --name=AlgebraicConnectivityCalculator java_connector.py
#
# 3. O executável será gerado na pasta:
#    .\core\dist
#
# 4. Para testar, coloque em uma pasta abra o terminal e rode:
#     AlgebraicConnectivityCalculator.exe 1,0,1,0,1,0 4
# 5. Ou rode direto do terminal da ide:
#    .\dist\AlgebraicConnectivityCalculator.exe 1,0,1,0,1,0 4
# 6. no projeto java coloque isso na pasta src/main/resoucers do projeto que
# chama esse código, eu coloquei dentro do projeto networkcreator.
# o metodo calculateCaFromPython da classe ExternalNetworkEvaluatorSettings
# tem o código necessário para chamar isso.
#
# ------------------------------------------------------------------------------

import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class JavaConnector:
    @staticmethod
    def evaluateCA(chromosome: list[int], num_nodes: int) -> list[float]:
        """
        Recebe um cromossomo e o número de nós.
        Retorna:
        - posição 0: conectividade algébrica (float com 6 dígitos)
        - posição 1: número de nós isolados (int)
        """
        connection_matrix_length = num_nodes * (num_nodes - 1) // 2
        connection_part = chromosome[:connection_matrix_length]

        ca = JavaConnector.calculate(connection_part, num_nodes)
        isolated_nodes = JavaConnector.detect(connection_part, num_nodes)

        return [ca, len(isolated_nodes)]

    @staticmethod
    def detect(cromossomo, num_nodes):
        degrees = [0] * num_nodes
        idx = 0
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if cromossomo[idx] != 0:
                    degrees[i] += 1
                    degrees[j] += 1
                idx += 1
        return [i for i, d in enumerate(degrees) if d == 0]

    @staticmethod
    def calculate(cromossomo, num_nodes):
        binary_cromossomo = [1 if gene > 0 else 0 for gene in cromossomo]
        adjacency = np.zeros((num_nodes, num_nodes))
        upper_idx = 0
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                adjacency[i][j] = adjacency[j][i] = binary_cromossomo[upper_idx]
                upper_idx += 1
        degree = np.diag(adjacency.sum(axis=1))
        laplacian = degree - adjacency
        eigenvalues = np.linalg.eigvalsh(laplacian)
        return round(sorted(eigenvalues)[1], 6)

if __name__ == "__main__":

    try:
        chromo_str = sys.argv[1]
        num_nodes = int(sys.argv[2])

        chromo = list(map(int, chromo_str.split(',')))

        result = JavaConnector.evaluateCA(chromo, num_nodes)

        print(f"{result[0]},{result[1]}")

    except Exception as e:
        print(f"Erro na execução: {e}")