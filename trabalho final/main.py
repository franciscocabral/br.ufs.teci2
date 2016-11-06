# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 19:28:43 2016

@author: Francisco Cabral
"""



import re
import nltk
import codecs
import time
import json
import random
import datetime
import calendar

current_time = lambda: int(round(time.time() * 1000))
initialTime = current_time()

corpusFile = codecs.open('corpus.txt','r', 'utf-8-sig')
corpusOriginal = corpusFile.read()
corpusFile.close()
corpusLower = corpusOriginal.lower()
corpus = corpusOriginal 

stopwordsFile = codecs.open('descarte.txt','r', 'utf-8-sig')
stopwords = nltk.word_tokenize(stopwordsFile.read().lower())
stopwordsFile.close()

verbosFile = codecs.open('verbos.txt','r', 'utf-8-sig')
verbos = nltk.word_tokenize(verbosFile.read().lower())
verbosFile.close()

stemmedVerbosFile = codecs.open('verbos.txt','r', 'utf-8-sig')
stemmedVerbos = nltk.word_tokenize(stemmedVerbosFile.read().lower())
stemmedVerbosFile.close()

'''
    Imprime uma lista em linha.
    
    @param {any[]} List Lista a ser impressa.
'''
def inlinePrint(List):
    for l in List:
        print(l, end=" ")

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


'''
    Procura todos os identificadores de pessoas dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @return {dictionary}
'''    
def getPersons(text):
    response = []
    names = re.findall(r'\b((?:com )(?:(?:a|o|as|os|um|uma) )?(?:(?:(?:minha|minhas|meu|meus) )?(?:[a-zà-úç]+)(?: (?:de|da|do|dos) ?(?:[a-zà-úç]+))*)?(?:(?: ?[A-ZÀ-Ú][a-zà-úç]+)(?: (?:de|da|do|dos)? ?(?:[A-ZÀ-Ú][a-zà-úç]+))*)?(?:(?:, | e )(?:(?:a|o|as|os|um|uma) )?(?:(?:(?:minha|minhas|meu|meus) )?(?:[a-zà-úç]+)(?: (?:de|da|do|dos) ?(?:[a-zà-úç]+))*)?(?:(?: ?[A-ZÀ-Ú][a-zà-úç]+)(?: (?:de|da|do|dos)? ?(?:[A-ZÀ-Ú][a-zà-úç]+))*)?)*|\s(?:da|do|a|o|A|O|Da|Do) (?:(?:[A-ZÀ-Ú][a-zà-úç]+)(?:(?:(?:, | e )?(?:da|do|a|o|dos|das|os|as|um|uma)? ?)(?:[A-ZÀ-Ú][a-zà-úç]+))*))',text)
    for group in names:
       tokens = nltk.word_tokenize(group)
       for token in tokens:
           if(token.lower() not in stopwords):
               response.append(token)
    return response
     
'''
    Procura todos os "lugares" dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @return {dictionary}
'''    
def getLocations(text):
    response = []
    regex = r'\b(?:(?:ao|no|na|pela|pelo|para a| para o|pra a|pra o) )(?!hora|prova|final|ano|dia|mês|semana)(([A-ZÀ-Úa-zà-ú\'\-]+)((?:(?: (?:de|da|do) )([A-ZÀ-Úa-zà-ú\'\-]+))| ([A-ZÀ-Ú][A-ZÀ-Úa-zà-ú\'\-]*))*)'
    names = re.findall(regex, text)
    for group in names:
        word = group[0]
        wordLower = word.lower()
        if (wordLower not in stopwords):
            response.append(word)
    return response

     
'''
    Procura todos as datas dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @return {dictionary}
'''       
def getDates(texto):    
    response =[]
    datesText = re.findall(r'\b((?:a partir (?:da|de|do|des[st]a|des[st]e))?(?:(?:(?:[pP]r[oó]xim[ao]|[nN]?[eE]s[st][ea]) (?:(?:semestre|Semestre|mês|Mês|meses|Meses|fim do mês|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|[jJ]unho|[jJ]ulho|[aA]gosto|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro|[jJ]an|[fF]ev|[mM]ar|[aA]br|[mM]ai|[jJ]un|[jJ]ul|[aA]go|[sS]et|[oO]ut|[nN]ov|[dD]ez)|(?:semana|Semana|[sS]egunda(?:-[fF]eira)?|[tT]erça(?:-[fF]eira)?|[qQ]uarta(?:-[fF]eira)?|[qQ]uinta(?:-[fF]eira)?|[sS]exta(?:-[fF]eira)?|[sS]ábado|[dD]omingo|[sS]eg|[tT]er|[qQ]ua|[qQ]ui|[sS]ex|[sS]ab|[dD]om|[fF]inal[- ]de[- ]semana|[fF]im[- ]de[- ]semana)|ano|feriado))|(?:(?:(?:mês|Mês|meses|Meses|fim do mês|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|[jJ]unho|[jJ]ulho|[aA]gosto|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro|[jJ]an|[fF]ev|[mM]ar|[aA]br|[mM]ai|[jJ]un|[jJ]ul|[aA]go|[sS]et|[oO]ut|[nN]ov|[dD]ez)|(?:semana|Semana|[sS]egunda(?:-[fF]eira)?|[tT]erça(?:-[fF]eira)?|[qQ]uarta(?:-[fF]eira)?|[qQ]uinta(?:-[fF]eira)?|[sS]exta(?:-[fF]eira)?|[sS]ábado|[dD]omingo|[sS]eg|[tT]er|[qQ]ua|[qQ]ui|[sS]ex|[sS]ab|[dD]om|[fF]inal[- ]de[- ]semana|[fF]im[- ]de[- ]semana)|ano) que vem)|(?:(?:[hH]oje|[aA]manh[aã] |[dD]epois de amanhã))|(?:(?:(?:mês|Mês|meses|Meses|fim do mês|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|[jJ]unho|[jJ]ulho|[aA]gosto|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro|[jJ]an|[fF]ev|[mM]ar|[aA]br|[mM]ai|[jJ]un|[jJ]ul|[aA]go|[sS]et|[oO]ut|[nN]ov|[dD]ez)|(?:semana|Semana|[sS]egunda(?:-[fF]eira)?|[tT]erça(?:-[fF]eira)?|[qQ]uarta(?:-[fF]eira)?|[qQ]uinta(?:-[fF]eira)?|[sS]exta(?:-[fF]eira)?|[sS]ábado|[dD]omingo|[sS]eg|[tT]er|[qQ]ua|[qQ]ui|[sS]ex|[sS]ab|[dD]om|[fF]inal[- ]de[- ]semana|[fF]im[- ]de[- ]semana)))|(?:(?:(?:Dia|dia) )?(?:3[012]|[0-2]?[0-9])(?! hrs| hs| ?h| horas|:)(?:\/(?:1[012]|0[1-9]))?(?: (?:de|do) (?:mês|Mês|meses|Meses|fim do mês|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|[jJ]unho|[jJ]ulho|[aA]gosto|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro|[jJ]an|[fF]ev|[mM]ar|[aA]br|[mM]ai|[jJ]un|[jJ]ul|[aA]go|[sS]et|[oO]ut|[nN]ov|[dD]ez)(?: que vem)?)?)|(?:[tT]odo (?:(?:[hH]oje|[aA]manhã|[dD]epois de amanhã)|(?:mês|Mês|meses|Meses|fim do mês|[jJ]aneiro|[fF]evereiro|[mM]arço|[aA]bril|[mM]aio|[jJ]unho|[jJ]ulho|[aA]gosto|[sS]etembro|[oO]utubro|[nN]ovembro|[dD]ezembro|[jJ]an|[fF]ev|[mM]ar|[aA]br|[mM]ai|[jJ]un|[jJ]ul|[aA]go|[sS]et|[oO]ut|[nN]ov|[dD]ez)|ano))|(?:final do (?:ano|período|semestre|mês|semana|bimestre|trimestre)))|(?:[dD]aqui a (?:[0-9]+) (?:dias|meses|anos)))\b', texto) 
    for text in datesText:
        textLower = text.lower()
        eventDate = datetime.datetime.now()
        if("daqui a" in textLower) and ('meses' in textLower ): 
            eventDate = addMonths(eventDate, int(re.findall('([0-9]+)', text)[0]))
            response.append((text,eventDate.strftime('%d/%m/%Y') ))
            continue
        elif("daqui a" in textLower) and ('dias' in textLower ):
            eventDate = eventDate + datetime.timedelta(days=int(re.findall('([0-9]+)', text)[0]))
            response.append((text,eventDate.strftime('%d/%m/%Y') ))
            continue
        if("amanha" in textLower) or ("amanhã" in textLower): 
            eventDate = eventDate + datetime.timedelta(days=1)
        if("depois de amanha" in textLower) or ("depois de amanhã" in textLower): 
            eventDate = eventDate + datetime.timedelta(days=2)
            
            
        proximo = False
        if(("proximo" in textLower) 
            or ("próximo" in textLower) 
            or ("proxima" in textLower) 
            or ("próxima" in textLower)
            or ("que vem" in textLower)):
            proximo = True
        
        if("seg" in textLower): eventDate = nextWeekday(eventDate, 0, proximo)
        elif("ter" in textLower): eventDate = nextWeekday(eventDate, 1, proximo)
        elif("qua" in textLower): eventDate = nextWeekday(eventDate, 2, proximo)
        elif("qui" in textLower): eventDate = nextWeekday(eventDate, 3, proximo)
        elif("sex" in textLower): eventDate = nextWeekday(eventDate, 4, proximo)
        elif("sab" in textLower) or ("sáb" in textLower): eventDate = nextWeekday(eventDate, 5, proximo)
        elif("dom" in textLower) or ("semana" in textLower): eventDate = nextWeekday(eventDate, 6, proximo)
        elif("final" in textLower): eventDate = nextWeekday(eventDate, 5, proximo)
        elif("ano" in textLower) and ("esse" not in textLower): eventDate = addMonths(eventDate, 12)
        elif("semestre" in textLower): eventDate = addMonths(eventDate, 6)
        elif("mês" in textLower) or ("mes" in textLower): eventDate = addMonths(eventDate, 1)

        if("jan" in textLower): eventDate = setMonth(eventDate, 1)
        elif("fev" in textLower): eventDate = setMonth(eventDate, 2)
        elif("mar" in textLower): eventDate = setMonth(eventDate, 3)
        elif("abr" in textLower): eventDate = setMonth(eventDate, 4)
        elif("mai" in textLower): eventDate = setMonth(eventDate, 5)
        elif("jun" in textLower): eventDate = setMonth(eventDate, 6)
        elif("jul" in textLower): eventDate = setMonth(eventDate, 7)
        elif("ago" in textLower): eventDate = setMonth(eventDate, 8)
        elif("set" in textLower): eventDate = setMonth(eventDate, 9)
        elif("out" in textLower): eventDate = setMonth(eventDate, 10)
        elif("nov" in textLower): eventDate = setMonth(eventDate, 11)
        elif("dez" in textLower): eventDate = setMonth(eventDate, 12)
        
        if("dia" in textLower) and ("/" not in textLower): 
            eventDate = setDay(eventDate,int(re.findall('([0-9]+)', text)[0]))
        if("/" in textLower): 
            numbers = re.findall('([0-9]+)\/([0-9]+)', text)
            day = int(numbers[0][0])
            month = int(numbers[0][1])
            year =eventDate.year if month <= eventDate.month and day < eventDate.day else eventDate.year+1
            eventDate = eventDate.replace(day=day, month=month, year = year)
        if(is_number(textLower)):
            if(int(textLower) == 00): continue
            eventDate = setDay(eventDate,int(textLower))
        response.append((text,eventDate.strftime('%d/%m/%Y') ))
    return response

'''
    Verifica se uma variável é um número ou não.
    
    @param {any} s Variável a ser tratada.
    @return {boolean}
'''  
def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True


def setMonth(date, month):
    lastMonth = date.month
    newDate = date
    if(lastMonth >= month and datetime.datetime.now().year == date.year):
        newDate = newDate.replace(year=newDate.year+1)
    return newDate.replace(month=month)
    
def setDay(date, day):
    lastDay = date.day
    newDate = date
    if(lastDay >= day and datetime.datetime.now().year == date.year):
        newDate = addMonths(date, 1)
    return newDate.replace(day=day)
    
def addMonths(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)
    
# 0 = Monday, 1=Tuesday, 2=Wednesday
def nextWeekday(date, weekday, proximo=False):
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    plus = 0
    if proximo: plus = 7
    return date + datetime.timedelta(days_ahead+plus) 

    
'''
    Procura todos os horários dentro de um texto.
    
    @param {String} text Texto a ser processado.
    @return {dictionary}
'''    
def getTimes(text):
    response = []
    regex = r'\b((?:(?:[01]?[0-9]|2[0-4])(?:(?::[0-5][0-9])? ?(?:horas|hs|hrs|h|:[0-5][0-9])))|(?:[mM]anh[aã]|[tT]arde|[nN]oite|[mM]adrugada))'
    times = re.findall(regex, text)
    for horario in times:
        timeLower = horario.lower()
        eventTime = datetime.datetime.now()
        if("h" in timeLower):
            numbers = re.findall('([0-9]+)', timeLower)
            if(len(numbers) > 0):
                horas = int(numbers[0])
                eventDate = eventTime.replace(hour=horas, minute=0)
        if(":" in timeLower):
            numbers = re.findall('([0-9]+):([0-9]+)', text)
            horas = int(numbers[0][0])
            minutos = int(numbers[0][1])
            eventDate = eventTime.replace(hour=horas, minute=minutos)
            
        if("manha" in timeLower or "manhã" in timeLower):
            horas = 9
            minutos = 0
            eventDate = eventTime.replace(hour=horas, minute=minutos)
        if("tarde" in timeLower):
            horas = 15
            minutos = 0
            eventDate = eventTime.replace(hour=horas, minute=minutos)
        if("noite" in timeLower):
            horas = 19
            minutos = 0
            eventDate = eventTime.replace(hour=horas, minute=minutos)
        if("madrugada" in timeLower):
            horas = 2
            minutos = 0
            eventDate = eventTime.replace(hour=horas, minute=minutos)
        response.append((horario,eventDate.strftime('%H:%M') ))
        
    return response

    
 
'''
    Trata o texto para descobrir entidades relacionadas.
    
    @param {String} text Texto a ser processado.
    @return {String}
'''     
def getLembreteJson(text):
    response = {
        'text': text,
        'persons': list(),
        'places': list(),
        'date': list(),
        'time': list(),
        }
    
    response['persons'] = getPersons(text)
    response['places'] = getLocations(text)
    response['date'] = getDates(text)
    response['time'] = getTimes(text)
        
    return json.dumps(response)

'''

'''
def main():
    texts = re.split("[\n]",corpus)
    random.shuffle(texts)
    for text in texts:
        
        print("Texto:", text)
        
        response = json.loads(getLembreteJson(text))
        if (len(response["persons"]) > 0):
            print("Pessoas Envolvidas:", response["persons"])
        if (len(response["places"]) > 0):
            print("Locais:", response["places"])
        if (len(response["date"]) > 0):
            print("Data:", response["date"])
        if (len(response["time"]) > 0):
            print("Horário:", response['time'])
        if input() == '0': break
        
    finalTime = current_time()
    print(finalTime-initialTime,"ms")
    



if __name__ == '__main__':
    main()
