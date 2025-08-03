"""
Implementação de Fila (Queue) com Visualização Gráfica

Descrição:
Esta classe implementa uma estrutura de dados do tipo fila (FIFO - First In, First Out)
com interface gráfica usando Tkinter. Permite realizar operações básicas de fila (enqueue, dequeue)
e visualizar os elementos em formato de fila horizontal com indicações de entrada e saída.

Componentes Principais:
1. Estrutura de dados: Lista para armazenar os elementos
2. Visualização horizontal dos elementos enfileirados
3. Setas indicando a direção do fluxo (entrada e saída)
4. Rótulos para frente (próximo a sair) e final (último a entrar)
5. Feedback visual para operações

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox

class Fila:
    """
    Classe que implementa uma fila com visualização gráfica
    
    Atributos:
        parent_frame: Frame do Tkinter para conter a visualização
        queue: Lista para armazenar os elementos da fila
        canvas: Área de desenho para visualização
        control_frame: Área para controles (entrada e botões)
        status: Barra de status para mensagens
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa a fila e a interface gráfica
        
        Parâmetros:
            parent_frame: Frame do Tkinter para renderização
        """
        self.parent_frame = parent_frame
        self.queue = []  # Inicializa fila vazia
        
        # Configuração da área de desenho
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)  # Redesenha ao redimensionar
        
        # Área de controles
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        # Campo de entrada para valores
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        # Botões de operações
        tk.Button(self.control_frame, text="Enqueue", command=self.enqueue_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Dequeue", command=self.dequeue_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_queue).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Fila Vazia", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Desenha a fila inicial
        self.visualize_queue()

    def on_resize(self, event=None):
        """Redesenha a fila ao redimensionar o canvas"""
        self.visualize_queue()

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def enqueue_gui(self):
        """Enfileira o valor da entrada"""
        try:
            value = self.entry.get()
            if value:
                self.enqueue(value)
                self.visualize_queue()
                self.status.config(text=f"Enfileirado: {value}")
                self.entry.delete(0, tk.END)  # Limpa o campo de entrada
            else:
                messagebox.showwarning("Aviso", "Digite um valor para enfileirar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def dequeue_gui(self):
        """Desenfileira o elemento da frente"""
        if not self.queue:
            self.status.config(text="Fila vazia!")
            return
            
        try:
            value = self.dequeue()
            self.visualize_queue()
            self.status.config(text=f"Desenfileirado: {value}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_queue(self):
        """Limpa toda a fila"""
        self.queue = []
        self.visualize_queue()
        self.status.config(text="Fila limpa")

    # ================================================================
    # OPERAÇÕES DA FILA
    # ================================================================
    
    def enqueue(self, value):
        """Adiciona um elemento no final da fila"""
        self.queue.append(value)
    
    def dequeue(self):
        """Remove e retorna o elemento da frente da fila"""
        if not self.queue:
            raise IndexError("Fila vazia!")
        return self.queue.pop(0)
    
    def is_empty(self):
        """Verifica se a fila está vazia"""
        return len(self.queue) == 0
    
    def size(self):
        """Retorna o número de elementos na fila"""
        return len(self.queue)

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_queue(self):
        """Renderiza a representação visual da fila"""
        self.canvas.delete("all")  # Limpa o canvas
        
        # Obtém dimensões atuais do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Define dimensões mínimas para evitar erros
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 300
        
        # Mostra mensagem se a fila estiver vazia
        if not self.queue:
            self.canvas.create_text(
                canvas_width/2, canvas_height/2, 
                text="Fila Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        
        # Configurações de desenho
        element_width = min(80, canvas_width // 12)  # Largura do elemento
        element_height = min(60, canvas_height // 10) # Altura do elemento
        spacing = 10  # Espaçamento entre elementos
        
        # Calcula a largura total necessária
        total_width = len(self.queue) * (element_width + spacing) - spacing
        
        # Posição inicial (centralizada horizontalmente)
        start_x = (canvas_width - total_width) / 2
        start_y = canvas_height / 2
        
        # Desenha seta de entrada (lado esquerdo)
        self.canvas.create_line(
            start_x - 50, start_y, 
            start_x, start_y, 
            arrow=tk.LAST, width=2
        )
        self.canvas.create_text(
            start_x - 25, start_y - 20, 
            text="Entrada", 
            font=("Arial", 10)
        )
        
        # Desenha seta de saída (lado direito)
        end_x = start_x + total_width
        self.canvas.create_line(
            end_x, start_y, 
            end_x + 50, start_y, 
            arrow=tk.LAST, width=2
        )
        self.canvas.create_text(
            end_x + 25, start_y - 20, 
            text="Saída", 
            font=("Arial", 10)
        )
        
        # Desenha cada elemento da fila
        for i, value in enumerate(self.queue):
            x = start_x + i * (element_width + spacing)
            y = start_y
            
            # Retângulo do elemento
            self.canvas.create_rectangle(
                x, y - element_height/2,
                x + element_width, y + element_height/2,
                fill="lightblue", outline="black", width=2
            )
            
            # Valor do elemento
            self.canvas.create_text(
                x + element_width/2, y,
                text=str(value), 
                font=("Arial", min(12, element_width//6), "bold")
            )
            
            # Rótulo "Frente" para o primeiro elemento (índice 0)
            if i == 0:
                self.canvas.create_text(
                    x + element_width/2, y + element_height/2 + 15,
                    text="Frente", 
                    font=("Arial", min(9, element_width//8))
                )
            
            # Rótulo "Final" para o último elemento (índice -1)
            if i == len(self.queue) - 1:
                self.canvas.create_text(
                    x + element_width/2, y + element_height/2 + 15,
                    text="Final", 
                    font=("Arial", min(9, element_width//8))
                )