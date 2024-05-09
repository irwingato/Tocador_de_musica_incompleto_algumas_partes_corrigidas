from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3
import mysql.connector
import tkinter as tk
import importlib
import tocador_musica_view

class Model:
    '''Classe modelo, abstrai os dados principais do padrão MVC, Modelo mantém atualizações de dados com base em eventos/chamadas
    que recebe do Controller. Dependência deve ser unidirecional, controlador para modelo, em outras palavras, as funções do modelo
    não devem chamar ativamente métodos de Controlador ou Visualização'''
    
    def __init__(self):
        super().__init__()   
        self.view :tocador_musica_view.View 
        
    # Criar uma função para favoritar uma música e salvar
    def favoritar_musica(self):      
        # Adicionar a música na lista de favoritos
        self.musica = self.view.get_lista_reproducao()
        # Favoritar uma música selecionada na lista
        self.cnx = mysql.connector.connect(user='root',password='AaZz$#!@1', host='127.0.0.1', database='Favoritos')
        self.cursor = self.cnx.cursor()
        self.query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
        self.valores = (self.musica) 
        
        try:
            # Executar a query e atualizar a mudanças no banco de dados
            self.cursor.execute(self.query, (self.valores,))
            self.cnx.commit()
        
        except mysql.connector.errors.IntegrityError:
            # Inferir o erro caso o id_musica já está na tabela de favoritos
            print('Erro: O ID da música já está em favoritos')         

    def favoritar_varias_musicas(self):
        self.cnx = mysql.connector.connect(user='root',password='AaZz$#!@1', host='127.0.0.1', database='Favoritos')
        self.cursor = self.cnx.cursor()
        self.musicas = [self.view.get_musicas_selecionadas()]
        for self.musica in self.musicas:
        # Usar um INSERT INTO query para adicionar uma nova linha na tabela favoritos
            self.query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
            self.valores = (self.musica)    
        
        try:
            # Executar a query e atualizar as mudanças para o banco de dados
            self.cursor.executemany(self.query, [(self.valores,)for self.valores in self.musicas])
            self.cnx.commit()
        except mysql.connector.errors.IntegrityError:
            # Lidar com o erro de ID_musica que já está na tabela de favoritos
            print(f'Erro: ID música {self.musica["ID_musica"]} já está nos favoritos') 
        
    # Definir uma função para abrir as músicas favoritas em uma janela
    def mostrar_favoritos(self):
    # Create the favorite songs window
        self.favoritos_janela = Toplevel()
        self.favoritos_janela.title("Músicas favoritas")

        # Criar uma Listbox widget para mostrar as músicas favoritas em uma janela
        self.janela_favoritos_listbox = Listbox(self.favoritos_janela)
        self.janela_favoritos_listbox.pack()
        self.janela_favoritos_listbox.configure(height=30, width=80)

        # Connect to the database
        self.cnx = mysql.connector.connect(user='root', password='AaZz$#!@1',
                                        host='127.0.0.1', database='Favoritos')
        self.cursor = self.cnx.cursor()

        # Definir um query de seleção
        self.query = "SELECT nome FROM Favoritos"

        # Executar a query de seleção
        self.cursor.execute(self.query)

        #  Buscar as linhas do conjunto de resultados
        self.linhas = self.cursor.fetchall()

        # Preencher a caixa de listagem com músicas favoritas
        for self.musica in self.linhas:
            self.janela_favoritos_listbox.insert(END, self.musica[0])
        
        # Criar um botão widget para permitir o usuário remover uma música da Listbox
        self.remover_botão = Button(self.favoritos_janela, text="Remover Música", command=self.remover_musica, bg="#51e2f5")
        self.remover_botão.pack() 
    
     # Definir uma função para remover a música selecionada da caixa da Listbox
    def remover_musica(self):
        # Connect to the database
        self.cnx = mysql.connector.connect(user='root', password='AaZz$#!@1',
                                        host='127.0.0.1', database='Favoritos')
        self.cursor = self.cnx.cursor()
        self.musica_selecionada = self.janela_favoritos_listbox.curselection()
        self.nome = self.janela_favoritos_listbox.get(ACTIVE)
        self.value = (self.nome)
        self.query = 'DELETE FROM Favoritos WHERE nome = %s'
        self.cursor.execute(self.query,(self.value,))
        self.cnx.commit()
        if self.musica_selecionada:
            self.janela_favoritos_listbox.delete(self.musica_selecionada[0])