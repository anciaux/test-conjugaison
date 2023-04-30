#!/usr/bin/env python3
################################################################
# import os
import random
import subprocess
import streamlit as st
import time
################################################################

tense_list = [
    'indicatif présent',
    'indicatif passé composé',
    'indicatif futur antérieur',
    'indicatif passé antérieur',
    'indicatif plus que parfait',
    'indicatif imparfait',
    'indicatif futur',
    'indicatif passé simple',
    'conditionnel présent',
    'conditionnel passé',
    'impératif présent',
    'impératif passé',
    'subjonctif présent',
    'subjonctif passé',
    'subjonctif imparfait'
]


################################################################
verb_list = [
    'être',
    'chanter',
    'avoir',
    'aller',
    'aimer',
    'finir',
    'dire',
    'faire',
    'entendre',
    'savoir',
    'vouloir',
    'manger',
    'commencer',
    'mettre',
    'pouvoir',
    'oublier',
    'prendre',
    'sortir',
    'courir',
    'voir',
    'venir',
    'employer',
    'payer',
    'acheter',
    'peler',
    'appeler',
    'boire',
    'craindre',
    'falloir',
    'fuir',
    'jeter',
    'ouvrir',
    'plaire',
    'rendre',
    'valoir',
    'vivre',
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
################################################################
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
################################################################


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

################################################################


def pick_entry(pronom, verb, tense):
    if isinstance(pronom, str):
        _pronom = map_pronom[pronom.lower()]

    if tense == 'indicatif présent':
        conj = conjugaisons[verb]["indicative present"]
        return conj[_pronom]

    if tense == 'indicatif passé composé':
        conj = conjugaisons[participes[verb]]["indicative present"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'indicatif futur antérieur':
        conj = conjugaisons[participes[verb]]["indicative future"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'indicatif plus que parfait':
        conj = conjugaisons[participes[verb]]["indicative imperfect"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'indicatif imparfait':
        conj = conjugaisons[verb]["indicative imperfect"]
        return conj[_pronom]

    if tense == 'indicatif futur':
        conj = conjugaisons[verb]["indicative future"]
        return conj[_pronom]

    if tense == 'indicatif passé simple':
        conj = conjugaisons[verb]["indicative past"]
        return conj[_pronom]

    if tense == 'conditionnel présent':
        conj = conjugaisons[verb]["conditional present"]
        return conj[_pronom]

    if tense == 'conditionnel passé':
        conj = conjugaisons[participes[verb]]["conditional present"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]
        return conj[_pronom]

    if tense == 'impératif présent':
        _pronom = map_pronom_imperatif[pronom.lower()]
        conj = conjugaisons[verb]["imperative present"]
        return conj[_pronom]

    if tense == 'impératif passé':
        _pronom = map_pronom_imperatif[pronom.lower()]
        conj = conjugaisons[participes[verb]]["imperative present"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'subjonctif présent':
        _pronom = map_pronom_imperatif[pronom.lower()]
        conj = conjugaisons[verb]["subjunctive present"]
        return conj[_pronom]

    if tense == 'subjonctif passé':
        conj = conjugaisons[participes[verb]]["subjunctive present"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    if tense == 'subjonctif imparfait':
        _pronom = map_pronom_imperatif[pronom.lower()]
        conj = conjugaisons[verb]["subjunctive imperfect"]
        return conj[_pronom]

    if tense == 'indicatif passé antérieur':
        conj = conjugaisons[participes[verb]]["indicative past"]
        conj2 = conjugaisons[verb]["participle past"]
        if len(conj2) == 1:
            return conj[_pronom] + " " + conj2[0]
        if participes[verb] == 'avoir':
            return conj[_pronom] + " " + conj2[0]
        __pronom = map_pronom_participe[pronom]
        return conj[_pronom] + " " + conj2[__pronom]

    raise RuntimeError(f"temps inconnu: {tense}")

################################################################


def find_answer(verb, pronom, tense):
    try:
        reponse = pick_entry(pronoms[pronom], verb, tenses[tense])
        reponse = [r.strip() for r in reponse.split(',')]
        return reponse
    except Exception as err:
        st.error(type(err), err)
        st.error(f"error: {verb} {pronom} {tense}")

################################################################


def display_question(pronom, verb, tense, reponse, key=''):

    col1, col2 = st.columns(2)
    col1.success(verb)
    col2.success(tenses[tense])
    if tenses[tense] in ['impératif présent', 'impératif passé']:
        p = replace_for_imperatif(pronoms[pronom])
    else:
        p = pronoms[pronom]

    st.success(p)

    e = st.empty()
    e.empty()
    i = st.session_state['current_question']
    res = e.text_input('', placeholder='Ta réponse',
                       key=key+"reponse"+str(i))

    if res != '':
        if res.lower() not in reponse:
            st.error("non!")
            st.session_state['first_shot'] += 1
            if st.session_state['first_shot'] == 2:
                st.warning('solution: ' + ' ou '.join(reponse))
                st.session_state['first_shot'] = 0
                st.session_state['current_question'] += 1
                time.sleep(2)
                st.experimental_rerun()
            return 0
        else:
            st.session_state['current_question'] += 1
            st.success("bravo!!!")
            if st.session_state['first_shot'] == 0:
                return 1
            st.session_state['first_shot'] = 0
            return 1
    return 0

################################################################


def main(N):

    if 'points' not in st.session_state:
        st.session_state['points'] = 0

    points = st.session_state['points']
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0

    i = st.session_state['current_question']
    questions = st.session_state['questions']

    progress_text = f"question {i}/{N}"
    my_bar = st.progress(0, progress_text)
    my_bar.progress(i/len(questions), text=progress_text)
    points_text = f"points: {points}/{N}"
    points_bar = st.progress(0, points_text)
    points_bar.progress(points/N, text=points_text)

    if 'first_shot' not in st.session_state:
        st.session_state['first_shot'] = 0

    if st.session_state['current_question'] < len(questions):
        verb, pronom, tense = questions[i]
        reponse = find_answer(verb, pronom, tense)

        add = display_question(pronom, verb, tense, reponse)
        if add:
            points += 1
            st.session_state['points'] = points
            time.sleep(.5)
            st.experimental_rerun()
    else:
        st.markdown('---')
        st.write('## Points: ' + str(points) + '/' + str(N))
        st.write('## Ta note: ' + str(int(points/N*12)/2))
        st.markdown('---')


################################################################


def generate_questions(verbs, tenses, N):

    random.seed()
    questions = set()
    verbs = list(conjugaisons.keys())
    Nverbs = len(verbs)
    Ntenses = len(tenses)

    if N > Nverbs*len(pronoms)*Ntenses:
        raise RuntimeError("not enough verbs")

    for i in range(0, N):
        verb = random.randint(0, Nverbs-1)
        verb = verbs[verb]
        pronom = random.randint(0, 8)
        tense = random.randint(0, Ntenses-1)

        while (verb, pronom, tense) in questions:
            verb = random.randint(0, Nverbs-1)
            verb = verbs[verb]
            pronom = random.randint(0, 8)
            tense = random.randint(0, Ntenses-1)

        reponse = find_answer(verb, pronom, tense)
        if not reponse:
            st.error("reponse inexistante")
            display_question(pronom, verb, tense, reponse, key='error')
        questions.add((verb, pronom, tense))

    return [e for e in questions]


################################################################
st.set_page_config(layout="wide")

if 'conjugaisons' not in st.session_state:
    conjugaisons = load_verbs()
    st.session_state['conjugaisons'] = conjugaisons

conjugaisons = st.session_state['conjugaisons']

start = st.empty()
s_cont = start.container()

verbs = s_cont.multiselect("Choisi les verbes à réviser",
                           options=verb_list, default=verb_list)

tenses = ['indicatif passé composé', 'indicatif plus que parfait',
          'subjonctif passé', 'indicatif futur antérieur',
          'impératif passé', 'conditionnel passé',
          'indicatif passé antérieur']

for t in tenses:
    if t not in tense_list:
        raise RuntimeError(f'we have a problem {t}')

tenses = s_cont.multiselect("Choisi les temps à réviser",
                            options=tense_list, default=tenses)

N = s_cont.number_input('Nombre de question', value=60)

button = s_cont.button('Démarer le test')
if 'started' not in st.session_state:
    st.session_state['started'] = False

if button or st.session_state['started']:
    st.session_state['started'] = True
    start.empty()
    if 'questions' not in st.session_state:
        questions = generate_questions(verbs, tenses, N)
        st.session_state['questions'] = questions
    main(N)
