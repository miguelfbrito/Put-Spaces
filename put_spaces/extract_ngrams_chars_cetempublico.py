#!/usr/bin/env python3

# Extração para o CETEMPublico não anotado, ignora os títulos e a pontuação.
# ./extract.py corpus.txt

import pickle, sys, os
from nltk import ngrams
import regex as re

pickle_dir = os.environ['HOME'] + '/.pickle/corpus_ngrams_chars_3'
file = sys.argv[1:][0]
ngrams_dict = {}

def create_ngrams_chars(text, N):
    list_ngrams = ["".join(c) for c in list(ngrams(text, N))]
    
    for el in list_ngrams:
        ngrams_dict[el] = ngrams_dict.get(el, 0) + 1


def extract_ngrams(N):

    i = 0
    with open(file, "r", encoding="ISO-8859-1") as f:

        read_sentence = False
        read_title = False
        first = False
        sentence = ""

        for line in f:
            i+=1
            if re.match(r"<s>", line):
                read_sentence = True
                first = True
            elif re.match(r"</s>", line):
                read_sentence = False
                create_ngrams_chars(sentence, N)
                sentence = ""

            if read_sentence and line != "<s>\n":
                #line = re.sub(r'([^\w\s]|\n)', '', line)
                line = line.replace("\n", "")
                if not re.match(r'\p{punct}', line):
                     sentence += line + " " 

            if i % 500000 == 0:
                print(i)

def dump_pickle():
    f = open(pickle_dir, "wb")
    pickle.dump(ngrams_dict, f)
    f.close()

def main():
    extract_ngrams(3)
    dump_pickle()
    print(len(ngrams_dict))

main()
