DIGITOS = ('1', '2', '3', '4', '5', '6')
N_DE_AUTOCOLANTES_POR_FACE = 4
N_DE_AUTOCOLANTES = 24
TABELA_MOVIMENTOS = ("U","U'","D","D'","L","L'","R","R'","F","F'","B","B'")
INDICES_REDE = {"U1": [0,1], "U2": [2,3], "meio1": [4,5,8,9,12,13,16,17], "meio2": [6,7,10,11,14,15,18,19], "D1": [20,21], "D2": [22,23] }  # este dicionário tem as posiçoes das varias linhas do esquema do cubo
CICLOS_MOVIMENTOS = {  # este dicionário tem três tuplos que são as posições dos autocolantes que mudam para cada movimento
    'U': ((0, 1, 3, 2),     (8, 4, 16, 12),  (9, 5, 17, 13)),
    'L': ((4, 5, 7, 6),     (0, 8, 20, 19),  (2, 10, 22, 17)),
    'F': ((8, 9, 11, 10),   (2, 12, 21, 7),  (3, 14, 20, 5)),
    'R': ((12, 13, 15, 14), (3, 16, 23, 11), (1, 18, 21, 9)),
    'B': ((16, 17, 19, 18), (1, 4, 22, 15),  (0, 6, 23, 13)),
    'D': ((20, 21, 23, 22), (10, 14, 18, 6), (11, 15, 19, 7)),
}
from cor import *
from movimento import *
def cria_cubo():
    """
    Devolve um cubo resolvido.
    
    cria_cubo: {} -> cubo
    """
    cubo = []
    for d in DIGITOS:
        cubo += [cria_cor(d)] * N_DE_AUTOCOLANTES_POR_FACE
    return cubo


def cria_cubo_de_str(s):
    """
    Recebe uma string e devolve o cubo correspondente.

    cria_cubo_de_str: str -> cubo
    Gera ValueError se o argumento for inválido
    """
    if type(s) != str or len(s) != N_DE_AUTOCOLANTES:
        raise ValueError('cria_cubo_de_str: argumentos invalidos')
    for c in s:
        if c not in DIGITOS:
            raise ValueError('cria_cubo_de_str: argumentos invalidos')
    cubo = []  # estrutura identica ao cria_cubo
    for c in s:
        cubo += [cria_cor(c)]
    return cubo


def cria_copia_cubo(cubo):
    """
    Recebe um cubo e devolve uma cópia nova do cubo.

    cria_copia_cubo: cubo -> cubo
    """
    copia_cubo = cubo[:] 
    return copia_cubo


def obtem_cor_face(cubo, s):
    """
    Recebe um cubo e uma face e devolve as cores dessa face.

    obtem_cor_face: cubo x str -> tuplo
    Gera ValueError se os argumentos forem inválidos.
    """
    if type(s) != str or s not in FACES:
        raise ValueError('obtem_cor_face: argumentos invalidos')
    f = (FACES.index(s) * N_DE_AUTOCOLANTES_POR_FACE)  # calculo as posições das faces e extraio do cubo
    return tuple(cubo[f:f + N_DE_AUTOCOLANTES_POR_FACE])


def eh_cubo(arg):
    """
    Devolve True se o argumento for um cubo

    eh_cubo: universal -> booleano
    """
    return type(arg) == list and len(arg) == N_DE_AUTOCOLANTES and all(eh_cor(c) for c in arg)

def eh_cubo_valido(cubo):
    """
    Recebe um cubo e devolve True se cada cor aparece exatamente 4 vezes.

    eh_cubo_valido: cubo -> booleano
    """
    cores = [cor_para_str(c) for f in FACES for c in obtem_cor_face(cubo, f)]
    return all(cores.count(d) == N_DE_AUTOCOLANTES_POR_FACE for d in DIGITOS)


def cubos_iguais(c1,c2):
    """
    Recebe dois universais e devolve True se forem cubos iguais.
    
    cubos_iguais: universal x universal -> booleano
    """
    return eh_cubo(c1) and eh_cubo(c2) and c1 == c2


def numero_faces_resolvidas(cubo):
    """
    Recebe um cubo e devolve o número de faces com uma única cor.
    
    numero_faces_resolvidas: cubo -> int
    """
    f_resolvidas = 0
    for face in FACES:
        cores_face = obtem_cor_face(cubo,face)
        if cores_face.count(cores_face[0]) == N_DE_AUTOCOLANTES_POR_FACE:
            f_resolvidas += 1
    return f_resolvidas


def esta_resolvido(cubo):
    """
    Recebe um cubo e devolve True se ele está resolvido.

    esta_resolvido: cubo -> booleano
    """
    return numero_faces_resolvidas(cubo) == len(FACES)


def linha_cubo(cubo,indices):  # função auxiliar para cubo_para_str
    """
    Recebe um cubo e uma lista de indices e devolve uma linha da rede.(Função auxiliar)

    linha_cubo: cubo x lista -> linha
    """
    linha = ""
    for i in indices:
        linha += f"[{cor_para_str(cubo[i])}]"
    return linha


def cubo_para_str(cubo):
    """
    Recebe um cubo e devolve a rede do cubo:
    
    cubo_para_str: cubo -> booleano
    """
    rede = " " * 6 + linha_cubo(cubo,INDICES_REDE["U1"])+ "\n" \
        +  " " * 6 + linha_cubo(cubo,INDICES_REDE["U2"])+ "\n"\
        +  linha_cubo(cubo,INDICES_REDE["meio1"])+ "\n"\
        +  linha_cubo(cubo,INDICES_REDE["meio2"])+ "\n"\
        +  " " * 6 + linha_cubo(cubo,INDICES_REDE["D1"])+ "\n"\
        +  " " * 6 + linha_cubo(cubo,INDICES_REDE["D2"])
    return rede


def roda_cubo(cubo, mov):
    """
    Recebe um cubo e um movimento, aplica esse movimento e devolve o cubo resultante.

    roda_cubo: cubo x movimento -> cubo
    """
    sentido = obtem_mov_sentido(mov)
    for ciclo in CICLOS_MOVIMENTOS[obtem_mov_face(mov)]:
        if not sentido:
            ciclo = ciclo[::-1]  # sentido anti-horário = ciclo percorrido ao contrário
        posições_antigas = [cubo[i] for i in ciclo]
        for k in range(N_DE_AUTOCOLANTES_POR_FACE):
            cubo[ciclo[(k + 1) % 4]] = posições_antigas[k]  # % 4 faz com que se k = 3 -> ciclo[0], assim a ultima posição vai para a primeira
    return cubo


def aplica_sequencia(cubo,seq):
    """
    Recebe um cubo e uma sequencia de movimentos, aplica essa sequencia e devolve o cubo resultante.
    
    aplica_sequencia: cubo x tuplo -> cubo
    """
    for mov in seq:
        cubo = roda_cubo(cubo,mov)
    return cubo


def baralha_cubo(cubo,n,semente):
    """
    Recebe um cubo, um número de movimentos e uma semente, aplica os movimentos gerados ao cubo e devolve o tuplo de movimentos.
    
    baralha_cubo: cubo x int x int -> tuplo
    Gera ValueError se os argumentos forem inválidos.
    """
    if not eh_cubo(cubo) or type(n) != int or n < 0 or type(semente) != int or not (1 <= semente <= 12):
        raise ValueError("baralha_cubo: argumentos invalidos")
    movimentos = ()
    while n:
        semente = (2 * semente) % 13
        movimentos += (str_para_movimento(TABELA_MOVIMENTOS[semente-1]),)
        n -= 1
    aplica_sequencia(cubo, movimentos)
    return movimentos

