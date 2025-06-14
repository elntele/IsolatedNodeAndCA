class Exporter:
    @staticmethod
    def save_to_txt(data, filename='resultado.txt'):
        with open(filename, 'w') as f:
            f.write(data)
