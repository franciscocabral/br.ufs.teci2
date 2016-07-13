"""
TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE

GRUPO: Francisco Cabral, Ícaro Oliveira, Ícaro Torres


leitura recomendada:
http://www.nltk.org/book/ch01.html
http://www.nltk.org/book/ch02.html
livro: Jurafsky 2.1, 3.9, 3.11
"""
import parte1 as p1
import parte2 as p2
import parte3 as p3
import parte4 as p4

ANY_PATTERN = '[\wáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\'\-]+|\S'
FILE_PATH = "bovespa.txt"

file = open(FILE_PATH, 'r')
TEXT = file.read()
TEXT = "\n"+TEXT
file.close()

TEXT_WITH_RUIDO = p4.ruidar(TEXT);
corrections = p4.get_corrections(p2.vocabulary(p2.tokenize(TEXT)), TEXT_WITH_RUIDO)

print("""
,_____________________________________________________________________________,
|                                                                             |
| TRABALHO DE TÓPICOS ESPECIAIS EM COMPUTAÇÃO INTELIGENTE                     |
| GRUPO: Francisco Cabral,                                                    |
|        Ícaro Oliveira,                                                      |
|        Ícaro Torres                                                         |
|_____________________________________________________________________________|""")

opt = -1
while (opt != "0"):
    print("""
,_____________________________________________________________________________,
|                                                                             |
| TRABALHO 1 - PARTE 1                                                        |
|_____________________________________________________________________________|
|                                                                             |
| OPÇÔES:                                                                     |
|     1) Ver texto ORIGINAL                                                   |
|     2) Ver NÚMEROS selecionados                                             |
|     3) Ver NOMES próprios elecionados                                       |
|     4) Ver texto sem NÚMEROS ou NOMES                                       |
|     5) Ver TAXA de falso POSITIVO e falsos NEGATIVOS                        |
|     6) Ver LISTA de falso POSITIVO                                          |
|     7) Ver LISTA de falso NEGATIVO                                          |
|     0) Continuar para PARTE 2                                               |
|_____________________________________________________________________________|""")
    opt = input('Opção:')
    nums_matches = p1.get_numbers_list(TEXT)
    nums_not_relevant = p1.get_not_relevants_count(TEXT, p1.RELEVANT_NUMBERS) 
    
    nums_fpl = p1.get_false_positives_list(nums_matches, p1.RELEVANT_NUMBERS)
    nums_fnl = p1.get_false_negatives_list(nums_matches, p1.RELEVANT_NUMBERS)
    
    nums_fpr = p1.get_false_positives_rate(len(nums_fpl), nums_not_relevant)
    nums_fnr = p1.get_false_negatives_rate(len(nums_fnl), len(p1.RELEVANT_NUMBERS))
        
    names_matches = p1.get_names_list(TEXT)
    names_not_relevant = p1.get_not_relevants_count(TEXT, p1.RELEVANT_NAMES) 
    
    names_fpl = p1.get_false_positives_list(names_matches, p1.RELEVANT_NAMES)
    names_fnl = p1.get_false_negatives_list(names_matches, p1.RELEVANT_NAMES)
    
    names_fpr = p1.get_false_positives_rate(len(names_fpl), names_not_relevant)
    names_fnr = p1.get_false_negatives_rate(len(names_fnl), len(p1.RELEVANT_NAMES))
    
    if(opt == "1"):
        for row in TEXT.split("\n"):
            print(row)
    if(opt == "2"):
        print(p1.get_numbers_list(TEXT))
    if(opt == "3"):
        print(p1.get_names_list(TEXT))
    if(opt == "4"):
        print(p1.print_text_without_names_and_numbers(TEXT))
    if(opt == "5"):
        
        print("Números:")
        print("Falso Positivo: "+str(round(nums_fpr,2))+"%")
        print("Falso Negativo: "+str(round(nums_fnr,2))+"%")
        
        print("Nomes Próprios:")
        print("Falso Positivo: "+str(round(names_fpr,2))+"%")
        print("Falso Negativo: "+str(round(names_fnr,2))+"%")
        
    if(opt == "6"):
        print("Números:")
        print(nums_fpl)
        print("Nomes Próprios:")
        print(names_fpl)
    if(opt == "7"):
        print("Números:")
        print(nums_fnl)
        print("Nomes Próprios:")
        print(names_fnl)
  

opt = -1
while (opt != "0"):
    print("""
,_____________________________________________________________________________,
|                                                                             |
| TRABALHO 1 - PARTE 2                                                        |
|_____________________________________________________________________________|
|                                                                             |
| OPÇÔES:                                                                     |
|     1) Ver TOKENS                                                           |
|     2) Ver VOCABULÁRIO                                                      |
|     3) Ver TAXA de falso POSITIVO e falsos NEGATIVOS                        |                                         
|     0) Continuar para PARTE 3                                               |
|_____________________________________________________________________________|""")
    opt = input('Opção:')
    
    if(opt == "1"):
        print(p2.tokenize(TEXT))
    if(opt == "2"):
        print(p2.vocabulary(p2.tokenize(TEXT)))
    if(opt == "3"):
        print("Falso Positivo: " + "0.00 %")
        print("Falso Negativo: " + "0.00 %")

opt = -1
while (opt != "0"):
    print("""
,_____________________________________________________________________________,
|                                                                             |
| TRABALHO 1 - PARTE 3                                                        |
|_____________________________________________________________________________|
|                                                                             |
| OPÇÔES:                                                                     |
|     1) Ver STEMMING                                                         |
|     2) Ver LEMMING                                                          |                                        
|     0) Continuar para PARTE 4                                               |
|_____________________________________________________________________________|""")
    opt = input('Opção:')
    tokens = p2.tokenize(TEXT)
    if(opt == "1"):
        print(p3.stemming(tokens))
    if(opt == "2"):
        print(p3.lemmatizer(tokens))
 
opt = -1

while (opt != "0"):
    print("""
,_____________________________________________________________________________,
|                                                                             |
| TRABALHO 1 - PARTE 4                                                        |
|_____________________________________________________________________________|
|                                                                             |
| OPÇÔES:                                                                     |
|     1) Ver texto COM ruido                                                  |
|     2) Ver texto SEM ruido                                                  | 
|     3) Ver lista de correções                                               | 
|     0) SAIR                                                                 |
|_____________________________________________________________________________|""")
    opt = input('Opção:')
    
    if(opt == "1"):
        print(TEXT_WITH_RUIDO)
    if(opt == "2"):
        print(TEXT)
    if(opt == "3"):
        for word, correction in corrections.items():
            print(word)
            for dist, possibilities in correction.items():
                print(" "+str(dist)+")")
                print("  "+str(possibilities))
            print()
#    if(opt == "4"):
#        print(p4.correct(corrections, TEXT_WITH_RUIDO))

