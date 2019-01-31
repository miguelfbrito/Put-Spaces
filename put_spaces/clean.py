#!/usr/bin/env python3

import sys, re
from nltk import sent_tokenize

'''
    Universidade do Minho
    Scripting no Processamento de Linguagem Natural 18/19
    TP3 - Opção 2: Reintrodução de espaços em textos
    Grupo 5: PG38418 Luís Dias, PG38419 Miguel Brito, A78434 Pedro Silva 
'''

def read_text(file):
    with open(file, "r") as f:
        text = f.read()
    return text

def split_sentences(text):
    return sent_tokenize(text)

def remove_extra_spaces(line):
    return re.sub(r'\s+', r' ', line)
    
def clean_text(file):
    text = read_text(file)
    sentences = split_sentences(text)

    cleaned_sentences = [remove_extra_spaces(line) for line in sentences]

    return cleaned_sentences

