import numpy as np
from numpy import random as rn
import random

debugPrint = False

Orase = ['Craiova', 'Bucuresti', 'Iasi', 'Cluj-Napoca', 'Timisoara', 'Constanta', 'Brasov', 'Galati', 'Oradea', 'Sibiu']
nrOrase = 10
nrCromozomiPerPopulatie = 50

Distante = [
    [0, 235, 629, 394, 342, 459, 265, 463, 439, 222],
    [235, 0, 391, 454, 548, 228, 185, 248, 600, 280],
    [629, 391, 0, 391, 668, 452, 308, 221, 576, 413],
    [394, 454, 391, 0, 315, 679, 271, 519, 160, 173],
    [342, 548, 668, 315, 0, 773, 412, 675, 170, 268],
    [459, 228, 452, 679, 773, 0, 339, 231, 824, 505],
    [265, 185, 308, 271, 412, 339, 0, 268, 417, 143],
    [463, 248, 221, 519, 675, 231, 268, 0, 665, 406],
    [439, 600, 576, 160, 170, 824, 417, 665, 0, 320],
    [222, 280, 413, 173, 268, 505, 143, 406, 320, 0]
]

def printPopulatie(populatie):
    for cromozom in populatie:
        print(cromozom, end=' ')
        print('fitness = {}'.format(fitness(cromozom)))

def printTraseu(cromozom):
    for geana in range(len(cromozom) - 1):
        print('{} -> '.format(Orase[cromozom[geana]]), end='')
    print(Orase[cromozom[len(cromozom) - 1]])

def initializare(nrCromozomi):
    populatie = []
    for i in range(nrCromozomi):
        cromozom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        rn.shuffle(cromozom)
        populatie.append(cromozom)
    return populatie

def fitness(cromozom):
    distanta = 0
    for index in range(len(cromozom)-1):
        distanta = distanta + Distante[cromozom[index]][cromozom[index+1]]
        # print('distanta = {}'.format(distanta))
    return distanta

def selectiaTurneu(populatie, nrTurnee, nrCromPerTurneu):
    parintiSelectati = []
    for i in range(nrTurnee):
        cromAleatori = random.sample(range(0, nrCromozomiPerPopulatie), nrCromPerTurneu)
        parinteSelectat = populatie[cromAleatori[0]]
        for j in range(1, nrCromPerTurneu):
            if (fitness(populatie[cromAleatori[j]]) < fitness(parinteSelectat)):
                parinteSelectat = populatie[cromAleatori[j]]
        parintiSelectati.append(parinteSelectat)
    # print('parintiSelectati = ')
    # printPopulatie(parintiSelectati)
    return parintiSelectati #pentru incrucisare

def incrucisareaDeOrdineOX(parintiSelectati):
    nrParinti = len(parintiSelectati)
    copiiGenerati = []

    for index1 in range(0, nrParinti-1):
        for index2 in range(index1+1, nrParinti):
            p1 = parintiSelectati[index1]
            # print('p1 ales = {}'.format(p1))
            p2 = parintiSelectati[index2]
            # print('p2 ales = {}'.format(p2))

            PunctDeTaiere1 = random.randint(0, len(p1)-2) #se aleg in mod aleator doua puncte de taiere
            PunctDeTaiere2 = random.randint(0, len(p1)-1)
            while PunctDeTaiere2 <= PunctDeTaiere1:
                PunctDeTaiere2 = random.randint(0, len(p1)-1)
            # print("PunctDeTaiere1={}".format(PunctDeTaiere1))
            # print("PunctDeTaiere2={}".format(PunctDeTaiere2))

            c1 = [-1] * len(p1) #se initializeaza copii cu valori de '-1' (valori de completat)
            c2 = [-1] * len(p1)

            for i in range(PunctDeTaiere1, PunctDeTaiere2 + 1): #se copiaza in copii valorile din parinti intre punctele de taiere
                c1[i] = p1[i]
                c2[i] = p2[i]

            # print("c1={} dupa copierea valorilor dintre punctele de taiere".format(c1))
            # print("c2={} dupa copierea valorilor dintre punctele de taiere".format(c2))

            aux1 = []
            aux2 = []
            for i in range(PunctDeTaiere2 + 1, len(p1)): #se initializeaza si construiesc cromozomii auxiliari
                aux1.append(p1[i])
                aux2.append(p2[i])

            for i in range(PunctDeTaiere2 + 1):
                aux1.append(p1[i])
                aux2.append(p2[i])

            # print("aux1={}".format(aux1)) #cromozomii auxiliari finali
            # print("aux2={}".format(aux2))

            aux1 = [elem for elem in aux1 if elem not in c2]
            aux2 = [elem for elem in aux2 if elem not in c1]
            for i in range(PunctDeTaiere2 + 1, len(p1)): #se completeaza c1 cu valorile din aux2 si c2 cu valorile din aux1 ce nu au fost inca atribuite
                c1[i] = aux2[0]
                del aux2[0]
                c2[i] = aux1[0]
                del aux1[0]

            for i in range(PunctDeTaiere1): #se completeaza c1 cu valorile din aux2 si c2 cu valorile din aux1 ce nu au fost inca atribuite
                c1[i] = aux2[0]
                del aux2[0]
                c2[i] = aux1[0]
                del aux1[0]

            # print("c1={}".format(c1)) #copii rezultati dupa incrucisarea de ordine OX
            # print("c2={}".format(c2))

            copiiGenerati.append(c1)
            copiiGenerati.append(c2)

        # print('Copii generati:')
        # printPopulatie(copiiGenerati)
    return copiiGenerati

def mutatiaSpecificaPrinSchimbare(copii):
    nrCromozomi = len(copii)
    pm = 0.2 #probabilitate de mutatie

    for i in range (nrCromozomi):
        p = round(random.uniform(0, 1), 2)
        if p<pm:
            geana1 = random.randint(0, len(copii[0])-1)
            geana2 = random.randint(0, len(copii[0])-1)
            while (geana2 == geana1):
                geana2 = random.randint(0, len(copii[0])-1)
            # print("copilul ales pentru mutatie = {}".format(copii[i]))
            # print("pozitie geana 1 = {}".format(geana1))
            # print("pozitie geana 2 = {}".format(geana2))
            # val_interschimbare = populatie[i][poz1]
            # populatie[i][poz1] = populatie[i][poz2]
            # populatie[i][poz2] = val_interschimbare
            copii[i][geana1], copii[i][geana2] = copii[i][geana2], copii[i][geana1]
            # print("copilul dupa mutatie = {}".format(copii[i]))
    return copii

def selectieBasic(populatie): #selecteaza
    populatieNoua = [] #initializez noua popuatie
    for i in range(nrCromozomiPerPopulatie):
        # print(i)
        bestFitnessIndex = 0
        bestFitnessCromozom = fitness(populatie[0])
        # print('bestFitnessIndex = {}'.format(bestFitnessIndex))
        # print('bestFitnessCromozom = {}'.format(bestFitnessCromozom))
        for j in range (1, len(populatie)):
            if fitness(populatie[j]) < bestFitnessCromozom:
                bestFitnessIndex = j
                bestFitnessCromozom = fitness(populatie[j])
            # print('bestFitnessIndex = {}'.format(bestFitnessIndex))
            # print('bestFitnessCromozom = {}'.format(bestFitnessCromozom))
        populatieNoua.append(populatie[bestFitnessIndex])
        # print('populatieNoua = {}'.format(populatieNoua))
        populatie = np.concatenate((populatie[:bestFitnessIndex], populatie[bestFitnessIndex+1:]))
    return populatieNoua

def selectiaStochasticaUniversalaMinimizare(populatie):
    populatieNoua = []
    vectorFitness = []
    for cromozom in populatie:
        vectorFitness.append(fitness(cromozom))
    # print('Vector fitness = {}'.format(vectorFitness))
    sumaFitness = sum(vectorFitness)
    medieFitness = round(sumaFitness/len(populatie), 5)
    probabMedie = round(medieFitness/sumaFitness, 5)
    # print('sumaFitness = {}'.format(sumaFitness))
    # print('medieFitness = {}'.format(medieFitness))
    # print('probabMedie = {}'.format(probabMedie))
    segmentFitness = [0]
    for fit in vectorFitness:
        p = round(fit/sumaFitness, 5)
        # print('p inainte= {}'.format(p))
        if p < probabMedie:
            p = probabMedie + (probabMedie - p)
        else:
            p = probabMedie - (p - probabMedie)
        # print('p dupa= {}'.format(p))
        segmentFitness.append(segmentFitness[-1] + p)
    segmentFitness[len(segmentFitness)-1] = 1
    # print('Segment fitness = {}'.format(segmentFitness))
    nrAleator = rn.random() * (1/nrCromozomiPerPopulatie)
    for i in range(nrCromozomiPerPopulatie):
        # print(nrAleator)
        for s in segmentFitness:
            if s >= nrAleator:
                # print("S-a selectat cromozomul: {}".format(populatie[segmentFitness.index(s) - 1]))
                populatieNoua.append(populatie[segmentFitness.index(s) - 1])
                break
        nrAleator += 1/nrCromozomiPerPopulatie
    return populatieNoua

def main(populatie, generatie):
    generatie = generatie + 1
    if generatie == 100:
        return populatie

    print()

    print('Generaratia nr {}'.format(generatie))
    #calcularea mediei
    fitnessTotal = 0
    for cromozom in populatie:
        fitnessTotal = fitnessTotal + fitness(cromozom)
    fitnessMediu = round(fitnessTotal / len(populatie), 5)
    print('medie fitness = {}'.format(fitnessMediu))

    #calcularea dispersiei
    variantaPopulatiei = 0
    for cromozom in populatie:
        variantaPopulatiei = variantaPopulatiei + pow((fitness(cromozom) - fitnessMediu), 2)
    dispersiaPopulatiei = variantaPopulatiei / (nrCromozomiPerPopulatie - 1)
    print('dispersia populatiei = {}'.format(dispersiaPopulatiei))

    # print('populatie:')
    # printPopulatie(populatie)

    parintiSelectati = selectiaTurneu(populatie, 10, 3)
    # print('parinti selectati:')
    # printPopulatie(parintiSelectati)

    copiiDupaIncrucisare = incrucisareaDeOrdineOX(parintiSelectati)
    # print('copii dupa incrucisare:')
    # printPopulatie(copiiDupaIncrucisare)

    copiiDupaMutatie = mutatiaSpecificaPrinSchimbare(copiiDupaIncrucisare)
    # print('copii dupa mutatie:')
    # printPopulatie(copiiDupaMutatie)

    populatie = np.concatenate((populatie, copiiDupaMutatie))
    # print('populatie dupa ce adaugam copii:')
    # printPopulatie(populatie)

    # populatieNoua = selectieBasic(populatie) #selecteaza cromozomii cu fitness-ul cel mai bun
    populatieNoua = selectiaStochasticaUniversalaMinimizare(populatie)
    # populatieNoua = selectiaStochasticaUniversalaModificata(populatie)

    return main(populatieNoua, generatie)

populatie = initializare(nrCromozomiPerPopulatie)
print('populatie initiala:')
printPopulatie(populatie)

generatie = 0
populatieFinala = main(populatie, generatie)

print()
print('populatie finala:')
printPopulatie(populatieFinala)

#determinarea celui mai bun rezultat:
bestFitness = fitness(populatieFinala[0])
bestResult = populatieFinala[0]
for cromozom in populatieFinala:
    if fitness(cromozom) < bestFitness:
        bestFitness = fitness(cromozom)
        bestResult = cromozom

print()
print("Cel mai bun traseu gasit:")
printTraseu(bestResult)
print("Distanta: {}".format(bestFitness))
