#!/usr/bin/env python3

# import os
import random
import subprocess


verb_list = [
    'être',        # ok
    'chanter',     # ok
    'avoir',       # ok
    'aller',       # ok
    'aimer',       #
    'finir',       # ok
    'dire',        # ok
    'faire',       # ok
    'entendre',    # ok
    'savoir',      # ok
    'vouloir',     # ok
    'manger',      # ok
    'commencer',   # ok
    'mettre',      # ok
    'pouvoir',     # ok
    'oublier',     # ok
    'prendre',     # ok
    'sortir',      # ok
    'courir',      # ok
    'voir',        # ok
    'venir',       # ok
    'employer',    # ok
    'payer',       # ok
    'acheter',     # ok
    'peler',       # ok
    'appeler',     # ok
    'boire',       # ok
    'craindre',    # ok
    'falloir',     # ok
    'fuir',        # ok
    'jeter',       # ok
    'ouvrir',      # ok
    'plaire',      # ok
    'rendre',      # ok
    'valoir',      # ok
    'vivre',       # ok
    'placer',
    'avancer',
    'devoir',
    'croire',
    'comprendre',
    'reprendre',
    'apprendre',
    'répondre',
    'attendre',
    'perdre',
    'descendre',
    'tenir',
    'devenir',
    'retenir',
    'sentir',
    'partir',
    'connaître',
    'paraître',
    'reconnaître',
    'apparaître',
    'suivre',
    'mourir',
    'couvrir',
    'offrir',
    'souffrir',
    'écrire',
    'lire'
]

participes = {
    'être':     'avoir',
    'chanter':  'avoir',
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
    'sortir':   'être',
    'courir':  'avoir',
    'voir':     'avoir',
    'venir':    'être',
    'employer': 'avoir',
    'payer':    'avoir',
    'acheter':  'avoir',
    'peler':    'avoir',
    'appeler':  'avoir',
    'boire':    'avoir',
    'craindre': 'avoir',
    'falloir':  'avoir',
    'fuir':     'avoir',
    'jeter':    'avoir',
    'ouvrir':   'avoir',
    'plaire':   'avoir',
    'rendre':   'avoir',
    'valoir':   'avoir',
    'vivre':    'avoir',
    'placer':   'avoir',
    'avancer':  'avoir',
    'devoir':   'avoir',
    'croire':   'avoir',
    'comprendre':   'avoir',
    'reprendre':    'avoir',
    'apprendre':    'avoir',
    'répondre':    'avoir',
    'attendre':    'avoir',
    'perdre':    'avoir',
    'descendre':    'avoir',
    'tenir':    'avoir',
    'devenir':    'être',
    'retenir':    'avoir',
    'sentir':    'avoir',
    'partir':    'être',
    'connaître':    'avoir',
    'paraître':    'avoir',
    'reconnaître':    'avoir',
    'apparaître':    'avoir',
    'suivre':    'avoir',
    'mourir':    'être',
    'couvrir':    'avoir',
    'offrir':    'avoir',
    'souffrir':    'avoir',
    'écrire':    'avoir',
    'lire':    'avoir',

}

################################################################


def conjugate(verb):
    conjugaison = {}
    p = subprocess.Popen('french-conjugator {0}'.format(verb),
                         shell=True, stdout=subprocess.PIPE)
    lists = p.stdout.read().decode()
    tenses = [e.strip() for e in lists.split('-')]
    tenses = [e for e in tenses if e != '']
    tenses = dict([tuple(e.split(':')) for e in tenses if e != ''])
    for t, c in tenses.items():
        conjugaison[t.strip()] = [e for e in c.split('\n') if e != '']
    return conjugaison

################################################################


def load_verbs():
    conjugaisons = {}
    print("Loading....", end='')
    s = set([x for x in verb_list if verb_list.count(x) > 1])
    if len(s) > 0:
        raise RuntimeError(f"found duplicates: {s}")
    for v in verb_list:
        if v not in participes:
            raise RuntimeError(f"missing participes: {v}")
    for v in verb_list:
        conjugaisons[v] = conjugate(v)

    print("done")
    return conjugaisons
################################################################


conjugaisons = load_verbs()

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

map_pronom_imperatif = {
    'je': 0,
    'tu': 0,
    'il': 0,
    'elle': 0,
    'on': 0,
    'nous': 1,
    'vous': 2,
    'ils': 1,
    'elles': 2,
}


pronoms = ['je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles']


def replace_for_imperatif(pronom):
    pronom = pronom.lower()
    if pronom == 'je':
        return '(tu)'
    if pronom == 'tu':
        return '(tu)'
    if pronom == 'il':
        return '(tu)'
    if pronom == 'elle':
        return '(tu)'
    if pronom == 'on':
        return '(tu)'
    if pronom == 'nous':
        return '(nous)'
    if pronom == 'vous':
        return '(vous)'
    if pronom == 'ils':
        return '(nous)'
    if pronom == 'elles':
        return '(vous)'
    raise RuntimeError('pronom indéfini')


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

    if tense == 'futur antérieur':
        conj = conjugaisons[participes[verb]]["indicative future"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'plus que parfait':
        conj = conjugaisons[participes[verb]]["indicative imperfect"]
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

    if tense == 'futur':
        conj = conjugaisons[verb]["indicative future"]
        return conj[_pronom]

    if tense == 'passé simple':
        conj = conjugaisons[verb]["indicative past"]
        return conj[_pronom]

    if tense == 'conditionnel':
        conj = conjugaisons[verb]["conditional present"]
        return conj[_pronom]

    if tense == 'impératif':
        _pronom = map_pronom_imperatif[pronom.lower()]
        conj = conjugaisons[verb]["imperative present"]
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

# tenses = ['present', 'passé composé', 'imparfait',
#           'passé simple', 'futur', 'conditionnel', 'impératif',
#           'plus que parfait', 'futur antérieur']
tenses = ['imparfait', 'futur', 'conditionnel']

# tenses = ['present', 'passé composé', 'impératif']
# tenses = ['imparfait', 'passé simple', 'futur', 'conditionnel']
# tenses = ['imparfait', 'plus que parfait']
# tenses = ['imparfait', 'plus que parfait']
# tenses = ['futur antérieur']

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
    try:
        verb = verbs[a]
        reponse = pick_entry(pronoms[b], verb, tenses[c])
        reponse = [r.strip() for r in reponse.split(',')]
    except:
        print(f"error: {a} {b} {c}")
        continue

    print("question " + str(i) + "/" + str(N) + " : points: " +
          str(points) + "/" + str(N))
    print("verbe: {0}, temps => {1}".format(verb, tenses[c]))

    # print(reponse)
    if tenses[c] == 'impératif':
        p = replace_for_imperatif(pronoms[b])
        res = input(p + " ")
    else:
        res = input(pronoms[b] + " ")
    first_shot = 0
    while res not in reponse:
        # os.system("beep")
        print("non!")
        first_shot += 1
        if first_shot == 2:
            print('solution: ' + ' ou '.join(reponse))
            break
        if tenses[c] == 'impératif':
            p = replace_for_imperatif(pronoms[b])
            res = input(p + " ")
        else:
            res = input(pronoms[b] + " ")

    print("bravo!!!")
    if first_shot == 0:
        points += 1

print('\n'*2 + '*'*20)
print('Points: ' + str(points) + '/' + str(N))
print('Ta note: ' + str(int(points/N*12)/2))
input('*'*10 + "\n")
