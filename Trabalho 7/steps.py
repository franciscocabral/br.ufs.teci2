def step2(data_corpus,new_instance_dict):
	context_list = []
	for group,member in new_instance_dict.items():
		group = group.split()
		member = member.split()
		compare_list = [group,member]
		for element in compare_list:#busca normal e busca invertida                           
			#reseta contextos
			#print("_______________________resetando contextos.")
			possible_context = ""
			context ="" #string de palavras do contexto onde ocorrem gorup e member
			is_inside_context = False #resetando contexto
			n_element = len(element)
			beginning_n = 0
			ending_n = 0
			index_aux = compare_list.index(element)
			element_aux = compare_list.pop(compare_list.index(element))
			other_element = compare_list[0] #outro elemento da relacao
			compare_list.insert(index_aux,element_aux)
				
			for word in data_corpus.split():
				#print("word em ",word)
				word = word + " "
				#print("element[beggining_n] em ",element[beginning_n], "n em ",beginning_n)
				#faz a comparacao
				if (not is_inside_context):
					#print("fora do contexto")                                                       
					if (element[beginning_n] in word and beginning_n < n_element):
						if element[beginning_n] in word and beginning_n == n_element - 1:
							#print("terminou de casar a primeira palavra")                                                               
							beginning_n = 0
							is_inside_context = True
						else:
							#print("casou para ",element[beginning_n], " ",word)    
							beginning_n = beginning_n + 1
					else:#se a comparacao falhar na metade
						if(beginning_n > 0):
							beginning_n = 0
				else:#contexto
				#print("dentro de context0")
				#print("outro elemento",other_element[ending_n])
				#print(word)
				#print(other_element[ending_n] in word)
					
					if (other_element[ending_n] in word):
						if (ending_n == len(other_element)-1):#palavra final
							context_list.append(context)
							#print(">>>>>>>>>>>>>>>>guardando contexto")
							#print(len(context))
							#reseta valores
							is_inside_context = False
							context = " "
							possible_context = ""
						else:
							#print("guardando no possible context a word ",word)
							ending_n = ending_n + 1
							possible_context = possible_context + word #guarda para o caso de falha
					else:
						if (ending_n > 0): #comparacao falhou na metade
							ending_n = 0
							context = context + possible_context #adiciona o falso final
							possible_context = "" #reseta contexto de falso final
						#print("guardando no contexto word ",word)
						context = context  + word #adiciona palavra atual ao contexto


	return context_list
	
def step3 (lista):
    freq = {}
    list_geral = []   
    #lista_geral = []
    for element in lista:
        cont = lista.index(element)
        elemento_lista = lista[cont]
        if (elemento_lista in list_geral):
            freq[elemento_lista] = freq[elemento_lista]+1
        else:
            freq[elemento_lista] = 1
            list_geral.append(elemento_lista)
    return list(freq.items())
    
def step4 (lista, padroes, k_termos):
    list_k_termos = [] 
    cont = 0
    if ((k_termos <= len(lista)) & (k_termos > 0)): 
        while ( (len(list_k_termos) < len(lista)) & (len(list_k_termos) < k_termos) ):
        #for i in range (0,k_termos):
            #lista2 = sorted(lista, key=itemgetter(1), reverse= True)
            #string = lista2[i][0] #[nome, frequencia]
            if not( sorted(lista, key=itemgetter(1), reverse= True)[cont][0] in padroes):
                list_k_termos.append(sorted(lista, key=getKey, reverse= True)[cont])
                
            cont += 1
    else:
        print ("k escolhido muito grande. Tente um menor")
    return list_k_termos
    
def step4_2 (lista):
    escolha = 0
    pattern_chosen = []
    #list_adapt = sorted(lista, key=itemgetter(0))
    while (escolha > -1):   
        print ("Lista de opções")        
        #print (list_adapt)
        print (lista)
        escolha = int(input("Digite a posição do termo  na lista exibida acima,que deseja escolher como novo padrão. (Digite valor negativo para encerrar as inserções "))
        #print(lista)
        if (escolha > len(lista)-1 ):
            print ("Escolha inválida! Posição não contida na lista. Escolha uma posição menor :), ou valor negativo para encerrar as inserções")
            print ("Padrões adicionados")
            print (pattern_chosen)
            
        else:
            if (escolha < 0):
                break
            else:
                if not (lista[escolha][0] in pattern_chosen):
                    pattern_chosen.append(lista[escolha][0])
                    print ("Padrões adicionados")
                    print (pattern_chosen)
                else:
                    print ("Padrão já selecionado anteriormente. Escolha um novo padrão ou digite valor negativo para encerrar as inserções")
                    print ("Padrões adicionados")
                    print (pattern_chosen)
                    
    return pattern_chosen 
    
def step5(corpus, pattern):
    new_instances = False
    pattern = pattern[1:-1]
    position = corpus.find(pattern)
    while position is not -1:
        tmp_pos = position - 1
        while not (tmp_pos >= 0 and (corpus[tmp_pos] == "." or
                   corpus[tmp_pos] == "," or corpus[tmp_pos] == "\n")): tmp_pos -= 1
        r2_sentence = clear(corpus[tmp_pos:position])
        r2_sentence = re.search("(([A-Z][a-z]*(\s[A-Z][a-z]+)+)|([A-Z][a-z]+(\s[A-Z][a-z]+)*)|([A-Z][a-z]\.([A-Z][a-z]+(\s[A-Z][a-z]+)*)))$", r2_sentence).group(0)

        tmp_pos = position + len(pattern)
        while not ((corpus[tmp_pos] == ".") or corpus[tmp_pos] == ","
                    or (corpus[tmp_pos] == "\n")): tmp_pos += 1
        r1_sentence = clear(corpus[(position + len(pattern)):tmp_pos])
        r1_sentence = re.search("(([A-Z][a-z]*(\s[A-Z][a-z]+)+)|([A-Z][a-z]+(\s[A-Z][a-z]+)*)|([A-Z][a-z]\.([A-Z][a-z]+(\s[A-Z][a-z]+)*)))", r1_sentence).group(0)

        position = corpus.find(pattern, position + len(pattern))

        if addinstances([r1_sentence, r2_sentence]):
            new_instances = True
    return new_instances
