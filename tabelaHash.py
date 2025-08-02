# hash_table.py
import tkinter as tk
from tkinter import messagebox
import hashlib

class HashTable:
    def __init__(self, parent_frame, capacity=10):
        self.parent_frame = parent_frame
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.selected_bucket = None
        self.selected_item = None
        
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        self.entry = tk.Entry(self.control_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.control_frame, text="Inserir", command=self.insert_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Buscar", command=self.search_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Remover", command=self.remove_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Limpar", command=self.clear_table).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Tabela Hash Vazia", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        self.visualize_table()

    def on_resize(self, event):
        self.visualize_table()
    
    def hash_function(self, key):
        """Função de hash simples usando SHA-256"""
        if isinstance(key, int):
            key = str(key)
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.capacity
    

    def insert_gui(self):
        try:
            key = self.entry.get()
            if key:
                value = f"Valor({key})"
                self.insert(key, value)
                self.visualize_table()
                self.status.config(text=f"Inserido: {key} → {value}")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite uma chave para inserir")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def search_gui(self):
        try:
            key = self.entry.get()
            if key:
                value, bucket_idx, item_idx = self.search(key)
                if value is not None:
                    self.selected_bucket = bucket_idx
                    self.selected_item = item_idx
                    self.visualize_table()
                    self.status.config(text=f"Encontrado: {key} → {value} (Balde {bucket_idx})")
                else:
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
        self.table = [[] for _ in range(self.capacity)]
        self.selected_bucket = None
        self.selected_item = None
        self.visualize_table()
        self.status.config(text="Tabela Hash limpa")
    

    def insert(self, key, value):

        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))
    
    def search(self, key):
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                return v, index, i
        return None, -1, -1
    
    def remove(self, key):
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False
    
    def visualize_table(self):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 500
        
        bucket_width = min(100, canvas_width // (self.capacity + 1))
        bucket_height = 80
        vertical_spacing = 20
        start_x = (canvas_width - (self.capacity * (bucket_width + 10))) / 2
        start_y = 50
        
        for i in range(self.capacity):
            x = start_x + i * (bucket_width + 10)
            y = start_y
            
            bucket_color = "lightgreen" if i == self.selected_bucket else "lightgray"
            self.canvas.create_rectangle(
                x, y,
                x + bucket_width, y + bucket_height,
                fill=bucket_color, outline="black", width=2
            )
            
            self.canvas.create_text(
                x + bucket_width/2, y - 15,
                text=f"Balde {i}", font=("Arial", 10)
            )
            
            item_y = y + 10
            for j, (key, value) in enumerate(self.table[i]):
                item_color = "gold" if (i == self.selected_bucket and j == self.selected_item) else "lightblue"
                
                self.canvas.create_rectangle(
                    x + 5, item_y,
                    x + bucket_width - 5, item_y + 20,
                    fill=item_color, outline="black", width=1
                )
                
                self.canvas.create_text(
                    x + bucket_width/2, item_y + 10,
                    text=f"{key}:{value}", 
                    font=("Arial", min(9, bucket_width//12))
                )
                
                item_y += 25
            
            if not self.table[i]:
                self.canvas.create_text(
                    x + bucket_width/2, y + bucket_height/2,
                    text="∅", 
                    font=("Arial", 24), 
                    fill="gray"
                )
        
        self.canvas.create_text(
            canvas_width/2, canvas_height - 20,
            text=f"Capacidade: {self.capacity} | Itens: {sum(len(b) for b in self.table)}",
            font=("Arial", 10)
        )