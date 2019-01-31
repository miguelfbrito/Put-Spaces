#!/usr/bin/env python3
import re, sys

'''
    Universidade do Minho
    Scripting no Processamento de Linguagem Natural 18/19
    TP3 - Opção 2: Reintrodução de espaços em textos
    Grupo 5: PG38418 Luís Dias, PG38419 Miguel Brito, A78434 Pedro Silva 
'''

def remove_spaces(texto):
    removed_spaces = []
    for line in texto:
        removed_spaces.append(re.sub(r" ", "", line))

    return removed_spaces
