"""
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres


leitura recomendada:
http://www.nltk.org/book/ch01.html
http://www.nltk.org/book/ch02.html
livro: Jurafsky 2.1, 3.9, 3.11
"""
import os,warnings
import nltk, re, collections, numpy as np
from sklearn import neighbors
from sklearn.naive_bayes import MultinomialNB

warnings.simplefilter('ignore')


TEXTOS_PATH = r"C:\Users\icaromarley5\Documents\GitHub\CC-UFS-Codes\2016.1\TECI 2\trabalho 3\textos"

WORDS = []
doc = {'ciencia':[],'esportes':[], 'negocios':[], 'saude':[]}
FULL_WORDS = {}   
MATRIZES = []
MATRIZES_PARTE2 = []
CATEGORIAS_MATRIZES = []



def count_words(texto, training = False):
    tokenizer = nltk.tokenize.RegexpTokenizer('[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ-]+')
    tokens = tokenizer.tokenize(texto)
    tokens = [token.lower() for token in tokens]
    counter = collections.Counter(tokens)


    if training:
        global FULL_WORDS
        dict_counter = dict(counter)
        for word,qtd in dict_counter.items():
            if word not in FULL_WORDS:
                FULL_WORDS.update({word:qtd})
            else:
                freq = FULL_WORDS[word]
                FULL_WORDS.update({word:freq + qtd})
        global WORDS 
        WORDS = set(list(WORDS)+list(tokens))
    return counter

def get_k_FULL_WORDS(k):
    sorted_words = collections.OrderedDict(sorted(FULL_WORDS.items()))
    list_words = list(sorted_words)
    return list_words[:k]


def read_file(file_dir):
    file = open(file_dir, 'r', encoding='utf8')
    texto = file.read()
    file.close
    return texto    
    
def get_words_matrix(counter, words):
    matrix = []
    for word in words:
        val = 0
        if(counter.get(word) != None):
            val = counter.get(word)
        matrix.append(val)
    return matrix
    
def get_words_matrix_binary(counter, words):
    matrix = []
    for word in words:
        val = 0
        if(counter.get(word) != None):
            val = 1
        matrix.append(val)
    return matrix
    
    
def knn():
    return neighbors.KDTree(MATRIZES)
    
def execute_knn(matrix, k=5):
    #matrix = get_words_matrix(get_counter("ciencia", 9),WORDS)
    return (knn().query(matrix, k=k, return_distance = False))
    
def get_counter(categoria, i, training = False):
    return count_words(read_file(TEXTOS_PATH+"\\"+categoria+"\\d"+str(i)+".txt"), training)
    
def get_categoria_by_tree_index(i):
    return get_categoria(knn().get_arrays()[0][i].tolist())
    
def get_categoria(matriz):
    for i in range(0,len(MATRIZES)):
        if matriz == MATRIZES[i]:
            return CATEGORIAS_MATRIZES[i]
def Bayes(corpus,classif):
       clf = MultinomialNB()
       clf.fit(corpus, classif)
       return clf

def execPart1():
    print("Executando KNN");
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
    global WORDS, doc, FULL_WORDS, MATRIZES, MATRIZES_PARTE2, CATEGORIAS_MATRIZES
           
    z = 0
    for RANGE in kfold_learn:
        WORDS = []
        doc = {'ciencia':[],'esportes':[], 'negocios':[], 'saude':[]}
        FULL_WORDS = {}   
        MATRIZES = []
        MATRIZES_PARTE2 = []
        CATEGORIAS_MATRIZES = []  
        print("Documentos de teste "+str(RANGE))
        corretos = 0
        for categoria in os.listdir(TEXTOS_PATH):
            for i in RANGE:
                counter = get_counter(categoria, i, True)
                doc[categoria].append(counter)
        
        for categoria in os.listdir(TEXTOS_PATH):
            for i in RANGE:
                counter = get_counter(categoria, i)
                matrix = get_words_matrix(counter,WORDS)
                MATRIZES.append(matrix)
                CATEGORIAS_MATRIZES.append(categoria)
                
        for categoria in os.listdir(TEXTOS_PATH):
            for i in kfold_test[z]:
                results = execute_knn(get_words_matrix(get_counter(categoria, i),WORDS), k=5)
                cat1 = 0
                cat2 = 0
                cat3 = 0
                cat4 = 0
                for result in results:
                    cat = (get_categoria_by_tree_index(result))
                    if cat == 'ciencia': 
                        cat1 += 1
                    if cat == 'esportes': 
                        cat2 += 1 
                    if cat == 'negocios': 
                        cat3 += 1
                    if cat == 'saude': 
                        cat4 += 1
                    
                if cat1 >= cat2 and cat1 >= cat3 and cat1 >= cat4:
                    cat = 'ciencia'
                if cat2 >= cat1 and cat2 >= cat3 and cat2 >= cat4:
                    cat = 'esportes'
                if cat3 >= cat1 and cat3 >= cat2 and cat3 >= cat4:
                    cat = 'negocios'
                if cat4 >= cat1 and cat4 >= cat2 and cat4 >= cat3:
                    cat = 'saude'
                
                if cat == categoria:
                    corretos += 1
        print("Taxa de acerto:"+str(corretos/8))
        z += 1






def execPart2(k = 1000):
    print("Executando Naïve Bayes com k="+str(k));
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
                
    classif = np.array(["ciencia","ciencia","ciencia","ciencia",
                        "ciencia","ciencia","ciencia","ciencia",
                        "esportes","esportes","esportes","esportes",
                        "esportes","esportes","esportes","esportes",
                        "negocios","negocios","negocios","negocios",
                        "negocios","negocios","negocios","negocios",
                        "saude","saude","saude","saude",
                        "saude","saude","saude","saude",])  

    global WORDS, doc, FULL_WORDS, MATRIZES, MATRIZES_PARTE2, CATEGORIAS_MATRIZES
           
    z = 0
    for RANGE in kfold_learn:
        WORDS = []
        doc = {'ciencia':[],'esportes':[], 'negocios':[], 'saude':[]}
        FULL_WORDS = {}   
        MATRIZES = []
        MATRIZES_PARTE2 = []
        CATEGORIAS_MATRIZES = []  
        print("Executando "+str(RANGE))
        corretos = 0
        for categoria in os.listdir(TEXTOS_PATH):
            for i in RANGE:
                counter = get_counter(categoria, i, True)
                doc[categoria].append(counter)
        
        for categoria in os.listdir(TEXTOS_PATH):
            for i in RANGE:
                counter = get_counter(categoria, i)
                matrix = get_words_matrix(counter,WORDS)
                MATRIZES.append(matrix)
                CATEGORIAS_MATRIZES.append(categoria)
        
                matrix_parte2 = get_words_matrix(counter,get_k_FULL_WORDS(k))
                MATRIZES_PARTE2.append(matrix_parte2)
                
        corpus  = np.array(MATRIZES_PARTE2)
        bayes = Bayes(corpus,classif)
        
        for categoria in os.listdir(TEXTOS_PATH):
            for i in kfold_test[z]:
                matriz = get_words_matrix(get_counter(categoria, i),get_k_FULL_WORDS(k))
                result = bayes.predict(matriz)
                if result[0] == categoria:
                    corretos += 1
        print("Taxa de acerto:"+str(corretos/8))
        z += 1

 
execPart1()
execPart2(1000)
