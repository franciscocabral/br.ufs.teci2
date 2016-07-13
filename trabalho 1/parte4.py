'''
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres

TRABALHO 1, PARTE 4

1) Passar o texto por um ruído

2) Executar correção ortográfica

'''

import nltk, re
import parte2 as p2
from random import randint

'''
inserir ruido
@var text {string} Texto a ser alterado
@return {string} Texto com ruído
'''
def ruidar(text):
    new_text = ""
    for i in range(len(text)):
        if randint(0,20) >= 19 and text[i] != " ":
            new_text = new_text + chr(ord(text[i]) + 1)
        else:
            new_text = new_text + text[i]
    return new_text

'''
@var vocabulary {list} Vocabulário base
@var text {string} Texto a ser corrigido
@return {list} Lista de correções possíveis
'''
def get_corrections(vocabulary, text):
    corrections = {}
    #corrections["caxorro"] = {}
    #corrections["caxorro"][2] = ["cachorro"]
    #corrections["caxorro"][3] = ["cachorra"]
    
    for word in p2.tokenize(text):
        if word not in corrections:
            corrections[word] = {}
            for correct in vocabulary:
                dist = nltk.edit_distance(word,correct)
                if dist <= 5:
                    if dist == 0:
                        corrections[word] = {}
                        corrections[word][0] = ["Not Needed"]
                        break
                    if dist not in corrections[word]:
                        corrections[word][dist] = []
                    corrections[word][dist].append(correct)
                
    return corrections
  
'''
@var corrections {list} Correções possíveis
@var text {string} Texto a ser corrigido
@return {string} Texto corrigido
'''  
def correct(corrections, text):
    for word, correction in corrections.items():
        for dist, possibilities in correction.items():
            if dist != 0:
                text = text.replace(word, possibilities[0])
                #@TODO str.replace() é inconsistente, 
                #      é necessário trocar por outra função
            break
    return text
