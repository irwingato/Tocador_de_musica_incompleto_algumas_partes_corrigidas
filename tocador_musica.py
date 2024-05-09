from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3
import mysql.connector
import tkinter as tk 

musicas_dir = {}

#Inicializar Pygame
pygame.mixer.init()

class Model:
    '''Classe modelo, abstrai os dados principais do padrão MVC, Modelo mantém atualizações de dados com base em eventos/chamadas
    que recebe do Controller. Dependência deve ser unidirecional, controlador para modelo, em outras palavras, as funções do modelo
    não devem chamar ativamente métodos de Controlador ou Visualização'''
    
    def __init__(self):
        super().__init__()   
        self.controller = None
        
    # Criar uma função para favoritar uma música e salvar
    def favoritar_musica(self):
        # Adicionar a música na lista de favoritos
        self.musica = tocador_musica_view.lista_de_reproducao.get(ACTIVE)
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
        self.musicas = [tocador_musica_view.lista_de_reproducao.get(i) for i in tocador_musica_view.lista_de_reproducao.curselection()]
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

class View(tk.Tk):
    
    def __init__(self):
        super().__init__()   
        self.controller = None
    
    def view_main(self):
        self.main_tela = self
        # Definir o tamanho da aplicação
        self.main_tela.geometry("500x450")
        # Definir o nome da aplicação
        self.main_tela.title("Tocador de música")
        # Criando quadro principal
        self.quadro_principal = Frame(self)
        self.quadro_principal.pack(pady= 20)
        # Trocar a imagem da logo do programa
        self.icone_imagem  = PhotoImage(file="logo.png")
        # Criando quadro para controlar o volume
        self.quadro_volume = LabelFrame(self.quadro_principal, text="Volume")
        self.quadro_volume.grid(row=0, column=1, padx=20)
        # Criando controle de volume deslizante
        self.volume_deslizante = ttk.Scale(self.quadro_volume, from_=100, to=0, orient=VERTICAL, length=125, value=1, command=self.volume)
        self.volume_deslizante.pack(pady=10)
        # Criar controle deslizante de música
        self.musica_deslizante = ttk.Scale(self.quadro_principal, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=self.deslizar)
        self.musica_deslizante.grid(row=2, column=0, pady=20)
        # Criando caixa de playlist
        self.lista_de_reproducao = Listbox(self.quadro_principal, selectmode="extended", bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
        self.lista_de_reproducao.grid(row=0, column=0)
        # Criando botão voltar com imagem
        self.botao_voltar_img = PhotoImage(file='images/previous.png')
        # Criando botão avançar com imagem
        self.avancar_botao_img = PhotoImage(file='images/next-button.png')
        # Criando botão reproduzir com imagem
        self.reproduzir_botao_img = PhotoImage(file='images/play-button.png')
        # Criando botão pausar com imagem
        self.pausar_botao_img = PhotoImage(file='images/pause-button.png')
        # Criando botão para com imagem
        self.parar_botao_img =  PhotoImage(file='images/stop-button.png')
        # Criando botão de frame
        self.controle_quadro = Frame(self.quadro_principal)
        self.controle_quadro.grid(row=1, column=0, pady=20)
        # Criando botões para todas as funcionalidades disponíveis
        self.botao_voltar = Button(self.controle_quadro, image=self.botao_voltar_img, borderwidth=0, command=self.musica_anterior)
        self.avancar_botao = Button(self.controle_quadro, image=self.avancar_botao_img, borderwidth=0, command=self.proxima_musica)
        self.reproduzir_botao = Button(self.controle_quadro, image=self.reproduzir_botao_img, borderwidth=0, command=self.reproduzir)
        self.pausar_botao = Button(self.controle_quadro, image=self.pausar_botao_img, borderwidth=0, command=lambda: self.pausar(pausado))
        self.parar_botao = Button(self.controle_quadro, image=self.parar_botao_img, borderwidth=0, command=self.parar)
        self.botao_voltar.grid(row=0, column=0, padx=10)
        self.avancar_botao.grid(row=0, column=1, padx=10)
        self.reproduzir_botao.grid(row=0, column=2, padx=10)
        self.pausar_botao.grid(row=0, column=3, padx=10)
        self.parar_botao.grid(row=0, column=4, padx=10)
        
        # Criar Menu Principal
        self.meu_menu = Menu(self)
        self.config(menu=self.meu_menu) 
        
        # Criar Menu Adicionar Som em lista suspensa 
        self.adicionar_musica_menu = Menu(self.meu_menu, tearoff=0)
        self.meu_menu.add_cascade(label="Adicionar Músicas", menu=self.adicionar_musica_menu)
        # Adicionar uma música para a playlist
        self.adicionar_musica_menu.add_command(label="Adicionar uma música para a playlist", command=self.adicionar_musica)
        # Adicionar várias músicas
        self.adicionar_musica_menu.add_command(label="Adicionar várias músicas para playlist", command=self.adicionar_varias_musicas)

        # Criar menu suspensos de exclusão de música
        self.remover_musica_menu = Menu(self.meu_menu, tearoff=0)
        self.meu_menu.add_cascade(label="Remover músicas", menu=self.remover_musica_menu)
        self.remover_musica_menu.add_command(label="Excluir uma música da lista de reprodução", command=self.excluir_musica)
        self.remover_musica_menu.add_command(label="Excluir todas as músicas da lista de reprodução", command=self.excluir_todas_musicas)
        
        # Criar menu suspensos para adicionar música favoritas
        self.favoritar_musica_menu = Menu(self.meu_menu, tearoff=0)
        self.meu_menu.add_cascade(label="Salvar aos favoritos", menu=self.favoritar_musica_menu)
        self.favoritar_musica_menu.add_command(label="Adicionar uma música aos favoritos", command=tocador_musica_model.favoritar_musica)
        self.favoritar_musica_menu.add_command(label="Adicionar várias as músicas aos favoritos", command=tocador_musica_model.favoritar_varias_musicas)
        
        # Criar barra de status
        self.barra_status = Label(self, text='', bd=1, relief=GROOVE, anchor=E)
        self.barra_status.pack(fill=X, side=BOTTOM, ipady=2)

        # Nome temporário
        self.meu_nome = Label(self, text='')
        self.meu_nome.pack(pady=20)

        self.favoritos_listbox = Listbox(self.quadro_principal, selectmode="extended", bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
        
        self.mostrar_favoritos = IntVar()
        
        # Criar um widget botão de verificar que permita que o usuário mostre ou esconda a lista de músicas favoritas
        self.mostrar_favoritos_verificar = Button(self, text="Mostrar músicas favoritas", command=tocador_musica_model.mostrar_favoritos, bg="#51e2f5")
        self.mostrar_favoritos_verificar.place(x = 150, y = 350)
                 
        self.main_tela.iconphoto(True, self.icone_imagem)
        self.main_tela.mainloop()    
    
    # Criar uma função para lidar com o tempo
    def tempo_reproducao(self):
        # Verificar se a música está parada
        if parado:
            return
        
        # Pegar o tempo atual da música
        self.tempo_atual = pygame.mixer.music.get_pos() / 1000
        # Converter o tempo da música no formato de hora
        self.tempo_atual_convertido = time.strftime('%M:%S', time.gmtime(self.tempo_atual))
            
        self.musica = self.lista_de_reproducao.get(ACTIVE) 
        # musica = f'C:/Users/Irwing Seiji Ato/Documents/IFPR/4º Semestre/Construção de Aplicações Orientada a Objetos/Trabalho 02 - Projeto da disciplina/mp3/audio/{musica}.mp3'
        self.musica = musicas_dir[self.musica]
        # Achar o tamanho da música atual
        self.musica_mut = MP3(self.musica) 
        global musica_tamanho
        self.musica_tamanho = self.musica_mut.info.length
        # Converter para o formato de minutos
        self.musica_convertida_tamanho = time.strftime('%M:%S', time.gmtime(self.musica_tamanho))
        
        # Verificar se a música acabou
        if int(self.musica_deslizante.get()) == int(self.musica_tamanho):
            self.parar()
        
        elif pausado:
            # Verificar se está pausado, se estiver passar
            pass    
        else:    
            # Mover o controle deslizante 1 segundo por tempo
            self.proximo_tempo = int(self.musica_deslizante.get()) + 1
            
            # Saída para o novo valor de tempo do controle deslizante, e a duração da música
            self.musica_deslizante.config(to=self.musica_tamanho, value=self.proximo_tempo)
            
            # Converter o controle deslizante no formato de minutos        
            self.tempo_atual_convertido = time.strftime('%M:%S', time.gmtime(int(self.musica_deslizante.get())))
            
            # Saída do controle deslizante
            self.barra_status.config(text=f'Tempo Decorrido: {self.tempo_atual_convertido} of {self.musica_convertida_tamanho}  ')
                    
        # Adicionar o tempo atual a barra de status
        if self.tempo_atual >= 1:
            self.barra_status.config(text=f'Tempo Decorrido: {self.tempo_atual_convertido} of {self.musica_convertida_tamanho}  ')
        
        # Criar uma repetição para verificar os minutos a cada segundo
        self.barra_status.after(1000, self.tempo_reproducao) 
    
     # Criar função para adicionar uma música para a playlist
    def adicionar_musica(self):
        self.musica = filedialog.askopenfilename(initialdir='audio/', title="Escolha uma música", filetypes=(("Arquivos mp3", "*.mp3"), ))
        # Retirar a estrutura de diretório e .mp3 do título de música
        self.nome = self.musica[self.musica.rfind("/") +1:]
        self.nome = self.nome.replace(".mp3", "")
            
        # Adicionar ao dicionário que mapea nome para o endereço do diretório
        musicas_dir[self.nome]=self.musica    
        
        # Adicionar ao fim da lista de reprodução
        self.lista_de_reproducao.insert(END, self.nome)
    
    # Criar uma função para excluir uma música da lista de reprodução
    def excluir_musica(self):
        # Excluir música selecionada da lista de reprodução
        self.lista_de_reproducao.delete(ANCHOR)

   
    # Criar uma função para excluir todas as músicas de uma lista de reprodução
    def excluir_todas_musicas(self):
        # Excluir todas as músicas
        self.lista_de_reproducao.delete(0, END)

    # Criar Função reproduzir
    def reproduzir(self):
        # Configurar parado para falso desde que a música está tocando agora
        global parado
        parado = False  
        
        # Reconstruir a música com material de estrutura do diretório
        self.musica = musicas_dir[self.lista_de_reproducao.get(ACTIVE)] 
            
        # Carregar música com pygame mixer
        pygame.mixer.music.load(self.musica)
        # Tocar música com pygame mixer
        pygame.mixer.music.play(loops=0)
        
        # Pegar o tempo da música
        self.tempo_reproducao()
    
    # Criar variável parado
    global parado
    parado = False
    
    # Criar função de pausar    
    def parar(self):
        # Parar a música
        pygame.mixer.music.stop()
        # Limpar a lista de reprodução
        self.lista_de_reproducao.selection_clear(ACTIVE)
        
        self.barra_status.config(text='')
        
        # Configurar o controle deslizante para zero
        self.musica_deslizante.config(value=0)
        
        # Configurar a variável parado para verdadeiro
        global parado 
        parado = True
    
    # Criar uma função para reproduzir a próxima música
    def proxima_musica(self):
        # Redefinir a posição do controle deslizante e a barra de status
        self.barra_status.config(text='')
        self.musica_deslizante.config(value=0)
        
        # Pegar o número da música atual
        self.proximo = self.lista_de_reproducao.curselection()
        # Adicionar mais um para o número da música atual tupla/lista
        self.proximo = self.proximo[0] + 1
        
        # Pegar o título do som da lista de reprodução
        self.musica = self.lista_de_reproducao.get(self.proximo)
        # Adicionar estrutura de diretório ao título da música
        # musica = f'C:/Users/Irwing Seiji Ato/Documents/IFPR/4º Semestre/Construção de Aplicações Orientada a Objetos/Trabalho 02 - Projeto da disciplina/mp3/audio/{musica}.mp3'
        self.musica = musicas_dir[self.musica]
        # Carregar música com pygame mixer
        pygame.mixer.music.load(self.musica)
        # Tocar música com pygame mixer
        pygame.mixer.music.play(loops=0)
        
        # Limpar barra ativa na lista de reprodução
        self.lista_de_reproducao.selection_clear(0, END)
        
        # Mover a barra ativa para a próxima música
        self.lista_de_reproducao.activate(self.proximo)
        
        # Definir barra ativa para a próxima música
        self.lista_de_reproducao.selection_set(self.proximo, last=None)  
    
    def musica_anterior(self):
        # Redefinir a posição do controle deslizante e a barra de status
        self.barra_status.config(text='')
        self.musica_deslizante.config(value=0)
        # Pegar o número da música atual
        self.proximo = self.lista_de_reproducao.curselection()
        # Adicionar mais um para o número da música atual tupla/lista
        self.proximo = self.proximo[0] - 1
        
        # Pegar o título do som da lista de reprodução
        self.musica = self.lista_de_reproducao.get(self.proximo)
        # Adicionar estrutura de diretório ao título da música
        self.musica = musicas_dir[self.musica]
        # Carregar música com pygame mixer
        pygame.mixer.music.load(self.musica)
        # Tocar música com pygame mixer
        pygame.mixer.music.play(loops=0)
        
        # Limpar barra ativa na lista de reprodução
        self.lista_de_reproducao.selection_clear(0, END)
        
        # Mover a barra ativa para a próxima música
        self.lista_de_reproducao.activate(self.proximo)
        
        # Definir barra ativa para a próxima música
        self.lista_de_reproducao.selection_set(self.proximo, last=None)     
    
    # Criar variável pausado
    global pausado
    pausado = False
    
    # Criar função de parar
    def pausar(self, esta_pausado):
        global pausado
        self.esta_pausado = esta_pausado
        pausado = self.esta_pausado
        
        if pausado:
            # Reproduzir de onde parou
            pygame.mixer.music.unpause()
            pausado = False
        else:
            # Pausar
            pygame.mixer.music.pause()
            pausado = True    
    
    # Criar função de volume
    def volume(self, x):
        pygame.mixer.music.set_volume(self.volume_deslizante.get())
    
    # Criar uma função para deslizar para posicionamento da música
    def deslizar(self):
        # Reconstruir a música com material de estrutura do diretório
        self.musica = self.lista_de_reproducao.get(ACTIVE)
        # musica = f'C:/Users/Irwing Seiji Ato/Documents/IFPR/4º Semestre/Construção de Aplicações Orientada a Objetos/Trabalho 02 - Projeto da disciplina/mp3/audio/{musica}.mp3'
        self.musica = musicas_dir[self.musica]    
        # Carregar música com pygame mixer
        pygame.mixer.music.load(self.musica)
        # Tocar música com pygame mixer
        pygame.mixer.music.play(loops=0, start=self.musica_deslizante.get())
    
    # Criar função para adicionar várias músicas à playlist
    def adicionar_varias_musicas(self):
        self.musicas = filedialog.askopenfilenames(initialdir='audio/', title="Escolha uma música", filetypes=(("Arquivos mp3", "*.mp3"), ))
        
        # Percorrer a lista de músicas e substituir a estrutura do diretório e mp3 do nome da música
        for self.musica in self.musicas:        
            # Retirar a estrutura de diretório e .mp3 do título de música
            self.nome = self.musica[self.musica.rfind("/") +1:]
            self.nome = self.nome.replace(".mp3", "")
                
            # Adicionar ao dicionário que mapea nome para o endereço do diretório
            musicas_dir[self.nome]=self.musica     
            
            # Adicionar ao fim da lista de reprodução    
            self.lista_de_reproducao.insert(END, self.nome)   


class Controller():
    '''Controlador é o principal coordenador no padrão MVC,
    ele coleta entrada do usuário, inicia mudanças necessárias no modelo (dados)
    e atualiza view para refletir quaisquer mudanças que poderiam ter acontecido'''
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def favoritar_musica(self):
        self.model.favoritar_musica()
    
    def favoritar_varias_musicas(self):
        self.model.favoritar_varias_musicas()    
    
    def remover_musica(self):
        self.model.remover_musica()
    
    def mostrar_favoritos(self):
        self.model.mostrar_favoritos(self)       
    
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
        
if __name__ == '__main__':
    '''Função principal, instância instâncias de Model, View e Controller'''
        
    tocador_musica_model = Model()
    tocador_musica_view = View()    
    tocador_musica_controller = Controller(model=tocador_musica_model, view=tocador_musica_view)
    tocador_musica_view.view_main()
    tocador_musica_controller.run()

