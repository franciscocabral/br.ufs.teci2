'''
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres

TRABALHO 1, PARTE 2

1) Aplique tokenização no restante do texto, gerando uma lista de
    palavras (vocabulário V) ordenadas de forma decrescente pelo
    número de aparições (frequência)
    
2) Compute a taxa de Falso Positivo 

3) Falso Negativo de sua solução


http://www.nltk.org/api/nltk.tokenize.html
'''

import nltk, re, collections
import parte1 as p1

TOKENS_PATTERN = '[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\'\-]+|\S'

'''
@var text {string} Texto que será processado
@return {list} Lista de tokens
'''
def tokenize(text):
    text = text.lower()
    text = re.sub(p1.NUMBER_PATTERN, '', text)
    text = re.sub(p1.NAME_PATTERN_BOVESPA, '', text)
    text = re.sub(p1.NAME_PATTERN, '', text)
    tokenizer = nltk.tokenize.RegexpTokenizer(TOKENS_PATTERN)

    tokens = tokenizer.tokenize(text)
    return tokens
  
'''
@var tokens {list} Lista de tokens
@return {list} Vocabulário ordenado de forma decrescente pelo número de aparições
'''  
def vocabulary(tokens):
    counts = collections.Counter(tokens)
    v = sorted(set(tokens), key=lambda x: -counts[x])
    return v


