#!/usr/bin/env python3

import subprocess
import random
import os

verb_list = [
    'être', 'avoir', 'aller', 'aimer', 'finir',
    'dire', 'faire', 'entendre', 'savoir', 'vouloir',
    'manger', 'commencer', 'mettre', 'pouvoir', 'oublier',
    'prendre', 'sortir', 'courir', 'voir', 'venir',
    'employer', 'payer', 'acheter', 'peler']

participes = {
    'être':     'avoir',
    'avoir':    'avoir',
    'aller':    'être',
    'aimer':    'avoir',
    'finir':    'avoir',
    'dire':     'avoir',
    'faire':    'avoir',
    'entendre': 'avoir',
    'savoir':   'avoir',
    'vouloir':  'avoir',
    'manger':   'avoir',
    'commencer': 'avoir',
    'mettre':   'avoir',
    'pouvoir':  'avoir',
    'oublier':  'avoir',
    'prendre':  'avoir',
    'sortir':   'avoir',
    'courir':  'avoir',
    'voir':     'avoir',
    'venir':    'être',
    'employer': 'avoir',
    'payer':    'avoir',
    'acheter':  'avoir',
    'peler':    'avoir',
}

conjugaisons = {}
for v in verb_list:
    conjugaisons[v] = {}

    p = subprocess.Popen('french-conjugator {0}'.format(v),
                         shell=True, stdout=subprocess.PIPE)
    lists = p.stdout.read().decode()
    tenses = [e.strip() for e in lists.split('-')]
    tenses = [e for e in tenses if e != '']
    tenses = dict([tuple(e.split(':')) for e in tenses if e != ''])
    for t, c in tenses.items():
        conjugaisons[v][t.strip()] = [e for e in c.split('\n') if e != '']

map_pronom = {
    'je': 0,
    'tu': 1,
    'il': 2,
    'elle': 2,
    'on': 2,
    'nous': 3,
    'vous': 4,
    'ils': 5,
    'elles': 5,
}

map_pronom_participe = {
    'je': 0,
    'tu': 0,
    'il': 0,
    'elle': 2,
    'on': 0,
    'nous': 1,
    'vous': 1,
    'ils': 1,
    'elles': 3,
}

pronoms = ['je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles']


def pick_entry(pronom, verb, tense):
    if isinstance(pronom, str):
        _pronom = map_pronom[pronom.lower()]

    if tense == 'present':
        conj = conjugaisons[verb]["indicative present"]
        return conj[_pronom]

    if tense == 'passé composé':
        conj = conjugaisons[participes[verb]]["indicative present"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'imparfait':
        conj = conjugaisons[verb]["indicative imperfect"]
        return conj[_pronom]

    raise RuntimeError(f"temps inconnu: {tense}")


random.seed()

# print(conjugaisons)

#N = input("Combien de questions ? ")
#N = int(N)
N = 60
points = 0
past = set()

verbs = list(conjugaisons.keys())
Nverbs = len(verbs)

tenses = ['present', 'passé composé', 'imparfait']
# tenses = ['imparfait']
Ntenses = len(tenses)

if N > Nverbs*len(pronoms)*Ntenses:
    raise RuntimeError("not enough verbs")

for i in range(0, N):
    a = random.randint(0, Nverbs-1)
    b = random.randint(0, 8)
    c = random.randint(0, Ntenses-1)

    while (a, b, c) in past:
        a = random.randint(0, Nverbs-1)
        b = random.randint(0, 8)
        c = random.randint(0, Ntenses-1)

    past.add((a, b, c))
    verb = verbs[a]
    print("question " + str(i) + "/" + str(N) + " : points: " +
          str(points) + "/" + str(N))
    print("verbe: {0}, temps {1}".format(verb, tenses[c]))
    reponse = pick_entry(pronoms[b], verb, tenses[c])
    reponse = [r.strip() for r in reponse.split(',')]
    # print(reponse)
    res = input(pronoms[b] + " ")
    first_shot = 0
    while res not in reponse:
        # os.system("beep")
        print("non!")
        first_shot += 1
        if first_shot == 2:
            print('solution: ' + ' ou '.join(reponse))
            break
        res = input(pronoms[b] + " ")

    print("bravo!!!")
    if first_shot == 0:
        points += 1

print('\n'*2 + '*'*20)
print('Points: ' + str(points) + '/' + str(N))
print('Ta note: ' + str(int(points/N*12)/2))
input('*'*10 + "\n")
