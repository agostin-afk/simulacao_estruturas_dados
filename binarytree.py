import tkinter as tk
from tkinter import messagebox
import random


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0
        
    def __str__(self):
        return str(self.value)

class BinaryTree:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.canvas = tk.Canvas(self.parent_frame, width=300, height=300, bg='white')
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
        
        self.setup(10)  
    
    def setup(self, root_value):
        tk.Button(self.control_frame, text="Insert", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Search", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Clear", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Comece", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        if root_value is not None:
            self.root = TreeNode(root_value)
        else:
            self.root = None
        
        tk.Button(self.traversal_frame, text="In-order", command=self.show_inorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Pre-order", command=self.show_preorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Post-order", command=self.show_postorder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.traversal_frame, text="Level-order", command=self.show_levelorder).pack(side=tk.LEFT, padx=5)
        
        if self.root:
            self.visualize_tree()
        else:
            self.canvas.create_text(500, 350, text="Árvore Vazia", font=("Arial", 24), fill="gray")
        
    # metodos para gui:
    def insert_gui(self):
        try:
            value = int(self.entry.get())
            self.insert(value)
            self.visualize_tree()
            self.status.config(text=f"inserido: {value}")
        except ValueError:
            messagebox.showerror("Error", "Coloque um valor inteiro")
     
    def delete_gui(self):
        try:
            value = int(self.entry.get())
            if self.delete(value):
                self.visualize_tree()
                self.status.config(text=f"Deletado: {value}")
            else:
                self.status.config(text=f"Value: {value} not found")
        except ValueError:
            messagebox.showerror("Error", "Coloque um valor inteiro")
    
    def search_gui(self):
        try:
            value = int(self.entry.get())
            if self.search(value):
                self.status.config(text=f"Found: {value}")
            else:
                self.status.config(text=f"value: {value} not found")
        except ValueError:
            messagebox.showerror("Error", "Insira um valor inteiro")
    
    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            return 
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = TreeNode(value)
                return
            else:
                queue.append(current.left)
            if current.right is None:
                current.right = TreeNode(value)
                return
            else:
                queue.append(current.right)
    
    def clear_tree(self):
        self.root = None
        self.canvas.delete("all")
        self.status.config(text="Tree cleared")
    
    def delete(self, value):
        if self.root is None:
            return False
        node_to_delete = None
        deepest_node = None
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.value == value:
                node_to_delete = current
            deepest_node = current
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        if node_to_delete is None:
            return False
        node_to_delete.value = deepest_node.value
        self.delete_deepest(deepest_node)
        return True

    def delete_deepest(self, node):
        if self.root == node:
            self.root = None
            return
        queue = [self.root]
        while queue:
            current = queue.pop(0)
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
        result = []
        self.inorder_helper(self.root, result)
        return result
    
    def inorder_helper(self, node, result):
        if node:
            self.inorder_helper(node.left, result)
            result.append(node.value)
            self.inorder_helper(node.right, result)
    
    def traverse_preorder(self):
        result = []
        self.preorder_helper(self.root, result)
        return result

    def preorder_helper(self, node, result):
        if node:
            result.append(node.value)
            self.preorder_helper(node.left, result)
            self.preorder_helper(node.right, result)
    
    def traverse_postorder(self):
        result = []
        self.postorder_helper(self.root, result)
        return result
    
    def postorder_helper(self, node, result):
        if node:
            self.postorder_helper(node.left, result)
            self.postorder_helper(node.right, result)
            result.append(node.value)
    
    def traverse_levelorder(self):
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
        if self.root is None:
            return False
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.value == value:
                return True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return False
    
    def show_inorder(self):
        traversal = self.traverse_inorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"In-order: {traversal_str}")

    def show_preorder(self):
        traversal = self.traverse_preorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Pre-order: {traversal_str}")

    def show_postorder(self):
        traversal = self.traverse_postorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Post-order: {traversal_str}")

    def show_levelorder(self):
        traversal = self.traverse_levelorder()
        traversal_str = ' '.join(map(str, traversal))
        self.status.config(text=f"Level-order: {traversal_str}")

    def visualize_tree(self):
        self.canvas.delete("all")
        if not self.root:
            return
        levels = []
        queue = [(self.root, 0)]
        while queue:
            node, level = queue.pop(0)
            if level == len(levels):
                levels.append([])
            levels[level].append(node)
            if node.left:
                queue.append((node.left, level+1))
            if node.right:
                queue.append((node.right, level+1))
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        tree_height = len(levels)
        if tree_height > 0:
            vertical_spacing = (canvas_height - 100) / tree_height
        else:
            vertical_spacing = 0
        for level_num, nodes in enumerate(levels):
            n = len(nodes)
            for i, node in enumerate(nodes):
                node.x = (i + 1) * canvas_width / (n + 1)
                node.y = 50 + level_num * vertical_spacing
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left:
                self.canvas.create_line(current.x, current.y, current.left.x, current.left.y, fill="blue", width=2)
                queue.append(current.left)
            if current.right:
                self.canvas.create_line(current.x, current.y, current.right.x, current.right.y, fill="blue", width=2)
                queue.append(current.right)
            self.canvas.create_oval(current.x-20, current.y-20, current.x+20, current.y+20, fill="lightblue", outline="black")
            self.canvas.create_text(current.x, current.y, text=str(current.value), font=("Arial", 12, "bold"))
    def on_resize(self, event):
        self.visualize_tree()