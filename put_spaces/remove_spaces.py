#!/usr/bin/env python3
import re, sys

def remove_spaces(texto):
    removed_spaces = []
    for line in texto:
        removed_spaces.append(re.sub(r" ", "", line))

    return removed_spaces

    # with open(file.replace(".txt","") + "_removed.txt", "w") as f:
    #     for line in removed_spaces:
    #         f.write(line)




