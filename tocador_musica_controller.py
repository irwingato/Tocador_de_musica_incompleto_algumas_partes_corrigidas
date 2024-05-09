from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3
import mysql.connector
import tkinter as tk 
from tocador_musica_model import Model
from tocador_musica_view import View 

class Controller():
    '''Controlador é o principal coordenador no padrão MVC,
    ele coleta entrada do usuário, inicia mudanças necessárias no modelo (dados)
    e atualiza view para refletir quaisquer mudanças que poderiam ter acontecido'''
    
    def __init__(self, model, view):
        self.model :Model = model            
        self.view :View = view
        
    
    def favoritar_musica(self):
        self.model.favoritar_musica()
    
    def favoritar_varias_musicas(self):
        self.model.favoritar_varias_musicas()    
    
    def remover_musica(self):
        self.model.remover_musica()
    
    def mostrar_favoritos(self):
        self.model.mostrar_favoritos()       
    
    def view_main(self):
        self.view_main()    
    
    def tempo_reproducao(self):
        self.view.tempo_reproducao()
    
    def adicionar_musica(self):
        self.view.adicionar_musica()
    
    def adicionar_varias_musicas(self):
        self.view.adicionar_varias_musicas()
    
    def excluir_musica(self):
        self.view.excluir_musica()
    
    def excluir_todas_musicas(self):
        self.view.excluir_todas_musicas()
        
    def reproduzir(self):
        self.view.reproduzir()
    
    def parar(self):
        self.view.parar()
    
    def proxima_musica(self):
        self.view.proxima_musica()
    
    def musica_anterior(self):
        self.view.musica_anterior()
    
    def pausar(self):
        self.view.pausar()
    
    def volume(self):
        self.view.volume()
    
    def deslizar(self):
        self.view.deslizar()  
    
    def run(self):
        self.view.mainloop()
        
    def get_lista_reproducao(self):
        return self.view.lista_de_reproducao.get(self.view.ACTIVE)
    
    def get_musicas_selecionadas(self):
        return self.view.get_musicas_selecionadas()
