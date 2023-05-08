import tkinter.messagebox
from tkinter import *
from random import *
import json
import datetime as dt


# TODO 03: Criar modo de vencer após apontar todas a bombas
# TODO 05: Criar registro de pontuação com pandas (nome, pontuação, data, hora e colocar na ordem decrescente)
import registro_pontos

dia = dt.datetime.now().day
mes = dt.datetime.now().month
ano = dt.datetime.now().year
data_hoje = f'{dia}/{mes}/{ano}'

def iniciar():
    jogador = inserir_nome.get()
    janela_inicial.destroy()
    nivel = var.get()
    janela = Tk()
    janela.title("CAMPO MINADO")
    janela.config(height=200, width=500, padx=50, pady=50)

    # Quantidade de linhas e colunas conforme a dificuldade
    if nivel == 1:
        linhas = 10
        colunas = 10
    elif nivel == 2:
        linhas = 10
        colunas = 20
    else:
        linhas = 13
        colunas = 25

    tela = Canvas(height=110, width=colunas * 38, bg="#ff9900", highlightthickness=0)
    tela.grid(row=0, column=0, columnspan=colunas)
    tela.create_text(131, 15, text=f"Tamanho do campo minado = {linhas}x{colunas}", font=("Arial", 12))
    global info_3
    info_3 = tela.create_text(133, 65, text='Quantidade de minas exploradas = 0', font=('Arial', 12))
    tela.create_text(189, 88, text='Clique com botão direito para marcar campo minado', font=('Arial', 12))

    espaco = Label(height=1)
    espaco.grid(row=1, column=0, columnspan=10)

    bomba = PhotoImage(file="venv/bomba.png").subsample(3)
    flag = PhotoImage(file="venv/flag.png").subsample(6)

    # //////////////////////////// Menssagem de GAMEOVER e reinicio \\\\\\\\\\\\\\\\\\\\\\\\\

    def show_message(r):
        recordista, pontos = registro_pontos.registrar(jogador, desativadas, data_hoje)
        tkinter.messagebox.showwarning(title="GAME OVER", message=f"{jogador}, Voce perdeu!\nSua pontuação: {desativadas} \nO recorde é de {recordista}, com {pontos} pontos")
        for i in range(linhas * colunas):
            campo = lista[i]
            campo.destroy()
        global info_2
        tela.delete(info_2)

        start(0)

    # TODO 02: Criar um botao para apontar as bombas (ativar e desativar a bandeira)
    # /////////////// Campo clicado com botão direito do mouse, para marcar possivel bomba \\\\\\\\\\\\

    def right_click(event):
        if event.widget.cget('state') != "disabled":
            if event.widget.cget("background") == 'green':

                # Aqui há algo importante: tive que determinar uma altura e largura muito grande para o botao,
                # para ficar normal.
                # No else, abaixo, quando tirei a imagem, determinei a altura original, bem menor.
                event.widget.configure(bg='white', relief='groove', fg='white', height=27, width=27, image=flag,
                                       compound='center')
            else:
                event.widget.configure(bg='green', fg='green', height=18, width=28, image='')

    # /////////////// Campo clicado, vai verificar se há bomba e, caso negativo, verificar quantas ao redor \\\\\\\\\\\\

    def clicado(r):
        if lista[r].cget('bg') == 'white':
            pass
        elif lista_bombas[r] == 1:  # Há bomba!!
            lista[r].destroy()
            label_bomba = Label(image=bomba)
            # Seleção da linha e coluna onde está a bomba. O FOR LOOP abaixo faz isto que está comentado mais abaixo:
            for j in range(0, linhas):
                if r < colunas * (j + 1):
                    label_bomba.grid(row=(j + 2), column=r - j * colunas)
                    show_message(r)
                    break
            # if r < colunas-1:
            #     label_bomba.grid(row=1, column=r)
            # elif r < colunas*2-1:
            #     label_bomba.grid(row=2, column=r-colunas)
            # elif r < colunas*3-1:
            #     label_bomba.grid(row=3, column=r-2*colunas)
            # elif r < colunas*4-1:
            #     label_bomba.grid(row=4, column=r-3*colunas)
            # ...

        else:  # Não há bomba!
            def testar_arredores(r):
                n = 0
                # Todos os quadrados que não pertencem a primeira e a última linhas:
                if colunas - 1 < r < (linhas - 1) * colunas:
                    if lista_bombas[r + colunas]: n += 1
                    if lista_bombas[r - colunas]: n += 1
                    if (r + 1) % colunas != 0:  # Se não for a última coluna
                        if lista_bombas[r + colunas + 1]: n += 1
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r - colunas + 1]: n += 1
                    if r % colunas != 0:  # Se não for a primeira coluna
                        if lista_bombas[r - colunas - 1]: n += 1
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r + colunas - 1]: n += 1
                elif r < colunas:  # Agora, na primeira linha
                    if lista_bombas[r + colunas]: n += 1
                    if r != colunas - 1:
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r + colunas + 1]: n += 1
                    if r != 0:
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r + colunas - 1]: n += 1
                else:  # Por fim, na última linha
                    if lista_bombas[r - colunas]: n += 1
                    if r != linhas * colunas - 1:
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r - colunas + 1]: n += 1
                    if r != (linhas - 1) * colunas:
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r - colunas - 1]: n += 1
                return n

            n = testar_arredores(r)

            if n == 0:  # Abrir quadrado ao redor do 0.
                # Todos os quadrados que não pertencem a primeira e a última linhas:
                if r > colunas - 1 and r < (linhas - 1) * colunas:
                    if lista[r + colunas].cget('bg') == 'green':
                        n = testar_arredores(r + colunas)
                        lista[r + colunas].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                  font=('Arial', 8), highlightthickness=0)
                    if lista[r - colunas].cget('bg') == 'green':
                        n = testar_arredores(r - colunas)
                        lista[r - colunas].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                  font=('Arial', 8), highlightthickness=0)
                    if (r + 1) % colunas != 0:  # Se não for a última coluna
                        if lista[r + colunas + 1].cget('bg') == 'green':
                            n = testar_arredores(r + colunas + 1)
                            lista[r + colunas + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                        if lista[r - colunas + 1].cget('bg') == 'green':
                            n = testar_arredores(r - colunas + 1)
                            lista[r - colunas + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                        if lista[r + 1].cget('bg') == 'green':
                            n = testar_arredores(r + 1)
                            lista[r + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                    if r % colunas != 0:  # Se não for a primeira coluna
                        if lista[r - colunas - 1].cget('bg') == 'green':
                            n = testar_arredores(r - colunas - 1)
                            lista[r - colunas - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                        if lista[r - 1].cget('bg') == 'green':
                            n = testar_arredores(r - 1)
                            lista[r - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                        if lista[r + colunas - 1].cget('bg') == 'green':
                            n = testar_arredores(r + colunas - 1)
                            lista[r + colunas - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                elif r < colunas:  # Agora, na primeira linha
                    if lista[r + colunas].cget('bg') == 'green':
                        n = testar_arredores(r + colunas)
                        lista[r + colunas].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                  font=('Arial', 8), highlightthickness=0)
                    if r != colunas - 1:
                        if lista[r + colunas + 1].cget('bg') == 'green':
                            n = testar_arredores(r + colunas + 1)
                            lista[r + colunas + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                        if lista[r + 1].cget('bg') == 'green':
                            n = testar_arredores(r + 1)
                            lista[r + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                    if r != 0:
                        if lista[r - 1].cget('bg') == 'green':
                            n = testar_arredores(r - 1)
                            lista[r - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                        if lista[r + colunas - 1].cget('bg') == 'green':
                            n = testar_arredores(r + colunas - 1)
                            lista[r + colunas - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                else:  # Por fim, na última linha
                    if lista[r - colunas].cget('bg') == 'green':
                        n = testar_arredores(r - colunas)
                        lista[r - colunas].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                  font=('Arial', 8), highlightthickness=0)
                    if r != linhas * colunas - 1:
                        if lista[r + 1].cget('bg') == 'green':
                            n = testar_arredores(r + 1)
                            lista[r + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                        if lista[r - colunas + 1].cget('bg') == 'green':
                            n = testar_arredores(r - colunas + 1)
                            lista[r - colunas + 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                    if r != (linhas - 1) * colunas:
                        if lista[r - 1].cget('bg') == 'green':
                            n = testar_arredores(r - 1)
                            lista[r - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                font=('Arial', 8), highlightthickness=0)
                        if lista[r - colunas - 1].cget('bg') == 'green':
                            n = testar_arredores(r - colunas - 1)
                            lista[r - colunas - 1].config(height=2, width=5, state="disabled", bg="light gray", text=n,
                                                          font=('Arial', 8), highlightthickness=0)
                if lista[r].cget('bg') == 'green':
                    lista[r].config(height=2, width=5, state="disabled", bg="light gray", text=n, font=('Arial', 8),
                                    highlightthickness=0)
            else:
                if lista[r].cget('bg') == 'green':
                    lista[r].config(height=2, width=5, state="disabled", bg="light gray", text=n, font=('Arial', 8),
                                    highlightthickness=0)

        # ////////////////////////// CONTAGEM DE CAMPOS JA CLICADOS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        global desativadas
        desativadas = 0
        global info_3
        for i in lista:
            if i.cget('state') == 'disabled':
                desativadas += 1
        tela.delete(info_3)
        info_3 = tela.create_text(134, 65, text=f'Quantidade de minas exploradas = {desativadas}',
                                  font=('Arial', 12))

    r = 0

    def start(r):
        # Criação de uma lista onde serão aleatoriamente indicadas as posições das bombas
        global lista_bombas
        lista_bombas = []
        global qnt
        qnt = 0
        for _ in range(linhas * colunas):
            num = randint(0, 9)
            if num == 1:
                lista_bombas.append(TRUE)
                qnt += 1
            else:
                lista_bombas.append(FALSE)
        # TODO 01: Mostrar quantidade de bombas no início (variavel qnt definida no final)
        global info_2
        info_2 = tela.create_text(94, 40, text=f"Quantidade de minas = {qnt}", font=("Arial", 12))

        # //////////////////////////// Criação dos campos  \\\\\\\\\\\\\\\\\\\\\\\\\\\\

        global lista
        lista = []
        for i in range(linhas):
            for j in range(colunas):
                botao = Button(height=18, width=28, relief='groove', bg="green", text=r, font=('Arial', 1), fg="green",
                               command=lambda c=r: clicado(lista[c].cget("text")))
                botao.grid(row=i + 2,
                           column=j)  # Row era mais 1, mas ficou mais 2 por causa das infos em cima dos quadrados
                botao.bind("<Button-3>", right_click)
                r += 1
                lista.append(botao)

    start(r)
    janela.mainloop()


# TODO 04: Criar modo de dificuldade diferentes (tamanho e quantidade de bombas)
# //////////////////////// INICIALIZAÇÃO DO PROGRAMA COM A JANELA DE ESCOLHA DA DIFICULDADE \\\\\\\\\\\\\\\\\

janela_inicial = Tk()

janela_inicial.title("Início")
janela_inicial.config(pady=5, padx=5)
janela_inicial.minsize(height=100, width=220, )
janela_inicial_menssagem = Label(text="        Escolha a dificuldade:")
janela_inicial_menssagem.grid(row=0, column=0)

var = IntVar()  # IntVar serve para utilizar a variavel var fora dos botões
var.set(1)
facil = Radiobutton(text="Fácil                ", variable=var, value=1)  # Os espaços são para alinhar o texto
facil.grid(row=1, column=0)
medio = Radiobutton(text="Intermediário", variable=var, value=2)
medio.grid(row=2, column=0)
dificil = Radiobutton(text="Difícil              ", variable=var, value=3)
dificil.grid(row=3, column=0)

def eliminar_texto(event):
    inserir_nome.delete(0,"end")

inserir_nome = Entry(width=20)
inserir_nome.insert(0, "Insira seu nome")
inserir_nome.grid(row=4,column=0, columnspan=1)
inserir_nome.bind('<FocusIn>', eliminar_texto)


ok_button = Button(text="Começar!", padx=5, pady=5, command=iniciar).grid(row=5, column=1)

janela_inicial.mainloop()
