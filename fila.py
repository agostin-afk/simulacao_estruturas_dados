import tkinter as tk
from tkinter import messagebox
import random


class Fila:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.queue = []
        
        self.canvas = tk.Canvas(self.parent_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.control_frame = tk.Frame(self.parent_frame)
        self.control_frame.pack(pady=10, fill=tk.X)
        
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.control_frame, text="Enqueue", command=self.enqueue_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Dequeue", command=self.dequeue_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Clear", command=self.clear_queue).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.parent_frame, text="Fila Vazia", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
        
        self.visualize_queue()

    def on_resize(self, event=None):
        self.visualize_queue()

    def enqueue_gui(self):
        try:
            value = self.entry.get()
            if value:
                self.enqueue(value)
                self.visualize_queue()
                self.status.config(text=f"Enfileirado: {value}")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite um valor para enfileirar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def dequeue_gui(self):
        if not self.queue:
            self.status.config(text="Fila vazia!")
            return
            
        try:
            value = self.dequeue()
            self.visualize_queue()
            self.status.config(text=f"Desenfileirado: {value}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def clear_queue(self):
        self.queue = []
        self.visualize_queue()
        self.status.config(text="Fila limpa")

    def enqueue(self, value):
        self.queue.append(value)
    
    def dequeue(self):
        if not self.queue:
            raise IndexError("Fila vazia!")
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def visualize_queue(self):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 300
        
        if not self.queue:
            self.canvas.create_text(
                canvas_width/2, canvas_height/2, 
                text="Fila Vazia", 
                font=("Arial", 24), 
                fill="gray"
            )
            return
        
        element_width = min(80, canvas_width // 12)
        element_height = min(60, canvas_height // 10)
        spacing = 10
    
        total_width = len(self.queue) * (element_width + spacing) - spacing
        
        start_x = (canvas_width - total_width) / 2
        start_y = canvas_height / 2
        
        self.canvas.create_line(
            start_x - 50, start_y, 
            start_x, start_y, 
            arrow=tk.LAST, width=2
        )
        self.canvas.create_text(
            start_x - 25, start_y - 20, 
            text="Entrada", 
            font=("Arial", 10)
        )
        
        end_x = start_x + total_width
        self.canvas.create_line(
            end_x, start_y, 
            end_x + 50, start_y, 
            arrow=tk.LAST, width=2
        )
        self.canvas.create_text(
            end_x + 25, start_y - 20, 
            text="Saída", 
            font=("Arial", 10)
        )
        
        for i, value in enumerate(self.queue):
            x = start_x + i * (element_width + spacing)
            y = start_y
            
            self.canvas.create_rectangle(
                x, y - element_height/2,
                x + element_width, y + element_height/2,
                fill="lightblue", outline="black", width=2
            )
            
            self.canvas.create_text(
                x + element_width/2, y,
                text=str(value), 
                font=("Arial", min(12, element_width//6), "bold")
            )
            
            if i == 0:
                self.canvas.create_text(
                    x + element_width/2, y + element_height/2 + 15,
                    text="Frente", 
                    font=("Arial", min(9, element_width//8))
                )
            
            if i == len(self.queue) - 1:
                self.canvas.create_text(
                    x + element_width/2, y + element_height/2 + 15,
                    text="Final", 
                    font=("Arial", min(9, element_width//8))
                )