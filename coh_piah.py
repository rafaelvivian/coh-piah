import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print()
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")
    print()

    wal = float(input("Entre o tamanho médio de palavra: "))
    ttr = float(input("Entre a relação Type-Token: "))
    hlr = float(input("Entre a Razão Hapax Legomana: "))
    sal = float(input("Entre o tamanho médio de sentença: "))
    sac = float(input("Entre a complexidade média da sentença: "))
    pal = float(input("Entre o tamanho medio de frase: "))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("\nDigite o texto " + str(i) +" (aperte enter para sair): ")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("\nDigite o texto " + str(i) +" (aperte enter para sair): ")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    tracos = [0, 0 ,0 , 0, 0, 0]
    total_tracos = 0
    i = 0
    while i < 6:
        tracos[i] = abs(as_a[i] - as_b[i])
        total_tracos = total_tracos + tracos[i]
        i = i + 1
    grau_similaridade = total_tracos / 6
    return grau_similaridade

def calcula_assinatura(texto):
    '''Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    tmp = tamanho_medio_palavra(texto)
    rtt = relacao_type_token(texto)
    rhl = razao_hapax_legomana(texto)
    tms = tamanho_medio_sentenca(texto)
    cs = complexidade_sentenca(texto)
    tmf = tamanho_medio_frase(texto)
    return [tmp, rtt, rhl, tms, cs, tmf]

def avalia_textos(textos, ass_cp):
    '''Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto 
    com maior probabilidade de ter sido infectado por COH-PIAH.'''
    ass_cp_b = ass_cp
    menor_grau_similaridade = 10000
    posicao = 0
    for texto in textos:  
        ass_cp_a = calcula_assinatura(texto)
        grau_similaridade = compara_assinatura(ass_cp_a, ass_cp_b)
        posicao = posicao + 1
        if grau_similaridade < menor_grau_similaridade:
            menor_grau_similaridade = grau_similaridade
            texto_infectado = posicao
    return texto_infectado

def tamanho_medio_palavra(texto):
    ''' Tamanho médio de palavra é a soma dos tamanhos das palavras dividida pelo número total de palavras '''
    nro_caracteres = 0
    nro_total_palavras = 0
    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        frases = separa_frases(sentenca)
        for frase in frases:
            palavras = separa_palavras(frase)
            for palavra in palavras:
                nro_caracteres = nro_caracteres + calcula_nro_caracteres(palavra)
                nro_total_palavras = nro_total_palavras + 1
    tamanho_medio_palavra = nro_caracteres / nro_total_palavras
    return tamanho_medio_palavra

def relacao_type_token(texto):
    ''' Relação Type-Token é o número de palavras diferentes dividido pelo número total de palavras '''
    lista_palavras = []
    nro_total_palavras = 0
    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        frases = separa_frases(sentenca)
        for frase in frases:
            palavras = separa_palavras(frase)            
            nro_total_palavras = nro_total_palavras + len(palavras)
            for palavra in palavras:
                lista_palavras.append(palavra)
    nro_palavras_diferentes = n_palavras_diferentes(lista_palavras)
    relacao_type_token = nro_palavras_diferentes / nro_total_palavras
    return relacao_type_token

def razao_hapax_legomana(texto):
    ''' Razão Hapax Legomana é o número de palavras que aparecem uma única vez dividido pelo total de palavras '''
    lista_palavras = []
    nro_total_palavras = 0
    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        frases = separa_frases(sentenca)
        for frase in frases:
            palavras = separa_palavras(frase)            
            nro_total_palavras = nro_total_palavras + len(palavras)
            for palavra in palavras:
                lista_palavras.append(palavra)
    nro_palavras_uma_vez = n_palavras_unicas(lista_palavras)
    razao_hapax_legomana = nro_palavras_uma_vez / nro_total_palavras
    return razao_hapax_legomana

def tamanho_medio_sentenca(texto):
    ''' Tamanho médio de sentença é a soma dos números de caracteres em todas as sentenças dividida pelo número de 
    sentenças (os caracteres que separam uma sentença da outra não devem ser contabilizados como parte da sentença) '''
    sentencas = separa_sentencas(texto)
    nro_sentencas = len(sentencas)
    nro_caracteres = 0
    for sentenca in sentencas:
        nro_caracteres = nro_caracteres + len(sentenca)
    tamanho_medio_sentenca = nro_caracteres / nro_sentencas
    return tamanho_medio_sentenca

def complexidade_sentenca(texto):
    ''' Complexidade de sentença é o número total de frases divido pelo número de sentenças '''
    nro_frases = 0
    nro_sentencas = calcula_nro_sentencas(texto)    
    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        nro_frases = nro_frases + calcula_nro_frases(sentenca)
    complexidade_sentenca = nro_frases / nro_sentencas
    return complexidade_sentenca

def tamanho_medio_frase(texto):
    ''' Tamanho médio de frase é a soma do número de caracteres em cada frase dividida pelo número de frases no 
    texto (os caracteres que separam uma frase da outra não devem ser contabilizados como parte da frase) '''
    nro_caracteres = 0
    nro_frases = 0
    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        frases = separa_frases(sentenca)
        nro_frases = nro_frases + len(frases)
        for frase in frases:
            nro_caracteres = nro_caracteres + len(frase)
    tamanho_medio_frase = nro_caracteres / nro_frases
    return tamanho_medio_frase

def calcula_nro_sentencas(texto):
    sentencas = separa_sentencas(texto)
    nro_sentencas = len(sentencas)
    return nro_sentencas

def calcula_nro_frases(sentenca):
    frases = separa_frases(sentenca)
    nro_frases = len(frases)
    return nro_frases

def calcula_nro_palavras(frase):
    palavras = separa_palavras(frase)
    nro_palavras = len(palavras)
    return nro_palavras

def calcula_nro_caracteres(palavra):
    nro_caracteres = len(palavra)
    return nro_caracteres

def main():
    ass_cp = le_assinatura()
    textos = le_textos()
    texto_infectado = avalia_textos(textos, ass_cp)
    print("\nO autor do texto", texto_infectado, "está infectado com COH-PIAH")

main()