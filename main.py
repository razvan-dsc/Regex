# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import copy

operatorPrecedence = {
    '*': 2,
    '.': 1,
    '|': 0
}

# aplic algoritmul postfixarii ce implica crearea a 2 stive
def computePostFix(string):
    polishNotation = []
    operatorStack = []

    for char in string:
        if char in operatorPrecedence.keys():
            # daca caracterul citit este un operator
            # dau pop la stiva de operatori si adaug la solutie cat timp nu intalnesc (
            # si precedenta operatorului din varful stivei este mai mare decat
            # precedenta celui citit  
            while len(operatorStack) and operatorStack[len(operatorStack) - 1] != '(' and operatorPrecedence[operatorStack[len(operatorStack) - 1]] > operatorPrecedence[char]:
                polishNotation.append(operatorStack.pop())
            operatorStack.append(char)
        elif char == '(':
            # daca intalnesc o parantez ( o adaug in striva de operatori
            operatorStack.append(char)
        elif char == ')':
            # daca intalnesc o paranteza ) atunci citesc elemente
            # atunci adaug elemente din stiva de operatori pana cand
            # intalnesc (
            while operatorStack[len(operatorStack) - 1] != '(':
                polishNotation.append(operatorStack.pop())
            # dau pop la (
            operatorStack.pop()
        else:
            polishNotation.append(char)
    # adaug elementele ramase la solutie 
    while len(operatorStack):
        polishNotation.append(operatorStack.pop())
    return polishNotation


#functie care combina 2 nfa-uri
# copiaza primul nfa intr-o variabila si apoi parcurge
#pe cel de-al 2lea adaugand starile acestuia in variabila auxiliara
def mergeDictNFA(dict11, dict22):
    aux = {}

    dict1 = copy.deepcopy(dict11)
    dict2 = copy.deepcopy(dict22)

    for keys in dict1:
        aux[keys] = dict1[keys]

    for keys in dict2:
        if keys not in aux:
            aux[keys] = dict2[keys]
        else:
            for char in dict2[keys]:
                l = dict2[keys][char]
                if char in aux[keys].keys():
                    if aux[keys][char]:
                        l.extend(aux[keys][char])
                aux[keys][char] = sorted(list(set(l)))

    return aux

def mergeDict(dict11, dict22):
    aux = {}

    dict1 = copy.deepcopy(dict11)
    dict2 = copy.deepcopy(dict22)

    for keys in dict1:
        aux[keys] = dict1[keys]

    for keys in dict2:
        if keys not in aux:
            aux[keys] = dict2[keys]
        else:
            l = aux[keys]
            l.extend(dict2[keys])
            aux[keys] = sorted(list(set(l)))

    return aux


# clasa va tine nfa-ul. are 2 variabile pentru a stii
# starea de inceput si starea de final si o variabila
# de tip dicitonar unde cheile sunt starile iar valorile
# sunt dictionare
class partialNfa:
    start = end = None
    nfa = {}

    def __init__(self, start, end, nfa):
        self.start = start
        self.end = end
        self.nfa = nfa

# functia de mai jos este apelata inainta 
# sa dau merge la cele 2 nfa-uri
# aceste 2 nfa-uri pot avea stari cu acelasi
# nume asa ca functia de mai jos schimba numele
# acestora in altele
def changeNames(nfa1, nfa2, l):
    cont = l[1]

    auxdict1 = {}
    auxdict2 = {}

    newnames1 = {}
    newnames2 = {}

    # in dictionarele new1names1 si newnames2 mapez vechile
    # nume ale starilor in nume noi
    for k in nfa1.nfa:
        newnames1[k] = cont
        cont = cont + 1
    for k in nfa2.nfa:
        newnames2[k] = cont
        cont = cont + 1

    # cu aceste 2 foruri reconstruiesc nfa-urile adaugand tranzitiile
    for states in nfa1.nfa:
        auxdict1[newnames1[states]] = {}
        for char in nfa1.nfa[states]:
            ns = []
            for nextState in nfa1.nfa[states][char]:
                ns.append(newnames1[nextState])
            auxdict1[newnames1[states]][char] = ns

    for states in nfa2.nfa:
        auxdict2[newnames2[states]] = {}
        for char in nfa2.nfa[states]:
            ns = []
            for nextState in nfa2.nfa[states][char]:
                ns.append(newnames2[nextState])
            auxdict2[newnames2[states]][char] = ns

    nfa1.start = newnames1[nfa1.start]
    nfa1.end = newnames1[nfa1.end]
    nfa2.start = newnames2[nfa2.start]
    nfa2.end = newnames2[nfa2.end]

    # la final dau merge la cele 2 dicitonare
    return mergeDict(auxdict1, auxdict2)


# am mers pe aceeasi idee ca mai sus insa aici modific doar un nfa
def changeName(nfa, cont):
    newnames = {}
    auxdict = {}
    for k in nfa.nfa:
        newnames[k] = cont
        cont = cont + 1

    for states in nfa.nfa:
        auxdict[newnames[states]] = {}
        for char in nfa.nfa[states]:
            ns = []
            for nextState in nfa.nfa[states][char]:
                ns.append(newnames[nextState])
            auxdict[newnames[states]][char] = ns
    nfa.start = newnames[nfa.start]
    nfa.end = newnames[nfa.end]

    return auxdict


def addNoNextStates(nfa):
    listStates = nfa.keys()
    listNextStates = []

    for k in nfa:
        for char in nfa[k]:
            for ns in nfa[k][char]:
                listNextStates.append(ns)

    listNextStates = list(set(listNextStates))

    for s in listNextStates:
        if s not in listStates:
            nfa[s] = {}

    return nfa


# functia de mai jos construieste uniunea a 2a nfa-uri
def computeUnion(nfa1, nfa2):
    # creez o lista cu elementa consecutive de lungime egala cu 
    # suma starilor din primul si cel de-al 2lea nfa + inca 2 stari
    # adaugate pentru a face uniunea.
    nrStates = len(list(nfa1.nfa.keys())) + len(list(nfa2.nfa.keys())) + 2
    l = list(range(nrStates))
    start = l[0]
    end = l[len(l) - 1]

    # in variabila dict se va afla nfa-ul merge-uit din cele 2 date ca parametru
    dict = changeNames(nfa1, nfa2, l)


    # adauga tranzitiile pe epsilon din prima stare catre inceputul celor 2 nfa-uri 
    dict[start] = {}
    dict[start]['eps'] = [nfa1.start]
    dict[start]['eps'].append(nfa2.start)

    # si adaug inca 2 tranzitii epsilon de la ultima stare a fiecarui nfa catre ultima stare
    dict[nfa1.end]['eps'] = [end]
    dict[nfa2.end]['eps'] = [end]

    # construiesc un nfa cu elemente sortate
    l = sorted(dict.keys())
    auxdict = {}
    for elem in l:
        auxdict[elem] = dict[elem]

    # returnez noul nfa
    return partialNfa(start, end, addNoNextStates(auxdict))

# functia de mai jos returneaza inchidea unui nfa
# merg pe aceeasi idee ca la union
def computeClosure(nfa):
    nrStates = len(list(nfa.nfa.keys())) + 2
    l = list(range(nrStates))
    start = l[0]
    end = l[len(l) - 1]

    cont = l[1]
    auxdict = changeName(nfa, cont)

    auxdict[nfa.end]['eps'] = [nfa.start]
    auxdict[nfa.end]['eps'].append(end)

    auxdict[start] = {}
    auxdict[start]['eps'] = [nfa.start]

    auxdict[start] = {}
    auxdict[start]['eps'] = [nfa.start]
    auxdict[start]['eps'].append(end)

    l = sorted(auxdict.keys())
    dict = {}
    for elem in l:
        dict[elem] = auxdict[elem]

    return partialNfa(start, end, addNoNextStates(dict))


# funtia de mai jos returneaza concatenarea a 2 nfa-uri
# aici doar schimb numele starilor si fac merge la dictionar,
# ultima stare al primului nfa coincidand cu prima stare a celui
# de-al 2lea
def computeConcatenation(nfa1, nfa2):
    nrStates = len(list(nfa1.nfa.keys())) + len(list(nfa2.nfa.keys())) - 1

    l = list(range(nrStates))
    start = l[0]
    end = l[len(l) - 1]
    auxdict1 = changeName(nfa1, 0)
    auxdict2 = changeName(nfa2, len(list(nfa1.nfa.keys())) - 1)

    dict = mergeDictNFA(auxdict1, auxdict2)

    l = sorted(dict.keys())
    auxdict = {}
    for elem in l:
        auxdict[elem] = dict[elem]

    return partialNfa(start, end, addNoNextStates(auxdict))


# functia de mai jos va parcurge forma polonez post fixata iar la fina;
# va returna nfa-ul regex-ului
# am mers pe ideea construirii unei stive
def computeNfa(postfix):
    if postfix == '':
        d = {}
        d[0] = {}
        return partialNfa(0, 0, d)

    stack = []
    for elem in postfix:
        if elem == '*':
            # in cazul in care intalnesc caracterul * atunci scot de pe stiva
            # primul element si adaug pe stiva un nou nfa ce va reprezenta inchiderea
            # nfa-ului deja scos
            nfa = stack.pop(len(stack) - 1)
            stack.append(computeClosure(nfa))
        elif elem == '.':
            # in cazul in care inalnesc caracterul . atunci scot de pe stiva 2 nfa-uri
            # si realizez concatenarea acestora pe care o adaug inapoi in stiva
            right = stack.pop(len(stack) - 1)
            left = stack.pop(len(stack) - 1)
            stack.append(computeConcatenation(left, right))

        elif elem == '|':
            # in cazul in care intalnesc caracterul | scot de pe stiva 2 nfa-uri,
            # realizez uniunea si o adaug inapoi in stiva
            right = stack.pop(len(stack) - 1)
            left = stack.pop(len(stack) - 1)
            stack.append(computeUnion(left, right))
        else:
            # daca prin parcurgerea
            # postfixarii intalnesc litere atunci construiesc un nfa cu 2 stari si cu
            # o tranzitiie pe acea litera iar nfa-ul respectiv il adaug in pe stiva
            d = {}
            d[0] = {}
            d[0][elem] = [1]
            d[1] = {}
            stack.append(partialNfa(0, 1, d))

    # la final returnez elementul care a mai ramas de pe stiva adica nfa-ul regexului
    return stack.pop(len(stack) - 1)


# adaug in regex-ul citit de la tastatura operatorul .
def addConc(input):
    res = []
    for i in range(0, len(input) - 1):
        res.append(input[i])
        if input[i].isalpha():
            if input[i + 1].isalpha() or input[i + 1] == '(':
                res.append('.')
        if input[i] == ')' and input[i + 1] == '(':
            res.append('.')
        if input[i] == '*' and input[i + 1] == '(':
            res.append('.')
        if input[i] == '*' and input[i + 1].isalpha():
            res.append('.')
        if input[i] == ')' and input[i + 1].isalpha():
            res.append('.')
    res.append(input[len(input) - 1])

    return ''.join(res)


def generateAlphabet(nfa):
    aux = []
    for k in nfa:
        for char in nfa[k]:
            if char != 'eps':
                aux.append(char)

    return list(set(aux))

def intListToStr(l):
    aux = []
    for elem in l:
        aux.append(str(elem))
    return aux

def intDictToStr(nfa):
    aux = {}
    for state in nfa.keys():
        dict = {}
        for char in nfa[state]:
            l = intListToStr(nfa[state][char])
            dict[char] = l
        aux[str(state)] = dict

    return aux

infile = sys.argv[1]
outfile1 = sys.argv[2]
outfile2 = sys.argv[3]

fin = open(infile, "r")
fout1 = open(outfile1,"w")
fout2 = open(outfile2,"w")

input = fin.readline()

regex = addConc(input)

result = computeNfa(computePostFix(regex))

#nr de stari
nrStates = len(list(result.nfa.keys()))

#lista  de stari finale
finalState_nfa = result.end

#alphabet
alphabet = generateAlphabet(result.nfa)

nfa = intDictToStr(result.nfa)



#ia o lista si o converteste la string
def toString(list):
    string = ""
    for lists in list:
        string += "".join(lists)
    return string


#facem merge la 2 dictionare
def mergeDict(dict11, dict22):
    aux = {}

    #realizam copiile lor
    dict1 = copy.deepcopy(dict11)
    dict2 = copy.deepcopy(dict22)


    #punem in aux elementele din dictionarul1
    for keys in dict1:
        aux[keys] = dict1[keys]


    for keys in dict2:
        #in cazul in care un element nu se afla in aux atunci il adaugam
        if keys not in aux:
            aux[keys] = dict2[keys]
        else:
            #iar daca se afla atunci extindem lista cu elementele celeilalte liste
            l = aux[keys]

            l.extend(dict2[keys])

            #utilizam set pentru a nu avea elemente duplicate
            aux[keys] = sorted(list(set(l)))

    return aux


def listtostring(dict1):
    for keys in dict1:
        l = dict1[keys]
        dict1[keys] = [toString(l)]
    return dict1


#functia de mai jos aplica un dfs pe fiecare stare din nfa si adauga intr-un diictionar epsilon(stare)
inchidere = ""
def compute_epsilon():
    d = {}
    global inchidere
    for i in range(0, nrStates):
        viz = [0 for j in range(0, nrStates)]
        inchidere = ""
        dfs(str(i), viz)
        d[i] = inchidere
    return d

#dfs-ul este aplicat pe dictionarul "nfa"
def dfs(stare, viz):
    viz[int(stare)] = 1
    global inchidere
    inchidere += stare

    if 'eps' not in nfa[stare]:
        return
    else:
        l = nfa[stare]['eps']
        if len(l) == 0:
            return
        else:
            for ns in l:
                if viz[int(ns)] == 0:
                    dfs(ns, viz)

#in dicitonarul epsilons se va afla inchiderea fiecarei stari
epsilons = compute_epsilon()


#functia de mai jos ia un dictionar si inlocuieste fiecare stare din acesta cu
#starea reprezentata de inchiderea fiecarei stari din dictionar
def compute_inchideri(dict1):
    aux = {}
    for keys in dict1:
        if keys != 'eps':
            l = []
            nextStates = dict1[keys][0]
            #ia fiecare stare din nextStates si adauga intr-o lista starile din epsilon(stare)
            for s in nextStates:
                l.append(epsilons[int(s)])
            #apelez toate aceste functii de mai jos pe lista l
            #pentru ca daca avem in l elementele: ['1', '12', '123']
            #sa adauga in aux lista cu elementul: '123'
            aux[keys] = [toString(sorted(list(set(toString(l)))))]
    return aux

dfa = {}
key_dictionary = {}
def computeDfa(nfa):
    #adaug prima stare din dfa obtinuta prin inchiderea stari initiale din nfa
    queue = []
    queue.append(epsilons[0])

    
    garbage = []
    while queue:
        currState = queue.pop(0)

        #in cazul in care o stare a fost verificata sa treaca la urmatoarea iteratie
        if currState in garbage:
            continue

        #fac merge pe dictionarele starilor din starea curenta
        t = nfa[currState[0]]
        for state in currState[1:]:
            t = mergeDict(t,nfa[state])
        t = listtostring(t)
        #in inchidere se va afla urmatoarele stari in care pot ajunge in dfa
        #din starea curenta
        inchidere = compute_inchideri(t)

        dfa[currState] = inchidere

        #adaug urmatoarele stari in coada
        for value in list(inchidere.values()):
            queue.append(value[0])

        garbage.append(currState)

    #mapez toate starile din dictionar cu rezultatul unui contor pe care
    #il incrementez la fiecare pas
    #astfel in dictinonarul de mai jos vor fi elemente de tipul "0123":"0"
    
    cont = 0
    dfa_keys = list(dfa.keys())
    for key in dfa_keys:
        key_dictionary[key] = str(cont)
        cont += 1

    dfa_values = list(dfa.values())

    for dictionar in dfa_values:
        for key in dictionar:
            if dictionar[key][0] not in key_dictionary:
                key_dictionary[dictionar[key][0]] = str(cont)
                cont += 1

    #starea de sink va fi ultima iteratie a lui cont
    sinkState = str(cont)

    # convertest starile de timp "012" etc. la stari de tip "0", "1", etc.
    #si adaug starile rezultate in dictionarul dfa_new
    dfa_new = {}
    for k in dfa:

        new_input = {}
        for k1 in dfa[k]:
            dfa[k][k1] = key_dictionary[dfa[k][k1][0]]

        new_input = dfa[k]
        dfa_new[key_dictionary[k]] = new_input


    #adaug sink stateul in dfa
    hasSink = False
    for state in dfa_new:

        chars = list(dfa_new[state].keys())
        for elem in alphabet:
            #in cazul in care ne lipseste o tranzitie pe un simbol atunci adaugam
            #o tranzitie in sink state cu simbolul respectiv
            if elem not in chars:
                dfa_new[state][elem] = sinkState
                hasSink = True

    #adaugam sink state-ul in dfa
    if hasSink:
        aux = {}
        for char in alphabet:
            aux[char] = sinkState
        dfa_new[sinkState] = aux

    return dfa_new

dfaResult = computeDfa(nfa)

def writeDFA(finiteAutomata):
    #adaug dfa-ul in fisier
    string = ""
    string = "{0}\n".format(str(len(finiteAutomata)))
    fout2.write(string)
    
    dfa_finalStates = []
    for state in list(dfa.keys()):
        if str(finalState_nfa) in state:
            dfa_finalStates.append(key_dictionary[state])
    
    aux = sorted(list(set(dfa_finalStates)))
    fout2.write(" ".join(aux))
    fout2.write("\n")
    
    string = ""
    for currState in finiteAutomata:
    	for char in finiteAutomata[currState]:
    		string = ""
    
    		string = "{0} {1} {2}\n".format(currState, char, finiteAutomata[currState][char])
    		fout2.write(string)

def writeNFA(finiteAutomata):
    #adaug dfa-ul in fisier
    string = ""
    string = "{0}\n".format(str(len(finiteAutomata)))
    fout1.write(string)
    fout1.write(str(finalState_nfa) + '\n')
    string = ""
    for currState in finiteAutomata:
        for char in finiteAutomata[currState]:
            string = ""
        
            string = "{0} {1}".format(currState, char, finiteAutomata[currState][char])

            for ns in finiteAutomata[currState][char]:
                string = string + ' ';
                string = string + ns;

            fout1.write(string + '\n')


writeDFA(dfaResult)
writeNFA(nfa)

