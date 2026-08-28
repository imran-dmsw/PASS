"""Pioche des questions dans toutes les UE disponibles pour un quiz surprise."""

import random

import streamlit as st

from utils.components import render_mascot_bubble
from utils.data_loader import load_all_ues
from utils.html import html
from utils.quiz_engine import reset_quiz, run_quiz
from utils.theme import inject_kawaii_theme

st.set_page_config(page_title="Révision aléatoire · PASS Kawaii", page_icon="🎲")
inject_kawaii_theme()

html("""<div style="text-align:center; padding: .5rem 0 1rem;">
<div style="font-size:2.6rem;">🎲</div>
<h1 style="margin:.2rem 0 .1rem;">Révision aléatoire</h1>
<p style="color:var(--text-soft);">Un mix surprise de toutes les UE, pour tester ta mémoire à 360° !</p>
</div>""")
render_mascot_bubble("Dr. Mochi mélange le paquet 🃏", "On ne sait jamais ce qui va tomber, courage ! 🌸", mood="happy")

all_ues = load_all_ues()
pool = []
for ue in all_ues:
    for chapter in ue["chapters"]:
        for q in chapter["quiz"]:
            pool.append({**q, "_ue": ue["ue_id"].upper(), "_chapter": chapter["title"]})

if "random_seed" not in st.session_state:
    st.session_state["random_seed"] = 0

max_q = min(20, len(pool))
n_questions = st.slider("Nombre de questions :", min_value=5, max_value=max_q, value=min(10, max_q), step=5)

if st.button("🔀 Nouveau mélange"):
    reset_quiz(f"quiz_random_{st.session_state['random_seed']}")
    st.session_state["random_seed"] += 1
    st.rerun()

seed = st.session_state["random_seed"]
quiz_key = f"quiz_random_{seed}"

if quiz_key not in st.session_state:
    st.session_state[f"{quiz_key}_pool"] = random.sample(pool, n_questions)

selected_questions = st.session_state.get(f"{quiz_key}_pool", random.sample(pool, n_questions))

run_quiz(selected_questions, quiz_key, title="Révision mélangée")
