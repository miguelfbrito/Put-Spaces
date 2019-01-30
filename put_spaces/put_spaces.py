#!/usr/bin/env python3

""" 
USAGE:

put_spaces -s <source> -r -m


"""
import re, sys, getopt, pickle
import remove_spaces, evaluate, clean, ps_dict, ngram_chars, ngram_words
from argparse import ArgumentParser

def set_arguments():
    parser = ArgumentParser(description="Add spaces to text with no spaces using NLP algorithms.")
    parser.add_argument("-s", "--source", help="Source file")
    parser.add_argument("-r", "--remove", help="Remove spaces from source file", action="store_true")
    parser.add_argument("-b", "--base", help="Use base solution as", action="store_true")
    parser.add_argument("-nc", "--ngrams_chars", help="Use ngrams of chars as algorithm", action="store_true")
    parser.add_argument("-nw", "--ngrams_words", help="Use ngrams of words as algorithm", action="store_true")
    parser.add_argument("-p", "--pos_tagging", help="Use POS-tagging", action="store_true")
    parser.add_argument("-c", "--corpus", help="Set corpus to be used by algorithm")
    parser.add_argument("-m", "--metrics", help="Calculate metrics such as precision and recall", action="store_true")
    return parser.parse_args()

def load_pickle():
    file = open("/home/mbrito/.pickle/corpus_ngrams_words_1", "rb")
    #file = open("/home/mbrito/.pickle/corpus_ngrams_chars_4", "rb")
    return pickle.load(file)


def main():
    # Args definidos como store_true avaliam-se por boolean, os restantes por None
    args = set_arguments()
    loaded_text = []
    text_removed_spaces = []

    if args.source is not None: 
        loaded_text = clean.clean_text(args.source)
        if args.remove: 
            text_removed_spaces = remove_spaces.remove_spaces(loaded_text)
            #print(text_removed_spaces)

    # TODO: Alterar ordem para o 'melhor' algoritmo
    # TODO: Escrever ficheiro após aplicar algoritmo
    file_with_spaces = ""
    if args.base is not None:
        dict_unigram = load_pickle()
        text_after_processing = ps_dict.put_space(dict_unigram, text_removed_spaces)
    elif args.ngrams_chars is not None:
        dict_ngrams_chars = load_pickle()
        text_after_processing = ngram_chars.put_spaces(4, dict_ngrams_chars, loaded_text) 
        print()
    elif args.ngrams_words is not None:
        dict_unigram = load_pickle()
        text_after_processing = ngram_words.put_spaces(dict_unigram, 1, text_removed_spaces)
        print()
    elif args.pos_tagging is not None:
        print()

    if args.metrics:
        if args.source is not None:
            evaluate.evalute_and_print(args.source, " ".join(text_after_processing)) # TODO: alterar para o ficheiro guardado após aplicar o algoritmo
        else: print("[WARNING] Source file not defined, metrics can not be calculated.")

main()

