#!/usr/bin/env python3
import fileinput, sys

#True Positive = Adicionou o espaço no sitio certo
#True Negative = Não adicionou espaço onde não era preciso
#False Positive = Adicionou um espaço onde não era para adicionar
#False Negative = Não adicionou espaço num sitio que era preciso ter adicionado

def avaliar_ps(exp, real):

    Tpos = Tneg = Fpos = Fneg = 0

    for lineEXP, lineRL in zip(fileinput.input(exp), real):
        #Tamanho das linhas
        n_EXP = len(lineEXP)
        n_RL = len(lineRL)

        #Posição nas linhas
        i_e = 0 
        i_r = 0

        while i_e < n_EXP and i_r < n_RL:
            #True Positive
            if lineEXP[i_e] == lineRL[i_r] and lineEXP[i_e] == ' ': 
                Tpos += 1
                i_e += 1
                i_r += 1
            #True Negative
            elif lineEXP[i_e] == lineRL[i_r] and lineEXP[i_e] != ' ': 
                Tneg += 1
                i_e += 1
                i_r += 1
            #False Positive
            elif lineEXP[i_e] != lineRL[i_r] and lineEXP[i_e] != ' ': 
                Fpos += 1 
                i_r += 1
            #False Negative
            elif lineEXP[i_e] != lineRL[i_r] and lineEXP[i_e] == ' ': 
                Fneg += 1 
                i_e += 1

    return (Tpos, Tneg, Fpos, Fneg)

#True Positive = Removeu o espaço no sitio certo
#True Negative = Não removeu o espaço onde não era preciso
#False Positive = Removeu um espaço onde não era para remover
#False Negative = Não removeu espaço num sitio que era preciso ter removido

def avaliar_rs(exp, real):

    Tpos = Tneg = Fpos = Fneg = 0

    for lineEXP, lineRL in zip(fileinput.input(exp), fileinput.input(real)):
        #Tamanho das linhas
        n_EXP = len(lineEXP)
        n_RL = len(lineRL)

        #Posição nas linhas
        i_e = 0 
        i_r = 0

        while i_e < n_EXP and i_r < n_RL:
            #True Positive
            if lineEXP[i_e] == lineRL[i_r] and lineEXP[i_e] != ' ': 
                Tpos += 1
                i_e += 1
                i_r += 1
            #True Negative
            elif lineEXP[i_e] == lineRL[i_r] and lineEXP[i_e] == ' ': 
                Tneg += 1
                i_e += 1
                i_r += 1
            #False Positive
            elif lineEXP[i_e] != lineRL[i_r] and lineEXP[i_e] == ' ': 
                Fpos += 1 
                i_e += 1
            #False Negative
            elif lineEXP[i_e] != lineRL[i_r] and lineEXP[i_e] != ' ': 
                Fneg += 1 
                i_r += 1

    return (Tpos, Tneg, Fpos, Fneg)

def evalute_and_print(before, after, ps=True):

    if not before and not after:
        return

    if ps:
        (Tpos, Tneg, Fpos, Fneg) = avaliar_ps(before, after)
    else:
        (Tpos, Tneg, Fpos, Fneg) = avaliar_rs(before, after)
    print("\n\nTrue Positive =", Tpos)
    print("True Negative =", Tneg)
    print("False Positive =", Fpos)
    print("False Negative =", Fneg)
    print("Precision:", Tpos / (Tpos + Fpos))
    print("Recall:", Tpos / (Tpos + Fneg))
