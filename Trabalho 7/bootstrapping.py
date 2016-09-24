import steps

#leitura do corpus
start = r"C:\Users\icaromarley5\Documents\GitHub"
corpus = start + r"\CC-UFS-Codes\2016.1\TECI 2\Trabalho 7\corpus\corpus.txt"
file_corpus = open(corpus,encoding='utf-8')
data_corpus = file_corpus.read()
#etapa de pre-processamento do corpus


#definicoes de relacoes
#passo1
relations = [["diretor","filme"]]#,["ator","filme"]]

#padroes pre definidos
instance_dict1 = {"Jerry Schatzberg":"Espantalho",
               "Bob Fozzy":"Cabaret",
               "Oliver Stone":"JFK - A Pergunta Que Não Quer Calar",
               }
instance_dict2 = {}

instances_list = [instance_dict1,instance_dict2]

#outros parametros necessarios
n_threshold = 2

i = 0
for relation in relations:
	pattern_list = []
	#tratamento para separar parte processada a parte ainda a ser processada
	instance_dict = instances_list[i]
	new_instance_dict = instance_dict #dict a ser processado
	instance_dict = {}                #dict processado

	while True:
		#passo2
		#para cada nova instancia
		#ache e guarde trechos do corpos onde essas instancias aparecem
		#lista de strings
		context_list = steps.step2(data_corpus,new_instance_dict)
		#anexe a lista de instâncias novas a lista de instâncias 				
		instance_dict.update(new_instance_dict) #guarda o dict processado
		
		
		#passo3
		#compute a frequencia dos trechos encontrados
		#(hipotese definida: os trechos com maior frequencia tem mais chance de serem padrões)
		
		freq_list = steps.step3(context_list) 
		#passo4
		#selecionar os 	n_threshold de maior frequencia
		#(que já não estiverem na lista de padrões)
		#lista de strings
		k_most = steps.step4(freq_list,pattern_list,threshold)


		if not k_most:#lista vazia. nao ha padroes novos
			break
		
		#informar ao programador os trechos selecionados
		#receber do programador quais são validos (pattern_chosen)
		#lista de strings
		pattern_chosen = steps.step4_2(k_most)
		#passo5
		#para cada padrao escolhido, ache instancias novas da relacao com esse padrao
		#adicione as instancias novas encontradas no dict de instancias novas
		if not pattern_chosen:#lista vazia. nao ha padroes escolhidos
			break
		for pattern in pattern_chosen:
			new_instances = [True for padrao in padroes if steps.step5(data_corpus, new_instance_dict)]
		#adicione os w padrões validados na lista de padrões  	
		if new_instances: pattern_list.append(patterns_chosen)
		i = i + 1
               

		
