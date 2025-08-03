"""
Implementação de Árvore Binária Completa com Visualização Gráfica

Descrição:
Esta classe implementa uma árvore binária completa (não de busca) com interface gráfica usando Tkinter.
A árvore mantém sua propriedade de completude em todas as operações. Permite inserir, remover e buscar nós,
além de visualizar a estrutura da árvore e realizar diferentes tipos de percursos.

Características:
- Inserção em nível (mantém a árvore completa)
- Remoção substituindo pelo nó mais profundo
- Visualização hierárquica com conexões
- Destaque para nós selecionados
- Suporte a quatro tipos de percurso

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import messagebox

class TreeNode:
    """
    Classe que representa um nó da árvore binária
    
    Atributos:
        value: Valor armazenado no nó
        left: Referência ao filho esquerdo
        right: Referência ao filho direito
        x, y: Coordenadas para posicionamento visual
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0  # Coordenada x para desenho
        self.y = 0  # Coordenada y para desenho
        
    def __str__(self):
        """Retorna representação string do nó"""
        return str(self.value)

class BinaryTree:
    """
    Classe que implementa uma árvore binária completa com visualização gráfica
    
    Atributos:
        parent_frame: Frame do Tkinter para conter a visualização
        root: Nó raiz da árvore
        selected_node: Nó selecionado para destaque visual
        canvas: Área de desenho para visualização
        control_frame: Área para controles (entrada e botões)
        status: Barra de status para mensagens
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa a árvore binária e a interface gráfica
        
        Parâmetros:
            parent_frame: Frame do Tkinter para renderização
        """
        self.parent_frame = parent_frame
        self.root = None  # Árvore inicia vazia
        self.selected_node = None  # Nenhum nó selecionado inicialmente
        
        # Configuração da área de desenho
        self.canvas = tk.Canvas(self.parent_frame, width=300, height=300, bg='white')
        self.parent_frame.pack_propagate(False)  # Impede redimensionamento automático
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Área de controles
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        # Campo de entrada para valores
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        # Área de botões de percurso
        self.traversal_frame = tk.Frame(self.parent_frame)
        self.traversal_frame.pack(pady=5, fill=tk.X)   
        
        # Configura evento de redimensionamento
        self.canvas.bind("<Configure>", self.on_resize)
        
        # Inicializa com um nó raiz de valor 45
        self.setup(45)

    # ================================================================
    # CONFIGURAÇÃO INICIAL
    # ================================================================
    
    def setup(self, root_value):
        """Configura os elementos da interface e inicializa a árvore"""
        # Botões de operações
        tk.Button(self.control_frame, text="Insert", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Search", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status = tk.Label(self.parent_frame, text="Comece", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        # Inicializa a árvore com um nó raiz
        if root_value is not None:
            self.root = TreeNode(root_value)
        else:
            self.root = None
        
        # Botões de percurso
        tk.Button(self.traversal_frame, text="In-order", command=self.show_inorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Pre-order", command=self.show_preorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Post-order", command=self.show_postorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Level-order", command=self.show_levelorder).pack(side=tk.LEFT, padx=5)
        
        # Desenha a árvore inicial
        self.visualize_tree()

    # ================================================================
    # INTERFACE GRÁFICA PARA OPERAÇÕES
    # ================================================================
    
    def insert_gui(self):
        """Insere valor na árvore mantendo sua completude"""
        try:
            value = int(self.entry.get())
            self.insert(value)
            self.visualize_tree()
            self.status.config(text=f"Inserido: {value}")
        except ValueError:
            messagebox.showerror("Error", "Coloque um valor inteiro")
     
    def delete_gui(self):
        """Remove valor da árvore substituindo pelo nó mais profundo"""
        try:
            value = int(self.entry.get())
            if self.delete(value):
                self.visualize_tree()
                self.status.config(text=f"Deletado: {value}")
            else:
                self.status.config(text=f"Valor: {value} não encontrado")
        except ValueError:
            messagebox.showerror("Error", "Coloque um valor inteiro")
    
    def search_gui(self):
        """Busca valor na árvore e destaca o nó encontrado"""
        try:
            value = int(self.entry.get())
            node = self.search(value)
            if node:
                self.selected_node = node
                self.status.config(text=f"Encontrado: {value}")
            else:
                self.selected_node = None
                self.status.config(text=f"Valor: {value} não encontrado")
            self.visualize_tree()
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
    
    def clear_tree(self):
        """Limpa completamente a árvore"""
        self.root = None
        self.selected_node = None
        self.visualize_tree()
        self.status.config(text="Árvore limpa")

    # ================================================================
    # OPERAÇÕES DA ÁRVORE BINÁRIA
    # ================================================================
    
    def insert(self, value):
        """
        Insere um novo nó com o valor especificado na próxima posição vaga (em nível)
        Mantém a árvore binária completa.
        """
        if self.root is None:
            self.root = TreeNode(value)
            return 
        
        # Usa uma fila para encontrar a próxima posição vaga
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            # Insere à esquerda se possível
            if current.left is None:
                current.left = TreeNode(value)
                return
            else:
                queue.append(current.left)
            # Insere à direita se possível
            if current.right is None:
                current.right = TreeNode(value)
                return
            else:
                queue.append(current.right)
    
    def delete(self, value):
        """
        Remove o nó com o valor especificado, substituindo-o pelo nó mais profundo
        
        Retorna:
            True se removeu, False se o valor não foi encontrado
        """
        if self.root is None:
            return False
        
        node_to_delete = None
        deepest_node = None
        queue = [self.root]
        
        # Encontra o nó a ser deletado e o nó mais profundo
        while queue:
            current = queue.pop(0)
            if current.value == value:
                node_to_delete = current
            deepest_node = current  # O último nó visitado será o mais profundo
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        
        # Valor não encontrado
        if node_to_delete is None:
            return False
        
        # Copia o valor do nó mais profundo para o nó a ser deletado
        node_to_delete.value = deepest_node.value
        # Remove o nó mais profundo
        self.delete_deepest(deepest_node)
        return True

    def delete_deepest(self, node):
        """
        Remove o nó mais profundo da árvore
        
        Parâmetros:
            node: Nó a ser removido (o mais profundo)
        """
        if self.root == node:
            self.root = None
            return
        
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            # Remove a referência ao nó mais profundo
            if current.left == node:
                current.left = None
                return 
            elif current.left:
                queue.append(current.left)
            if current.right == node:
                current.right = None
                return 
            elif current.right:
                queue.append(current.right)
    
    def traverse_inorder(self):
        """Retorna lista de valores em percurso in-order (esquerda, raiz, direita)"""
        result = []
        self.inorder_helper(self.root, result)
        return result
    
    def inorder_helper(self, node, result):
        """Função auxiliar recursiva para percurso in-order"""
        if node:
            self.inorder_helper(node.left, result)
            result.append(node.value)
            self.inorder_helper(node.right, result)
    
    def traverse_preorder(self):
        """Retorna lista de valores em percurso pre-order (raiz, esquerda, direita)"""
        result = []
        self.preorder_helper(self.root, result)
        return result

    def preorder_helper(self, node, result):
        """Função auxiliar recursiva para percurso pre-order"""
        if node:
            result.append(node.value)
            self.preorder_helper(node.left, result)
            self.preorder_helper(node.right, result)
    
    def traverse_postorder(self):
        """Retorna lista de valores em percurso post-order (esquerda, direita, raiz)"""
        result = []
        self.postorder_helper(self.root, result)
        return result
    
    def postorder_helper(self, node, result):
        """Função auxiliar recursiva para percurso post-order"""
        if node:
            self.postorder_helper(node.left, result)
            self.postorder_helper(node.right, result)
            result.append(node.value)
    
    def traverse_levelorder(self):
        """Retorna lista de valores em percurso por nível (largura)"""
        result = []
        if self.root is None:
            return result
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            result.append(current.value)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result
        
    def search(self, value):
        """Busca um valor na árvore e retorna o nó correspondente (ou None)"""
        if self.root is None:
            return None
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.value == value:
                return current
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return None

    # ================================================================
    # VISUALIZAÇÃO E PERCURSOS (INTERFACE)
    # ================================================================
    
    def show_inorder(self):
        """Exibe percurso in-order na barra de status"""
        traversal = self.traverse_inorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"In-order: {traversal_str}")

    def show_preorder(self):
        """Exibe percurso pre-order na barra de status"""
        traversal = self.traverse_preorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Pre-order: {traversal_str}")

    def show_postorder(self):
        """Exibe percurso post-order na barra de status"""
        traversal = self.traverse_postorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Post-order: {traversal_str}")

    def show_levelorder(self):
        """Exibe percurso por nível na barra de status"""
        traversal = self.traverse_levelorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Level-order: {traversal_str}")

    # ================================================================
    # VISUALIZAÇÃO GRÁFICA
    # ================================================================
    
    def visualize_tree(self):
        """Renderiza a representação visual da árvore"""
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
        queue = [(self.root, 0)]  # (nó, nível)
        while queue:
            node, level = queue.pop(0)
            if level == len(levels):
                levels.append([])
            levels[level].append(node)
            if node.left:
                queue.append((node.left, level+1))
            if node.right:
                queue.append((node.right, level+1))
        
        # Calcula dimensões
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        tree_height = len(levels)
        vertical_spacing = (canvas_height - 100) / tree_height if tree_height > 0 else 0
        
        # Atribui coordenadas a cada nó
        for level_num, nodes in enumerate(levels):
            n = len(nodes)
            for i, node in enumerate(nodes):
                # Posição horizontal proporcional ao número de nós no nível
                node.x = (i + 1) * canvas_width / (n + 1)
                node.y = 50 + level_num * vertical_spacing
        
        # Desenha as conexões entre nós (arestas)
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left:
                self.canvas.create_line(
                    current.x, current.y, 
                    current.left.x, current.left.y, 
                    fill="blue", width=2
                )
                queue.append(current.left)
            if current.right:
                self.canvas.create_line(
                    current.x, current.y, 
                    current.right.x, current.right.y, 
                    fill="blue", width=2
                )
                queue.append(current.right)
            
            # Desenha o nó (círculo)
            fill_color = "lightgreen" if current == self.selected_node else "lightblue"
            self.canvas.create_oval(
                current.x-20, current.y-20, 
                current.x+20, current.y+20, 
                fill=fill_color, outline="black"
            )
            # Valor do nó
            self.canvas.create_text(
                current.x, current.y, 
                text=str(current.value), 
                font=("Arial", 12, "bold")
            )
    
    def on_resize(self, event):
        """Redesenha a árvore ao redimensionar o canvas"""
        self.visualize_tree()