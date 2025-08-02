import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.x = 0
        self.y = 0

class ListaEncadeada:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.head = None
        self.selected_node = None 
        
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.control_frame, text="Inserir Início", command=self.insert_start_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Inserir Fim", command=self.insert_end_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Remover", command=self.remove_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Buscar", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_list).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Lista Vazia", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        self.visualize_list()

    def on_resize(self, event):
        self.visualize_list()
    
    def insert_start_gui(self):
        try:
            value = self.entry.get()
            if value:
                self.insert_start(value)
                self.visualize_list()
                self.status.config(text=f"Inserido no início: {value}")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para inserir")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def insert_end_gui(self):
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
        self.head = None
        self.selected_node = None
        self.visualize_list()
        self.status.config(text="Lista limpa")
    
    def insert_start(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def insert_end(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def remove(self, value):
        if not self.head:
            return False
        
        if self.head.value == value:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def search(self, value):
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
    
    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def visualize_list(self):
        self.canvas.delete("all")
        
        if not self.head:
            self.canvas.create_text(
                self.canvas.winfo_width()/2, 
                self.canvas.winfo_height()/2, 
                text="Lista Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        node_radius = min(30, canvas_width // 20)
        spacing = min(80, canvas_width // 10)
        
        current = self.head
        x = canvas_width / 2 - ((self.size() - 1) * spacing) / 2
        y = canvas_height / 2
        
        while current:
            fill_color = "lightgreen" if current == self.selected_node else "lightblue"
            
            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=fill_color, outline="black", width=2
            )
            
            self.canvas.create_text(x, y, text=str(current.value), font=("Arial", min(12, node_radius//2), "bold"))
            
            if current.next:
                self.canvas.create_line(
                    x + node_radius, y,
                    x + spacing - node_radius, y,
                    arrow=tk.LAST, width=2
                )
            
            current.x = x
            current.y = y
            
            current = current.next
            x += spacing