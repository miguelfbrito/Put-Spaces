#!/usr/bin/env python3

import sys, os, fileinput, getopt
import regex as re
import pickle


def put_spaces(N, ngram, texto):
    #N-1 últimos caracteres da linha anterior
    lastN = ''

    for line in texto:
        #Caractere da linha em análise
        i = 0
        #Tamanho da linha
        line_len = len(line)

        while i < line_len:
            #Se não é necessário considerar os caracteres da linha anterior
            if i >= N-1:
                #N-1 caracteres anteriores
                section = line[i-(N-1):i]
            else:
                section = lastN[i:] + line[:i]

            #Número de ocorrências com espaço antes de 'i'
            with_space = 0

            if section[1:] + ' ' + line[i] in ngram:
                with_space = ngram[section[1:] + ' ' + line[i]]

            #Número de ocorrências sem espaço antes de 'i'
            wo_space = 0

            if section + line[i] in ngram:
                wo_space = ngram[section + line[i]]

            #Adicionamos o espaço sse o seu número de ocorrencias
            #for estritamente maior
            if with_space > wo_space:
                line = line[:i] + ' ' + line[i:]
                #Adaptamos o tamanho da linha
                line_len += 1
                #Avançamos
                i += 2
            else:
                i += 1

        #Atualizamos os N-1 caracteres anteriores (excluímos o '\n')
        lastN = line[-N:-1]
        print(line, end='')