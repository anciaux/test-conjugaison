#!/usr/bin/env python3
################################################################
import pandas as pd
import time
import streamlit as st
import random
# import os
################################################################


class InexistingForm(RuntimeError):
    def __init__(self, pronom, verb, tense):
        super().__init__(f"Unknown form for: {pronom} {verb} {tense}")


################################################################
st.set_page_config(layout="wide")

df = pd.read_csv('german_verbs.csv')

if 'Infinitif' not in df:
    df['Infinitif'] = None

to_remove = [e for e in df.columns if e.startswith('Unnamed')]
df.drop(labels=to_remove, inplace=True, axis=1)


df.rename(columns=lambda x: x.strip(), inplace=True)
# from stqdm import stqdm
# for i in stqdm(range(df.shape[0])):
#     from googletrans import Translator
#     translator = Translator(service_urls=[
#         'translate.googleapis.com',
#     ])
#
#     e = df.iloc[i]
#     if e['Infinitif'] is not None and not isinstance(e['Infinitif'], float):
#         # st.write(
#         #    f'already done {e["Infinitiv"]}: {e["Infinitif"]} {type(e["Infinitif"])}')
#         continue
#     else:
#         st.write(f'doing {e["Infinitiv"]}')
#
#     infinitiv = e['Infinitiv']
#     infinitif = translator.translate(
#         infinitiv, src='german', dest='french')
#     df.loc[i, ('Infinitif',)] = infinitif.text
# df.to_csv('german_verbs.csv')

# st.dataframe(df)

tense_list = [
    'Infinitiv',
    'Präsens',
    # 'Präteritum',
    'Perfekt',
    'Infinitif',
    #    'Partizip',
    #    'Konjunctive',
    #    'Imperative Singular'
]


################################################################
verb_list = list(df['Infinitiv'])


def load_verbs():
    print("Loading....", end='')
    s = set([x for x in verb_list if verb_list.count(x) > 1])
    if len(s) > 0:
        raise RuntimeError(f"found duplicates: {s}")

    print("done")
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
map_tense = {
    'Präsens': 'Präsens_er,sie,es',
    'Präteritum': 'Präteritum_ich',
    'Infinitif': 'Infinitif',
    'Infinitiv': 'Infinitiv'
}


def find_direct_form(verb, tense):
    tense = map_tense[tense].strip()
    try:
        return verb[tense].iloc[0]
    except KeyError as err:
        st.error(verb)
        for e in verb.columns:
            st.error('"' + e + '"')
        raise err


map_passive_tenses = {
    'Perfekt': ("Partizip II", "Hilfsverb", "Hilfsverb*")
}


def find_passive_form(verb, tense):
    tense, aux1, aux2 = map_passive_tenses[tense]
    conj = verb[tense].iloc[0]
    aux1 = verb[aux1].iloc[0]
    aux1 = df[df['Infinitiv'] == aux1]
    aux1 = aux1['Präsens_er,sie,es'].iloc[0]
    aux2 = verb[aux2].iloc[0]
    if not isinstance(aux2, float):
        aux2 = df[df['Infinitiv'] == aux2]
        aux2 = aux2['Präsens_er,sie,es'].iloc[0]
        aux2 = '/' + aux2
    else:
        aux2 = ''
    try:
        form = aux1 + aux2 + " " + conj
    except IndexError:
        raise InexistingForm(verb, tense)
    return form


################################################################


def pick_entry(verb, tenses):
    res = []
    for tense in tenses:
        # tense = tense_list[tense]
        if tense != 'Perfekt':
            res.append(find_direct_form(verb, tense))
        else:
            res.append(find_passive_form(verb, tense))
    return res

################################################################


def find_answers(verb, tenses):
    verb = df[df['Infinitiv'] == verb]
    reponse = pick_entry(verb, tenses)
    return reponse

################################################################


def display_question(verb, tenses, given_tense, responses, key=''):
    cols = st.columns(len(tenses))

    if 'current_question' in st.session_state:
        i = st.session_state['current_question']
    else:
        i = -1

    results = []
    for col, tense, response in zip(cols, tenses, responses):
        if tense == 'Präsens':
            _tense = 'Présent (er)'
        elif tense == 'Perfekt':
            _tense = 'Parfait (er)'
        elif tense == 'Infinitiv':
            _tense = 'Infinitif (Allemand)'
        elif tense == 'Infinitif':
            _tense = 'Traduction'

        # col.success(_tense)
        # col.write(given_tense)
        # col.write(tense_list)
        if tense == tense_list[given_tense]:
            col.text_input(_tense, placeholder=response, disabled=True,
                           key=key+"reponse"+str(i)+tense)
            res = response
        else:
            res = col.text_input(_tense, placeholder='Ta réponse',
                                 key=key+"reponse"+str(i)+tense,
                                 )
        res = res.strip()
        results.append(res)

    score = 0
    for col, tense, response, result in zip(cols, tenses, responses, results):
        response = response.lower().strip()
        response = [e.strip() for e in response.split(',')]
        result = result.lower().strip()
        result = [e.strip() for e in result.split(',')]
        result = ','.join(result)
        # col.write(response)
        # col.write(result)
        if result not in response and result != ','.join(response) and result != '':
            st.session_state['first_shot'] += 1
            col.error('Non!')
        elif (result in response or result == ','.join(response)) and tense != tense_list[given_tense]:
            col.success('OK')
            if st.session_state['first_shot'] == 0:
                score += 1
    st.markdown(
        f'score: {score} {len(results)} {results} {st.session_state["first_shot"]}')
    if score >= len(results)-1:
        st.session_state['current_question'] += 1
        st.success("bravo!!!")
        st.session_state['first_shot'] = 0
        st.session_state['points'] += 1
        time.sleep(.5)
        st.experimental_rerun()
    elif st.session_state['first_shot'] >= 2:
        st.markdown('---\n\nReponse')
        cols = st.columns(len(tenses))
        for col, response in zip(cols, responses):
            col.warning(response)
        st.session_state['first_shot'] = 0
        st.session_state['current_question'] += 1
        ok = st.button("prochaine question", type='primary',
                       use_container_width=True)
        if ok:
            st.experimental_rerun()


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
        verb, given_tense = questions[i]
        reponses = find_answers(verb, tense_list)
        display_question(verb, tenses, given_tense, reponses)

    else:
        st.markdown('---')
        st.write('## Points: ' + str(points) +
                 '/' + str(N))
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
    Ntenses = len(tense_list)

    if N > Nverbs:
        st.error("Pas assez de verbes")
        raise RuntimeError("not enough verbs")

    random_verbs = [e for e in range(0, Nverbs)]
    random.shuffle(random_verbs)
    for i in range(0, N):
        # verb = random.randint(0, Nverbs-1)
        verb = random_verbs[i]
        verb = verbs[verb]
        given_tense = random.randint(0, Ntenses-1)

        while verb in questions:
            verb = random.randint(0, Nverbs-1)
            verb = verbs[verb]
            given_tense = random.randint(0, Ntenses)

        try:
            find_answers(verb, tenses)
        except InexistingForm as err:
            print(err)
            continue
        questions.add((verb, given_tense))

    return [e for e in questions]


################################################################

if 'conjugaisons' not in st.session_state:
    conjugaisons = load_verbs()
    st.session_state['conjugaisons'] = conjugaisons

conjugaisons = st.session_state['conjugaisons']

start = st.empty()
s_cont = start.container()

selected_verb_list = [
    'beginnen',
    'bieten',
    'bitten',
    'bleiben',
    'brechen',
    'einladen',
    'empfehlen',
    'essen',
    'fahren',
    'fallen',
    'fangen',
    'finden',
    'fliehen',
    'fliegen',
    'geben',
    'gehen',
    'halten',
    'hängen',
    'helfen',
    'gewinnen',
    'kommen',
    'rufen',
    'schlafen',
    'schließen',
    'schreiben',
    'schwimmen',
    'sehen',
    'sein',
    'singen',
    'sitzen',
    'sprechen',
    'stehen',
    'steigen',
    'sterben',
    'sich streiten',
    'tragen',
    'treffen',
    'treiben',
    'trinken',
    'tun'
]

# selected_verb_list = ['treiben']

with st.expander('full data'):
    _df = df[df['Infinitiv'].isin(selected_verb_list)]
    _df = _df.sort_values('Infinitiv', )
    st.dataframe(_df)

for v in selected_verb_list:
    if v not in verb_list:
        raise RuntimeError(f'we have a problem {v}')


verbs = s_cont.multiselect("Choisi les verbes à réviser",
                           options=verb_list, default=selected_verb_list)

# tenses = ['indicatif passé composé', 'indicatif plus que parfait',
#           'subjonctif passé', 'indicatif futur antérieur',
#           'impératif passé', 'conditionnel passé',
#           'indicatif passé antérieur']
selected_tense_list = tense_list

for t in selected_tense_list:
    if t not in tense_list:
        raise RuntimeError(f'we have a problem {t}')

tenses = s_cont.multiselect("Choisi les temps à réviser",
                            options=tense_list, default=selected_tense_list)

N = s_cont.number_input('Nombre de question', value=len(
    selected_verb_list))
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
