FACES = ('U', 'L', 'F', 'R', 'B', 'D')  # tuplo com as seis faces do cubo
MOVIMENTOS_SENTIDO_INVERSO = ("U'", "L'", "F'", "R'", "B'", "D'") 

def cria_movimento(f,s):
    """
    Recebe uma face e um sentido e devolve um movimento.
    
    cria_movimento: str x booleano -> movimento
    Gera ValueError se os argumentos forem inválidos.
    """
    if type(f) != str or f not in FACES or type(s) != bool:     
        raise ValueError('cria_movimento: argumentos invalidos')
    return ('mov',f,s)


def eh_movimento(m):
    """
    Recebe um universal e devolve True se o argumento for um movimento.

    eh_movimento: universal -> booleano
    """
    return type(m) == tuple and len(m) == 3 and m[0] == 'mov' and type(m[1]) == str and m[1] in FACES and type(m[2]) == bool



def obtem_mov_face(m):
    """
    Recebe um movimento e devolve a face.
    
    obtem_mov_face: movimento -> str
    """
    return m[1]


def obtem_mov_sentido(m):
    """
    Recebe um movimento e devolve um sentido.

    obtem_mov_sentido: movimento -> booleano
    """
    return m[2]


def movimentos_iguais(m1,m2):
    """
    Recebe dois movimentos e devolve True se forem iguais
    
    movimentos_iguais: universal x universal -> booleano
    """
    return eh_movimento(m1) and eh_movimento(m2) and m1 == m2


def movimento_para_str(m):
    """
    Recebe um movimento e converte na sua representação externa.

    movimento_para_str: movimento -> str
    """
    if not obtem_mov_sentido(m):
        return obtem_mov_face(m) + "'"
    else: 
        return obtem_mov_face(m)


def str_para_movimento(s):
    """
    Recebe a representação externa de um movimento e devolve o movimento correspondente.
    
    str_para_movimento: str -> movimento
    Gera ValueError se os argumentos forem inválidos.
    """
    if type(s) != str or (s not in FACES and s not in MOVIMENTOS_SENTIDO_INVERSO):
        raise ValueError("str_para_movimento: argumentos invalidos")
    elif s in FACES:
        return cria_movimento(s,True)
    else:
        return cria_movimento(s[0],False)


def movimento_inverso(m):
    """
    Recebe um movimento e devolve o movimento no sentido inverso.

    movimento_inverso: movimento -> movimento
    """
    return cria_movimento(obtem_mov_face(m),not obtem_mov_sentido(m)) 


def str_para_sequencia(s):
    """
    Recebe uma cadeia de caracteres e devolve um tuplo de movimentos.
    
    str_para_sequencia: str -> tuplo
    """
    seq = ()
    i = 0
    while i < len(s):  # ciclo que verifica se o caracter seguinte é uma plica e guarda os movimentos num tuplo
        if s[i+1:i+2] == "'":  # este slicing faz com que a função funcione enquanto que s[i+1] não funcionaria quando não existisse o elemento seguinte
            seq += (cria_movimento(s[i], False),)
            i += 2
        else:
            seq += (cria_movimento(s[i], True),)
            i += 1
    return seq


def sequencia_para_str(seq):
    """
    Recebe um tuplo de movimentos e devolve  uma cadeia de caracteres.

    sequencia_para_str: tuplo -> str
    """
    r = ""
    for m in seq:
        r += movimento_para_str(m)
    return r


def sequencia_inversa(seq):
    """
    Recebe um tuplo de movimentos e devolve um tuplo com os movimentos inversos na ordem inversa.
    
    sequencia_inversa: tuplo -> tuplo
    """
    t = ()
    for mov in seq:
        t = (movimento_inverso(mov),) + t
    return t


def simplifica_sequencia(seq):  # O caso "UUUU" funciona porque a função transforma os primeiros 3 em "U'" que vai de seguida anular com "U"
    """
    Recebe um tuplo de movimentos e junta voltas consecutivas da mesma face.
    
    simplifica_sequencia: tuplo -> tuplo  
    """
    t = ()  # funciona como uma pilha à qual vamos juntando os movimentos, comparando o próximo que vamos inserir com os últimos elem. de t
    for m in seq:
        if t != () and movimentos_iguais(m, movimento_inverso(t[-1])):
           t = t[:-1]      
        else:
            t += (m,) 
            if len(t) >= 3 and movimentos_iguais(t[-1], t[-2]) and movimentos_iguais(t[-2], t[-3]):
                            t = t[:-3] + (movimento_inverso(t[-1]),) 
    return t

