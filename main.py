import tkinter.messagebox
from tkinter import *
from random import *

# TODO 02: Criar um botao para apontar as bombas (ativar e desativar a bandeira)
# TODO 03: Criar modo de vencer após apontar todas a bombas
# TODO 05: Criar registro de pontuação com pandas (nome, pontuação, data, hora)


def inicio():
    janela_inicial.destroy()
    nivel = var.get()
    janela = Tk()
    janela.title("CAMPO MINADO")
    janela.config(height=200, width=500, padx=50, pady=50)

    # Quantidade de linhas e colunas de acordo com a dicficuldade
    if nivel == 1:
        LINHAS = 10
        COLUNAS = 10
    elif nivel == 2:
        LINHAS = 10
        COLUNAS = 20
    else:
        LINHAS = 13
        COLUNAS = 25

    # Criação de uma lista onde serão aleatoriamente indicadas as posições das bombas
    lista_bombas = []
    qnt = 0
    for _ in range(LINHAS * COLUNAS):
        num = randint(0, 9)
        if num == 1:
            lista_bombas.append(TRUE)
            qnt += 1
        else:
            lista_bombas.append(FALSE)

    tela = Canvas(height=80, width=COLUNAS * 38, bg="#ff9900", highlightthickness=0)
    tela.grid(row=0, column=0, columnspan=COLUNAS)
    info_1 = tela.create_text(165, 15, text=f"Tamanho do campo minado = {LINHAS}x{COLUNAS}", font=("Arial", 15))
    # TODO 01: Mostrar quantidade de bombas no início (variavel qnt definida no final)
    info_2 = tela.create_text(120, 40, text=f"Quantidade de minas = {qnt}", font=("Arial", 15))

    espaco = Label(height=1)
    espaco.grid(row=1, column=0, columnspan=10)

    bomba = PhotoImage(file="venv/bomba.png").subsample(3)
    flag = PhotoImage(file="venv/flag.png").subsample(7)

    # //////////////////////////// Menssagem de GAMEOVER e reinicio \\\\\\\\\\\\\\\\\\\\\\\\\
    def show_message(r):
        tkinter.messagebox.showwarning(title="GAME OVER", message="You Lost! Click Ok to restart.")
        for i in range(LINHAS * COLUNAS):
            campo = lista[i]
            campo.destroy()
        start(r)

    # /////////////// Campo clicado, vai verificar se há bomba e, caso negativo, verificar quantas ao redor \\\\\\\\\\\\
    def clicado(r):

        if lista_bombas[r] == 1:  # Há bomba!!
            lista[r].destroy()
            label_bomba = Label(image=bomba, bg="red")
            # Seleção da linha e coluna onde está a bomba - O FOR LOOP abaixo faz isto que está comentado mais abaixo:
            for j in range(0, LINHAS):
                if r < COLUNAS * (j + 1):
                    label_bomba.grid(row=(j + 2), column=r - j * COLUNAS)
                    show_message(r)
                    break
            # if r < COLUNAS-1:
            #     label_bomba.grid(row=1, column=r)
            # elif r < COLUNAS*2-1:
            #     label_bomba.grid(row=2, column=r-COLUNAS)
            # elif r < COLUNAS*3-1:
            #     label_bomba.grid(row=3, column=r-2*COLUNAS)
            # elif r < COLUNAS*4-1:
            #     label_bomba.grid(row=4, column=r-3*COLUNAS)
            # ...

        else:  # Não há bomba!
            def testar_arredores(r):
                n = 0
                # Todos os quadrados que não pertencem a primeira e a ultima LINHAS:
                if r > COLUNAS - 1 and r < (LINHAS - 1) * COLUNAS:
                    if lista_bombas[r + COLUNAS]: n += 1
                    if lista_bombas[r - COLUNAS]: n += 1
                    if (r + 1) % COLUNAS != 0:  # Se não for a ultima coluna
                        if lista_bombas[r + COLUNAS + 1]: n += 1
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r - COLUNAS + 1]: n += 1
                    if r % COLUNAS != 0:  # Se não for a primeira coluna
                        if lista_bombas[r - COLUNAS - 1]: n += 1
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r + COLUNAS - 1]: n += 1
                elif r < COLUNAS:  # Agora, na primeira linha
                    if lista_bombas[r + COLUNAS]: n += 1
                    if r != COLUNAS - 1:
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r + COLUNAS + 1]: n += 1
                    if r != 0:
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r + COLUNAS - 1]: n += 1
                else:  # Por fim, na ultima linha
                    if lista_bombas[r - COLUNAS]: n += 1
                    if r != LINHAS * COLUNAS - 1:
                        if lista_bombas[r + 1]: n += 1
                        if lista_bombas[r - COLUNAS + 1]: n += 1
                    if r != (LINHAS - 1) * COLUNAS:
                        if lista_bombas[r - 1]: n += 1
                        if lista_bombas[r - COLUNAS - 1]: n += 1
                return n

            n = testar_arredores(r)
            if n == 0:  # Abrir quadrado ao redor do 0.
                # Todos os quadrados que não pertencem a primeira e a ultima LINHAS:
                if r > COLUNAS - 1 and r < (LINHAS - 1) * COLUNAS:
                    n = testar_arredores(r + COLUNAS)
                    lista[r + COLUNAS].config(state="disabled", bg="light gray", text=n)
                    n = testar_arredores(r - COLUNAS)
                    lista[r - COLUNAS].config(state="disabled", bg="light gray", text=n)
                    if (r + 1) % COLUNAS != 0:  # Se não for a ultima coluna
                        n = testar_arredores(r + COLUNAS + 1)
                        lista[r + COLUNAS + 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r - COLUNAS + 1)
                        lista[r - COLUNAS + 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r + 1)
                        lista[r + 1].config(state="disabled", bg="light gray", text=n)
                    if r % COLUNAS != 0:  # Se não for a primeira coluna
                        n = testar_arredores(r - COLUNAS - 1)
                        lista[r - COLUNAS - 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r - 1)
                        lista[r - 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r + COLUNAS - 1)
                        lista[r + COLUNAS - 1].config(state="disabled", bg="light gray", text=n)
                elif r < COLUNAS:  # Agora, na primeira linha
                    n = testar_arredores(r + COLUNAS)
                    lista[r + COLUNAS].config(state="disabled", bg="light gray", text=n)
                    if r != COLUNAS - 1:
                        n = testar_arredores(r + COLUNAS + 1)
                        lista[r + COLUNAS + 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r + 1)
                        lista[r + 1].config(state="disabled", bg="light gray", text=n)
                    if r != 0:
                        n = testar_arredores(r - 1)
                        lista[r - 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r + COLUNAS - 1)
                        lista[r + COLUNAS - 1].config(state="disabled", bg="light gray", text=n)
                else:  # Por fim, na ultima linha
                    n = testar_arredores(r - COLUNAS)
                    lista[r - COLUNAS].config(state="disabled", bg="light gray", text=n)
                    if r != LINHAS * COLUNAS - 1:
                        n = testar_arredores(r + 1)
                        lista[r + 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r - COLUNAS + 1)
                        lista[r - COLUNAS + 1].config(state="disabled", bg="light gray", text=n)
                    if r != (LINHAS - 1) * COLUNAS:
                        n = testar_arredores(r - 1)
                        lista[r - 1].config(state="disabled", bg="light gray", text=n)
                        n = testar_arredores(r - COLUNAS - 1)
                        lista[r - COLUNAS - 1].config(state="disabled", bg="light gray", text=n)
                lista[r].config(state="disabled", bg="light gray", text=0)

            else:
                lista[r].config(state="disabled", bg="light gray", text=n)

    r = 0

    def start(r):
        global lista
        lista = []
        for i in range(LINHAS):
            for j in range(COLUNAS):
                botao = Button(height=2, width=4, bg="green", text=r, fg="green",
                               command=lambda c=r: clicado(lista[c].cget("text")))
                botao.grid(row=i + 2,
                           column=j)  # Row era mais 1, mas ficou mais 2 por causa das infos em cima dos quadrados

                r += 1
                lista.append(botao)

    start(r)
    janela.mainloop()

# TODO 04: Criar modo de dificuldade diferentes (tamanho e quantidade de bombas)
#//////////////////////// INICIALIZAÇÃO DO PROGRAMA COM A JANELA DE ESCOLHA DA DIFICULDADE \\\\\\\\\\\\\\\\\

janela_inicial = Tk()
janela_inicial.title("Início")
janela_inicial.config(pady=5, padx=5)
janela_inicial.minsize(height=100, width=220, )
janela_inicial_menssagem = Label(text="        Escolha a dificuldade:")
janela_inicial_menssagem.grid(row=0, column=0)

var = IntVar()   #IntVar serve para utilizar a variavel var fora dos botões
var.set(1)
facil = Radiobutton(text="Fácil                ", variable=var, value=1) #Os espaços são para alinhar o texto
facil.grid(row=1, column=0)
medio = Radiobutton(text="Intermediário", variable=var, value=2)
medio.grid(row=2, column=0)
dificil = Radiobutton(text="Difícil              ", variable=var, value=3)
dificil.grid(row=3, column=0)
ok_button = Button(text= "Começar!",padx=5,pady=5, command=inicio).grid(row=4,column=1)


janela_inicial.mainloop()
