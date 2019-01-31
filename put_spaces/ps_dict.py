#!/usr/bin/env python3
import fileinput
from collections import Counter
import regex as re

#Construir um dicionário de palavras a partir de um corpus
def create_word_dict(corpus):
    dic = Counter()

    for line in fileinput.input(corpus):
        #Remover pontuação
        line = re.sub(r'\p{punct}', r'', line)
        #Limpar separadores
        line = re.sub(r'\s+', r' ', line)

        for palavra in re.split(r' ', line):
            dic[palavra] += 1
            
    return dict(dic)


#Converter um dicionário da palavras para um dicionário
#que agrupa palavras que são iguais do ponto de vista 'case insensitive'
def dict_to_case_ins(dic):
    dic_ins = Counter()
    palavras = dic.keys()

    for palavra in palavras:
        dic_ins[r'(?i)' + palavra.lower()] += dic[palavra]

    return dict(dic_ins)

#Recebe um dicionário de palavras e adiciona espaços a uma linha
def put_space_line(dic, line, case_insensitive=False):
    N = len(line)
    pos = 0         #Caractere da string que representa o primeiro caracter da palavra

    while pos < N:
        match = []  #Lista de palavras possíveis a serem formadas a partir de pos

        #offset = Número de caracters da palavra
        for offset in range(0, N - pos):
            palavra = line[pos:pos + offset]
            
            #Se estamos a analisar do ponto de vista case insensitive
            #formatamos a sequência de cracteres em questão
            if case_insensitive:
                palavra = r'(?i)' + palavra.lower()

            #Se formou uma palavra do dicionário, registamos
            if palavra in dic:
                match.append(palavra)
            
        if len(match) > 0:
            #Escolhemos a palavra com maior número de ocorrências
            palavra = max(match, key = lambda p : dic[p])          
            len_pal = len(palavra)
            
            #Precisamos adaptar len_pal a (?i) se for o caso
            if case_insensitive:
                len_pal -= 4

            #Adicionamos espaço à frente, sse à frente estiver uma letra  
            addSpaceAhead = re.match(r'\p{L}', line[pos + len_pal]) != None 
            #Isolamos a palavra, i.e., se atrás estiver uma letra  
            addSpaceBehind = pos > 0 and re.match(r'\p{L}', line[pos-1]) != None

            #Indica quantas posições na string vamos avançar
            step = len_pal
            
            #Expressão para adição de espaços
            subExp = r'\1'

            if addSpaceAhead:
                subExp = subExp + r' '

                #Adaptamos N ao novo tamanho da linha
                N += 1
                #Adaptar passo
                step += 1

            if addSpaceBehind:
                subExp = r' ' + subExp
                #Adaptamos N ao novo tamanho da linha
                N += 1
                #Incrementamos o passo de forma a posicionar corretamente
                #'pos' na iteração seguinte
                step += 1


            if addSpaceAhead or addSpaceBehind:   
                if case_insensitive:
                    palavra = r'(?i)' + re.sub(r'[()]', r'', palavra[4:])
                else:
                    palavra = re.sub(r'[()]', r'', palavra)
                line = line[:pos] + re.sub(r'('+ palavra + r')', subExp, line[pos:pos + len_pal]) + line[pos + len_pal:]
                
            #Avançamos na linha
            pos += step

        else: pos += 1

    return line

#Recebe um dicionário de palavras e adiciona espaços ao texto
def put_space(dic, texto, case_insensitive=False):
    #Se prentedemos case insensitive, convertemos o dicionário
    if case_insensitive:
        dic = dict_to_case_ins(dic)

    for line in fileinput.input(texto):
        line = put_space_line(dic, line, case_insensitive)
        print(line, end='') 

#Recebe um dicionário de palavras e remove espaços erradamente colocados no texto
def rm_wrong_space(dic, texto, case_insensitive=False):
    #Se prentedemos case insensitive, convertemos o dicionário
    if case_insensitive:
        dic = dict_to_case_ins(dic)

    for line in fileinput.input(texto):
        #Limpar separadores
        line = re.sub(r'\s+', r' ', line)
        #Remover pontuação da linha
        dup_line = re.sub(r'\p{punct}', r'', line)
        #Obter palavras
        palavras = re.split(r' ', dup_line)
        
        #Se estamos a tratar de forma case insensitive
        #adaptamos a lista de palavras à syntax do dicionário
        palavras = list(map(lambda pal: r'(?i)' + pal.lower(), palavras))

        #Analisamos as palavras par a par
        for i in range(1, len(palavras)):
            pal1 = palavras[i-1]
            pal2 = palavras[i]
           
            if case_insensitive:
                cat_pal = pal1 + pal2[4:] #Removemos o '(?i)' da segunda expressão
            else: 
                cat_pal = pal1 + pal2

            #Se a palavra formada pelos caracteres existe no dicionário,
            #Verificamos se o espaço deve ser removido
            if cat_pal in dic:
                #Ocorrencias da palavra 1 e palavra 2 em análise, 
                # no dicionário, a existirem
                sum_oco = 0
                if pal1 in dic:
                    sum_oco += dic[pal1]
                if pal2 in dic:
                    sum_oco += dic[pal2]

                #removemos o espaço sse o seu número de ocorrências for superior
                if dic[cat_pal] > sum_oco:
                    line = re.sub(r'(' + pal1 + r') (' + pal2 + r')', r'\1\2', line)

        print(line)
