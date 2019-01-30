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
    parser.add_argument("-r", "--remove", help="Remove spaces from source file")
    parser.add_argument("-b", "--base", help="Use base solution as algorithm")
    parser.add_argument("-nc", "--ngrams_chars", help="Use ngrams of chars as algorithm. Must specify N first.", nargs='+')
    parser.add_argument("-nw", "--ngrams_words", help="Use ngrams of words as algorithm. Must specify N first.", nargs='+')
    parser.add_argument("-i", "--case_insensitive", help="Do case insensitive analysis, if applicable", action="store_true")
    parser.add_argument("-mp", "--metrics_put", help="Given expected and obtained results, calculate metrics such as precision and recall for added spaces", nargs='+')
    parser.add_argument("-mr", "--metrics_remove", help="Given expected and obtained results, calculate metrics such as precision and recall for removed spaces", nargs='+')
    return parser.parse_args()

def load_pickle(source):
    file = open(source, "rb")
    return pickle.load(file)

def print_error():
    print("[ERROR] Invalid arguments, cannot proceed.")


def main():
    # Args definidos como store_true avaliam-se por boolean, os restantes por None
    args = set_arguments()
    texto = ''

    if args.source is not None: 
        texto = args.source

    if args.base is not None:
        if texto != '':
            dict_unigram = load_pickle(args.base)
            ps_dict.put_space(dict_unigram, texto, args.case_insensitive)
        else: print_error()

    elif args.ngrams_chars is not None:
        if len(args.ngrams_chars) == 2 and args.ngrams_chars[0].isdigit() and texto != '':           
            dict_ngrams_chars = load_pickle(args.ngrams_chars[1])
            ngram_chars.put_spaces(int(args.ngrams_chars[0]), dict_ngrams_chars, texto) 
        else: print_error()

    elif args.ngrams_words is not None:
        if len(args.ngrams_words) >= 2 and args.ngrams_words[0].isdigit() and texto != '':
            dict_ngrams_words = load_pickle(args.ngrams_words[1])
            dict_unigram = {}
            if len(args.ngrams_words) == 3:
                dict_unigram = load_pickle(args.ngrams_words[2])
            ngram_words.put_spaces(dict_ngrams_words, int(args.ngrams_words[0]), texto, dict_unigram)
        else: print_error()

    elif args.remove is not None:
        if texto != '':
            dict_unigram = load_pickle(args.remove)
            ps_dict.rm_wrong_space(dict_unigram, texto, args.case_insensitive)
        else: print_error()
        

    elif args.metrics_put is not None:
        if len(args.metrics_put) == 2:
            evaluate.evalute_and_print(args.metrics_put[0], args.metrics_put[1])
        else: print_error()

    elif args.metrics_remove is not None:
        if len(args.metrics_remove) == 2:
            evaluate.evalute_and_print(args.metrics_remove[0], args.metrics_remove[1], ps=False)
        else: print_error()

main()

