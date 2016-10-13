'''

Tarefa 01
    • Crie um pequeno sistema de QA baseado em IR
    • Um guia para a tarefa é implementar uma versão simples do sistema
    AskMSR, que é descrito no artigo
    • Brill, Eric, Susan Dumais, and Michele Banko. "An analysis of the AskMSR questionanswering
        system." Proceedings of the ACL-02 conference on Empirical methods in natural 
        language processing-Volume 10. Association for Computational Linguistics,2002.
    • Prioridade deve ser dada para Pt BR
    • Uma simplificação da tarefa é selecionar previamente um conjunto de
        documentos de um mesmo assunto/domínio (ao invés de se executar a
        etapa de IR na Web). Neste caso, o sistema de QA funciona como uma
        espécie de FAQ automático para um determinado domínio.

'''

'''
Quem interpretou o coringa em "The Dark Knight"?
Quem dirigiu Ghostbusters?
Quem dirigiu Batman?
Quem dirigiu Efeito Borboleta?
Quanto vendeu o filme The Dark Knight?
Qual personagem interpretado por Bill Murray no filme Ghostbusters?
De quanto foi a maior bilheteria da história?
Quem elegeu Ghostbusters melhor filme de comédia?
Quais categorias do Oscar Birdman venceu?
Quanto arrecadou o filme WALL·E em seu primeiro dia?
Quando foi dirigido batman?
Quantos ingressos o filme The Dark Knight vendeu?
Quem andou no batpod de papelão?
Quando ledger morreu?
Quando a warner anunciou the dark knight?
'''

import re
import nltk
import codecs
from operator import itemgetter

VERBOSE = True
ACCURACY_TEST = True
BEST_ANSWER_COUNT = 5

questions = {
     'Quem interpretou o coringa em "The Dark Knight"?'                        : "Heath Ledger",
     "Quem dirigiu Ghostbusters?"                                              : "Ivan Reitman",
     "Quando ledger morreu?"                                                   : "22 de janeiro de 2008",
     "Quando a warner anunciou the dark knight?"                               : "31 de julho de 2006",
     "Quantos ingressos o filme The Dark Knight vendeu?"                       : "22,37 milhões",
     "Quanto arrecadou o filme WALL-E em seu primeiro dia?"                    : "US$ 23.7 milhões",
     "Quem dirigiu Ghostbusters?"	                                            :	"Ivan Reitman"	,
     "who do you gonna call?"	                                            :	"Ghostbusters!"	,
     "Qual personagem interpretado por Bill Murray no filme Ghostbusters?"	    :	"Peter Venkman"	,
     "quem elegeu ghostbusters um dos melhores filmes de comédia?"	          :	"American Film Institute"	,
     "De quando é ghostbusters?"	                                            :	"1984"	,
     "quando estreou ghostbusters?"	                                       :	"1984"	,
     "Quem andou no batpod de papelão?"	                                       :	"Hugh Jackman"	,
     "quanto foi a bilheteria do filme cavaleiro das trevas?"	                :	"US$ 1.001.921.825"	,
     "quando a warner anunciou the dark knight?"	                           :	"31 de julho de 2006"	,
     "quando ledger morreu?"	                                                  :	"22 de janeiro de 2008"	,
     "Quem dirigiu independence day?"	                                       :	"Roland Emmerich"	,
     "quem ganhou oscar de melhores efeitos visuais?"                          :	"Independence day"	,
     "quando estreou independence day?"	                                       :	"1996"	,
     "Quem dirigiu As aventuras de Pi ?"	                                 :	"Ang Lee"	,
     "As aventuras de Pi estreou em que ano?"	                                 :	"2012"	,
     "Quem dirigiu  Waking Life?"	                                            :	"Richard Linklater"	,
     "quando estreou Waking Life?"	                                            :	"2001"	,
     "quem dirigiu O Menino da Internet: A História de Aaron Swartz?"	    :	"Brian Knappenberger"	,
     "em que ano estreou O menino da internet: A História de Aaron Swartz?"    :	"2014"	,
     "quando estreou O menino da internet: A História de Aaron Swartz?"	    :	"2014"	,
     "Quem dirigiu birdman?"	                                                  :	"Alejandro González Iñárritu"	,
     "qual foi o personagem de michael keaton em birdman?"	                :	"Riggan Thomson"	,
     "quando foi a estreia de birdman?"	                                       :	"2014"	,
     "Quem dirigiu  Dogville?"	                                            :	"Lars von Trier"	,
     "quando estreou Dogville?"	                                            :	"2003"	,
     "Quem dirigiu efeito borboleta?"	                                      :	"Eric Bress"	,
     "quando estreou Efeito borboleta?"	                                       :	"2004"	,
     "quando filmaram o discurso do rei?"	                                 :	"2010"	,
     "quem dirigiu O discurso do rei?"	                                       :	"Tom Hooper"	,
     "quem dirigiu inception?"	                                            :	"Christopher Nolan"	,
     "quem estrelou inception?"	                                            :	"Leonardo Dicaprio"	,
     "onde inception teve sua estréia?"	                                       :	" em Londres"	,
     "quanto foi o orçamento oficial de inception?"	                           :	"160 milhões de dólares"	,
     }

'''
    A partir de um grupo de tokens(words), aplica o stemming para encontrar a 
    base da palavra.

    @param {String[]} words Texto tokenizado a ser manipulado
    @return {String[]}   
'''
def stemming(words):
    stemmedWords = []
    st = nltk.stem.RSLPStemmer()
    for word in words:
        stemmedWords.append(st.stem(word))
    return stemmedWords

    
pronomes = {
       "quem":       "entity",
       "qual":       "entity",
       "quais":      "entity",
       "que ano":    "time",
       "quando":     "time",
       "onde":       "location",
       "aonde":      "location", 
       "quanto":     "measure",
       "quantos":    "measure",
       "quanta":     "measure",
       "quantas":    "measure",
       "who":        "entity"}
           
verbosInfinitivo = [
      "Permitir", "Aplicar", "Cozer", "Diminuir", "Descartar", "Dirigir", "Secar", "Eliminar",
      "Friccionar", "Acabar", "Despedir", "Formular", "Gerar", "Melhorar", "Elevar", "Carregar",
      "Minimizar", "Modificar", "Mover", "Produzir", "Receber", "Reduzir", "Remover", "Resistir",
      "Restringir", "Dar forma", "Organizar", "Estocar", "Suportar", "Transmitir", "Transportar",
      "Pesar", "Empacotar", "Atuar", "Amplificar", "Aplicar", "Mudar", "Fechar", "Coletar", "Conduzir",
      "Conter", "Controlar", "Criar", "Diminuir", "Emitir", "Estabelecer", "Prender", "Filtrar",
      "Segurar", "Inflamar", "Impedir", "Melhorar", "Aumentar", "Induzir", "Isolar", "Interromper",
      "Limitar", "Localizar", "Manter", "Modular", "Equipar", "Mover", "Prevenir", "Proteger",
      "Corrigir", "Reduzir", "Repelir", "Rotacionar", "Proteger", "Fortalecer", "Encurtar", "Espaçar",
      "Sustentar", "Determinar","APONTA", "DISTINGUIR", "PESQUISAR", "ADOTAR", "DIZER", "PREPARAR",
      "APLICAR", "ELABORAR", "PREVER", "AMPLIAR", "ENUMERAR", "PRODUZIR", "AUTORIZAR", "ENFATIZAR",
      "RECONSTRUIR", "CALCULAR", "ENUNCIAR", "REDIGIR", "CARACTERIZAR", "ESCOLHER", "REESCREVER",
      "CATEGORIZAR", "ESBOÇAR", "RELACIONAR", "CITAR", "ESCREVER", "RELATAR", "CLASSIFICAR", "ESPECIFICAR",
      "REPRODUZIR", "COMBINAR", "ESTABELECER", "RESOLVER", "COMPILAR", "EXEMPLIFICAR", "RESUMIR", "COMPARAR",
      "EXPLICAR", "REORGANIZAR", "COMPOR", "EXPRESSAR", "REVER", "CONCEITUAR", "FAZER", "RESUMO", "SELECIONAR",
      "CONCLUIR", "GENERALIZAR", "SER", "CAPAZ", "CONFIRMAR", "IDENTIFICAR", "SUBDIVIDIR", "CONSTATAR",
      "ILUSTRAR", "SUBLINHAR", "CONTRASTAR", "INDICAR", "SUMARIZAR", "CONVERTER", "INFERIR", "SITUAR",
      "CRITICAR", "INVENTAR", "TRADUZIR", "DISCRIMINAR", "JUSTIFICAR", "TRAÇAR", "DEFENDER", "LISTAR",
      "UTILIZAR", "DEFINIR", "MANIPULAR", "VALORIZAR", "DELIMITAR", "MARCAR", "VERIFICAR", "DEMONSTRAR",
      "MODIFICAR", "ORGANIZAR", "DETERMINAR", "MOSTRAR", "DESCREVER", "NUMERAR", "DESTACAR", "OBTER",
      "DIFERENCIAR", "OPERAR"]
      
verbos = ["é","são","teve","condecorado", "estrelou","fotografaram", "fotografado", "fotografou" , "estava", "era", "ocoreu", "criou", "dirigiu", "escreveu", "custou", "filmou",
      "filmado", "andou", "interpretou", "call" ,"representou","irá","lançado","produzido","gravado","distribuido",
      "escrito","começou","foi","morreu", "anunciou", "estreou","exibido", "ganhou", "indicado","arrecadou"]
      
verbosStemmed = stemming(verbosInfinitivo+verbos)
          
namedEntitiesPerType = {
    "entity":["AFI's", 'Aaron', 'Aaron Eckhart', 'Aaron Hillel Swartz', 'Aaron Swartz', 'Abadia', 'Abadia de Westminster', 'Adam Baldwin', 'Adam Goldberg', 'Adil Hussain', 'Adoro Cinema', 'Adrien Brody', 'Agência de Proteção Ambiental dos Estados Unidos', 'Ainda', 'Al Franken', 'Alan Bernett', 'Albert', 'Albert Nimzicki', 'Albert Wolsky', 'Alberta', 'Alberto', 'Alejandro González Iñárritu', 'Alemanha', 'Alemanha Nazista', 'Alexander Dinelaris', 'Alexandre Desplat', 'Alfred Pennyworth', 'Alice', 'Alice Drummond', 'Alicia Casse', 'Alien', 'Allegretto', 'Am Legend', 'America', 'American Film Institute', 'Ammy Smart', 'Amy Ryan', 'Amy Smart', 'América do Norte', 'An Eternal Golden Braid', 'Anandi', 'Andrea Di Stefano', 'Andrea Riseborough', 'Andrea Treborn', 'Andrew Garfield', 'Andrew Klavan', 'Andrew Roberts', 'Andrew Stanton', 'Ang Lee', 'Anna Ramirez', 'Annie', 'Annie Potts', 'Anonymous', 'Anos de American Film Institute', 'Antes de Eckhart', 'Antes de Gyllenhaal', 'Anthony Andrews', 'Anthony Crivello', 'Anthony Dod Mantle', 'Anthony Michael Hall', 'Anthony Rhulen', 'Antonio Sanchez', 'Antonio Sánchez', 'Antônio Moreno', 'Apesar da Catedral de Lincoln', 'Apple Macintosh', 'Apresenta', 'Aqui', 'Arcebispo da Cantuária', 'Ariadne', 'Arkham Asylum', 'Armador', 'Armando Bó', 'Arnon Milchan', 'Arquiteta', 'Arquitetura', 'Arrecadou US', 'Arthur', 'As Aventuras de Pi', "As Aventuras de Pi'", 'Ashton Kutcher', 'Asilo Arkham', 'Associação Nacional de Entretenimento', "At World's End", 'Austrália', 'Autoridades', 'Avatar', 'Axiom', 'Ayan Khan', 'Aykoryd', 'Aykroyd', 'Ayush Tandon', 'Azure', 'B-B-Bertie', 'BAFTA', 'BAFTA Award', 'BBC', 'BBFC', 'BKS', 'Bach', 'Bale', 'Banqueiro Chinês', 'Barack Obama', 'Barbara Beck', 'Barcelona', 'Baseado', 'Bat-Sinal', 'Bat-roupa de Batman Begins', 'Batman', 'Batman Begins', 'Batman Begins Hans Zimmer', 'Batman da DC Comics', 'Batman de Nolan', 'Batman de Tim Burton', 'Batmoto', 'Batmóvel', 'Batpod', 'Bedlam Productions', 'Beetlejuice', 'Believe', 'Belushi', 'Ben Burtt', 'BenderSpink', 'Benjamin Kerstein', 'Berlim', 'Bertie', 'Bertolt Brecht', 'Big Ben', 'Bill Murray', 'Bill Pullman', 'Bill Smitrovich', 'Billboard', 'Birdman', 'BitTorrent', 'Black Singles', 'Blu-ray de Batman Begins', 'BnL', 'Bob Hoskins', 'Bobby Hosea', 'Boomer', 'Brandon', 'Brasil', 'Brava', 'Bravo', 'Brent Spiner', 'Brian Azzarello', 'Brian Knappenberger', 'British Board', 'British Empire Exhibition', 'Broadway', 'Browning', 'Bruce', 'Bruce Timm', 'Bruce Wayne', 'Burtt', 'Bush', 'Butler', 'Buy-n-Large', 'Buy-n-Large Corporation', 'CEO da Wayne Enterprises', 'Cadillac Miller-Meteor', 'California Filmes', 'Callum Keith Rennie', 'Cameron Bright', 'Canadá', 'Capitão Hiller', 'Capitão Jimmy Wilder', 'Capitão Steven “Steve” Hiller', 'Caribbean', 'Carlos Alberto Vaccari', 'Carlos Campanile', 'Carly Simon', 'Casa Branca', 'Casey Kasem', 'Casino Royale', 'Castelo de Balmoral', 'Castelo de Nij', 'Catedral de Ely', 'Catedral de São Basílio', 'Cathy Schultz', 'Cavaleiro das Trevas', 'Caça-Fantasmas', 'Caça-Fantasmas!', 'Celine', 'Central Park', 'Central Park West', 'Centro Experimental de Ética da Universidade Harvard', 'Certamente', 'Chaplain', 'Charles Gunning', 'Charles Roven', 'Chechen', 'Chertsey', 'Chevy Chase', 'Chicago', 'Chicago Board', 'Chin Han', 'China', 'Chotier', 'Chris Bender', 'Chris Corbould', 'Chris de Batman', 'Christian Bale', 'Christina Ricci', 'Christopher Hitchens', 'Christopher Nolan', 'Chuck', 'Churchill', 'Cidade do Limbo', 'Cillian Murphy', 'Cinema', 'CinemaScore', 'Cineplayers', 'Claire Bloom', 'Clockwork Orange', 'Cobb', 'Colecionáveis', 'Coleman Reese', 'Colin Barclay', 'Colin Firth', 'Colin McFarlane', 'Columbia Pictures', 'Com Fischer', 'Comandante da Real Ordem Vitoriana', 'Comando de Defesa Aérea', 'Comissário', 'Comissário Gillian B. Loeb', 'Comissário Gordon', 'Completando', 'Confessor', "Conor O'Sullivan", 'Constance', 'Constance Spano', 'Constantemente', 'Conway Wickliffe', 'Coringa', 'Coringa de Jack Nicholson', 'Coringa de Ledger', 'Cosmo Landesman', 'Cosmo Lang', 'Costa da Califórnia', 'Creative Commons', "Critics' Choice Awards", 'Crowley', 'Cumberland Lodge', 'Curiosamente', 'DC', 'Daley Center', 'Dan Aykroyd', 'Dana', 'Dana Barrett', 'Danielle Feinberg', 'Danna Barrett', 'Danny Cohen', 'Danny DeVito', 'Dark City', 'David', 'David Ansen', 'David Banner', 'David Levinson', 'David Magee', 'David Margulies', 'David S', 'David Seidler', 'David Spear', 'De Volta', 'Dean Devlin', 'Deathly Hallows', 'Demand Progress', 'Denise Simonetto', 'Dent', 'Dentmóveis', 'Dentre', 'Departamento de Polícia de Gotham', 'Departamento de Polícia de Gotham City', 'Derek Jacobi', 'Desde', 'Desenho', 'Deserto Setentrional Iraquiano', 'Desplat', 'Detetive', 'Deus', 'Devido', 'Devlin', 'Devon Gummersall', 'DiCaprio', 'Dick Tracy', 'Diferentemente', 'Dileep Rao', 'Dinamarca', 'Dirigido', 'Discurso do Rei', 'Disney', 'Divulgação', 'Dix', 'Dogma', 'Dogville', 'Dom', 'Dom Cobb', "Don't Think About Elephants", 'Douglas Crise', 'Douglas Hofstadter', 'Dr. Brackish Okun', 'Dr. Cosmo Lang', 'Dr. Egon Spengler', 'Dr. Isaacs', 'Dr. Jonathan Crane', 'Dr. Okun', 'Dr. Peter Venkman', 'Dr. Raymond "Ray" Stantz', 'Dream', 'Dream Is Collapsing', 'Dream Within', 'Duas-Caras', 'Dublada', 'Dublagem', 'Duque', 'Duque de Iorque', 'Duque de York', 'Duquesa de Iorque', 'Duração', 'Dwight Sings Buck', 'Dwight Yoakam', 'Dylan Dubrow', 'Dário de Castro', 'EMI', 'EPA', 'ETs', 'EUA', 'EUA David Seidler', 'EVA', 'Eames', 'Earth Class', 'Eckhart', 'Ed', 'Ed Novick', 'Eddie Murphy', 'Edifício Altino Arantes', 'Edith Piaf', 'Eduardo', 'Eduardo Borgerth', 'Eduardo Dascar', 'Eduardo VIII', 'Edward Norton', 'Efeito Borboleta', 'Efeitos', 'Egon', 'El Toro', 'Elden Henson', 'Elissa Knight', 'Elizabeth', 'Elizabeth II', 'Elland Road', 'Ellen Page', 'Elmer Bernstein', 'Ely', 'Em Hong Kong', 'Em Los Angeles', 'Emma Stone', 'Emma Thomas', 'Emmanuel Lubezki', 'Emmerich', 'Empire', 'Empire State Building', 'Enquanto Logue', 'Enquanto The Dark Knight', 'Enquanto o Rei', 'Entertainment', 'Eric Bress', 'Eric Roberts', 'Eric Stoltz', 'Ernie Anastos', 'Ernie Hudson', 'Escher', 'Escritor Yann Martel', 'Espanha', 'Estado Democrático de Direito', 'Estado de Nova York', 'Estados Unidos', 'Estes', 'Estilo', 'Estrelado', 'Estádio de Wembley', 'Ethan Hawke', 'Ethan Suplee', 'Ettore Zuim', 'Eu', 'Europa', 'Eva', 'Evan', 'Evan Treborn', 'Eve Best', 'Exatidão', 'Existem', 'Extraterrestrial Vegetation Evaluator', 'Extrator', 'Extreme Ghostbusters', 'Faixas', 'Falcone', 'Falsificador', 'Família Real', 'Fernanda Fernandes', 'Festim Diabólico de Alfred Hitchcock', 'Festival Internacional de Cinema de Toronto', 'Festival Internacional do Cinema Fantástico de Bruxelas', 'Festival de Cinema Internacional do Rio de Janeiro', 'Festival de Cinema de Telluride', 'Festival de Londres', 'Fichtner', 'Figaro', 'Film Classification', 'FilmEngine', 'Finding Nemo', 'Finlândia', 'Firth', 'Fischer', 'Flávio Dias', 'Flórida', 'Ford Econoline', 'Forma Longa', 'Forrest Tucker', 'Forthright', 'Força Aérea', 'Força Aérea dos Estados Unidos', 'Fox', 'Fox Searchlight Pictures', 'Framestore', 'Frances Bacon', 'Frank Novak', 'Franklin', 'França', 'Fred Willard', 'Freya Wilson', 'Friedrich D', 'Futuro', 'Fábio Freire', 'Gambol', 'Gareth Unwin da Bedlam Productions', 'Garfield', 'Gary A', 'Gary Oldman', 'Gary Rizzo', 'Gasparzinho', 'Gautam Belur', 'Geléia', 'Geléia! E os Verdadeiros Caça-Fantasmas', 'General Grey', 'General William Grey', 'Geo Euzébio', 'Geoffrey Rush', 'George Miller', 'George W', 'George Wendt', 'Gerald Stephens', 'Gerente do Banco Nacional de Gotham', 'Ghostbusters', 'Ghostbusters II', 'Ghostbusters!', 'Gillian B', 'Gita Patel', 'Giuseppe Andrews', 'Glasgow', 'Globo de Ouro', 'Globo de Ouro de Melhor Ator', 'Golden Globe Award', 'Golden Globe Award de Melhor Filme de Animação', 'Gordon', 'Gotham', 'Gotham Cable News', 'Gotham City', 'Gotham Knight', 'Gothan', 'Goyer', 'Gozer', 'Grace', 'Grande Depressão', 'Grande Prêmio da Grã-Bretanha', 'Gravadora', 'Green', 'Greg Rucka', 'Gremlins', 'Guerra', 'Guillermo', 'Guy Forsyth', 'Guy Hendrix Dyas', 'Guy Pearce', 'Gyllenhaal', 'Gérard Depardieu', 'Gödel', 'HAL', 'HD', 'HQ Jeph Loeb', 'Haha', 'Hal', 'Half Remembered Dream', 'Half-Blood Prince', 'Hamlet', 'Hancock', 'Hans Zimmer', 'Harold Ramis', 'Harry Connick', 'Harry Potter', 'Harvey', 'Harvey Dent', 'Harvey Dent Too', 'Harvey Fierstein', 'Hatfield House', 'Heat', 'Heath Ledger', 'Heath Ledger do Coringa', 'Hecker', 'Helena Bonham Carter', 'Hemming', 'Hiatt', 'Hiller', 'História de Aaron Swartz', 'Hitchens', 'Hititas', 'Hitler', 'Hollywood', 'Holmes', 'Holocausto', 'Homem de Marshmallow', 'Homem de Marshmallow Stay Puft', 'Homem-Aranha', 'Hong Kong', 'Hooper', 'Hora do Espanto', 'Hospital de Gotham', 'Howard', 'Huey Lewis', 'Hugh Jackman', 'Hugo Award de Melhor Apresentação Dramática', 'Hugo Vickers', 'Hélio Ribeiro', 'IGN', 'IMAX', 'IMDb', 'Iain Canning da See Saw Films', 'Iggy Pop', 'Imagine Games Network', 'Impulsionado', 'In the Company', 'Incapaz', 'Inception', 'Independence Day', 'Indiana Jones', 'Indicado', 'Indicações', 'Inesperada Virtude da Ignorância', 'Inglaterra', 'Instituto Americano de Filmes', 'Internet', 'Irene Cara', 'Irene Gorovaia', 'Ironicamente', 'Irrfan Khan', 'Isaac Chotiner', 'Isaura Gomes', 'Ivan Reitman', 'Iñárritu', 'JSTOR', 'Jack Moore', 'Jack Nicholson', 'Jacobi', 'Jake', 'Jake Kaese', 'James Bond', 'James Caan', 'James Duval', 'James Gandolfini', 'James Gordon', 'James Newton Howard', 'James Rebhorn', 'James Theatre', 'James W', 'Janet Maslin do The New York Times', 'Janine', 'Janine MelnitZ', 'Janine Melnitz', 'Jarno Trulli', 'Jasmine', 'Jasmine Dubrow', 'Jason Treborn', 'Jean-Pierre Goy', 'Jeff Garlin', 'Jeff Goldblum', 'Jeffrey Abelson', 'Jeffrey Tambor', 'Jennifer', 'Jennifer Ehle', 'Jennifer Runyon', 'Jeremy Lasky', 'Jeremy Shamos', 'Jerry Robinson', 'Jesse', 'Jesse James', 'Jim Morris', 'Jim Reardon', 'Joan Lane', 'Joe Franklin', 'John', 'John Belushi', 'John Bradley', 'John Caglione', 'John Candy', 'John Capodice', 'John Christensen', 'John Hurt', 'John Lesher', 'John Patrick Amedori', 'John Ratzenberger', 'John Storey', 'Johnny Marr', 'Johnny Rotten', 'Joker', 'Jon Matthews', 'Jonathan Nolan', 'Jordan Goldberg', 'Jorge', 'Jorge Barcellos', 'Jorge Luis Borges', 'Jorge V', 'Jorge VI', 'Joseph', 'Joseph Gordon-Levitt', 'Josh Lucas', 'Josh Olson', 'Joshua Harto', 'Joyce Cohen', 'Jr', 'Judd Hirsch', 'Julho', 'Julie Delpy', 'Julius Levinson', 'Junho', 'Katalyst', 'Kathy Najimy', 'Katie Holmes', 'Kaufman Astoria Studios', 'Kayleigh', 'Kayleigh Miller', 'Keith Szarabajka', 'Keith Williams', 'Ken Watanabe', 'Kevin Conroy', 'Kevin G', 'Kevin Thompson', 'Keysi', 'Kickstarter', 'Kiersten Warren', 'Kim Peters', 'Klavan', 'Knight', 'Kraftwerk', 'Kutcher', "L'École Internationale de Théâtre Jacques Lecoq", 'LED', 'La Môme', 'Lachy Hulme', 'Lancashire', 'Lancaster House', 'Landesman', 'Lane', 'Larry King', 'Larry Storch', 'Lars', 'Lars Von Trier', 'Lau', 'Laura', 'Le', 'Le Grisbi Productions', 'Ledger', 'Lee Smith', 'Legendary Pictures', 'Lenny', 'Lenny Kagan', 'Leonardo DiCaprio', 'Leonetti', 'Lesley', 'Lewis', 'Liev Schreiber', 'Life', 'Lincoln', 'Lincoln D', 'Lindsay Duncan', 'Lindy Hemming', 'Lionel Logue', 'Lions Gate Entertainment', 'Lisa Jakub', 'Liverpool', 'Locações', 'Locutor', 'Loeb', 'Logan Lerman', 'Logue', 'Loius', "London's West End", 'Londres', 'Lora Hirschberg', 'Lorde Halifax', 'Lorde Hoare', 'Los Angeles', 'Louis', 'Louis Black', 'Louis Mackey', 'Louis Tully', 'Lua', 'Lubezki', 'Lucas', 'Lucius Fox', 'Lukas Haas', 'M-O', 'MIT', 'MPAA', 'MTV', 'Ma Ginger', 'MacInTalk', 'Mackye Gruber', 'Macy', "Macy's Holiday Parade", 'Mae Whitman', 'Maggie Gyllenhaal', 'Maguire', 'Maiores Personagens de Cinema de Todos os Tempos', 'Major Danowitz', 'Major Mitchell', 'Mal', 'Mal Cobb', 'Manderlay', 'Manhattan', 'Manifesto Dogma', 'Manohla Dargis', 'Marcelo Forlani', 'Marcelo Torreão', 'Margaret Colin', 'Margarida', 'Marinheiro', 'Mario', 'Marion Cotillard', 'Mark Hamill', 'Maroni', 'Marr', 'Martin Filler', 'Marty Gilbert', 'Mary', 'Mary McDonnell', 'Mas Hiller', 'Massachusetts Institute', 'Matrix', 'Mattel', 'Matthew F', 'Maurice Fischer', 'Mauro Ramos', 'Max', 'McCrea', 'Melhor Ator Coadjuvante', 'Melhor Diretor', 'Melhor Edição de Som', 'Melhor Filme', 'Melhor Filme de Ficção Científica', 'Melhor Fotografia', 'Melhor Roteiro', 'Melhor Roteiro Original', 'Melhor Trilha Sonora', 'Melhores Efeitos Visuais', 'Melhores Filmes da Década', 'Melhores Filmes de Todos os Tempos', 'Melissa Gilbert', 'Melora Walters', 'Memento', 'Men', 'Menino da Internet', 'Merritt Wever', 'Mesopotâmia', 'Metacritic', 'Michael Caine', 'Michael Gambon', 'Michael Jai White', 'Michael Keaton', 'Michael Suby', 'Michael Vacca', 'Michael Wuertz', 'Microbe Obliterator', 'Miguel Casse', 'Mike Dodge', 'Mike Engel', 'Mike Monteleone', 'Mike Shiner', 'Miles', 'Ministério Público dos Estados Unidos', 'Minotauro', 'Mitologia Grega', 'Moacyr Scliar', 'Mohamed Abbas Khaleeli', 'Molly Marlene Stensgard', 'Mombasa', 'Mombaça', 'Mona Lee', 'Monica Soloway', 'Monique Curnen', 'Montanhas Rochosas', 'Monte Everest', 'Mordomo', 'Morgan Freeman', 'Moscou', 'Motion Picture', 'Motion Picture Association', 'Mozart', 'Music', 'Musical', 'Myrtle Logue', 'Márcia Gomes', 'Márcio Simões', 'Mário Tupinambá', 'México', 'NECA', 'Na Axiom', 'Naomi Watts', 'Naquela', 'Nash', 'Nathan Crowley', 'National Entertainment Collectibles Association', 'Nesse', 'Neste', 'Nestor Carbonell', 'Network', 'Nevada', 'New Drug', 'New Line Cinema', 'New Moon', 'New Regency Productions', 'Newsweek', 'Nick Davis', 'Nickolas Ashford', 'Nicole Kidman', 'Nicolás Giacobone', 'No Fim do Mundo', 'No Metacritic', 'Nolan', 'Non', 'Noruega', 'Nos Estados Unidos', 'Nostromo', 'Notavelmente', 'Nova Deli', 'Nova Iorque', 'Nova York', 'Novosibirsk', 'Odasal Stadium', 'Odsal Stadium', 'Old Souls', 'Oldman', 'Omelete', "On Her Majesty's Secret Service", 'One Simple Idea', 'Origem', 'Origens', 'Originalmente', 'Orlando Viggiani', 'Os Caça-Fantasmas', 'Os Caça-fantasmas', 'Os Felinos', 'Oscar', 'Oscar de Melhor Ator Coadjuvante', 'Oscar de Melhor Filme de Animação', 'Oscars', 'Pablo Villaça', 'Pacífico', 'Palácio de Buckingham', 'Paradox', 'Paris', 'Parker', 'Parker Jr', 'Part I', 'Participaram', 'Pat Skipper', 'Patricia Whitmore', 'Patrick Russ', 'Paul Bettany', 'Paul Dini', 'Paul Franklin', 'Paul J', 'Paul Reubens', 'Países Baixos', 'Peck', 'Pedra de Scone', 'Penrose', 'Pete Docter', 'Pete Doherty', 'Pete Postlethwaite', 'Peter', 'Peter Amundson', 'Peter Atherton', 'Peter Bernstein', 'Peter Browning', 'Peter Falk', 'Peter Finch', 'Peter Lando', 'Peter Leisure', 'Peter Parker', 'Peter Venkman', 'Pfister', 'Philip', 'Pi', 'Piaf', 'Pictures', 'Pinewood Studios', 'Piratas do Caribe', 'Pirates', 'Piscine Molitor "Pi" Patel', 'Pixar', 'Pixar Animation Studios', 'Po-Chieh Wang', 'Polícia de Nova Iorque', 'Pondicherry', 'Ponte Comodoro Schuyler F. Heim', 'Portugal', 'Precisa', 'Prefeito Anthony Garcia', 'Premiações', 'Presidente', 'Presidente George W. Bush', 'Presidente Thomas J. Whitmore', 'Primeira Dama Marilyn Whitmore', 'Primeira Guerra Mundial', 'Primeira-dama Marilyn Whitmore', 'Priscilla Amorim', 'Productions', 'Produtores', 'Produção', 'Projections', 'Promotor Público Harvey Dent', 'Prêmio Saturno', 'Prêmio Screen Actors Guild de Melhor Elenco', 'Prêmio do Público', 'Príncipe', 'Príncipe Albert', 'Príncipe John', 'Príncipe de Gales', 'Pullens', 'Pádua Moreira', 'Pôster', 'Quando Eduardo VIII', 'Quando Ernie Hudson', 'Quando o Rei', 'Queen Street Mill Textile Museum', 'RSS', 'Rachel', 'Rachel Dawes', 'Radical Notion', 'Rafe Spall', 'Rainha Elizabeth', 'Rainha Maria', 'Ralph', 'Ralph Eggleston', 'Ramis', 'Ramona Marquez', 'Rance Howard', 'Randy Oglesby', 'Randy Quaid', 'Rapadura', 'Ratatouille', 'Ravi', 'Ravi Patel', 'Ray', 'Ray Parker Jr', 'Ray Stantz', 'Raymond', 'Raymond Carver', 'Reddit', 'Redneck', 'Reese', 'Regency Enterprises', 'Reginald VelJohnson', 'Rei', 'Rei Eduardo VIII', 'Rei Jorge V', 'Rei Jorge VI', 'Rei Minos', 'Reino Unido', 'Reitman', 'Reprise Records', 'Resurgence', 'Revenge', 'Rex Black', 'Ricardo Schnetzer', 'Richard Edlund', 'Richard J', 'Richard King', 'Richard Linklater', 'Richard Parker', 'Richard Speight Jr', 'Rick Moranis', 'Riggan', 'Riggan Thomson', 'Ritchie Coster', 'Robert', 'Robert Fischer', 'Robert Loggia', 'Robert Logue', 'Roberto Cunha', 'Roberts', 'Robin Higgs', 'Robin Williams', 'Roger Ebert', 'Roger Grimsby', 'Roland Emmerich', 'Roma', 'Ron Dean', "Rory's Death Kiss", "Rory's First Kiss", 'Ross Bagley', 'Roswell', 'Roteiro', 'Rotten Tomatoes', "Rubies' Costumes", 'Rush', 'Russel Case', 'Russell Casse', 'Ryan Phillippe', 'Rússia', 'SWAT', 'SWAT de Gordon', 'Saito', 'Sal Maroni', 'Salt', 'Salvatore Maroni', 'Sam Thomson', 'San Diego Comic-Con', 'Santosh Patel', 'Sarah Widdows', 'Saturday Night Live', 'Saturn Awards', 'Schmidt', 'Screen Actors Guild Award', 'Secretário de Defesa', 'Secretário de Defesa dos Estados Unidos', 'Sedgewick Hotel', 'Seguindo', 'Segunda Guerra Mundial', 'Segundo', 'Seidler', 'Seinfeld', 'Serious Earth', 'Serious House', 'Serviço Secreto dos Estados Unidos', 'Shakespeare', 'Shelby Forthright', 'Shravanthi Sainath', 'Sid Vicious', 'Sigourney Weaver', 'Simon Egan da Bedlam Productions', 'Sindicato dos Diretores da América', 'Sindicato dos Produtores da América', 'Sindicato dos Roteiristas da América', 'Sith', 'Six Flags Great Adventure', 'Six Flags Great America', 'Skotchdopole', 'Slavitza Jovan', 'Slimer! And the Real Ghostbusters', 'Slumdog Millionaire', 'Smoking', 'Sobre', 'Sobre Aaron Swartz', 'Som', 'Sombra', 'Somente Tom', 'Sony Studios', 'Southwark', 'Space Odyssey', 'Spengler', 'Spider-Man', 'Spink', 'Sr. Stay Puft', 'St', 'Stanley Baldwin', 'Stanley Kubrick', 'Stanton', 'Stantz', 'Star Wars Episode III', 'Stargate', 'Stay-Puft', 'Steadicam', 'Steadicam Chris Haarhoff', 'Stephen Mirrione', 'Stephen Schaffer', 'Steve Brudniak', 'Steve Carell', 'Steven Soderbergh', 'Steven Spielberg', 'Stoney Jackson', 'Suméria', 'Sundance', 'Suraj Sharma', 'Surilo', 'Suécia', 'Swartz', 'Sydney', 'Sylvia Thomson', 'São Paulo', 'Sétima Sinfonia de Beethoven', 'TIME', 'TSG Entertainment', 'TV', 'Tabitha Dickinson', 'Tabu', 'Tavern', 'Technology', 'Teddy', 'Teen Choice Awards', 'Tenente Coronel Watson', 'Tenente James Gordon', 'Tenente Peterson', 'Tentei', 'Teri Garr', 'Terra de Oportunidades', 'Terror', 'Teseu', 'Teve', 'Thank You', 'The Amazing Spider-Man', 'The Animated Series', 'The Black Dahlia', 'The Butterfly Effect', 'The Dark Knight', 'The Dark Knight Rises', 'The Ghost Busters', 'The Gotham Times', "The Internet's Own Boy", 'The Killing Joke', "The King's Speech", 'The Long Halloween', 'The Matrix', 'The New York Times', 'The Other Guys', 'The Pirate Bay', 'The Real Ghostbusters', 'The Return de Sholly Fisch', 'The Secret Code', 'The Smiths', 'The Story', 'The Sunday Times', 'The Twilight Saga', 'The Unexpected Virtue', 'The Wall Street Journal', 'Thiago Siqueira', 'Thomas Edison Jr', 'Thomas J', 'Thomas Newman', 'Thompson', 'Thomson', 'Thumper', 'Tiffany', 'Time', 'Timothy "Speed" Levitch', 'Timothy Spall', 'Timothy Webber', 'Titanic', 'Tobey Maguire', 'Tom', 'Tom Berenger', 'Tom Hardy', 'Tom Hooper', 'Tommy', 'Tommy Miler', 'Tommy Miller', 'Toro', 'Torre Eiffel', 'Total Film', 'Toy Story', 'Toyota Racing', 'Trade Building', 'Train', 'Trazer o Joker', 'Trevor Jack Brooks', 'Trier', 'Trilha Sonora', 'Trono de Eduardo', 'Troy Casse', 'Tumbler', 'Turista', 'Twister', 'Two International Finance Centre', 'Tânger', 'Tóquio', 'UK Film Council', 'US Bank Tower', 'Um Tira', 'Um Tira da Pesada', 'Uma Odisséia', 'Universal', 'Universal Studios Florida', 'Universidade Columbia de Nova Iorque', 'University College London', 'Usina Termelétrica de Battersea', 'Velha Senhora', 'Venkman', 'Vibish Sivakumar', 'Vida', 'Vida de Pi', 'Vinz', 'Vinz Clortho', 'Vinz Clothor', 'WALL', 'Waking Life', 'Wallis', 'Wallis Simpson', 'Wally Pfister', 'Walt Disney Pictures', 'Walt Disney Studios Motion Pictures', 'Walter Peck', 'Want', 'Warner', 'Warner Bros', 'Washington', 'Waste Allocation Load Lifter', 'Wayne', 'Wayne Enterprises', 'We Built Our Own World', 'Weaver', 'Wembley', 'Why So Serious', 'Why So Serius', 'WhySoSerious', 'Wickliffe', 'Wikipédia', 'Wild Thyme', 'Will Smith', 'William Atherton', 'William Fichtner', 'William Lee Scott', 'Winston Churchill', 'Winston Zeddemore', 'Withmore', 'WonderCon', 'Wonderland', 'Worldview Entertainment', 'Yann Martel', 'Yorkshire', 'YouTube', 'Young Americans de David Bowie', 'Yusuf', 'Zach Galifianakis', 'Zimmer', 'Zuul', 'dr. Egon', 'dr. Peter Venkman', 'dr. Ray', 'Ézio Ramos', 'Índia', 'Óscar'],
    "time":["1984","8 de junho de 1984", "1989", "2000","2005","2006", "2014",],
    "location":['100 Anos de American Film Institute… 100 risadas', '100 Filmes mais Divertidos', "AFI's 100 Years… 100 Laughs", 'Abadia', 'Alberta', 'América', 'Austrália', 'BAFTA', 'Barcelona', 'Batman Begins', 'Belushi', 'Blu-ray', 'Brasil', 'Broadway', 'Canadá', 'Cannes', 'Castelo', 'Catedral', 'Cena', 'Central Park', 'Chicago', 'China', 'Cinema', 'Constance', 'Coringa', 'Costa', 'DVD', 'Deserto Setentrional Iraquiano', 'Dogville', 'Eckhart', 'Elland Road', 'Espaço', 'Estados Unidos', 'Europa', 'Festival', 'Festival Internacional', 'Flórida', 'França', 'Globo', 'Gotham', 'Gozer', 'Grande Prêmio', 'Guerra', 'Harvard', 'Heath Ledger', 'Hong Kong', 'IMDb', 'Internet', 'Londres', 'Los Angeles', 'MTV', 'Manhattan', 'Manifesto Dogma', 'México', 'Network', 'Nova Iorque', 'Nova York', 'Odsal Stadium', 'Orleans', 'Oscar', 'Paris', 'Pondicherry', 'Portugal', 'Queen Street Mill Textile Museum', 'Reino Unido', 'Roswell', 'Slimer', 'Sony Studios', 'Southwark', 'Suécia', 'Sydney', 'Terra', 'The Dark Knight', 'Tóquio', 'Washington', 'WonderCon', 'YouTube', 'lista das 100 melhores', 'melhor filme de comédia', 'Índia'],
    "measure":['10 milhões', '100 milhões de dólares', '103 milhões de dólares', '12 anos', '14 anos', '15 anos', '16 anos', '160 milhões de dólares', '17 anos', '19 anos', '20 anos', '21,96 milhões', '22,37 milhões', '26 anos', '28°', '291 milhões de dólares', '30 anos', '30º', '35 anos', '360º', '4,45 milhões', '44°', '50 milhões de dólares', '52 milhões de dólares', '55º', '73 anos', '76°', 'US$ 1.001.921.825', 'US$ 103', 'US$ 13.7 milhões', 'US$ 151.116.516', 'US$ 158.411.583', 'US$ 16.9 milhões', 'US$ 18 milhões', 'US$ 18.5 milhões', 'US$ 2,12 milhões', 'US$ 2.3 milhões', 'US$ 20.868.722', 'US$ 22 milhões', 'US$ 23.7 milhões', 'US$ 24.493.313', 'US$ 28.6 milhões', 'US$ 292.576.195', 'US$ 36.283', 'US$ 4.7 milhões', 'US$ 41.3 milhões', 'US$ 45 milhões', 'US$ 468.576.467', 'US$ 500 milhões', 'US$ 531.000.000', 'US$ 533.345.358', 'US$ 59.8 milhões', 'US$ 6.2 milhões', 'US$ 6.88', 'US$ 62.7 milhões', 'US$ 650.000', 'US$ 67.165.092', 'US$ 7.08', 'US$ 7.5 milhões', 'US$ 73 milhões', 'US$ 75 mil', 'US$ 823.576.195', 'US$ 94 mil', 'anos depois', 'cinco milhões de dólares', 'seis anos', 'seis mil anos']
  }        

stopwordsFile = codecs.open('descarte.txt','r', 'utf-8-sig')
stopwords = nltk.word_tokenize(stopwordsFile.read().lower())

corpusFile = codecs.open('corpus1.txt','r', 'utf-8-sig')
corpusOriginal = corpusFile.read()
corpusLower = corpusOriginal.lower()
corpus = corpusOriginal 




'''
    A partir de um texto seleciona o tipo da pergunta, 
    baseando-se na lista de pronomes pré-estabelecida.
    
    @param {String} text Texto a ser manipulado
    @return {String}
'''
def getResponseType(text):
    textLower = text.lower()
    for pronome, tipo in pronomes.items():
        if pronome.lower() in textLower:
            return tipo

'''
    A partir de um texto seleciona todas as palavras que estão dentre aspas.
    
    @param {String} text Texto a ser manipulado
    @return {String[]}
'''
def getQuotatedWords(text):
    quotes = re.findall(r'["“`]([A-ZÀ-Úa-zà-ú0-9\'\-,…. ]+)["”`]',text)
    response = []
    for quote in quotes:
        words = nltk.word_tokenize(quote.lower())
        for word in words:
            if (word not in stopwords):
                response.append(word)
        response = response + [x[0] for x in re.findall(r'([A-ZÀ-Úa-zà-ú\'\-]+(( [A-ZÀ-Úa-zà-ú\'\-]+)?( [A-ZÀ-Ú]\.)?)*)', quote)]
    return response
   
'''
    A partir de um texto seleciona todas as palavras que já foram reconhecidas
    como entidades nomeadas.
    
    @param {String} text Texto a ser manipulado
    @return {String[]}
''' 
def getRecognizedNamedEntitiesWords(text):
    text = text.lower()
    response = []
    for entitiesType, namedEntities in namedEntitiesPerType.items():
        for namedEntity in namedEntities:
            if namedEntity.lower() in text:
                response.append(namedEntity)
    return response    

'''
    A partir de um grupo de tokens(words) seleciona a palavra central.
    
    @param {String[]} words Texto tokenizado a ser manipulado
    @return {String}
'''         
def getCentralWords(words):
    for word in words:
        if (word not in stopwords) and (stemming([word])[0] in verbosStemmed):
            return word
 
'''
    A partir de um grupo de tokens(words) seleciona as palavras auxiliares.
    
    @param {String[]} words Texto tokenizado a ser manipulado
    @param {String} central Palavra central do texto
    @return {String}
'''             
def getAuxiliarWords(words, central):
    aux=[]
    for word in words:
        if (word in corpusLower) and (word not in stopwords) and (stemming([word])[0] not in verbosStemmed) and (word != central):
            aux.append(word)
    return aux
    
    
'''
    A partir de uma questão efetua o processamento para descobrir o "Tipo de resposta",
    "Palavra Central" e as "Palavras auxiliares".
    
    @param {String} words Questão a ser processada.
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''      
def processQuestion(question, verbose = False):
    quesionLower = question.lower()
    questionTokens = nltk.word_tokenize(quesionLower)
    
    questionResponseType = getResponseType(question)  
    questionCentralWord = getCentralWords(questionTokens) 
    questionQuotedlWords = getQuotatedWords(question)
    questionRecognizedNamedEntitiesWords = getRecognizedNamedEntitiesWords(question)
    questionAuxiliarWords = getAuxiliarWords(questionTokens,questionCentralWord)
    
    if(verbose):
        print("================================================================================")
        print("= Processamento da pergunta                                                    =")
        print("================================================================================")
        print("= Pergunta recebida:\t",     question)
        print("= Tipo de resposta:\t",      questionResponseType)
        print("= Palavra central:\t",       questionCentralWord)
        print("= Palavras quotadas:\t",     questionQuotedlWords)
        print("= EN reconhecidas:\t",       questionRecognizedNamedEntitiesWords)
        print("= Palavras auxiliares:\t",   questionAuxiliarWords)
        print("================================================================================\n")
    
    return {
        "question": question,
        "lower":    quesionLower,
        "type":     questionResponseType,
        "central":  questionCentralWord, 
        "quoted":   questionQuotedlWords,  
        "namedEntities":   questionRecognizedNamedEntitiesWords,  
        "auxiliars":questionAuxiliarWords}
    
    
'''
    A partir de um corpus(variavel global), "palavra central" e "palavras auxiliares" efetua o 
    processamento para descobrir o quão importante é o paragrafo.
    
    @param {dictionary} processedQuestion Informações do processamento da questão. {look: processQuestion()}
    @param {String} stopPoint Expressão regular que define onde deve quebrar o texto(default: [\n]).
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''     
def processCorpus(processedQuestion, stopPoint=r"[\n]", verbose=False):
    textImportance = {}
    texts = re.split(stopPoint,corpus)
    mostImportant = ["",0]
    
    questionType = processedQuestion['type']
    centralWord = processedQuestion['central']
    auxiliarWords = processedQuestion['auxiliars']
    quotedWords = processedQuestion['quoted']
    namedEntities = processedQuestion['namedEntities']
    
    if verbose:
        print("================================================================================")
        print("= Processamento do corpus                                                      =")
        print("================================================================================")

    for text in texts:
        importance = 0
        textLower = text.lower()
        paragraphTokens = nltk.word_tokenize(textLower)
        paragraphTokensStemmed = stemming(paragraphTokens)
        quotedWordsStemmed = stemming(quotedWords)
        centralWordStemmed = stemming([centralWord])[0]
        auxiliarWordsStemmed = stemming(auxiliarWords)
        computedWords = []
        
        for word in paragraphTokensStemmed:
            if word not in computedWords:
                if word == centralWordStemmed: 
                    importance = importance+50
                if word in quotedWordsStemmed: 
                    importance = importance+60
                if word in auxiliarWordsStemmed:
                    weight = 50 - 10*auxiliarWordsStemmed.index(word)
                    weight = weight if weight > 10  else 10
                    importance = importance+ weight
                computedWords.append(word)
                
        for namedEntity in namedEntities:
            if namedEntity in textLower:
                importance = importance+2   
        for namedEntity in namedEntitiesPerType[questionType]:
            if namedEntity.lower() in textLower:
                importance = importance+1
        
        if mostImportant[1] < importance:
            mostImportant = [text, importance]

        if verbose and importance >= 150:
            print("= Trecho:", text)
            print("= Importancia:", importance)
            print("================================================================================")

        textImportance[text]=importance
    if verbose:
        print("= Trechos selecionados:", len(texts))
        print("= Trechos mais importante:", mostImportant)
        print("================================================================================\n")
    #textSortedImportance = sorted(textImportance.items(), key=itemgetter(1), reverse=True)
    return textImportance
     
'''
    Procura todos os "nomes de entidades" dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @param {String} question Pergunta que foi feita.
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''    
def getNames(text, question, verbose = False):
    quesionLower = question.lower()
    questionTokens = nltk.word_tokenize(quesionLower)
    
    if verbose:
        print("================================================================================")
        print("= Processamento do paragrafo                                                   =")
        print("================================================================================")
    response =[]
    names = re.findall(r'(((Dr|Dra|Sr|Sra|dr|dra|sr|sra)\. )?([A-ZÀ-Ú]+[A-ZÀ-Úa-zà-ú\'\-!]+((( [A-ZÀ-Ú]+[A-ZÀ-Úa-zà-ú\'\-]*)|(( (the|de|da|do|das|dos|os|as|o|a|von) [A-ZÀ-Ú][A-ZÀ-Úa-zà-ú\'\-]+|( ["“][A-ZÀ-Ú]+[A-ZÀ-Úa-zà-ú\'\-]*)["”])))?( [A-ZÀ-Ú]\.)?)*))', text)
    for group in names:
        word = group[0]
        wordLower = word.lower()
        if (wordLower not in questionTokens) and (wordLower not in stopwords):
            response.append(word)
    if verbose:
        print("= Objetos candidatos:", response)
        print("================================================================================")
    return response
     
'''
    Procura todos os "tempos" dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @param {String} question Pergunta que foi feita.
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''       
def getTimes(text, question, verbose = False):
    quesionLower = question.lower()
    questionTokens = nltk.word_tokenize(quesionLower)
    
    if verbose:
        print("================================================================================")
        print("= Processamento do paragrafo                                                   =")
        print("================================================================================")
    response =[]
    names = re.findall(r'((\b(3[0-1]|2[0-9]|1[0-9]|0?[1-9]) de (janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro|jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez) de ([0-9]{4})\b)|\b(3[0-1]|2[0-9]|1[0-9]|0?[1-9])(( [d](e|o) )|\/)(1[0-2]|0?[1-9]{1})(\/|( [d](e|o) ))([0-9]{2,4})\b|\b(década de |anos )([2-9]0{1,3})\b|\b([0-9]{4})\b)', text) 
    for group in names:
        word = group[0]
        wordLower = word.lower()
        if (wordLower not in questionTokens) and (wordLower not in stopwords):
            response.append(word)
    if verbose:
        print("= Objetos candidatos:", response)
        print("================================================================================")
    return response
     
'''
    Procura todos os "lugares" dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @param {String} question Pergunta que foi feita.
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''    
def getLocations(text, question, verbose = False):
    quesionLower = question.lower()
    questionTokens = nltk.word_tokenize(quesionLower)

    if verbose:
        print("================================================================================")
        print("= Processamento do paragrafo                                                   =")
        print("================================================================================")
    response = []
    regex = r'((?: (em|no|na|para) )(([A-ZÀ-Ú]+[A-ZÀ-Úa-zà-ú\'\-]+(( [A-ZÀ-Ú]+[A-ZÀ-Úa-zà-ú\'\-]*)?( [A-ZÀ-Ú]\.)?)*)))'
    names = re.findall(regex, text)
    for group in names:
        word = group[0]
        wordLower = word.lower()
        if (wordLower not in questionTokens) and (wordLower not in stopwords):
            response.append(word)
    if verbose:
        print("= Objetos candidatos:", response)
        print("================================================================================")
    return response


'''
    Procura todos os "lugares" dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @param {String} question Pergunta que foi feita.
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {dictionary}
'''    
def getMeasures(text, question, verbose = False):
    quesionLower = question.lower()
    questionTokens = nltk.word_tokenize(quesionLower)

    if verbose:
        print("================================================================================")
        print("= Processamento do paragrafo                                                   =")
        print("================================================================================")
    response = []
    names = re.findall(r'((((US.\s|R.\s)&? ?)?((([0-9]+[,\.]?)+[0-9]+)|cinco|seis)( (milhões de dólares|milhões|mil|milhão|anos|prêmios))+)|(((US.\s|R.\s)&? ?)(([0-9]+[,\.]?)+[0-9]+))|([0-9]+[°º]))',
                       text)
    for group in names:
        word = group[0]
        wordLower = word.lower()
        if (wordLower not in questionTokens) and (wordLower not in stopwords):
            response.append(word)
    if verbose:
        print("= Objetos candidatos:", response)
        print("================================================================================")
    return response

    
'''
    Extração de resposta para Entidades.
    
    @param {dictionary} textImportance Importância de cada paragrafo do texto {look: processCorpus()}
    @param {dictionary} processedQuestion Informações do processamento da questão. {look: processQuestion()}
    @param {boolean} verbose Define se vai printar ou não o processamento.
    @return {String[]}
'''
def processAnswer(textImportance, processedQuestion, verbose=False):
    
    getByType = {
       "entity":    getNames,
       "time":      getTimes,
       "location":  getLocations,
       "measure":   getMeasures
       }
    
    
    #ordena para que o melhor trecho fique no inicio
    textSortedImportance = sorted(textImportance.items(), key=itemgetter(1), reverse=True)
    questionType = processedQuestion["type"]
    centralWord = processedQuestion["central"]
    auxiliarWords = processedQuestion["auxiliars"]

    lastImportance = -1
    allEntities = []
    if verbose:
        print("================================================================================")
        print("= Processamento de distancias                                                  =")
        print("================================================================================")
    
    bestAnswers = {}
    
    for tuples in textSortedImportance:
        paragraph = tuples[0]
        importance = tuples[1]
        if lastImportance == -1:
            lastImportance = importance
        if lastImportance != importance:
            break
        paragraphLower = paragraph.lower()
        entities = getByType[questionType](paragraph, processedQuestion["question"], verbose)
        allEntities = allEntities + entities
        
        paragraphTokens = nltk.word_tokenize(paragraphLower)
        centralWordInTheText = ""
        for token in paragraphTokens:
            if stemming([token])[0] == stemming([centralWord.lower()])[0]:
                centralWordInTheText = token
                break
            
        centralPosition = paragraphLower.find(centralWordInTheText)
        
        paragraphMiddle = len(paragraph)/2
        
        distancesToCentral = {}
        for entity in entities:
            distancesToCentral[entity] = paragraphMiddle
            if centralPosition > -1:
                distancesToCentral[entity] = abs(paragraph.find(entity) - centralPosition)
                
        if verbose:
            sortedDistancesToCentral = sorted(distancesToCentral.items(), key=itemgetter(1), reverse=False)
            print("================================================================================")
            print("= Possíveis respostas antes das palavras auxiliares                            =")
            print("= Todas distâncias:", sortedDistancesToCentral)
            print("================================================================================")
        
        distancesToCentralAndAuxiliar = distancesToCentral
        
        #if centralPosition == -1:
        auxiliarLength = len(auxiliarWords)*2
        for auxiliar in auxiliarWords:
            auxiliarPosition = paragraphLower.find(auxiliar.lower())
            for entity in entities: 
                distancesToCentralAndAuxiliar[entity] = distancesToCentralAndAuxiliar[entity] + (abs(paragraph.find(entity) - auxiliarPosition)/auxiliarLength)
            
        sortedDistancesToCentralAndAuxiliar = sorted(distancesToCentralAndAuxiliar.items(), key=itemgetter(1), reverse=False)
        if verbose:
            print("================================================================================")
            print("= Possíveis respostas após palavras auxiliares                                 =")
            print("= Todas distâncias:", sortedDistancesToCentralAndAuxiliar)    
            print("================================================================================")
        
        for i in range(0, BEST_ANSWER_COUNT):
            if len(sortedDistancesToCentralAndAuxiliar)>i:
                name = sortedDistancesToCentralAndAuxiliar[i][0]
                distance = sortedDistancesToCentralAndAuxiliar[i][1]
                if(name in bestAnswers):
                    newDistance = (bestAnswers[name] if bestAnswers[name] < distance else distance)
                    bestAnswers[name] = newDistance*2/3
                else:            
                    bestAnswers[name] = distance
                
    #Palavra composta            
    for name, distance in bestAnswers.items():
        if name.find(" ") > -1:
            bestAnswers[name] = bestAnswers[name]*2/3
        if name in namedEntitiesPerType[questionType]:
            bestAnswers[name] = bestAnswers[name]*2/3
            
    
    bestAnswers = sorted(bestAnswers.items(), key=itemgetter(1), reverse=False)
    
    names = [x[0] for x in bestAnswers]
    start = 0
    for name in names:
        i = start
        while i < len(names):
            if name in names[i] and i != names.index(name):
                names[names.index(name)] = names[i] 
                names.pop(i)	
            i = i + 1
        start = start + 1
        
    if verbose:
        print("================================================================================")
        print("= Todas as entidades:", allEntities)
        print("================================================================================")
        print("= Melhores respostas:", bestAnswers)
        print("================================================================================")
        print("= Respostas filtradas:", names)
        print("================================================================================")

    return bestAnswers
    
    
        
'''
    Execução do FAQ para filmes.
'''
def main():
    if(ACCURACY_TEST):
        totalMean = 0
        totalQueries = len(questions)
        print("================================================================================")
        print("= Teste de Acurácia                                                            =")
        print("================================================================================")
        for question, answer in questions.items():
            print("Pergunta:", question)
            print("Resposta correta:", answer)
            processedQuestion = processQuestion(question, False)            
            textImportance = processCorpus(processedQuestion, stopPoint="[\n]", verbose=False)    
            answers = processAnswer(textImportance, processedQuestion, False)  
            
            print("Respostas obtidas:",  [x[0] for x in answers])
            filterAnswers = [x[0].lower() for x in answers]
            if answer.lower() in filterAnswers:
                answerPosition = filterAnswers.index(answer.lower())+1
            else:
                answerPosition = 0
            print("Posição da correta(0 para não encontrads):",  answerPosition)
            print("================================================================================")
            mean = 0
            if answerPosition > 0:
                mean = 1/answerPosition
                
            totalMean = totalMean + mean   
        accuracy = totalMean/totalQueries
        print("= Perguntas testadas:", totalQueries) 
        print("= Acurácia:","{:2.5f}%".format(accuracy*100))
        print("================================================================================")
            
            
    else:
        while(True):
            print("O que deseja perguntar(exit para sair)?", end=" ")
            question = input()
            if(question == "exit" or question == ""): 
                break
            
            processedQuestion = processQuestion(question, VERBOSE)
        
            if(processedQuestion["central"] == None):
                print("Não foi possível identificar o verbo na frase...")
                continue
            
            if(processedQuestion["type"] == None):
                print("Pergunta inválida, reformule-a por favor...")
                continue
            
            #dicionario de trechos com sua importancia
            textImportance = processCorpus(processedQuestion, stopPoint="[\n]", verbose=VERBOSE)       
    
            answers = processAnswer(textImportance, processedQuestion, VERBOSE)  
            if(VERBOSE):
                print(question)
            if len(answers) > 0:
                print("Melhor resposta:", answers[0][0])
                print("Outras possíveis respostas:", [x[0] for x in answers[1:]])
            else:
                print("Nenhuma resposta encontrada...")
            print()
        
if __name__ == '__main__':
    main()
