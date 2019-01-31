#!/usr/bin/env python3
import fileinput
import regex as re
from collections import Counter
from ps_dict import put_space_line

'''
    Universidade do Minho
    Scripting no Processamento de Linguagem Natural 18/19
    TP3 - Opção 2: Reintrodução de espaços em textos
    Grupo 5: PG38418 Luís Dias, PG38419 Miguel Brito, A78434 Pedro Silva 
'''

# Constrói um dicionário de palavras a partir de um N-grama
def ngram_to_dic(ngram):
    dic = Counter()

    for (k, v) in ngram.items():
        palavras = re.split(r' ', k)

        for palavra in palavras:
            dic[palavra] += v

    return dict(dic)

#ngram - N-grama de palavras
#N - valor do N-grama
#texto - ao qualvamos adicionar os espaços
#dic - eventual dicionário de palavras que deve ser utilizado na solução de base
#se não for especificado, será construido a partir do N-grama
def put_spaces(ngram, N, texto, dic={}):

    #N-1 palavras anteriores
    lastN = []

    for line in fileinput.input(texto):
        #Caractere da string que representa o primeiro caracter da palavra
        pos = 0         
        #Tamanho da linha
        line_len = len(line)
        
        while pos < line_len:
            #Se não tivermos N-1 palavras anteriores, reduzimos a unigrama
            if len(lastN) != N-1 :
                #Se não temos o dicionário, construímos a partir do n-gram
                if len(dic) == 0:
                    dic = ngram_to_dic(ngram)

                line_w_space = put_space_line(dic, line[pos:-1])
                words = re.split(r' ', line_w_space)

                #Se exceder N-1 palavras
                if len(lastN) + len(words) > N - 1:
                    #Determinamos o nº de palavras de 'words' necessárias
                    n_needed = (N-1) - len(lastN) 
                    words = words[:n_needed]

                    #Encontramos a posição da ultima palavra
                    last_w_line = pos     #Na linha
                    last_w_line_space = 0 #Na linha resultante da solução de base
                    for word in words:
                        last_w_line  = last_w_line + line[last_w_line:].find(word) + len(word)
                        last_w_line_space  = last_w_line_space + line_w_space[last_w_line_space:].find(word) + len(word)

                    #Adicionamos os espaços apenas às palavras consideradas
                    line = line[:pos] + line_w_space[:last_w_line_space+1] + line[last_w_line:]

                    #Atualizar lastN
                    lastN = lastN + words

                    #Atualizar tamanho da linha
                    line_len = len(line)
                    #Novo valor de pos é a posição seguinte ao último espaço
                    new_pos = line.rfind(' ') + 1
                    #Se não foi adicionado nenhum espaço, i.e., new_pos = 0
                    if new_pos == 0:
                        pos = line_len
                    else:
                        pos = new_pos
                else:
                    #Atualizar lastN
                    lastN = lastN + words
                    #Consideramos então que já inserimos todos os espaços
                    line = line[:pos] + line_w_space
                    pos = line_len
                    
            if pos < line_len:       
                #Lista de palavras possíveis a serem formadas a partir de pos           
                match = []  
                #N-1 últimas palavras
                if N != 1 :
                    antN = ' '.join(lastN) + ' '
                else: #Se N=1 não existem palavras anteriores
                    antN = ''
                #Avanço de pos
                step = 1

                #offset = Número de caracters da palavra
                for offset in range(0, N - pos):
                    palavra = line[pos:pos + offset]


                    if  antN + palavra in ngram:
                        match.append(palavra)

                #Se existem candidatos
                if len(match) > 0:
                    #Escolhemos a palavra que resulta no maior número de ocorrências
                    palavra = max(match, key = lambda p : ngram[antN + p])
                    len_pal = len(palavra)

                    #Adicionamos espaço à frente, sse à frente estiver uma letra  
                    addSpaceAhead = re.match(r'\p{L}', line[pos + len_pal]) != None 
                    #Isolamos a palavra, i.e., se atrás estiver uma letra  
                    addSpaceBehind = pos > 0 and re.match(r'\p{L}', line[pos-1]) != None

                    #Expressão para adição de espaços
                    subExp = r'\1'

                    if addSpaceAhead:
                        subExp = subExp + r' '

                        #Adaptamos o tamanho da linha
                        line_len += 1
                        #Adaptar passo
                        step += 1

                    if addSpaceBehind:
                        subExp = r' ' + subExp
                        #Adaptamos o tamanho da linha
                        line_len += 1
                        #Incrementamos o passo de forma a posicionar corretamente
                        #'pos' na iteração seguinte
                        step += 1

                    if addSpaceAhead or addSpaceBehind:   
                        line = line[:pos] + re.sub(r'('+ palavra + r')', subExp, line[pos:pos + len_pal]) + line[pos + len_pal:]

                    #Atualizamos as N-1 palavras
                    lastN.pop(0)
                    lastN.append(palavra)

                    #Adaptamos o passo
                    step += len(palavra)
                else:
                    #Reset às N-1 palavras
                    lastN = []
                
                pos += step

        #Adicionar espaço à frente da pontuação, se for o caso
        line = re.sub(r'(\p{punct})(?=\p{L})', r'\1 ', line)
        #Tratar de palavras com hífen
        line = re.sub(r'(?<=\p{L})(\-)( )', r'\1', line)

        if line[-1] == '\n': line = line[:-1]
        print(line)

