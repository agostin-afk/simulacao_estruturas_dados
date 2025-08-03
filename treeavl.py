"""
Implementação de Árvore AVL com Visualização Gráfica

Descrição:
Esta classe implementa uma árvore AVL (árvore binária de busca balanceada) com interface gráfica
usando Tkinter. Inclui operações básicas como inserção, remoção, busca e diferentes tipos de percurso,
com visualização em tempo real da estrutura da árvore.

Componentes Principais:
1. Classe TreeNode: Representa um nó da árvore
2. Classe AVLTree: Gerencia a lógica da árvore e a interface gráfica
3. Visualização gráfica da árvore com informações de altura
4. Operações de rotação para balanceamento
5. Diferentes métodos de percurso (in-order, pre-order, post-order, level-order)

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox

class TreeNode:
    """Classe que representa um nó da árvore AVL"""
    def __init__(self, value):
        """
        Inicializa um novo nó
        
        Parâmetros:
            value: Valor a ser armazenado no nó
            
        Atributos:
            value: Valor do nó
            left: Filho esquerdo
            right: Filho direito
            height: Altura do nó na árvore
            x, y: Coordenadas para visualização gráfica
        """
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Altura inicial do nó
        self.x = 0       # Coordenada x para desenho
        self.y = 0       # Coordenada y para desenho
        
    def __str__(self):
        """Retorna representação string do nó"""
        return str(self.value)

class AVLTree:
    """Classe principal que implementa a árvore AVL com interface gráfica"""
    def __init__(self, parent_frame):
        """
        Inicializa a visualização da árvore AVL
        
        Parâmetros:
            parent_frame: Frame do Tkinter onde será renderizada a árvore
        """
        # Configuração do frame pai e área de desenho
        self.parent_frame = parent_frame
        self.canvas = tk.Canvas(self.parent_frame, width=500, height=400, bg='white')
        self.parent_frame.pack_propagate(False)  # Impede redimensionamento automático
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Área de controles
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        self.entry = tk.Entry(self.control_frame, width=10)  # Entrada de valores
        self.entry.pack(side=tk.LEFT, padx=5)
        
        # Área de botões de percurso
        self.traversal_frame = tk.Frame(self.parent_frame)
        self.traversal_frame.pack(pady=5, fill=tk.X)   
        
        # Configuração de eventos e estado inicial
        self.canvas.bind("<Configure>", self.on_resize)  # Redesenha ao redimensionar
        self.root = None           # Raiz da árvore
        self.selected_node = None  # Nó selecionado (para destaque)
        
        self.setup()  # Configura a interface

    # ================================================================
    # MÉTODOS DE CONFIGURAÇÃO DA INTERFACE
    # ================================================================
    
    def setup(self):
        """Configura os elementos da interface gráfica"""
        # Botões de operações
        tk.Button(self.control_frame, text="Insert", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Search", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Árvore AVL - Inicie com inserções", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Botões de percurso
        tk.Button(self.traversal_frame, text="In-order", command=self.show_inorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Pre-order", command=self.show_preorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Post-order", command=self.show_postorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Level-order", command=self.show_levelorder).pack(side=tk.LEFT, padx=5)
        
        self.visualize_tree()  # Desenha a árvore inicial

    # ================================================================
    # OPERAÇÕES BÁSICAS DA AVL
    # ================================================================
    
    def get_height(self, node):
        """Retorna a altura de um nó (0 para nós nulos)"""
        return node.height if node else 0
    
    def get_balance(self, node):
        """Calcula o fator de balanceamento do nó"""
        return self.get_height(node.left) - self.get_height(node.right) if node else 0
    
    def update_height(self, node):
        """Atualiza a altura de um nó com base nos filhos"""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def rotate_right(self, z):
        """Rotação simples à direita"""
        y = z.left
        T3 = y.right
        
        # Realiza a rotação
        y.right = z
        z.left = T3
        
        # Atualiza alturas
        self.update_height(z)
        self.update_height(y)
        
        return y  # Nova raiz da subárvore
    
    def rotate_left(self, z):
        """Rotação simples à esquerda"""
        y = z.right
        T2 = y.left
        
        # Realiza a rotação
        y.left = z
        z.right = T2
        
        # Atualiza alturas
        self.update_height(z)
        self.update_height(y)
        
        return y  # Nova raiz da subárvore
    
    def balance_node(self, node):
        """Aplica rotações para balancear o nó se necessário"""
        if not node:
            return node
        
        # Atualiza altura e calcula balanceamento
        self.update_height(node)
        balance = self.get_balance(node)
        
        # Casos de desbalanceamento e rotações correspondentes
        # Caso Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
            
        # Caso Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
            
        # Caso Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
            
        # Caso Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
            
        return node  # Nó já balanceado

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def insert_gui(self):
        """Insere valor da entrada na árvore"""
        try:
            value = int(self.entry.get())
            self.root = self.insert(self.root, value)
            self.visualize_tree()
            self.status.config(text=f"Inserido: {value}")
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
     
    def delete_gui(self):
        """Remove valor da entrada da árvore"""
        try:
            value = int(self.entry.get())
            self.root = self.delete(self.root, value)
            self.visualize_tree()
            self.status.config(text=f"Deletado: {value}")
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
    
    def search_gui(self):
        """Busca valor na árvore e destaca o nó"""
        try:
            value = int(self.entry.get())
            node = self.search(self.root, value)
            if node:
                self.selected_node = node
                self.status.config(text=f"Encontrado: {value}")
            else:
                self.selected_node = None
                self.status.config(text=f"Valor não encontrado: {value}")
            self.visualize_tree()
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
    
    def clear_tree(self):
        """Limpa toda a árvore"""
        self.root = None
        self.selected_node = None
        self.canvas.delete("all")
        self.status.config(text="Árvore limpa")
        self.visualize_tree()

    # ================================================================
    # OPERAÇÕES INTERNAS DA ÁRVORE
    # ================================================================
    
    def insert(self, node, value):
        """Insere valor recursivamente e balanceia a árvore"""
        if not node:
            return TreeNode(value)
            
        # Inserção BST padrão
        if value < node.value:
            node.left = self.insert(node.left, value)
        else:
            node.right = self.insert(node.right, value)
            
        # Balanceamento após inserção
        return self.balance_node(node)
        
    def delete(self, node, value):
        """Remove valor recursivamente e balanceia a árvore"""
        if not node:
            return node
            
        # Busca pelo nó a ser removido
        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        else:
            # Nó com um ou nenhum filho
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
                
            # Nó com dois filhos: obtém sucessor in-order
            temp = self.get_min_node(node.right)
            node.value = temp.value
            node.right = self.delete(node.right, temp.value)
            
        # Balanceamento após remoção
        return self.balance_node(node)
    
    def get_min_node(self, node):
        """Obtém o nó com menor valor na subárvore"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def search(self, node, value):
        """Busca recursiva por um valor na árvore"""
        if not node:
            return None
        
        if value == node.value:
            return node
        elif value < node.value:
            return self.search(node.left, value)
        else:
            return self.search(node.right, value)

    # ================================================================
    # PERCURSOS DA ÁRVORE
    # ================================================================
    
    def traverse_inorder(self, node):
        """Percurso in-order: esquerda, raiz, direita"""
        return (self.traverse_inorder(node.left) + [node.value] + self.traverse_inorder(node.right)) if node else []
    
    def traverse_preorder(self, node):
        """Percurso pre-order: raiz, esquerda, direita"""
        return ([node.value] + self.traverse_preorder(node.left) + self.traverse_preorder(node.right)) if node else []
    
    def traverse_postorder(self, node):
        """Percurso post-order: esquerda, direita, raiz"""
        return (self.traverse_postorder(node.left) + self.traverse_postorder(node.right) + [node.value]) if node else []
    
    def traverse_levelorder(self):
        """Percurso por níveis (largura)"""
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.value)
                queue.append(node.left)
                queue.append(node.right)
        return result
        
    def show_inorder(self):
        """Exibe percurso in-order na barra de status"""
        traversal = self.traverse_inorder(self.root)
        self.status.config(text=f"In-order: {' '.join(map(str, traversal))}")

    def show_preorder(self):
        """Exibe percurso pre-order na barra de status"""
        traversal = self.traverse_preorder(self.root)
        self.status.config(text=f"Pre-order: {' '.join(map(str, traversal))}")

    def show_postorder(self):
        """Exibe percurso post-order na barra de status"""
        traversal = self.traverse_postorder(self.root)
        self.status.config(text=f"Post-order: {' '.join(map(str, traversal))}")

    def show_levelorder(self):
        """Exibe percurso por níveis na barra de status"""
        traversal = self.traverse_levelorder()
        self.status.config(text=f"Level-order: {' '.join(map(str, traversal))}")

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_tree(self):
        """Renderiza a árvore no canvas"""
        self.canvas.delete("all")
        
        # Mostra mensagem se a árvore estiver vazia
        if not self.root:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Árvore Vazia",
                font=("Arial", 24),
                fill="gray"
            )
            return
        
        # Organiza os nós por níveis usando BFS
        levels = []
        queue = [(self.root, 0)]
        while queue:
            node, level = queue.pop(0)
            if level == len(levels):
                levels.append([])
            levels[level].append(node)
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        
        # Calcula posições dos nós
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        node_radius = 20
        vertical_spacing = 80
        
        for level_idx, level_nodes in enumerate(levels):
            y = 50 + level_idx * vertical_spacing
            for node_idx, node in enumerate(level_nodes):
                # Distribuição horizontal dos nós
                x = (node_idx + 1) * canvas_width / (len(level_nodes) + 1)
                node.x = x
                node.y = y
        
        # Desenha as arestas primeiro (linhas)
        for level_nodes in levels:
            for node in level_nodes:
                if node.left:
                    self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="blue", width=2)
                if node.right:
                    self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="blue", width=2)
        
        # Desenha os nós (círculos)
        for level_nodes in levels:
            for node in level_nodes:
                x, y = node.x, node.y
                # Destaca nó selecionado (busca)
                fill_color = "lightgreen" if node == self.selected_node else "lightblue"
                
                # Círculo do nó
                self.canvas.create_oval(
                    x - node_radius, y - node_radius,
                    x + node_radius, y + node_radius,
                    fill=fill_color, outline="black", width=2
                )
                
                # Valor do nó
                self.canvas.create_text(
                    x, y,
                    text=str(node.value),
                    font=("Arial", 12, "bold"),
                    fill="black"
                )
                
                # Altura do nó
                self.canvas.create_text(
                    x, y + 30,
                    text=f"h={node.height}",
                    font=("Arial", 8),
                    fill="darkgreen"
                )
    
    def on_resize(self, event):
        """Redesenha a árvore ao redimensionar o canvas"""
        if event.width > 50 and event.height > 50:
            self.visualize_tree()