#!/usr/bin/env python3
################################################################
# import os
import random
import subprocess
import streamlit as st
import streamlit.components.v1 as components
import time
################################################################


class InexistingForm(RuntimeError):
    def __init__(self, pronom, verb, tense):
        super().__init__(f"Unknown form for: {pronom} {verb} {tense}")

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
    'subjonctif imparfait',
    'subjonctif plus que parfait'
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
    'lire',
    'dormir',
    'conduire',
    'recevoir',
    'apercevoir',
    'apprécier',
    'crier',
    'envoyer',
    'peser',
    'élever',
    'cuire',
    'asseoir',
    'servir',
    'céder',
    'espérer',
    'rire',
    'agir',
    'essayer'
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
    'sortir':   'avoir',
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
    'dormir': 'avoir',
    'conduire': 'avoir',
    'recevoir': 'avoir',
    'apercevoir': 'avoir',
    'apprécier': 'avoir',
    'crier': 'avoir',
    'envoyer': 'avoir',
    'peser': 'avoir',
    'élever': 'avoir',
    'cuire': 'avoir',
    'asseoir': 'être',
    'servir': 'avoir',
    'céder': 'avoir',
    'espérer': 'avoir',
    'rire': 'avoir',
    'agir': 'avoir',
    'essayer': 'avoir'
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
map_direct_tenses = {
    'indicatif présent': "indicative present",
    'indicatif imparfait': "indicative imperfect",
    'indicatif futur': "indicative future",
    'indicatif passé simple': "indicative past",
    'conditionnel présent': "conditional present",
    'impératif présent': "imperative present",
    'subjonctif imparfait': "subjunctive imperfect",
    'subjonctif présent': "subjunctive present"
}


map_tense_map_pronom = {
    'indicatif présent': map_pronom,
    'indicatif imparfait': map_pronom,
    'indicatif futur': map_pronom,
    'indicatif passé simple': map_pronom,
    'indicatif passé composé': map_pronom,
    'indicatif passé antérieur': map_pronom,
    'indicatif futur antérieur': map_pronom,
    'indicatif plus que parfait': map_pronom,
    'conditionnel présent': map_pronom,
    'conditionnel passé': map_pronom,
    'subjonctif présent': map_pronom,
    'subjonctif imparfait': map_pronom,
    'subjonctif passé': map_pronom,
    'subjonctif plus que parfait': map_pronom,
    'impératif présent': map_pronom_imperatif,
    'impératif passé': map_pronom_imperatif,
}


def find_direct_form(pronom, verb, tense):
    _map_pronom = map_tense_map_pronom[tense]
    _pronom = _map_pronom[pronom.lower()]
    _tense = map_direct_tenses[tense]
    try:
        _conj = conjugaisons[verb][_tense]
    except KeyError as e:
        print(pronom, _pronom, verb, tense, _tense)
        raise e
    try:
        form = _conj[_pronom]
    except IndexError:
        raise InexistingForm(pronom, verb, tense)
    return form


map_passive_tenses = {
    'indicatif passé composé': "indicative present",
    'indicatif futur antérieur': "indicative future",
    'indicatif plus que parfait': "indicative imperfect",
    'conditionnel passé': "conditional present",
    'impératif passé': "imperative present",
    'subjonctif passé': "subjunctive present",
    'subjonctif plus que parfait': "subjunctive imperfect",
    'indicatif passé antérieur': "indicative past"
}


def find_passive_form(pronom, verb, tense):
    _tense = map_passive_tenses[tense]
    _map_pronom = map_tense_map_pronom[tense]
    _pronom = _map_pronom[pronom.lower()]
    conj = conjugaisons[participes[verb]][_tense]
    try:
        conj2 = conjugaisons[verb]["participle past"]
    except KeyError as e:
        print(_tense, _pronom, verb, conj)
        raise e
    if len(conj2) == 1:
        return conj[_pronom] + " " + conj2[0]
    if participes[verb] == 'avoir':
        return conj[_pronom] + " " + conj2[0]
    __pronom = map_pronom_participe[pronom]
    try:
        form = conj[_pronom] + " " + conj2[__pronom]
    except IndexError:
        raise InexistingForm(pronom, verb, tense)
    return form


################################################################


def pick_entry(pronom, verb, tense):
    # if isinstance(pronom, str):
    #     _pronom = map_pronom[pronom.lower()]

    if tense in map_direct_tenses:
        return find_direct_form(pronom, verb, tense)

    if tense in map_passive_tenses:
        return find_passive_form(pronom, verb, tense)

    raise RuntimeError(f"temps inconnu: {tense}")

################################################################


def find_answer(verb, pronom, tense):
    reponse = pick_entry(pronoms[pronom], verb, tenses[tense])
    reponse = [r.strip() for r in reponse.split(',')]
    return reponse

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
    if 'current_question' in st.session_state:
        i = st.session_state['current_question']
    else:
        i = -1
    res = e.text_input('', placeholder='Ta réponse',
                       key=key+"reponse"+str(i))
    res = res.strip()

    if res != '':
        if res.lower() not in reponse:
            st.error("non!")
            st.session_state['first_shot'] += 1
            if st.session_state['first_shot'] == 2:
                st.warning('solution: ' + ' ou '.join(reponse))
                st.session_state['first_shot'] = 0
                st.session_state['current_question'] += 1
                ok = st.button("prochaine question", type='primary',
                               use_container_width=True)
                if ok:
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

    st.components.v1.html(
        """
        <div>some hidden container</div>
        <script>
            var input = window.parent.document.querySelectorAll("input[type=text]");
            for (var i = 0; i < input.length; ++i) {{
                input[i].focus();
            }}
    </script>
    """,
        height=0,
    )

################################################################


def generate_questions(verbs, tenses, N):

    random.seed()
    questions = set()
    Nverbs = len(verbs)
    Ntenses = len(tenses)

    if N > Nverbs*len(pronoms)*Ntenses:
        st.error("Pas assez de verbes")
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

        try:
            find_answer(verb, pronom, tense)
        except InexistingForm as err:
            print(err)
            continue
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

selected_verb_list = [
    'servir',
    'céder',
    'espérer',
    'rire',
    'craindre',
    'finir',
    'agir',
    'valoir',
    'payer',
    'essayer',
    'plaire'
]

ok = True
for v in selected_verb_list:
    if v not in verb_list:
        st.error(f'we have a problem {v}')
        ok = False

if not ok:
    import sys
    sys.exit(-1)

verbs = s_cont.multiselect("Choisi les verbes à réviser",
                           options=verb_list, default=selected_verb_list)

# tenses = ['indicatif passé composé', 'indicatif plus que parfait',
#           'subjonctif passé', 'indicatif futur antérieur',
#           'impératif passé', 'conditionnel passé',
#           'indicatif passé antérieur']
selected_tense_list = [
    'impératif présent',
    'impératif passé',
    'indicatif présent',
    'indicatif passé composé',
    'indicatif futur',
    'indicatif futur antérieur',
    'indicatif imparfait',
    'indicatif plus que parfait',
    'conditionnel présent',
    'conditionnel passé',
    'subjonctif présent',
    'subjonctif passé',
    'subjonctif imparfait',
    'subjonctif plus que parfait',
    'indicatif passé antérieur',
    'indicatif passé simple',
]

for t in selected_tense_list:
    if t not in tense_list:
        raise RuntimeError(f'we have a problem {t}')

tenses = s_cont.multiselect("Choisi les temps à réviser",
                            options=tense_list, default=selected_tense_list)

N = s_cont.number_input('Nombre de question', value=120)
button = s_cont.button('Démarer le test')
if 'started' not in st.session_state:
    st.session_state['started'] = False

if button or st.session_state['started']:
    st.session_state['started'] = True
    start.empty()
    if 'questions' not in st.session_state:
        questions = generate_questions(verbs, tenses, N)
        # print(questions)
        st.session_state['questions'] = questions
    main(N)
