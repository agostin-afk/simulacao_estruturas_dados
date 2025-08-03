"""
Aplicação Gráfica para Visualização de Estruturas de Dados

Descrição:
Este programa implementa uma interface gráfica usando Tkinter que permite visualizar e interagir com 
diferentes estruturas de dados através de uma interface com abas.

Componentes Principais:
1. Janela principal com abas para cada estrutura de dados
2. Estruturas implementadas:
   - Árvore Binária
   - Árvore AVL
   - Pilha
   - Fila
   - Lista Encadeada
   - Tabela Hash

Módulos Importados:
- tkinter: Interface gráfica principal
- ttk: Componentes temáticos do Tkinter (Notebook para abas)
- Estruturas personalizadas (binarytree, treeavl, fila, pilha, lista, tabelaHash)

Classe Principal:
MainWindow: Gerencia a janela principal e a organização das abas

Autor: Agostinho Ferreira (little_agosto)
Data da última atualização: 02/08/2025
"""

import tkinter as tk
from tkinter import ttk
from binarytree import BinaryTree
from fila import Fila
from pilha import Pilha
from lista import ListaEncadeada
from tabelaHash import HashTable
from treeavl import AVLTree

class MainWindow():
    """Classe principal que cria e gerencia a janela da aplicação"""
    
    def __init__(self):
        """Inicializa a janela principal com configurações básicas"""
        self.root = tk.Tk()
        self.root.title("Estruturas De Dados")
        
        # Configuração do tamanho e posição da janela (centralizada)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.window_width = 600
        self.window_height = 600
        self.center_x = int(screen_width/2 - self.window_width / 2)
        self.center_y = int(screen_height/2 - self.window_height / 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')
        
        # Configuração do sistema de grid para expansão
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Cria os componentes da interface
        self.Options()
        self.root.mainloop()
        
    def Options(self):
        """
        Cria o sistema de abas (notebook) e inicializa cada estrutura de dados
        em seu respectivo frame
        """
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        
        # Cria frames para cada aba
        frame_arvore = ttk.Frame(notebook)
        frame_arvoreAVL = ttk.Frame(notebook)
        frame_pilha = ttk.Frame(notebook)
        frame_fila = ttk.Frame(notebook)
        frame_lista = ttk.Frame(notebook)
        frame_hash = ttk.Frame(notebook)
        
        # Adiciona as abas ao notebook
        notebook.add(frame_arvore, text='Árvore Binária')
        notebook.add(frame_arvoreAVL, text='Árvore AVL')
        notebook.add(frame_pilha, text='Pilha')
        notebook.add(frame_fila, text='Fila')
        notebook.add(frame_lista, text='Lista Encadeada')
        notebook.add(frame_hash, text='Tabela Hash')
        
        # Configura expansão para todos os frames
        for frame in [frame_arvore, frame_arvoreAVL, frame_pilha, 
                      frame_fila, frame_lista, frame_hash]:
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
        
        # Instancia cada estrutura de dados em seu frame correspondente
        self.tree = BinaryTree(frame_arvore)          # Árvore Binária
        self.avltree = AVLTree(frame_arvoreAVL)       # Árvore AVL
        self.stack = Pilha(frame_pilha)               # Pilha
        self.queue = Fila(frame_fila)                # Fila
        self.linked_list = ListaEncadeada(frame_lista) # Lista Encadeada
        self.hash_table = HashTable(frame_hash)       # Tabela Hash
    
# Ponto de entrada da aplicação
win = MainWindow()