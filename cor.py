# Funções para a cor 
DIGITOS = ('1', '2', '3', '4', '5', '6')


def cria_cor(d):
    """
    Recebe um caracter de 1 a 6 e devolve a cor correspondente.

    cria_cor: str -> cor
    Gera ValueError se o argumento não for válido.
    """
    if type(d) != str or d not in DIGITOS:
        raise ValueError('cria_cor: argumentos invalidos')
    return ('cor',d)  # cor representada por um tuplo 


def eh_cor(c):
    """
    Recebe um universal e devolve True se o argumento for uma cor.

    eh_cor: universal -> booleano
    """
    return type(c) == tuple and len(c) == 2 and c[0] == 'cor' and type(c[1]) == str and c[1] in DIGITOS


def cores_iguais(c1,c2):
    """
    Recebe dois universais e devolve True se forem cores iguais.

    cores_iguais: universal x universal -> booleano
    """
    return eh_cor(c1) and eh_cor(c2) and c1[1] == c2[1]


def cor_para_str(c):
    """
    Recebe uma cor e devolve o dígito correspondente em string.

    cor_para_str: cor -> str
    """
    return c[1]

    
def str_para_cor(s):
    """
    Recebe um caracter de 1 a 6 e devolve a cor correspondente.

    str_para_cor: str -> cor
    """   
    return cria_cor(s)


def cor_para_int(c):
    """
    Recebe uma cor e devolve o inteiro correspondente ao caracter da cor.

    cor_para_int: cor -> int
    """
    return int(c[1])