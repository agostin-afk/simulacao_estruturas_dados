"""
Implementação de Pilha com Visualização Gráfica

Descrição:
Esta classe implementa uma estrutura de dados do tipo pilha (LIFO - Last In, First Out)
com interface gráfica usando Tkinter. Permite realizar operações básicas de pilha (push, pop, top)
e visualizar os elementos em formato de pilha vertical com destaque para o topo.

Componentes Principais:
1. Estrutura de dados: Lista para armazenar os elementos
2. Visualização vertical dos elementos empilhados
3. Destaque especial para o elemento do topo
4. Seta indicadora do topo da pilha
5. Feedback visual para operações

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox

class Pilha:
    """
    Classe que implementa uma pilha com visualização gráfica
    
    Atributos:
        parent_frame: Frame do Tkinter para conter a visualização
        stack: Lista para armazenar os elementos da pilha
        canvas: Área de desenho para visualização
        control_frame: Área para controles (entrada e botões)
        status: Barra de status para mensagens
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa a pilha e a interface gráfica
        
        Parâmetros:
            parent_frame: Frame do Tkinter para renderização
        """
        self.parent_frame = parent_frame
        self.stack = []  # Inicializa pilha vazia
        
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
        tk.Button(self.control_frame, text="Push", command=self.push_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Pop", command=self.pop_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Top", command=self.top_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_stack).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Pilha Vazia", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Desenha a pilha inicial
        self.visualize_stack()

    def on_resize(self, event=None):
        """Redesenha a pilha ao redimensionar o canvas"""
        self.visualize_stack()

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def push_gui(self):
        """Empilha o valor da entrada"""
        try:
            value = self.entry.get()
            if value:
                self.push(value)
                self.visualize_stack()
                self.status.config(text=f"Empilhado: {value}")
                self.entry.delete(0, tk.END)  # Limpa o campo de entrada
            else:
                messagebox.showwarning("Aviso", "Digite um valor para empilhar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def pop_gui(self):
        """Desempilha o elemento do topo"""
        if not self.stack:
            self.status.config(text="Pilha vazia!")
            return
            
        try:
            value = self.pop()
            self.visualize_stack()
            self.status.config(text=f"Desempilhado: {value}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def top_gui(self):
        """Consulta o elemento do topo"""
        if not self.stack:
            self.status.config(text="Pilha vazia!")
            return
            
        try:
            value = self.top()
            self.status.config(text=f"Topo: {value}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_stack(self):
        """Limpa toda a pilha"""
        self.stack = []
        self.visualize_stack()
        self.status.config(text="Pilha limpa")

    # ================================================================
    # OPERAÇÕES DA PILHA
    # ================================================================
    
    def push(self, value):
        """Adiciona um elemento no topo da pilha"""
        self.stack.append(value)
    
    def pop(self):
        """Remove e retorna o elemento do topo"""
        if not self.stack:
            raise IndexError("Pilha vazia!")
        return self.stack.pop()
    
    def top(self):
        """Retorna o elemento do topo sem removê-lo"""
        if not self.stack:
            raise IndexError("Pilha vazia!")
        return self.stack[-1]
    
    def is_empty(self):
        """Verifica se a pilha está vazia"""
        return len(self.stack) == 0
    
    def size(self):
        """Retorna o número de elementos na pilha"""
        return len(self.stack)

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_stack(self):
        """Renderiza a representação visual da pilha"""
        self.canvas.delete("all")  # Limpa o canvas
        
        # Obtém dimensões atuais do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Define dimensões mínimas para evitar erros
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 300
        
        # Mostra mensagem se a pilha estiver vazia
        if not self.stack:
            self.canvas.create_text(
                canvas_width/2, canvas_height/2, 
                text="Pilha Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        
        # Configurações de desenho
        element_width = min(100, canvas_width // 6)   # Largura do elemento
        element_height = min(60, canvas_height // 10) # Altura do elemento
        spacing = 10  # Espaçamento entre elementos
        
        # Posição inicial (base da pilha)
        start_x = canvas_width / 2
        start_y = canvas_height - 50  # Começa a empilhar a partir da base
        
        # Desenha a seta indicadora do topo
        if self.stack:
            # Calcula a posição do topo
            top_y = start_y - (len(self.stack) * (element_height + spacing) + element_height/2)
            # Seta apontando para o topo
            self.canvas.create_line(
                start_x + element_width/2 + 20, top_y,
                start_x + element_width/2 + 40, top_y,
                arrow=tk.LAST, width=2
            )
            # Rótulo "Topo"
            self.canvas.create_text(
                start_x + element_width/2 + 50, top_y - 10,
                text="Topo", 
                font=("Arial", 10)
            )
        
        # Desenha cada elemento da pilha (de baixo para cima)
        for i, value in enumerate(self.stack):
            # Posição vertical do elemento
            y = start_y - i * (element_height + spacing)
            
            # Retângulo do elemento
            self.canvas.create_rectangle(
                start_x - element_width/2, y - element_height/2,
                start_x + element_width/2, y + element_height/2,
                fill="lightblue", outline="black", width=2
            )
            
            # Valor do elemento
            self.canvas.create_text(
                start_x, y,
                text=str(value), 
                font=("Arial", min(12, element_width//8), "bold")
            )
        
        # Destaca o elemento do topo com um retângulo vermelho tracejado
        if self.stack:
            top_y = start_y - (len(self.stack) * (element_height + spacing)) + element_height/2
            self.canvas.create_rectangle(
                start_x - element_width/2 - 5, top_y - element_height/2 - 5,
                start_x + element_width/2 + 5, top_y + element_height/2 + 5,
                outline="red", width=2, dash=(4, 2),
            )