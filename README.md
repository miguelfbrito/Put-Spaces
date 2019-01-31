# USAGE EXAMPLES

#### Remoção de espaços de um ficheiro:
    
    put_space -rs [ficheiro_texto] > [ficheiro_texto_sem_espacos]
    
#### Aplicação do algoritmo de adição de espaços base com case-insensitive:
    
    put_space -s [ficheiro_texto_sem_espacos] -b [dic_pickle] -i > [resultado]
    
#### Aplicação do algoritmo de adição de espaços recorrendo a ngrams de caracteres:
    
    put_space -s [ficheiro_texto_sem_espacos] -nc [4] [dic_pickle_chars_4] > [resultado]
    
#### Aplicação do algoritmo de adição de espaços recorrendo a ngrams de palavras:
    
    put_space -s [ficheiro_texto_sem_espacos] -nw [2] [dic_pickle_words_2] > [resultado]
    
#### Remoção de espaços adicionados incorretamente:
    
    put_space -s [ficheiro_espacos_adicionados] -r [dic_pickle_words] > [resultado]
    
#### Avaliar métricas no processo de adição de espaços:
    
    put_space -mp [ficheiro_texto] [resultado]
    
#### Avaliar métricas no processo de remoção de espaços incorretos:
    
    put_space -mr [resultado] [resultado_espacos_inc_removidos]


# CONTENTS

## relatorio.pdf

	Relatório descritivo da ferramenta desenvolvida e das estratégias utilizadas na sua construção.

## put_spaces.py

	Ponto de entrada da ferramenta. Ver secção 9 do relatório para mais informação, ou recorrer ao --help
	./put_spaces -h

## ps_dict.py

	Soluções que tiram partido de Dicionários de Palavras. (Secção 2 e 7 do relatório)

## ngram_chars.py

	Implementação que tira partido de um N-grama de caracteres. (Secção 3)

## ngram_words.py

	Solução que recorre a N-grama de palavras. (Secção 4)

## evaluate.py

	Responsável pelo cálculo das métricas Precision e Recall. (Secção 8)

## remove_spaces.py

	Utilizado para remover todos os espaços de um texto.

## clean.py

	Funções auxiliares à limpeza de textos.

## extract_ngrams_chars_cetempublico.py

	Extração de ngrams de chars do repositório CETEMPúblico para um dict("chars" : #ocorrencias). Terminada a extração é realizado um dump pickle da estrutura de dados.

## extract_ngrams_words_cetempublico.py

	Extração de ngrams de words do repositório CETEMPúblico para um dict("chars" : #ocorrencias). Terminada a extração é realizado um dump pickle da estrutura de dados. O dicionário de palavras é gerado recorrendo a esta função para N=1.
	
# AUTHORS

	PG38418 - Luís Dias
	PG38419 - Miguel Brito
	A78434 - Pedro Silva
