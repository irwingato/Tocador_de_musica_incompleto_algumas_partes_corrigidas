from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3
import mysql.connector
import tkinter as tk 
import json
        
root = Tk()

root.title("Tocador de música")
root.geometry("500x450")

musicas_dir = {}

# Inicializar Pygame
pygame.mixer.init()

# Criar uma função para lidar com o tempo
def tempo_reproducao():
        # Verificar se a música está parada
        if parado:
            return
        
        # Pegar o tempo atual da música
        tempo_atual = pygame.mixer.music.get_pos() / 1000
        # Converter o tempo da música no formato de hora
        tempo_atual_convertido = time.strftime('%M:%S', time.gmtime(tempo_atual))
            
        musica = lista_de_reproducao.get(ACTIVE)         
        musica = musicas_dir[musica]
        # Achar o tamanho da música atual
        musica_mut = MP3(musica) 
        global musica_tamanho
        musica_tamanho = musica_mut.info.length
        # Converter para o formato de minutos
        musica_convertida_tamanho = time.strftime('%M:%S', time.gmtime(musica_tamanho))
        
        # Verificar se a música acabou
        if int(musica_deslizante.get()) == int(musica_tamanho):
            parar()
        
        elif pausado:
            # Verificar se está pausado, se estiver passar
            pass    
        else:    
            # Mover o controle deslizante 1 segundo por tempo
            proximo_tempo = int(musica_deslizante.get()) + 1
            
            # Saída para o novo valor de tempo do controle deslizante, e a duração da música
            musica_deslizante.config(to=musica_tamanho, value=proximo_tempo)
            
            # Converter o controle deslizante no formato de minutos        
            tempo_atual_convertido = time.strftime('%M:%S', time.gmtime(int(musica_deslizante.get())))
            
            # Saída do controle deslizante
            barra_status.config(text=f'Tempo Decorrido: {tempo_atual_convertido} of {musica_convertida_tamanho}  ')
                    
        # Adicionar o tempo atual a barra de status
        if tempo_atual >= 1:
            barra_status.config(text=f'Tempo Decorrido: {tempo_atual_convertido} of {musica_convertida_tamanho}  ')
        
        # Criar uma repetição para verificar os minutos a cada segundo
        barra_status.after(1000, tempo_reproducao) 

# Criar função para adicionar uma música para a playlist
def adicionar_musica():
    musica = filedialog.askopenfilename(initialdir='audio/', title="Escolha uma música", filetypes=(("Arquivos mp3", "*.mp3"), ))
    # Retirar a estrutura de diretório e .mp3 do título de música
    nome = musica[musica.rfind("/") +1:]
    nome = nome.replace(".mp3", "")
        
    # Adicionar ao dicionário que mapea nome para o endereço do diretório
    musicas_dir[nome]=musica    
    
    # Adicionar ao fim da lista de reprodução
    lista_de_reproducao.insert(END, nome)

def adicionar_varias_musicas():
    musicas = filedialog.askopenfilenames(initialdir='audio/', title="Escolha uma música", filetypes=(("Arquivos mp3", "*.mp3"), ))
        
    # Percorrer a lista de músicas e substituir a estrutura do diretório e mp3 do nome da música
    for musica in musicas:        
        # Retirar a estrutura de diretório e .mp3 do título de música
        nome = musica[musica.rfind("/") +1:]
        nome = nome.replace(".mp3", "")
        # Adicionar ao dicionário que mapea nome para o endereço do diretório
        musicas_dir[nome]=musica   
        # Adicionar ao fim da lista de reprodução    
        lista_de_reproducao.insert(END, nome)

# Criar uma função para excluir uma música da lista de reprodução
def excluir_musica():
    # Excluir música selecionada da lista de reprodução
    lista_de_reproducao.delete(ANCHOR)

# Criar uma função para favoritar uma música e salvar
def favoritar_musica():
    # Adicionar a música na lista de favoritos
    musica = lista_de_reproducao.get(ACTIVE)
    # Favoritar uma música selecionada na lista
    cnx = mysql.connector.connect(user='root',password='AaZz$#!@1', host='127.0.0.1', database='Favoritos')
    cursor = cnx.cursor()
    query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
    valores = (musica) 
    
    try:
        # Executar a query e atualizar a mudanças no banco de dados
        cursor.execute(query, (valores,))
        cnx.commit()
    
    except mysql.connector.errors.IntegrityError:
        # Inferir o erro caso o id_musica já está na tabela de favoritos
        print('Erro: O ID da música já está em favoritos')   

def favoritar_todas_musicas():
    cursor = cnx.cursor()
    cnx = mysql.connector.connect(user='root',password='AaZz$!@#1', host='127.0.0.1', database='Favoritos')
    musicas = [lista_de_reproducao.get(i) for i in lista_de_reproducao.curselection()]
    for musica in musicas:
        # Usar um INSERT INTO query para adicionar uma nova linha na tabela favoritos
        query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
        valores = (musicas)  
        
    try:
        # Executar a query e atualizar as mudanças para o banco de dados
        cursor.execute(query, (valores,))
        cnx.commit()
    except mysql.connector.errors.IntegrityError:
        # Lidar com o erro de ID_musica que já está na tabela de favoritos
        print(f'Erro: ID música {musica["ID_musica"]} já está nos favoritos') 

# Criar uma função para favoritar uma música e salvar
def favoritar_musica():
# Adicionar a música na lista de favoritos
    musica = lista_de_reproducao.get(ACTIVE)
    # Favoritar uma música selecionada na lista
    cnx = mysql.connector.connect(user='root',password='AaZz$#!@1', host='127.0.0.1', database='Favoritos')
    cursor = cnx.cursor()
    query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
    valores = (musica) 
        
    try:
    # Executar a query e atualizar a mudanças no banco de dados
        cursor.execute(query, (valores,))
        cnx.commit()
        
    except mysql.connector.errors.IntegrityError:
        # Inferir o erro caso o id_musica já está na tabela de favoritos
        print('Erro: O ID da música já está em favoritos')

def favoritar_todas_musicas():
    cnx = mysql.connector.connect(user='root',password='AaZz$#!@1', host='127.0.0.1', database='Favoritos')
    cursor = cnx.cursor()
    musicas = [lista_de_reproducao.get(i) for i in lista_de_reproducao.curselection()]
    for musica in musicas:
    # Usar um INSERT INTO query para adicionar uma nova linha na tabela favoritos
        query = 'INSERT INTO Favoritos (nome) VALUES (%s)'
        valores = (musica) 
    
    try:
        # Executar a query e atualizar as mudanças para o banco de dados
        cursor.execute(query, (valores,))
        cnx.commit()
    except mysql.connector.errors.IntegrityError:
        # Lidar com o erro de ID_musica que já está na tabela de favoritos
        print(f'Erro: ID música {musica["ID_musica"]} já está nos favoritos') 

def mostrar_favoritos():
    # Create the favorite songs window
    favoritos_janela = Toplevel(root)
    favoritos_janela.title("Músicas favoritas")

    # Criar uma Listbox widget para mostrar as músicas favoritas em uma janela
    janela_favoritos_listbox = Listbox(favoritos_janela)
    janela_favoritos_listbox.pack()
    janela_favoritos_listbox.configure(height=30, width=80)

    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='AaZz$#!@1',
        host='127.0.0.1', database='Favoritos')
    cursor = cnx.cursor()

    # Definir um query de seleção
    query = "SELECT nome FROM Favoritos"

    # Executar a query de seleção
    cursor.execute(query)

    #  Buscar as linhas do conjunto de resultados
    linhas = cursor.fetchall()

    # Preencher a caixa de listagem com músicas favoritas
    for musica in linhas:
        janela_favoritos_listbox.insert(END, musica[0])
    
     
    # Criar um botão widget para permitir o usuário remover uma música da Listbox
    remover_botão = Button(favoritos_janela, text="Remover Música", command=remover_musica, bg="#51e2f5")
    remover_botão.pack()      

# Definir uma função para remover a música selecionada da caixa da Listbox
def remover_musica():    
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='AaZz$#!@1',
            host='127.0.0.1', database='Favoritos')
    cursor = cnx.cursor()
    musica_selecionada = janela_favoritos_listbox.curselection()
    nome = janela_favoritos_listbox.get(ACTIVE)
    valor = (nome)
    query = 'DELETE FROM Favoritos WHERE nome = %s'
    cursor.execute(query,(valor,))
    cnx.commit()
    if musica_selecionada:
        janela_favoritos_listbox.delete(musica_selecionada[0])   

# Criar uma função para excluir todas as músicas de uma lista de reprodução
def excluir_todas_musicas():
    # Excluir todas as músicas
    lista_de_reproducao.delete(0, END)

# Criar Função reproduzir
def reproduzir():
    # Configurar parado para falso desde que a música está tocando agora
    global parado
    parado = False  
        
    # Reconstruir a música com material de estrutura do diretório
    musica = musicas_dir[lista_de_reproducao.get(ACTIVE)] 
        
    # Carregar música com pygame mixer
    pygame.mixer.music.load(musica)
    # Tocar música com pygame mixer
    pygame.mixer.music.play(loops=0)
    
    # Pegar o tempo da música
    tempo_reproducao()

# Criar variável parado
global parado
parado = False
# Criar função de pausar    
def parar():
    # Parar a música
    pygame.mixer.music.stop()
    # Limpar a lista de reprodução
    lista_de_reproducao.selection_clear(ACTIVE)
    
    barra_status.config(text='')
    
    # Configurar o controle deslizante para zero
    musica_deslizante.config(value=0)
    
    # Configurar a variável parado para verdadeiro
    global parado 
    parado = True

# Criar uma função para reproduzir a próxima música
def proxima_musica():
    # Redefinir a posição do controle deslizante e a barra de status
    barra_status.config(text='')
    musica_deslizante.config(value=0)
    
    # Pegar o número da música atual
    proximo = lista_de_reproducao.curselection()
    # Adicionar mais um para o número da música atual tupla/lista
    proximo = proximo[0] + 1
    
    # Pegar o título do som da lista de reprodução
    musica = lista_de_reproducao.get(proximo)
    # Adicionar estrutura de diretório ao título da música
    musica = musicas_dir[musica]
    # Carregar música com pygame mixer
    pygame.mixer.music.load(musica)
    # Tocar música com pygame mixer
    pygame.mixer.music.play(loops=0)
    
    # Limpar barra ativa na lista de reprodução
    lista_de_reproducao.selection_clear(0, END)
    
    # Mover a barra ativa para a próxima música
    lista_de_reproducao.activate(proximo)
    
    # Definir barra ativa para a próxima música
    lista_de_reproducao.selection_set(proximo, last=None)

def musica_anterior():
    # Redefinir a posição do controle deslizante e a barra de status
    barra_status.config(text='')
    musica_deslizante.config(value=0)
    # Pegar o número da música atual
    proximo = lista_de_reproducao.curselection()
    # Adicionar mais um para o número da música atual tupla/lista
    proximo = proximo[0] - 1
    
    # Pegar o título do som da lista de reprodução
    musica = lista_de_reproducao.get(proximo)
    # Adicionar estrutura de diretório ao título da música
    musica = musica = musicas_dir[musica] 
    # Carregar música com pygame mixer
    pygame.mixer.music.load(musica)
    # Tocar música com pygame mixer
    pygame.mixer.music.play(loops=0)
    
    # Limpar barra ativa na lista de reprodução
    lista_de_reproducao.selection_clear(0, END)
    
    # Mover a barra ativa para a próxima música
    lista_de_reproducao.activate(proximo)
    
    # Definir barra ativa para a próxima música
    lista_de_reproducao.selection_set(proximo, last=None)

# Criar variável pausado
global pausado
pausado = False

# Criar função de parar
def pausar(esta_pausado):
    global pausado
    pausado = esta_pausado
    
    if pausado:
        # Reproduzir de onde parou
        pygame.mixer.music.unpause()
        pausado = False
    else:
        # Pausar
        pygame.mixer.music.pause()
        pausado = True    

# Criar função de volume
def volume(x):
    pygame.mixer.music.set_volume(volume_deslizante.get())

# Criar uma função para deslizar para posicionamento da música
def deslizar(x):
    # Reconstruir a música com material de estrutura do diretório
    musica = lista_de_reproducao.get(ACTIVE)
    musica = musicas_dir[musica]         
    # Carregar música com pygame mixer
    pygame.mixer.music.load(musica)
    # Tocar música com pygame mixer
    pygame.mixer.music.play(loops=0, start=musica_deslizante.get())

# Criar um objeto PhotoImage a partir do arquivo de imagem
icone_imagem = PhotoImage(file="logo.png")

root.title("Tocador de música")
root.geometry("500x450")

# Criar quadro principal
quadro_principal = Frame(root)
quadro_principal.pack(pady=20)

# Criar quadro de volume deslizante
quadro_volume = LabelFrame(quadro_principal, text="Volume")
quadro_volume.grid(row=0, column=1, padx=20)

# Criar controle deslizante de volume
volume_deslizante = ttk.Scale(quadro_volume, from_=100, to=0, orient=VERTICAL, length=125, value=1, command=volume)
volume_deslizante.pack(pady=10)

# Criar controle deslizante de música
musica_deslizante = ttk.Scale(quadro_principal, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=deslizar)
musica_deslizante.grid(row=2, column=0, pady=20)
        
# Criar caixa de playlist
lista_de_reproducao = Listbox(quadro_principal, selectmode="extended", bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
lista_de_reproducao.grid(row=0, column=0)

# Definindo imagens de botões para controles
botao_voltar_img = PhotoImage(file='images/previous.png')
avancar_botao_img = PhotoImage(file='images/next-button.png')
reproduzir_botao_img = PhotoImage(file='images/play-button.png')
pausar_botao_img = PhotoImage(file='images/pause-button.png')
parar_botao_img =  PhotoImage(file='images/stop-button.png')

# Criar um botão de frame
controle_quadro = Frame(quadro_principal)
controle_quadro.grid(row=1, column=0, pady=20)

# Criar botões Reproduzir/Parar 
botao_voltar = Button(controle_quadro, image=botao_voltar_img, borderwidth=0, command=musica_anterior)
avancar_botao = Button(controle_quadro, image=avancar_botao_img, borderwidth=0, command=proxima_musica)
reproduzir_botao = Button(controle_quadro, image=reproduzir_botao_img, borderwidth=0, command=reproduzir)
pausar_botao = Button(controle_quadro, image=pausar_botao_img, borderwidth=0, command=lambda: pausar(pausado))
parar_botao = Button(controle_quadro, image=parar_botao_img, borderwidth=0, command=parar)

botao_voltar.grid(row=0, column=0, padx=10)
avancar_botao.grid(row=0, column=1, padx=10)
reproduzir_botao.grid(row=0, column=2, padx=10)
pausar_botao.grid(row=0, column=3, padx=10)
parar_botao.grid(row=0, column=4, padx=10)

# Criar Menu Principal
meu_menu = Menu(root)
root.config(menu=meu_menu)

# Criar Menu Adicionar Som em lista suspensa 
adicionar_musica_menu = Menu(meu_menu, tearoff=0)
meu_menu.add_cascade(label="Adicionar Músicas", menu=adicionar_musica_menu)
# Adicionar uma música para a playlist
adicionar_musica_menu.add_command(label="Adicionar uma música para a playlist", command=adicionar_musica)
# Adicionar várias músicas
adicionar_musica_menu.add_command(label="Adicionar várias músicas para playlist", command=adicionar_varias_musicas)

# Criar menu suspensos de exclusão de música
remover_musica_menu = Menu(meu_menu, tearoff=0)
meu_menu.add_cascade(label="Remover músicas", menu=remover_musica_menu)
remover_musica_menu.add_command(label="Excluir uma música da lista de reprodução", command=excluir_musica)
remover_musica_menu.add_command(label="Excluir todas as músicas da lista de reprodução", command=excluir_todas_musicas)

# Criar menu suspensos para adicionar música favoritas
favoritar_musica_menu = Menu(meu_menu, tearoff=0)
meu_menu.add_cascade(label="Salvar aos favoritos", menu=favoritar_musica_menu)
favoritar_musica_menu.add_command(label="Adicionar uma música aos favoritos", command=favoritar_musica)
favoritar_musica_menu.add_command(label="Adicionar todas as músicas aos favoritos", command=favoritar_todas_musicas)

# Criar barra de status
barra_status = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
barra_status.pack(fill=X, side=BOTTOM, ipady=2)

# Criar um widget botão de verificar que permita que o usuário mostre ou esconda a lista de músicas favoritas
mostrar_favoritos_verificar = Button(root, text="Mostrar músicas favoritas", command=mostrar_favoritos, bg="#51e2f5")
mostrar_favoritos_verificar.place(x = 150, y = 350)

favoritos_listbox = Listbox(quadro_principal, selectmode="extended", bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")

mostrar_favoritos = IntVar()   

# Definir o ícone da janela para a imagem
root.iconphoto(True, icone_imagem)

root.mainloop()

