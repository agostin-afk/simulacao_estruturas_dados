"""
Implementação de Lista Encadeada Simples com Visualização Gráfica

Descrição:
Esta classe implementa uma lista encadeada simples com interface gráfica usando Tkinter.
Permite realizar operações básicas como inserção no início/fim, remoção, busca e limpeza,
com visualização dos nós e conexões entre eles.

Componentes Principais:
1. Classe Node: Representa um nó da lista
2. Classe ListaEncadeada: Gerencia a lista e a interface gráfica
3. Visualização horizontal dos nós com setas indicando as conexões
4. Destaque para nó selecionado em operações de busca

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox

class Node:
    """
    Classe que representa um nó da lista encadeada
    
    Atributos:
        value: Valor armazenado no nó
        next: Referência ao próximo nó
        x, y: Coordenadas para posicionamento visual
    """
    def __init__(self, value):
        self.value = value
        self.next = None
        self.x = 0  # Coordenada x para desenho
        self.y = 0  # Coordenada y para desenho

class ListaEncadeada:
    """
    Classe que implementa uma lista encadeada com visualização gráfica
    
    Atributos:
        parent_frame: Frame do Tkinter para conter a visualização
        head: Primeiro nó da lista
        selected_node: Nó selecionado para destaque visual
        canvas: Área de desenho para visualização
        control_frame: Área para controles (entrada e botões)
        status: Barra de status para mensagens
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa a lista encadeada e a interface gráfica
        
        Parâmetros:
            parent_frame: Frame do Tkinter para renderização
        """
        self.parent_frame = parent_frame
        self.head = None  # Lista inicia vazia
        self.selected_node = None  # Nenhum nó selecionado inicialmente
        
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
        tk.Button(self.control_frame, text="Inserir Início", command=self.insert_start_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Inserir Fim", command=self.insert_end_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Remover", command=self.remove_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Buscar", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_list).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Lista Vazia", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Desenha a lista inicial
        self.visualize_list()

    def on_resize(self, event):
        """Redesenha a lista ao redimensionar o canvas"""
        self.visualize_list()

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def insert_start_gui(self):
        """Insere valor no início da lista"""
        try:
            value = self.entry.get()
            if value:
                self.insert_start(value)
                self.visualize_list()
                self.status.config(text=f"Inserido no início: {value}")
                self.entry.delete(0, tk.END)  # Limpa o campo de entrada
            else:
                messagebox.showwarning("Aviso", "Digite um valor para inserir")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def insert_end_gui(self):
        """Insere valor no final da lista"""
        try:
            value = self.entry.get()
            if value:
                self.insert_end(value)
                self.visualize_list()
                self.status.config(text=f"Inserido no fim: {value}")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para inserir")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def remove_gui(self):
        """Remove valor da lista, se existir"""
        try:
            value = self.entry.get()
            if value:
                if self.remove(value):
                    self.visualize_list()
                    self.status.config(text=f"Removido: {value}")
                else:
                    self.status.config(text=f"Valor {value} não encontrado")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para remover")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def search_gui(self):
        """Busca valor na lista e destaca o nó encontrado"""
        try:
            value = self.entry.get()
            if value:
                node = self.search(value)
                if node:
                    self.selected_node = node
                    self.visualize_list()
                    self.status.config(text=f"Valor {value} encontrado")
                else:
                    self.selected_node = None
                    self.visualize_list()
                    self.status.config(text=f"Valor {value} não encontrado")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para buscar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_list(self):
        """Limpa completamente a lista"""
        self.head = None
        self.selected_node = None
        self.visualize_list()
        self.status.config(text="Lista limpa")

    # ================================================================
    # OPERAÇÕES DA LISTA ENCADEADA
    # ================================================================
    
    def insert_start(self, value):
        """Insere novo nó no início da lista"""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def insert_end(self, value):
        """Insere novo nó no final da lista"""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        
        # Percorre até o último nó
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def remove(self, value):
        """
        Remove o primeiro nó com o valor especificado
        
        Retorna:
            True se removeu, False se não encontrou
        """
        # Lista vazia
        if not self.head:
            return False
        
        # Remoção do primeiro nó
        if self.head.value == value:
            self.head = self.head.next
            return True
        
        # Busca pelo nó a ser removido
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
        
        return False  # Valor não encontrado
    
    def search(self, value):
        """
        Busca um valor na lista
        
        Retorna:
            Nó contendo o valor, ou None se não encontrado
        """
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
    
    def size(self):
        """Retorna o número de nós na lista"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_list(self):
        """Renderiza a representação visual da lista encadeada"""
        self.canvas.delete("all")  # Limpa o canvas
        
        # Mostra mensagem se a lista estiver vazia
        if not self.head:
            self.canvas.create_text(
                self.canvas.winfo_width()/2, 
                self.canvas.winfo_height()/2, 
                text="Lista Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        
        # Obtém dimensões atuais do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Configurações de desenho
        node_radius = min(30, canvas_width // 20)  # Raio do nó
        spacing = min(80, canvas_width // 10)      # Espaçamento entre nós
        
        # Posição inicial (centralizada horizontalmente)
        x = canvas_width / 2 - ((self.size() - 1) * spacing) / 2
        y = canvas_height / 2
        
        # Percorre todos os nós para desenhá-los
        current = self.head
        while current:
            # Cor do nó: destaque se selecionado
            fill_color = "lightgreen" if current == self.selected_node else "lightblue"
            
            # Desenha o nó (círculo)
            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=fill_color, outline="black", width=2
            )
            
            # Valor do nó
            self.canvas.create_text(
                x, y, 
                text=str(current.value), 
                font=("Arial", min(12, node_radius//2), "bold")
            )
            
            # Desenha seta para o próximo nó, se existir
            if current.next:
                self.canvas.create_line(
                    x + node_radius, y,
                    x + spacing - node_radius, y,
                    arrow=tk.LAST, width=2  # Seta no final da linha
                )
            
            # Armazena coordenadas para possível uso futuro
            current.x = x
            current.y = y
            
            # Avança para o próximo nó
            current = current.next
            x += spacing  # Move para a próxima posição horizontal