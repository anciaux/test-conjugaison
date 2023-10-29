#!/usr/bin/env python3
################################################################
import pandas as pd
import time
import streamlit as st
import random
# import os
################################################################


st.set_page_config(layout="wide")

df = pd.read_csv('german_voc.csv', sep=':')

to_remove = [e for e in df.columns if e.startswith('Unnamed')]
df.drop(labels=to_remove, inplace=True, axis=1)


df.rename(columns=lambda x: x.strip(), inplace=True)

################################################################
voc_list = list(df['allemand'])
print(voc_list)


def find_answers(voc):
    voc = df[df['allemand'] == voc]
    reponse = voc
    return reponse.iloc[0]

################################################################


def display_question(voc, responses, key=''):
    st.write(voc)
    st.write(responses)

    st.warning("&#9888; Il faut écrire 'Ss' pour le caractère 'ß'")
    cols = st.columns(responses.shape[0])

    if 'current_question' in st.session_state:
        i = st.session_state['current_question']
    else:
        i = -1

    results = []
    headers = df.columns
    for (i, col), response in zip(enumerate(cols), responses):

        if i == 0:
            col.text_input(response, placeholder=response, disabled=True,
                           key=key+"reponse"+str(i)+response)
            res = response
        else:
            res = col.text_input(headers[i], placeholder='Ta réponse',
                                 key=key+"reponse"+str(i)+response,
                                 )
        res = res.strip()
        results.append(res)

    score = 0
    for (i, col), response, result in zip(enumerate(cols), responses, results):
        response = response.lower().strip()
        response = [e.strip() for e in response.split('/')]
        result = result.replace('Ss', 'ß').lower().strip()
        result = result.replace(',', ' ').lower().strip()
        result = [e.strip() for e in result.split(',')]
        result = ','.join(result)
        if result not in response and result != ','.join(response) and result != '':
            st.session_state['first_shot'] += 1
            col.error('Non!')
        elif (result in response or result == '/'.join(response)
              ) and i != 0:
            col.success('OK')
            score += 1
    if score >= len(results)-1:
        st.session_state['current_question'] += 1
        st.success("bravo!!!")
        st.session_state['first_shot'] = 0
        st.session_state['points'] += 1
        time.sleep(.5)
        st.experimental_rerun()
    elif st.session_state['first_shot'] >= 2:
        st.markdown('---\n\nReponse')
        cols = st.columns(responses.shape[0])
        for col, response in zip(cols, responses):
            col.warning(response)
        st.session_state['first_shot'] = 0
        st.session_state['current_question'] += 1
        ok = st.button("prochaine question", type='primary',
                       use_container_width=True)
        if ok:
            st.experimental_rerun()
    # st.markdown(
    #    f'score: {score} {len(results)} {results} {st.session_state["first_shot"]}')


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
        voc = questions[i]
        reponses = find_answers(voc)
        display_question(voc, reponses)

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


def generate_questions(vocs, N):

    random.seed()
    questions = set()
    Nvocs = len(vocs)

    if N > Nvocs:
        st.error("Pas assez de vocs")
        raise RuntimeError("not enough vocs")

    random_vocs = [e for e in range(0, Nvocs)]
    random.shuffle(random_vocs)
    for i in range(0, N):
        voc = random_vocs[i]
        voc = voc_list[voc]

        while voc in questions:
            voc = random.randint(0, Nvocs-1)
            voc = voc_list[voc]

        find_answers(voc)
        questions.add(voc)

    return [e for e in questions]


################################################################

start = st.empty()
s_cont = start.container()


N = s_cont.number_input('Nombre de question', value=len(
    voc_list))
button = s_cont.button('Démarer le test')
if 'started' not in st.session_state:
    st.session_state['started'] = False

with st.expander('full data'):
    _df = df
    _df = _df.sort_values('allemand', )
    st.dataframe(_df)

if button or st.session_state['started']:
    st.session_state['started'] = True
    start.empty()
    if 'questions' not in st.session_state:
        questions = generate_questions(voc_list, N)
        # print(questions)
        st.session_state['questions'] = questions
    main(N)
