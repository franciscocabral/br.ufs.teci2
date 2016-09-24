from __future__ import division
from nltk import FreqDist
import nltk, re, pprint, string
import codecs
import numpy
import math
import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from unicodedata import normalize

pergunta_txt = codecs.open('pergunta.txt','r', 'utf-8-sig')
corpus_txt = codecs.open('corpus.txt','r', 'utf-8-sig')
verbos_txt = codecs.open('verbos.txt','r', 'utf-8-sig')
descarte_txt = codecs.open('descarte.txt','r', 'utf-8-sig')
pronomes_txt = codecs.open('pronomes_relativos.txt','r', 'utf-8-sig')
labels_pronomes_txt = codecs.open('label_pronomes.txt','r', 'utf-8-sig')

pergunta_original = pergunta_txt.read()
pergunta = pergunta_original.lower()
corpus_original = corpus_txt.read()
corpus = corpus_original
descarte = nltk.word_tokenize(descarte_txt.read().lower())
pronomes = nltk.word_tokenize(pronomes_txt.read().lower())
labels_pronomes = nltk.word_tokenize(labels_pronomes_txt.read().lower())
verbos = nltk.word_tokenize(verbos_txt.read())

## Funcoes Features -----------------------------------------------------------------------------------
## ----------------------------------------------------------------------------------------------------

## A funcao word_feat_tipo(words), Rotula a pergunta como pessoa, tempo, lugar ou medida --------------
## ----------------------------------------------------------------------------------------------------
def word_feats_tipo(words):
    for word in words:
        if word in pronomes:
            return labels_pronomes[pronomes.index(word)]
  
## A funcao word_feat_central(words), seleciona a palavra central da pergunta -------------------------
## ----------------------------------------------------------------------------------------------------
def word_feats_central(words):
    new_words = []
    for word in words:
        if word not in descarte:
            new_words.append("".join(word))
    for word in new_words:
        if word in verbos:
            return new_words[new_words.index(word)+1]

## A funcao word_feat_auxiliares(words), seleciona as palavras auxiliares na pergunta -----------------
## ----------------------------------------------------------------------------------------------------
        
def word_feats_auxiliares(words, central):
    aux=[]
    for word in words:
        if word in corpus.lower() and word not in descarte and word not in verbos and word != central:
            aux.append("".join(word))
    return aux

## A funcao word_feat_descarte(words), exclui stopwords -----------------------------------------------
## ----------------------------------------------------------------------------------------------------
def word_feats_descarte(words):
    aux=[]
    for word in words:
        if word not in descarte:
            aux.append(word)
    return aux

## A funcao word_feat_NP(words), seleciona os nomes proprios de uma STRING-----------------------------
## ----------------------------------------------------------------------------------------------------
def word_features_NP(words):
    nomes_final =[]
    nomes = re.findall(r'\b[A-Z][\'?a-z]+ \b', words) #palavras que comecam com letra maiuscula n precedidas por ponto
    nomes = re.findall(r'\b[A-Z][\'?a-z]+\b', "".join(nomes))
    for w in nomes:
        if w.lower() not in nltk.word_tokenize(pergunta.lower()) and w.lower() not in descarte:
            nomes_final.append(w)
    return nomes_final

## A funcao word_feat_DATA(words), seleciona as datas de uma STRING-----------------------------
## ----------------------------------------------------------------------------------------------------
def word_features_DATA(words):
    anos = re.findall(r'\b[0-9]{4}|[0-9]{2}\b', words)
    datas_precisas = re.findall(r'\b^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/([12][0-9]{3}|[0-9]{2})\b', words)
    data = anos+datas_precisas
    return data

## ----------------------------------------------------------------------------------------------------
## ----------------------------------------------------------------------------------------------------

## laco para remover pontuacao da pergunta, exceto hifen.
## ----------------------------------------------------------
for c in string.punctuation:
    if c != "-":
        pergunta = pergunta.replace(c,"")
        corpus = corpus.replace(c,"")
        
## Cria uma lista tuple com os comentarios e seus respectivos labels, detalhe para a chamada da funcao word_feats explicada acima.
## -------------------------------------------------------------------------------------------------------------------------------
tipo_resposta = word_feats_tipo(nltk.word_tokenize(pergunta))
#print tipo_resposta

central = word_feats_central(nltk.word_tokenize(pergunta))
#print "".join(central)

auxiliares = word_feats_auxiliares(nltk.word_tokenize(pergunta), central)
#print "".join(auxiliares)

print ("Pergunta: ", pergunta_original)
print ("Tipo: ", tipo_resposta, "\nPalavra Central: ", "".join(central), "\nPalavra(s) Auxiliare(s): ", ", ".join(auxiliares))
maximas = []
frase = []
ocorrencia = []

#text3.count("smote")

count = 0
count_importancia = 0
importancia_frase=[]

for w in corpus:
    if w != '\n':
        frase.append("".join(w)) #forma uma frase
    else:
        maximas.append("".join(frase)) #todas as frases
        for word in nltk.word_tokenize(maximas[count]):
            if word.lower() == central: #se achar a palavra central
                count_importancia=count_importancia+10
                #print central, count
                
        for num in range(0,len(auxiliares)):
            for word in nltk.word_tokenize(maximas[count]):
                if word.lower() == auxiliares[num]:
                    count_importancia=count_importancia+40 #se achar uma das auxiliares
                    #print auxiliares[num], count
        importancia_frase.append(count_importancia)
        frase=[]
        count = count + 1
        count_importancia=0

print ("Importancia de casa paragrafo: ", importancia_frase)
paragrafo=(importancia_frase.index(max(importancia_frase)))
print ("Paragrafo de maior importancia: ", paragrafo+1)
print(maximas[paragrafo])
#print " ".join(word_feats_descarte(nltk.word_tokenize(maximas[paragrafo-1])))

########################################################################################################################################
#######   TIPO = PESSOA    #############################################################################################################
########################################################################################################################################
'''

não está funcionando direito


'''

paragraphTokens = nltk.word_tokenize(maximas[paragrafo])
tokensLower = nltk.word_tokenize((maximas[paragrafo]).lower())
wordsNonStopword = word_feats_descarte(paragraphTokens)
wordsNonStopwordLower = word_feats_descarte(tokensLower)


if tipo_resposta == 'pessoa':
    ## Caso o tipo de resposta seja pessoa, espera-se um Nome Proprio como resposta.
    NP=word_features_NP(wordsNonStopword)
    print (NP)
    distancias=[]
    distancias_aux=[]
    posicao=0
    
    for num in range(0,len(NP)):
        if central in tokensLower:
            posicao= wordsNonStopword.index(NP[num])
            posicao_aux = wordsNonStopword.index(central)
            distancias.append(posicao-posicao_aux)
        else:
            distancias.append(0)
            
    for num in range(0,len(distancias)):
        if distancias[num] < 0:
            distancias[num]=-distancias[num]
        else:
            distancias[num]=distancias[num]
                
    print ("Atualizacao das distancias: ",distancias)
    
    if central in  tokensLower:
        if wordsNonStopword[min(distancias)+posicao_aux+1] in NP:
            print ("Resposta antes das auxiliares: ", 
                   wordsNonStopword[min(distancias)+posicao_aux], 
                    wordsNonStopword[min(distancias)+posicao_aux+1])
        else:
            print ("Resposta antes das auxiliares: ", wordsNonStopword[min(distancias)+posicao_aux])
        
    distancias_aux=distancias
    
    for aux in range(0,len(auxiliares)):
        for num in range(0,len(NP)):
            posicao= wordsNonStopword.index(NP[num])
            posicao_aux =wordsNonStopwordLower.index(auxiliares[aux])
            if posicao>posicao_aux:
                diferenca=posicao-posicao_aux
            else:
                diferenca=posicao_aux-posicao
            distancias_aux[num]=distancias_aux[num]+diferenca
        print ("Atualizacao das distancias: ",distancias_aux)
            
    for num in range(0,len(distancias_aux)):
        if distancias_aux[num] < 0:
            distancias_aux[num]=-distancias_aux[num]
        else:
            distancias_aux[num]=distancias_aux[num]
    
    posicao_resposta= wordsNonStopword.index(NP[distancias_aux.index(min(distancias_aux))])
    if wordsNonStopword[posicao_resposta+1] in NP:
        print ("Resposta: ",NP[distancias_aux.index(min(distancias_aux))], NP[(distancias_aux.index(min(distancias_aux))+1)])
    else:
        print ("Resposta: ",NP[distancias_aux.index(min(distancias_aux))])
    

########################################################################################################################################
#######   TIPO = TEMPO   ###############################################################################################################
########################################################################################################################################


if tipo_resposta == 'tempo':
    ## Caso o tipo de resposta seja tempo, espera-se uma data como resposta.
    #encontra possiveis datas no paragrafo
    DATA=word_features_DATA(wordsNonStopword)
    print("possiveis respostas")
    print (", ".join(DATA))
    distancias=[]
    distancias_aux=[]
    posicao=0
    
    for num in range(0,len(DATA)):
        if central in  tokensLower:
            posicao= wordsNonStopword.index(DATA[num])
            posicao_aux = wordsNonStopword.index(central)
            distancias.append(posicao-posicao_aux)
        else:
            distancias.append(0)
            
    for num in range(0,len(distancias)):
        if distancias[num] < 0:
            distancias[num]=-distancias[num]
        else:
            distancias[num]=distancias[num]
                
    print ("Atualizacao das distancias: ", distancias)
    
    if central in  tokensLower:
        if wordsNonStopword[min(distancias)+posicao_aux+1] in DATA:
            print ("Resposta antes das auxiliares: ", wordsNonStopword[min(distancias)+posicao_aux],  wordsNonStopword[min(distancias)+posicao_aux+1])
        else:
            print ("Resposta antes das auxiliares: ", wordsNonStopword[min(distancias)+posicao_aux])
    else:
        print ("Nao possui Resposta antes de analise das palavras auxiliares."  )
    distancias_aux=distancias
    for aux in range(0,len(auxiliares)):
        for num in range(0,len(DATA)):
            posicao= wordsNonStopword.index(DATA[num])
            posicao_aux =(word_feats_descarte(nltk.word_tokenize(maximas[paragrafo].lower()))).index("".join(auxiliares[aux]))
            if posicao>posicao_aux:
                diferenca=posicao-posicao_aux
            else:
                diferenca=posicao_aux-posicao
            distancias_aux[num]=distancias_aux[num]+diferenca
        print ("Atualizacao das distancias: ", distancias_aux)
            
    for num in range(0,len(distancias_aux)):
        if distancias_aux[num] < 0:
            distancias_aux[num]=-distancias_aux[num]
        else:
            distancias_aux[num]=distancias_aux[num]
    
    posicao_resposta= wordsNonStopword.index(DATA[distancias_aux.index(min(distancias_aux))])

    if wordsNonStopword[posicao_resposta+1] in DATA:
        print ("Resposta: ",DATA[distancias_aux.index(min(distancias_aux))], DATA[(distancias_aux.index(min(distancias_aux))+1)])
    else:
        print ("Resposta: ",DATA[distancias_aux.index(min(distancias_aux))])
    




'''

falta codificar para

medida
lugar


'''




        
        
        
        
        
        
        
        
        
        
        
        
        
