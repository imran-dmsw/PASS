"""Moteur de quiz : affichage question par question, feedback immédiat, score final."""

from __future__ import annotations

import random

import streamlit as st

from utils.components import render_mascot_bubble
from utils.mascot import pick_feedback, score_reaction


def _init_quiz_state(quiz_key: str, questions: list) -> dict:
    if quiz_key not in st.session_state:
        shuffled_questions = questions[:]
        random.shuffle(shuffled_questions)

        # Pour chaque question, on mélange l'ordre des options et on retrouve
        # le nouvel index de la bonne réponse.
        prepared = []
        for q in shuffled_questions:
            option_indices = list(range(len(q["options"])))
            random.shuffle(option_indices)
            prepared.append(
                {
                    "question": q["question"],
                    "options": [q["options"][i] for i in option_indices],
                    "correct_index": option_indices.index(q["correct_index"]),
                    "explanation": q["explanation"],
                }
            )

        st.session_state[quiz_key] = {
            "questions": prepared,
            "index": 0,
            "score": 0,
            "answered": False,
            "selected": None,
            "finished": False,
        }
    return st.session_state[quiz_key]


def reset_quiz(quiz_key: str) -> None:
    if quiz_key in st.session_state:
        del st.session_state[quiz_key]


def run_quiz(questions: list, quiz_key: str, on_finish=None, title: str | None = None) -> None:
    """Affiche un quiz interactif question par question.

    on_finish(score, total) est appelé une seule fois, quand le quiz se termine.
    """
    if not questions:
        st.info("Pas encore de questions ici, reviens bientôt ! 🌸")
        return

    state = _init_quiz_state(quiz_key, questions)
    total = len(state["questions"])

    if state["finished"]:
        ratio = state["score"] / total
        title_msg, message, mood = score_reaction(ratio)
        st.markdown(f"### 🎉 Score final : {state['score']} / {total}")
        render_mascot_bubble(title_msg, message, mood)
        if ratio >= 0.8:
            st.balloons()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Refaire ce quiz", key=f"{quiz_key}_retry"):
                reset_quiz(quiz_key)
                st.rerun()
        return

    q = state["questions"][state["index"]]
    st.progress((state["index"]) / total, text=f"Question {state['index'] + 1} / {total}")
    if title:
        st.caption(title)
    st.markdown(f"#### {q['question']}")

    selected = st.radio(
        "Choisis ta réponse :",
        options=list(range(len(q["options"]))),
        format_func=lambda i: q["options"][i],
        key=f"{quiz_key}_radio_{state['index']}",
        index=None,
        disabled=state["answered"],
    )

    if not state["answered"]:
        if st.button("✅ Valider", key=f"{quiz_key}_validate_{state['index']}", disabled=selected is None):
            state["answered"] = True
            state["selected"] = selected
            if selected == q["correct_index"]:
                state["score"] += 1
            st.rerun()
    else:
        is_correct = state["selected"] == q["correct_index"]
        for i, option in enumerate(q["options"]):
            if i == q["correct_index"]:
                st.markdown(f"✅ **{option}**")
            elif i == state["selected"]:
                st.markdown(f"❌ ~~{option}~~")
            else:
                st.markdown(f"&nbsp;&nbsp;{option}")

        fb_title, fb_message, fb_mood = pick_feedback(is_correct)
        render_mascot_bubble(
            fb_title,
            f"{fb_message}<br/><span style='font-size:.9rem;'>{q['explanation']}</span>",
            fb_mood,
            style="success" if is_correct else "oops",
        )

        button_label = "➡️ Question suivante" if state["index"] + 1 < total else "🏁 Voir mon score"
        if st.button(button_label, key=f"{quiz_key}_next_{state['index']}"):
            state["index"] += 1
            state["answered"] = False
            state["selected"] = None
            if state["index"] >= total:
                state["finished"] = True
                if on_finish:
                    on_finish(state["score"], total)
            st.rerun()
