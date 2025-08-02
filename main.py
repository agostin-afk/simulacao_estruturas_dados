import tkinter as tk
from tkinter import ttk
from binarytree import BinaryTree
from fila import Fila
from pilha import Pilha
from lista import ListaEncadeada
from tabelaHash import HashTable
import random
from os import getenv
from dotenv import load_dotenv


class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Estruturas De Dados")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.window_width = 600
        self.window_height = 600
        self.center_x = int(screen_width/2 - self.window_width / 2)
        self.center_y = int(screen_height/2 - self.window_height / 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        
        self.Options()
        self.root.mainloop()
        
    def Options(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)    
        frame_arvore = ttk.Frame(notebook)
        frame_pilha = ttk.Frame(notebook)
        frame_fila = ttk.Frame(notebook)
        frame_lista = ttk.Frame(notebook)
        frame_hash = ttk.Frame(notebook)
        
        
        notebook.add(frame_arvore, text='Arvore')
        notebook.add(frame_pilha, text='Pilha')
        notebook.add(frame_fila, text='Fila')
        notebook.add(frame_lista, text='Lista Encadeada')
        notebook.add(frame_hash, text='Tabela Hash')
        
        for frame in [frame_arvore, frame_pilha, frame_fila, frame_lista, frame_hash]:
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
        
        self.tree = BinaryTree(frame_arvore)
        self.stack = Pilha(frame_pilha)
        self.queue = Fila(frame_fila)
        self.linked_list = ListaEncadeada(frame_lista)
        self.hash_table = HashTable(frame_hash)
    
    
win = MainWindow()
