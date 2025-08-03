"""
Implementação de Tabela Hash com Visualização Gráfica

Descrição:
Esta classe implementa uma tabela hash com tratamento de colisões por encadeamento,
com interface gráfica usando Tkinter. Permite inserir, buscar e remover itens, além de
visualizar a estrutura completa da tabela hash.

Componentes Principais:
1. Estrutura de dados: Lista de listas para armazenar os buckets
2. Função hash: Utiliza SHA-256 para distribuição uniforme
3. Interface gráfica com visualização dos buckets e itens
4. Destaque visual para operações de busca
5. Informações de capacidade e carga

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox
import hashlib

class HashTable:
    """
    Classe que implementa uma tabela hash com visualização gráfica
    
    Atributos:
        parent_frame: Frame do Tkinter onde será renderizada a tabela
        capacity: Capacidade inicial da tabela (número de buckets)
        table: Estrutura de dados para armazenar os itens (lista de listas)
        selected_bucket: Bucket selecionado para destaque visual
        selected_item: Índice do item selecionado para destaque visual
        canvas: Área de desenho para visualização da tabela
        control_frame: Área para controles (entrada e botões)
        status: Barra de status para mensagens
    """
    
    def __init__(self, parent_frame, capacity=10):
        """
        Inicializa a tabela hash e a interface gráfica
        
        Parâmetros:
            parent_frame: Frame do Tkinter para conter a visualização
            capacity: Capacidade inicial da tabela hash (padrão=10)
        """
        self.parent_frame = parent_frame
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # Tabela vazia
        self.selected_bucket = None   # Nenhum bucket selecionado inicialmente
        self.selected_item = None     # Nenhum item selecionado inicialmente
        
        # Configuração da área de desenho
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)  # Redesenha ao redimensionar
        
        # Área de controles
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        # Campo de entrada para chaves
        self.entry = tk.Entry(self.control_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        # Botões de operações
        tk.Button(self.control_frame, text="Inserir", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Buscar", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Remover", command=self.remove_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_table).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Tabela Hash Vazia", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Desenha a tabela inicial
        self.visualize_table()

    def on_resize(self, event):
        """Redesenha a tabela ao redimensionar o canvas"""
        self.visualize_table()
    
    def hash_function(self, key):
        """
        Calcula o índice do bucket para uma chave usando SHA-256
        
        Parâmetros:
            key: Chave a ser hasheada (string ou inteiro)
            
        Retorna:
            Índice do bucket (0 a capacidade-1)
        """
        if isinstance(key, int):
            key = str(key)
        # Converte a chave para hash SHA-256 e aplica módulo pela capacidade
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.capacity

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def insert_gui(self):
        """Insere chave da entrada na tabela hash"""
        try:
            key = self.entry.get()
            if key:
                # Valor arbitrário associado à chave
                value = f"Valor({key})"  
                self.insert(key, value)
                self.visualize_table()
                self.status.config(text=f"Inserido: {key} → {value}")
                self.entry.delete(0, tk.END)  # Limpa a entrada
            else:
                messagebox.showwarning("Aviso", "Digite uma chave para inserir")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def search_gui(self):
        """Busca chave na tabela e destaca o item encontrado"""
        try:
            key = self.entry.get()
            if key:
                value, bucket_idx, item_idx = self.search(key)
                if value is not None:
                    # Atualiza seleção e redesenha
                    self.selected_bucket = bucket_idx
                    self.selected_item = item_idx
                    self.visualize_table()
                    self.status.config(text=f"Encontrado: {key} → {value} (Bucket {bucket_idx})")
                else:
                    # Remove seleção se não encontrado
                    self.selected_bucket = None
                    self.selected_item = None
                    self.visualize_table()
                    self.status.config(text=f"Chave {key} não encontrada")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite uma chave para buscar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def remove_gui(self):
        """Remove chave da tabela, se existir"""
        try:
            key = self.entry.get()
            if key:
                if self.remove(key):
                    self.visualize_table()
                    self.status.config(text=f"Removido: {key}")
                else:
                    self.status.config(text=f"Chave {key} não encontrada")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite uma chave para remover")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_table(self):
        """Limpa completamente a tabela hash"""
        self.table = [[] for _ in range(self.capacity)]
        self.selected_bucket = None
        self.selected_item = None
        self.visualize_table()
        self.status.config(text="Tabela Hash limpa")

    # ================================================================
    # OPERAÇÕES DA TABELA HASH
    # ================================================================
    
    def insert(self, key, value):
        """
        Insere um par chave-valor na tabela
        
        Parâmetros:
            key: Chave do item
            value: Valor associado à chave
            
        Observação:
            Se a chave já existe, atualiza o valor
        """
        index = self.hash_function(key)
        # Verifica se chave já existe no bucket
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                # Atualiza valor existente
                self.table[index][i] = (key, value)
                return
        # Adiciona novo item no final do bucket
        self.table[index].append((key, value))
    
    def search(self, key):
        """
        Busca uma chave na tabela
        
        Parâmetros:
            key: Chave a ser buscada
            
        Retorna:
            (valor, índice_bucket, índice_item) se encontrado
            (None, -1, -1) se não encontrado
        """
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                return v, index, i
        return None, -1, -1
    
    def remove(self, key):
        """
        Remove uma chave da tabela
        
        Parâmetros:
            key: Chave a ser removida
            
        Retorna:
            True se a chave foi removida, False se não foi encontrada
        """
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]  # Remove o item
                return True
        return False

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_table(self):
        """Renderiza a tabela hash no canvas"""
        self.canvas.delete("all")  # Limpa o canvas
        
        # Obtém dimensões atuais do canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Define valores padrão se o canvas for muito pequeno
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 500
        
        # Configurações de desenho
        bucket_width = min(100, canvas_width // (self.capacity + 1))
        bucket_height = 80
        vertical_spacing = 20
        start_x = (canvas_width - (self.capacity * (bucket_width + 10))) / 2
        start_y = 50
        
        # Desenha cada bucket
        for i in range(self.capacity):
            x = start_x + i * (bucket_width + 10)  # Posição horizontal
            y = start_y
            
            # Cor do bucket: destaque se selecionado
            bucket_color = "lightgreen" if i == self.selected_bucket else "lightgray"
            self.canvas.create_rectangle(
                x, y,
                x + bucket_width, y + bucket_height,
                fill=bucket_color, outline="black", width=2
            )
            
            # Rótulo do bucket
            self.canvas.create_text(
                x + bucket_width/2, y - 15,
                text=f"Bucket {i}", font=("Arial", 10)
            )
            
            # Desenha os itens dentro do bucket
            item_y = y + 10
            for j, (key, value) in enumerate(self.table[i]):
                # Cor do item: destaque se selecionado
                item_color = "gold" if (i == self.selected_bucket and j == self.selected_item) else "lightblue"
                
                # Retângulo do item
                self.canvas.create_rectangle(
                    x + 5, item_y,
                    x + bucket_width - 5, item_y + 20,
                    fill=item_color, outline="black", width=1
                )
                
                # Texto do item (chave:valor)
                self.canvas.create_text(
                    x + bucket_width/2, item_y + 10,
                    text=f"{key}:{value}", 
                    font=("Arial", min(9, bucket_width//12))  # Tamanho adaptativo
                )
                
                item_y += 25  # Espaçamento vertical entre itens
            
            # Símbolo para bucket vazio
            if not self.table[i]:
                self.canvas.create_text(
                    x + bucket_width/2, y + bucket_height/2,
                    text="∅",  # Símbolo de conjunto vazio
                    font=("Arial", 24), 
                    fill="gray"
                )
        
        # Rodapé com informações da tabela
        total_items = sum(len(b) for b in self.table)
        self.canvas.create_text(
            canvas_width/2, canvas_height - 20,
            text=f"Capacidade: {self.capacity} | Itens: {total_items}",
            font=("Arial", 10)
        )