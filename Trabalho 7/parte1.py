'''
Crie um extrator de relações via bootstrap seguindo a orientação da seção 2.2 
de Hearst (92), "Automatic acquisition of hyponyms from large text corpora":
        http://acl-arc.comp.nus.edu.sg/archives/acl-arc-090501d3/data/pdf/anthology-PDF/C/C92/C92-2082.pdf

    • Defina pelo menos dois tipos de relações distintas
    • Você pode usar uma base de conhecimento (DBPedia, Wordnet, etc.) para 
        identificar exemplos que seguem as relações desejadas (conforme passo 2
        do procedimentos de Hearst)
    • Use o corpus Paramopama; OU
    • Gere um novo corpus usando o WTCoGen a partir de uma URL com conteúdo 
        desejado/orientado
        
OBS: De repente uma olhadela em serve para algumas inspirações também
    http://ilpubs.stanford.edu:8090/421/1/1999-65.pdf
 




____________________________________________________________
Corpus e relações propostas:

    





Artigo topico 2.2

2.2 Discovery of New Patterns
How can these patterns be found? Initially we discovered patterns (1)-(3) 
by observation, looking through text and noticing the patterns and the 
relationships they indicate. In order to find new patterns automatically, 
we sketch the following procedure:
    
1. Decide on a lexical relation, R, that is of interest, e.g., "group/member"
    (in our formulation this is a subset of the hypouylny relation).

2. Gather a list of terms for which this relation is known to hold, e.g., 
    "England-country'. This list can be found autonmtically using the method 
    described here, bootstrapping from patterns found by hand, or by 
    bootstrapping from an existing lexicon or knowledge base.

3. Find places in the corpus where these expressions occur syntactically near 
    one another and record the environment.

4. Find the commonalities among these environiments and hypothesize that
    common ones yield patterns that indicate the relation of interest.

5. Once a new pattern has been positively identified, use it to gather more 
    instances of the target relation and go to Step 2. 

We tried this procedure by hand using just one pair of terms at a time. In the 
first case we tried the "Fngland-country" example, and with just this pair
we tound new patterns (4) and (5), as well as (1)-(3) which were already known.
Next we tried "tank-vehicle" and discovered a very productive pattern, pattern 
(6). (Note that for this pattern, even though it has an emphatic element, this 
does not affect the fact that the relation indicated is hypouymic.) 

We have tried applying this technique to meronymy (i.e., the part/whole relation), 
but without great success. The patterns found for this relation do dot tend 
to uniquely identify it, but can be used to express other relations as well. It
may be the case that in English the hyponymy relation is especially amenable to
this kind of analysis, perhaps due to its "naming" nature. However, we have had 
some success at identification of more specific relations, such as patterns that 
indicate certain types of proper nouns. 

We have not implemented an automatic version of this algorithm, primarily 
because Step 4 is underdetermined.


Links sobre extração de relação com bootstrap(checar):
http://www.aclweb.org/anthology/R09-2014
http://www.dfki.de/~feiyu/thesisfeiyuxu.pdf
http://www.emnlp2015.org/proceedings/EMNLP/pdf/EMNLP056.pdf
http://stp.lingfil.uu.se/~santinim/sais/2016/09_PracticalActivity_RelationExtraction.pdf


'''

from bs4 import *
import urllib.request as urllib

with open('corpusdefilmes.txt', 'w') as file:
    for i in range(1,200):
        print("Filme:",i)
        try:
            url = "http://www.adorocinema.com/filmes/filme-"+str(i)
            html = urllib.urlopen(url).read()
            continuar = True
        except:
            print("\tNão Encontrado")  
            continuar = False
        if(continuar):
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.findAll("div", {"class":"titlebar-title titlebar-title-lg"})
            file.write(str("Nome do filme: "+title[0].get_text()+"\n"))
            
            metaDatas = soup.select("div.meta-body-item")
            for metaData in metaDatas:
                if(metaData.contents[1].get_text() == "Data de lançamento"):
                    if(len(metaData.contents) > 3):
                        data = metaData.contents[3].get_text().strip()
                    else:
                        data = metaData.contents[2].strip()[:4]
                    file.write(str("\tData de lançamento: "+data+"\n"))
                if(metaData.contents[1].get_text() == "Direção:"):
                    file.write(str("\tDireção: "+metaData.contents[3].get_text().strip()+"\n"))
                if(metaData.contents[1].get_text() == "Elenco:"):
                    file.write(str("\tElenco: "+metaData.contents[3].get_text().strip()))
                    if(len(metaData.contents)>5):
                        file.write(str(", "+metaData.contents[5].get_text().strip()))
                    if(len(metaData.contents)>7):
                        file.write(str(", "+metaData.contents[7].get_text().strip()))
                    file.write(str("\n"))
                if(metaData.contents[1].get_text() == "Gêneros"):
                    file.write(str("\tGêneros: "+metaData.contents[3].get_text().strip()))
                    if(len(metaData.contents)>5):
                        file.write(str(", "+metaData.contents[5].get_text().strip()))
                    if(len(metaData.contents)>7):
                        file.write(str(", "+metaData.contents[7].get_text().strip()))
                    file.write(str("\n"))
                if(metaData.contents[1].get_text() == "Nacionalidade"):
                    file.write(str("\tNacionalidade: "+metaData.contents[3].get_text().strip()+"\n"))
    file.close()




















