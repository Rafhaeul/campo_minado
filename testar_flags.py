
def verificar(lista_bombas,lista_flag):
    lista_verificada=[]
    for i in range(len(lista_flag)):
        lista_verificada.append(lista_flag[i] == lista_bombas[i])
    if False not in lista_verificada:
        return True
