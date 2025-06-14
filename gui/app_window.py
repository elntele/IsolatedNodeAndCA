import tkinter as tk
from tkinter import filedialog, scrolledtext, StringVar, Entry, Button, Frame, Label

from core.topology_loader import TopologyLoader
from core.algebraic_connectivity import AlgebraicConnectivityCalculator
from core.isolated_nodes import IsolatedNodesDetector
from utils.exporter import Exporter


class AppWindow:
    def __init__(self, root):
        self.root = root
        self.topologies = []
        self.file_path_var = StringVar()
        self.line_var = StringVar()
        self.node_count_var = StringVar()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Analisador de Topologias")
        frame = Frame(self.root, padx=10, pady=10)
        frame.pack()

        # Linha com campo + botão de seleção de arquivo
        file_frame = Frame(frame)
        file_frame.pack(pady=5)

        self.path_entry = Entry(file_frame, textvariable=self.file_path_var, width=60)
        self.path_entry.pack(side="left", padx=4)
        Button(file_frame, text="Abrir Arquivo CSV", command=self.load_csv).pack(side="left")

        # Campo para número de nós
        node_frame = Frame(frame)
        node_frame.pack(pady=2)
        Entry(node_frame, textvariable=self.node_count_var, width=5).pack(side="left", padx=(0, 6))
        Label(node_frame, text="Informe o número de nós").pack(side="left")

        # Campo para linha + botão
        line_frame = Frame(frame)
        line_frame.pack(pady=4)
        Entry(line_frame, textvariable=self.line_var, width=5).pack(side="left", padx=(0, 6))
        Button(line_frame, text="Analisar Linha", command=self.analyze_line).pack(side="left")

        # Área de saída
        self.output = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.output.pack()

        # Botões gerais
        Button(frame, text="Analisar Todas as Topologias", command=self.analyze_all).pack(pady=2)
        Button(frame, text="Salvar Resultado", command=self.save_output).pack(pady=4)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.file_path_var.set(path)
            self.topologies = TopologyLoader.load(path)
            self.output.insert("end", f"Arquivo carregado: {path}\n")

    def analyze_all(self):
        try:
            num_nodes = int(self.node_count_var.get().strip())
            tam_matriz = num_nodes * (num_nodes - 1) // 2

            for i, cromossomo_completo in enumerate(self.topologies):
                if len(cromossomo_completo) < tam_matriz:
                    self.output.insert(tk.END, f"Topo {i + 1}: dados insuficientes\n")
                    continue
                matriz_conexao = cromossomo_completo[:tam_matriz]
                result = self.analyze_topology(matriz_conexao, num_nodes)
                self.output.insert(tk.END, f"Topo {i + 1}: {result}\n")
        except ValueError:
            self.output.insert("end", "Digite um número válido de nós antes de analisar todas as topologias.\n")

    def analyze_topology(self, chrom, num_nodes):
        ca = AlgebraicConnectivityCalculator.calculate(chrom, num_nodes)
        isolated = IsolatedNodesDetector.detect(chrom, num_nodes)
        return f"CA: {ca:.4f}, Isolados: {isolated}"

    def save_output(self):
        Exporter.save_to_txt(self.output.get(1.0, tk.END))

    def analyze_line(self):
        if not self.topologies:
            self.output.insert("end", "Nenhum arquivo carregado.\n")
            return

        try:
            raw_line = self.line_var.get().strip()
            raw_nodes = self.node_count_var.get().strip()

            if not raw_line or not raw_nodes:
                self.output.insert("end", "Preencha ambos os campos: linha e número de nós.\n")
                return

            line = int(raw_line)
            num_nodes = int(raw_nodes)
            index = line - 1  # linha 1 corresponde ao índice 0

            if index < 0 or index >= len(self.topologies):
                self.output.insert("end", f"Linha inválida: {line}\n")
                return

            tam_matriz = num_nodes * (num_nodes - 1) // 2
            cromossomo_completo = self.topologies[index]

            if len(cromossomo_completo) < tam_matriz:
                self.output.insert("end", f"Dados insuficientes na linha {line}.\n")
                return

            matriz_conexao = cromossomo_completo[:tam_matriz]
            result = self.analyze_topology(matriz_conexao, num_nodes)
            self.output.insert("end", f"Topo {line}: {result}\n")

        except ValueError:
            self.output.insert("end", "Digite valores válidos (números inteiros) para linha e número de nós.\n")
