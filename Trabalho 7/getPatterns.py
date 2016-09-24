import io
import re
from operator import itemgetter

corpus_path = './corpus2/corpus.txt'  #'corpus.test'#

instances = [["boyhood", "richard linklater"],
             ["mr. nobody", "jaco van dormael"],
             ["cidadão quatro", "laura poitras"],
             ["indie game: the movie", "lisanne pajot e james swirsky"],
             ["a viagem de chihiro", "hayao miyazaki"],
             ["batman o cavaleiro das trevas", "christopher nolan"],
             ["interestelar", "christopher nolan"],
             ["a origem", "christopher nolan"],
             ["perdido em marte", "ridley scott"],
             ["independence day", "roland emmerich"]]
relations = {'X':"Filme:", 'Y':"Diretor:"}
'''
instances = [["mr. nobody", "jared leto"]]
relations = {'X':"Filme", 'Y':"Ator"}
'''
def main():
    i = 1
    pattern_min = 2
    patterns = {}
    print("Lendo corpus:utf8 e armazenando em memória")
    with io.open(corpus_path, 'r', encoding='utf8') as file:
        corpus = file.read()
        file.close()

    print("Pré-processamento:")
    print("     -> Colocando todas as palavras do corpus em mínusculo")
    lower_corpus = corpus.lower()
    print("Processamento:")
    print("     -> Buscando padrões a partir das instâncias:")
    for instance in instances:
        print("          ", instance)
        searchpatterns(lower_corpus, instance, patterns)
    sorted_patterns = sorted(patterns.items(), key=itemgetter(1), reverse=True)
    print("     -> Padrões encontrados:")
    padroes = [pattern[0] for pattern in sorted_patterns if pattern[1] >= pattern_min]
    for padrao in padroes: print("          ", padrao)
    print("     -> Refinando: ")
    print("          Iteração (" + str(i) + ')')
    new_instances = [True for padrao in padroes if searchinstances(corpus, lower_corpus, padrao)]
    while new_instances:
        i+=1
        print("         Iteração ("+str(i)+')')
        for instance in instances:
            searchpatterns(lower_corpus, instance, patterns)
        sorted_patterns = sorted(patterns.items(), key=itemgetter(1), reverse=True)
        padroes = [pattern[0] for pattern in sorted_patterns if pattern[1] >= i*pattern_min]
        new_instances = [True for padrao in padroes if searchinstances(corpus, lower_corpus, padrao)]
    print("     Após "+str(i)+" iterações não foram encontrados novos padrões. Processo encerrado.\n\n\n Instâncias encontradas:")
    for instance in instances:
        print("          ", instance)


def clear(string): return string.replace('"', '').replace('“', '').replace('‘', '').replace('’','').replace('\'', '').replace('\n', '')


def searchpatterns(corpus, keywords, patterns):
    for i in range(0, 2):
        position1 = corpus.find(keywords[0])
        while position1 is not -1:
            position2 = corpus.find(keywords[1], position1)
            if position2 == -1: break
            pattern = corpus[position1 + len(keywords[0]):position2]
            position1 = corpus.find(keywords[0], position1 + len(keywords[i]))
            if ('.' in pattern) or ('\n' in pattern) or not (len(pattern) > 6): continue
            if i == 0: add('X' + pattern + 'Y', patterns)
            else: add('Y' + pattern + 'X', patterns)
        keywords[0:2] = reversed(keywords[0:2])


def add(pattern, patterns):
    pattern = clear(pattern)
    if not pattern in patterns:
        patterns[pattern] = 1
    else:
        patterns[pattern] += 1


def addinstances(instance):
    if not instance in instances:
        instances.append(instance)
        return True
    else:
        return False


def searchinstances(corpus, lower_corpus, pattern):
    new_instances = False
    print("             Buscando padrão:", pattern)
    r1 = relations.__getitem__(pattern[-1:])
    r2 = relations.__getitem__(pattern[:1])
    pattern = pattern[1:-1]
    position = lower_corpus.find(pattern)
    while position is not -1:
        tmp_pos = position - 1
        while not (tmp_pos >= 0 and (lower_corpus[tmp_pos] == "." or
                   lower_corpus[tmp_pos] == "," or lower_corpus[tmp_pos] == "\n")): tmp_pos -= 1
        r2_sentence = clear(corpus[tmp_pos:position])
        try: r2_sentence = re.search("(([A-Z][a-z]*(\s[A-Z][a-z]+)+)|([A-Z][a-z]+(\s[A-Z][a-z]+)*)|([A-Z][a-z]\.([A-Z][a-z]+(\s[A-Z][a-z]+)*)))$", r2_sentence).group(0)
        except:
            position = lower_corpus.find(pattern, position + len(pattern))
            continue

        tmp_pos = position + len(pattern)
        while not ((lower_corpus[tmp_pos] == ".") or lower_corpus[tmp_pos] == ","
                    or (lower_corpus[tmp_pos] == "\n")): tmp_pos += 1
        r1_sentence = clear(corpus[(position + len(pattern)):tmp_pos])
        try: r1_sentence = re.search("(([A-Z][a-z]*(\s[A-Z][a-z]+)+)|([A-Z][a-z]+(\s[A-Z][a-z]+)*)|([A-Z][a-z]\.([A-Z][a-z]+(\s[A-Z][a-z]+)*)))", r1_sentence).group(0)
        except:
            position = lower_corpus.find(pattern, position + len(pattern))
            continue

        position = lower_corpus.find(pattern, position + len(pattern))

        if addinstances([r1_sentence.lower(), r2_sentence.lower()]):
            new_instances = True
            print("                 Encontrado ->", r1, r1_sentence, r2, r2_sentence)
    return new_instances


if __name__ == '__main__':
    main()
