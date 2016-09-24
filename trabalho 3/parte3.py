'''
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres

TRABALHO 3, PARTE 3

Crie um analisador de sentimentos Boolean Multinomial Naïve Bayes para PtBR
• Construa um corpus de textos de opiniões (positivas e negativas) com o WTCoGen. Essas críticas podem ser encontradas em sites como
    • filmes: www.cineclick.com.br, http://www.adorocinema.com/filmes/, http://omelete.uol.com.br/, etc..
    • outros assuntos: twitter
• A fim de rotular apropriadamente com polaridade cada opinião como positiva ounegativa, utilize o algoritmo de Turney
• Elimine do vocabulário os K% termos mais frequentes (stopwords) (varie K empiricamente)
• Treine o NaiveBayes no conjunto de treinamento para distinguir críticas positivas (classe P) de críticas negativas (classe N).
• Calcule a taxa de erro do algoritmo no conjunto de teste (validação cruzada k-fold).

'''

import os 
import nltk, re, collections, numpy as np
from sklearn.naive_bayes import MultinomialNB

WORDS = []
MATRIZES = []
NOTAS = []
CATEGORIAS = []
TEXTOS_PATH = r"C:\Users\icaromarley5\Documents\GitHub\CC-UFS-Codes\2016.1\TECI 2\trabalho 3\textos-2"
FILES_RANGE = range(1,26) #de 1 a 25
    
def generate_WORDS():#gera palavras
    for i in FILES_RANGE:
        tokenizer = nltk.tokenize.RegexpTokenizer('[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ-]+')
        tokens = tokenizer.tokenize(read_file(TEXTOS_PATH+"\\d"+str(i)+".txt"))
        tokens = [token.lower() for token in tokens]
        global WORDS 
        WORDS = WORDS + list(tokens)
    WORDS = [word.lower() for word in WORDS]

'''

def generate_WORDS():#gera palavras, modificar algortimo
    for i in FILES_RANGE:
        tokenizer = nltk.tokenize.RegexpTokenizer('[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ-]+')
        tokens = tokenizer.tokenize(read_file(TEXTOS_PATH+"\\d"+str(i)+".txt"))
        tokens = set([token.lower() for token in tokens])
        global WORDS 
        WORDS = set(list(WORDS)+list(tokens))
        WORDS = [word.lower() for word in WORDS]
'''

#diminui palavras, ordenando por frequencia#############
def summarize_WORDS():
    global WORDS

    words_aux = {}
    for word in WORDS:
        freq = WORDS.count(word)
        
        if freq not in words_aux:
            #se dict nao tem a frequencia, adiciona a entrada
            words_aux.update({freq:[word]})
        else:
            value = words_aux[freq]
            #se a palavra não consta na entrada
            if word not in value:
                value.append(word)
                del words_aux[freq]
                words_aux.update({freq:value})

    #ordena o dict pela frequencia
    words_aux = collections.OrderedDict(sorted(words_aux.items()))
    aux_list = []
    # itera dict para cada chave, formando lista
    for key,value in words_aux.items():
        aux_list = aux_list + value
    #inverte a lista auxiliar para que os elementos mais frequentes fiquem em
    #primeiro
    WORDS = aux_list[::-1]
   
    
#retira as k primeiras palavras
def stop_words(k):
    print("removendo",k,"stop words")
    global WORDS 
    WORDS = WORDS[k:]
    

def get_words_matrix_binary(texto):#gera matriz esparsa com 0s e 1s
    tokenizer = nltk.tokenize.RegexpTokenizer('[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ-]+')
    tokens = tokenizer.tokenize(texto)
    tokens = set([token.lower() for token in tokens])
    
    matrix = []

    ####TALVEZ ESSA PARTE SEJA ALTERADA
    for word in WORDS:
        val = 0
        if(word in tokens):
            val = 1
        matrix.append(val)
    return matrix
    
def read_file(file_dir):
    file = open(file_dir, 'r', encoding='utf8')
    texto = file.read()
    file.close
    return texto    
    
def get_matrix(i):
    return get_words_matrix_binary(read_file(TEXTOS_PATH+"\\d"+str(i)+".txt"))
    
def get_categoria(matriz):
    for i in range(0,len(MATRIZES)):
        if matriz == MATRIZES[i]:
            return NOTAS[i]

def bayes_com_notas():
    clf = MultinomialNB()
    clf.fit(MATRIZES, NOTAS)
    return clf
    
def bayes_com_categoria():
    clf = MultinomialNB()
    clf.fit(MATRIZES, CATEGORIAS)
    return clf
    
def init():
    print('Processando documentos...')
    notas = read_file(TEXTOS_PATH+"\\notas.txt")
    notas = notas.split()
    generate_WORDS()
    
    for i in FILES_RANGE:
        MATRIZES.append(get_matrix(i))
        NOTAS.append(notas[i-1])
        if int(notas[i-1]) > 5 :
            CATEGORIAS.append("Bom")
        else:
            CATEGORIAS.append("Ruim")
        print(i, end=" ")
    print("")


    
def execPart3(k=20):#K%
    print("Executando Boolean Naïve Bayes com k="+str(k));
    init()
    summarize_WORDS()
    percent_value = round(len(WORDS) * k / 100)
    stop_words(percent_value)
    bayes_notas = bayes_com_categoria()
    bayes_categoria = bayes_com_notas()
    #fazer k-fold

execPart3()
'''
    kfold_learn = [[1,2,3,4,5,6,7,8],
                 [1,2,3,4,5,6,9,10],
                 [1,2,3,4,7,8,9,10],
                 [1,2,5,6,7,8,9,10],
                 [3,4,5,6,7,8,9,10]]
    kfold_test = [[9,10],
                  [7,8],
                  [5,6],
                  [3,4],
                  [1,2],]



cria todos os tokens
gera matriz esparsa para cada texto



def get_k_FULL_WORDS(k):
    sorted_words = collections.OrderedDict(sorted(FULL_WORDS.items()))
    list_words = list(sorted_words)
    return list_words[:k]

matrix_parte2 = get_words_matrix(counter,get_k_FULL_WORDS(k))

'''

