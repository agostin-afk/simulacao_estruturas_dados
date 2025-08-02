import tkinter as tk
from tkinter import messagebox
import random

class Pilha:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.stack = []
        
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.control_frame, text="Push", command=self.push_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Pop", command=self.pop_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Top", command=self.top_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Clear", command=self.clear_stack).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Pilha Vazia", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        self.visualize_stack()

    def on_resize(self, event=None):
        self.visualize_stack()

    def push_gui(self):
        try:
            value = self.entry.get()
            if value:
                self.push(value)
                self.visualize_stack()
                self.status.config(text=f"Empilhado: {value}")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para empilhar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def pop_gui(self):
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
        if not self.stack:
            self.status.config(text="Pilha vazia!")
            return
            
        try:
            value = self.top()
            self.status.config(text=f"Topo: {value}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_stack(self):
        self.stack = []
        self.visualize_stack()
        self.status.config(text="Pilha limpa")

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        if not self.stack:
            raise IndexError("Pilha vazia!")
        return self.stack.pop()
    
    def top(self):
        if not self.stack:
            raise IndexError("Pilha vazia!")
        return self.stack[-1]
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
    def visualize_stack(self):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 300
        
        if not self.stack:
            self.canvas.create_text(
                canvas_width/2, canvas_height/2, 
                text="Pilha Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        

        element_width = min(100, canvas_width // 6)
        element_height = min(60, canvas_height // 10)
        spacing = 10
        
        start_x = canvas_width / 2
        start_y = canvas_height - 50
        
        if self.stack:
            top_y = start_y - (len(self.stack) * (element_height + spacing) + element_height/2)
            self.canvas.create_line(
                start_x + element_width/2 + 20, top_y,
                start_x + element_width/2 + 40, top_y,
                arrow=tk.LAST, width=2
            )
            self.canvas.create_text(
                start_x + element_width/2 + 50, top_y - 10,
                text="Topo", 
                font=("Arial", 10)
            )
        
        for i, value in enumerate(self.stack):
            y = start_y - i * (element_height + spacing)
            
            self.canvas.create_rectangle(
                start_x - element_width/2, y - element_height/2,
                start_x + element_width/2, y + element_height/2,
                fill="lightblue", outline="black", width=2
            )
            
            self.canvas.create_text(
                start_x, y,
                text=str(value), 
                font=("Arial", min(12, element_width//8), "bold")
            )
        
        if self.stack:
            top_y = start_y - (len(self.stack) * (element_height + spacing)) + element_height/2
            self.canvas.create_rectangle(
                start_x - element_width/2 - 5, top_y - element_height/2 - 5,
                start_x + element_width/2 + 5, top_y + element_height/2 + 5,
                outline="red", width=2, dash=(4, 2),
            )