# -*- coding: utf-8 -*-
'''
Tarefa 01
• Treine um modelo de regressão linear para prever taxa de visualização
diária de um texto publicado na Web. Ou seja, #visualizações / (dataatual -
datapublicação).
• Fonte dos textos: http://www.saense.com.br/artigos-publicados/  OK
• Arquivo com taxas de visualizações dos textos: download        OK
• Monte o dicionário, eliminando os M% termos mais frequentes (stopwords)
(varie M empiricamente).   OK
• A matriz termo x documento deve conter o TF-IDF das palavras do dicionário. OK
• Mostre o erro quadrático do modelo final. OK
• Liste os atributos (palavras) com maior peso para o modelo. OK
• Aplique o modelo treinado em outros textos disponíveis na Web.
'''

'''
Tarefa 02
Repita Tarefa 01 considerando apenas os títulos dos textos.
'''



import nltk
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

PARTE = "2"
USER = "FranciscoLinux"

MAX_FILES = 29
PERCENTUAL_DE_STOPWORDS = 0.025
NUM_PALAVRAS_MAIOR_PESO = 50

####              PARTE 2 ONLY

VALUE = "alcance" #"alcance", "likes"



slash = r'\\'
if USER == "FranciscoWindows":
    initial_path = r'D:\Projetos\UFS'
elif USER == "FranciscoLinux":
    initial_path = "/home/francisco/git-files"
    slash = "/"
else:
    initial_path = r'C:\Users\icaromarley5\Documents\GitHub'
    
if PARTE == "1":
    parte = slash+'corpusParte1'
    part_path = initial_path + slash+'CC-UFS-Codes'+slash+'2016.1'+slash+'TECI 2'+slash+'trabalho 5'+slash+'Entrada' + parte
    path = part_path +slash +'Saense'
    extra_path = part_path +slash+'OutrosTextos'
    values_path = initial_path +slash+'CC-UFS-Codes'+slash+'2016.1'+slash+'TECI 2'+slash+'trabalho 5'+slash+'Entrada'+slash+'views.txt'
    values_name = "visuzliações/dia"
else:
    parte = slash+'corpusParte2'
    part_path = initial_path +slash+'CC-UFS-Codes'+slash+'2016.1'+slash+'TECI 2'+slash+'trabalho 5'+slash+'Entrada' + parte
    path = part_path + slash+'Saense'
    extra_path = part_path +slash+'OutrosTextos'
    alcance = slash+'alcance.txt'
    likes = slash+'likes.txt'
    values_name = VALUE
    
    if VALUE == "likes":
        values_path = part_path + likes
    else:
        values_path = part_path + alcance
        
    values_path = initial_path +slash+'CC-UFS-Codes'+slash+'2016.1'+slash+'TECI 2'+slash+'trabalho 5'+slash+'Entrada'+slash+'views.txt'
    values_name = "visuzliações/dia"
    
token_dict = {}

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(item)
    return stems
    
def get_text_words(i,path):
    filename = str(i)+".txt"
    file = path+slash+filename
    with open(file, encoding='utf-8') as pearl:
        text = pearl.read()
        return text.lower().translate(string.punctuation)
   
def less_commons(FredDist, n=100):
    tot = len(FredDist.most_common())
    return list((set(FredDist.most_common()) - set(FredDist.most_common(tot - n))))
     
#montando dicionario    {arquivo:palavras}
print("Montando dicionario Geral...")
#for dirpath, dirs, files in os.walk(path):
#    for f in files:
#        fname = os.path.join(dirpath, f)
for i in range(1,MAX_FILES+1):
    filename = str(i)+".txt"
    file = path+slash+filename
    with open(file, encoding='utf-8') as pearl:
        text = pearl.read()
        token_dict[filename] = text.lower().translate(string.punctuation)
            
        
        
#juntar entradas do dicionario em uma so lista
dictionary_list = [] #lista de todas as palavras de todos os textos
text_words = [] #lista dos textos
files = {}
tot = 0
i = 1
for file_name, words in token_dict.items():
    tmp = words.split()
    dictionary_list = dictionary_list + tmp #adiciona lista de palavras
    text_words.append(words) #adiciona texto
    tot = tot + len(tmp)
    files[i] = file_name
    i = i+1
    print(file_name , len(tmp))
print("Total de Palavras:", tot)
print("Tamanho do Dicionario:",len(set(dictionary_list)))
print()



#identificando m% stopwords
percent = PERCENTUAL_DE_STOPWORDS
print("Identificando Stopwords usando", percent)
length = len(dictionary_list)
fdist1 = nltk.FreqDist(dictionary_list)
m = round(percent * length)
stopwords = fdist1.most_common(m) 

print("Quantidade de StopWords:",len(stopwords))
#print("StopWords escolhidas:")
#for word, freq in stopwords:
#    print(word,end=", ")
print("\n")



#remocao de stopwords no dicionario e nos textos
print("Removendo StopWords...")
for tuple_word in stopwords:
    i = 0
    #remocao em cada texto
    for text in text_words:
        if (tuple_word[0]) in text_words:
            text_words[i] = text_words[i].replace(tuple_word[0],"")
        i = i + 1
    #remocao no dicionario
    while tuple_word[0] in dictionary_list:
        dictionary_list.remove(tuple_word[0])
print("Tamanho do novo Dicionario:",len(set(dictionary_list)))
print()



#tfidf
print("Motando TF-IDF...")
tfidf = TfidfVectorizer(tokenizer=tokenize)
print("Executando TF-IDF...")
tfs = tfidf.fit_transform(text_words)
print(tfs.toarray())
print()


mystr = 'Feche os olhos e se imagine vivendo em um mundo sem barreiras, de quaisquer tipo. Um mundo completamente aberto onde você é livre para explorar caminhos e moldar o ambiente à seu bel-prazer.'
response = tfidf.transform([mystr])
print("Teste do TF-IDF:")
print("String de teste:",mystr)
feature_names = tfidf.get_feature_names()
for col in response.nonzero()[1]:
    print(feature_names[col],' \t ',response[0, col])

print()



print("Pegando",values_name,"de cada texto...")
views_per_day = [0]*(MAX_FILES)
i = 1
with open(values_path) as fp:
    for views in fp:
        print(files[i],float(views))
        views_per_day[i-1] = float(views)
        i=i+1
        if i > MAX_FILES:
            break
print()

clf = linear_model.LinearRegression()
print("Executando Regressão Linear...")
clf.fit(tfs.toarray(), views_per_day)
print("Coefidientes:",clf.coef_)
print()


print("Testando Regressão Linear para:")
text1 = tfidf.transform([get_text_words(1,path)])
text2 = tfidf.transform([get_text_words(2,path)])
text9 = tfidf.transform([get_text_words(30,path)])
text10 = tfidf.transform([get_text_words(31,path)])
print("Texto 1:",clf.predict(text1.toarray())[0])
print("Texto 2:",clf.predict(text2.toarray())[0])
print("Texto 30:",clf.predict(text9.toarray())[0])
print("Texto 31:",clf.predict(text10.toarray())[0])
print()



predict = [0]*(MAX_FILES)
for i in range(1, MAX_FILES+1):
    text = tfidf.transform([get_text_words(i,path)])
    predict[i-1] = clf.predict(text.toarray())[0]
erro = mean_squared_error(views_per_day, predict)
print("Erro Médio Quadrático:", erro)
print()




n = NUM_PALAVRAS_MAIOR_PESO
print("As",n,"palavras de maior peso:")    
for word, freq in less_commons(fdist1,n):
    print("'"+word+"'",end=", ")
print("\n")

print("-----------------------------------------------------")
print("Aplicando modelo treinado para outros dados da web...")
path = extra_path
#leitura dos textos
predict = [0]*(MAX_FILES)
for i in range(1, MAX_FILES+1):
    text = tfidf.transform([get_text_words(i,path)])
    predict[i-1] = clf.predict(text.toarray())[0]
erro = mean_squared_error(views_per_day, predict)
print("Erro Médio Quadrático:", erro)
print()
