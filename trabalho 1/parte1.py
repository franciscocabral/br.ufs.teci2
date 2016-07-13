'''
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ãcaro Oliveira, Ãcaro Torres

TRABALHO 1, PARTE 1

1) Crie Expressões Regulares para extrair e listar todos os valores 
    numéricos (inteiros, moedas e percentuais) existentes no texto.
        ex: 0,85%, R$ 5,90, 10 mil
    
2) Crie Expressões Regulares para extrair e listar os nomes próprios (e siglas).
       ex: Oi, OIBR3, Banco Central, Eike Batista
    
3) Compute a taxa de Falso Positivo.

4) Compute a taxa de Falso Negativo.

'''
import re

NUMBER_PATTERN = r'(?<!\w)(((R\$ ?)?[\+-\.,\/:$h]*[0-9]+[%º]?( ?mil)?)+)'
NAME_PATTERN = r'(?!Atualizada|Com Reuters|Internacionais)(?<!\n)([A-Z][\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\'-]+( (([A-Z][\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\'-]+)|&|[0-9]+))*)(?:[ \.?!,\):;])'
NAME_PATTERN_BOVESPA = r'(Bovespa)'
RELEVANT_NUMBERS = ["2,6%","4%8","27/08/2013","17h32","20/03/2014",
    "19h36","0:00","27","2,6%","50.091,55","4%",
    "2","4,24%","0,65%","R$ 2,368","11","4,07%","R$ 17,45","3,33%","R$ 16,57",
    "74","0,85%","R$ 5,90","0,49%","R$ 4,14","0,46%","R$ 19,49",
    "14,8%","R$ 0,69","6,72%","R$ 2,22","5,56%","R$ 1,70",
    "1,46%","R$ 31,73","10 mil","16","17","18","135.300","1º",
    "17","18","1,14%","14.776","500","1,59%","1.630","2,16%",
    "3.578","300","1,7%","1.202","50","2,6%","2.749","0,79%",
    "2,28%","2,42%","3,96%","3,71%","0,69%","0,59","0,11%","0,94%",
    "1,63%","0,34%","0,11%"]
RELEVANT_NAMES = ["Bovespa","Síria","Petrobras","UOL","São Paulo","Bovespa","Ibovespa","Bolsa",
    "Petrobras","PETR3", "PETR4","Bolsa","Bolsa","Bolsa","Ibovespa","Eike Batista","Síria",
    "Estados Unidos","Síria","Petrobras","Petrobras","PETR4","Bolsa","PETR3","Bolsa",
    "Marfrig","MRFG3","Oi","OIBR3","CPFL","CPFE3","Eike Batista","OGX","OGXP3","PDG","PDGR3",
    "Brookfield","BISA3","Vale","VALE5","BC","Banco Central","BC","Federal Reserve","EUA","Síria",
    "Estados Unidos","Dow Jones","Standard & Poor's 500","Nasdaq","FTSEurofirst 300","Euro STOXX 50",
    "Londres","Financial Times","Frankfurt","DAX","Paris","CAC-40","Filipinas","Indonésia",
    "Nikkei","Japão","Hong Kong","Seul","Taiwan","Cingapura","Bolsa","Xangai","Sydney",
    "Reuters"]
    
'''
@var text {string} Texto a ser processado
@return void
'''
def print_text_without_names_and_numbers(text):
    text = re.sub(NUMBER_PATTERN, '{number}', text)
    text = re.sub(NAME_PATTERN, '{name}', text)
    text = re.sub(NAME_PATTERN_BOVESPA, '{name}', text)
    rows = text.split("\n")
    for row in rows:
        print(row)

'''
@var text {string} Texto a ser processado
@return {list} Lista com os valores que foram encontrados pela expressão regular
'''
def get_numbers_list(text):
    matchs = re.findall(NUMBER_PATTERN, text)    
    return [x[0] for x in matchs]
    
'''
@var text {string} Texto a ser processado
@return {list} Lista com os valores que foram encontrados pela expressão regular
'''
def get_names_list(text):
    matchs = re.findall(NAME_PATTERN, text)
    matchs.append(re.findall(NAME_PATTERN_BOVESPA, text))
    return [x[0] for x in matchs]

'''
@todo esta função esta errada @icaro irá corrigir

OBS: A função utiliza a heurística a nivel de granularidade 
de que cada palavra é o elemento mínimo a ser considerado

@var text {string} Texto a ser processado 
@var text {list} Lista de elementos relevantes
@return   {int} Diferença da quantidade de palavras no texto pela quantidade de elementos relevantes 
'''
def get_not_relevants_count(text, relevants):
    return len(text.split()) - len(relevants)
    

'''
@var matches {list} Lista de valores a serem testados
@var relevants {list} Lista de valores relevantes
@return {list} Lista de falsos positivos
'''
def get_false_positives_list(matches, relevants):
    false_positives = []
    for match in matches:
        if (match not in relevants): 
            false_positives.append(match)
    return false_positives
    
'''
@var matches {list} Lista de valores a serem testados
@var relevants {list} Lista de valores relevantes
@return {list} Lista de falsos negativos
'''
def get_false_negatives_list(matches, relevants):
    false_negatives = []
    for relevant in relevants:
        if relevant not in matches:
            false_negatives.append(relevant)
    return false_negatives
   

'''
@var false_positives_count {int} Quantidade de falsos positivos
@var not_relevant_count {int} Quantidade de valores não relevantes
@return {float} Taxa percentual de falsos positivos
'''
def get_false_positives_rate(false_positives_count, not_relevant_count):
    return false_positives_count/ not_relevant_count* 100
   
'''
@var false_negatives_count {int} Quantidade de falsos negativos
@var relevant_count {int} Quantidade de valores relevantes
@return {floar} Taxa percentual de falsos negativos
''' 
def get_false_negatives_rate(false_negatives_count,relevant_count):
    return false_negatives_count/ relevant_count* 100

