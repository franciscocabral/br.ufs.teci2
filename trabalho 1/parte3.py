'''
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres

TRABALHO 1, PARTE 3

1) Aplique Lematização a Vocabulário

1) Aplique Stemming a Vocabulário


http://www.nltk.org/api/nltk.stem.html
http://www.nltk.org/api/nltk.stem.html#module-nltk.stem.rslp
https://pt.wikipedia.org/wiki/Lexema

'''

import nltk, parte1

def stemming(tokens):
    st = nltk.stem.SnowballStemmer('portuguese')
    words = []
    for token in tokens:
        words.append(st.stem(token))
    return words
    
def lemmatizer(tokens):
    wnl = nltk.stem.WordNetLemmatizer()
    words = []
    for token in tokens:
        words.append(wnl.lemmatize(token))
    return words
    

