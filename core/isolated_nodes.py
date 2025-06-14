class IsolatedNodesDetector:
    @staticmethod
    def detect(cromossomo, num_nodes):
        degrees = [0] * num_nodes
        idx = 0
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                if cromossomo[idx] != 0:
                    degrees[i] += 1
                    degrees[j] += 1
                idx += 1
        return [i for i, d in enumerate(degrees) if d == 0]
