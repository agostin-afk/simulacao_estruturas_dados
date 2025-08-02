import tkinter as tk
from tkinter import messagebox

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.x = 0
        self.y = 0
        
    def __str__(self):
        return str(self.value)

class AVLTree:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.canvas = tk.Canvas(self.parent_frame, width=500, height=400, bg='white')
        self.parent_frame.pack_propagate(False)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.traversal_frame = tk.Frame(self.parent_frame)
        self.traversal_frame.pack(pady=5, fill=tk.X)   
        self.canvas.bind("<Configure>", self.on_resize)
        self.root = None
        self.selected_node = None
        
        self.setup()  
    
    def setup(self):
        tk.Button(self.control_frame, text="Insert", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Search", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Clear", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Árvore AVL - Inicie com inserções", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        tk.Button(self.traversal_frame, text="In-order", command=self.show_inorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Pre-order", command=self.show_preorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Post-order", command=self.show_postorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Level-order", command=self.show_levelorder).pack(side=tk.LEFT, padx=5)
        
        self.visualize_tree()

    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def balance_node(self, node):
        if not node:
            return node
        
        self.update_height(node)
        balance = self.get_balance(node)
        
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
            
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
            
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
            
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
            
        return node

    def insert_gui(self):
        try:
            value = int(self.entry.get())
            self.root = self.insert(self.root, value)
            self.visualize_tree()
            self.status.config(text=f"Inserido: {value}")
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
     
    def delete_gui(self):
        try:
            value = int(self.entry.get())
            self.root = self.delete(self.root, value)
            self.visualize_tree()
            self.status.config(text=f"Deletado: {value}")
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
    
    def search_gui(self):
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
    
    def insert(self, node, value):
        if not node:
            return TreeNode(value)
            
        if value < node.value:
            node.left = self.insert(node.left, value)
        else:
            node.right = self.insert(node.right, value)
            
        return self.balance_node(node)
    
    def clear_tree(self):
        self.root = None
        self.selected_node = None
        self.canvas.delete("all")
        self.status.config(text="Árvore limpa")
        self.visualize_tree()
        
    def delete(self, node, value):
        if not node:
            return node
            
        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
                
            temp = self.get_min_node(node.right)
            node.value = temp.value
            node.right = self.delete(node.right, temp.value)
            
        return self.balance_node(node)
    
    def get_min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def search(self, node, value):
        if not node:
            return None
        
        if value == node.value:
            return node
        elif value < node.value:
            return self.search(node.left, value)
        else:
            return self.search(node.right, value)
    
    def traverse_inorder(self, node):
        result = []
        if node:
            result = self.traverse_inorder(node.left)
            result.append(node.value)
            result += self.traverse_inorder(node.right)
        return result
    
    def traverse_preorder(self, node):
        result = []
        if node:
            result.append(node.value)
            result += self.traverse_preorder(node.left)
            result += self.traverse_preorder(node.right)
        return result
    
    def traverse_postorder(self, node):
        result = []
        if node:
            result = self.traverse_postorder(node.left)
            result += self.traverse_postorder(node.right)
            result.append(node.value)
        return result
    
    def traverse_levelorder(self):
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
        traversal = self.traverse_inorder(self.root)
        self.status.config(text=f"In-order: {' '.join(map(str, traversal))}")

    def show_preorder(self):
        traversal = self.traverse_preorder(self.root)
        self.status.config(text=f"Pre-order: {' '.join(map(str, traversal))}")

    def show_postorder(self):
        traversal = self.traverse_postorder(self.root)
        self.status.config(text=f"Post-order: {' '.join(map(str, traversal))}")

    def show_levelorder(self):
        traversal = self.traverse_levelorder()
        self.status.config(text=f"Level-order: {' '.join(map(str, traversal))}")

    def visualize_tree(self):
        self.canvas.delete("all")
        if not self.root:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Árvore Vazia",
                font=("Arial", 24),
                fill="gray"
            )
            return
        
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
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if not levels:
            return
        
        max_width = max(len(level) for level in levels)
        node_radius = 20
        vertical_spacing = 80
        
        for level_idx, level_nodes in enumerate(levels):
            y = 50 + level_idx * vertical_spacing
            for node_idx, node in enumerate(level_nodes):
                x = (node_idx + 1) * canvas_width / (len(level_nodes) + 1)
                node.x = x
                node.y = y
        
        for level_nodes in levels:
            for node in level_nodes:
                if node.left:
                    self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="blue", width=2)
                if node.right:
                    self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="blue", width=2)
        
        for level_nodes in levels:
            for node in level_nodes:
                x, y = node.x, node.y
                fill_color = "lightgreen" if node == self.selected_node else "lightblue"
                self.canvas.create_oval(
                    x - node_radius, y - node_radius,
                    x + node_radius, y + node_radius,
                    fill=fill_color, outline="black", width=2
                )
                self.canvas.create_text(
                    x, y,
                    text=str(node.value),
                    font=("Arial", 12, "bold"),
                    fill="black"
                )
                self.canvas.create_text(
                    x, y + 30,
                    text=f"h={node.height}",
                    font=("Arial", 8),
                    fill="darkgreen"
                )
    def on_resize(self, event):
        if event.width > 50 and event.height > 50:
            self.visualize_tree()
