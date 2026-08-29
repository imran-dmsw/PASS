"""Rendu générique d'une page UE (cours + fiche + quiz + ressources). Chaque
page pages/*.py appelle render_ue_page(ue_id) : pour ajouter une UE, il suffit
d'ajouter data/ueX.json et un fichier pages/X_emoji_Nom.py de quelques lignes
(voir pages/1_🧪_UE1_Chimie.py)."""

import streamlit as st

from utils.components import (
    render_course_block,
    render_exercises_section,
    render_fiche,
    render_mascot_bubble,
    render_resource,
)
from utils.config import STUDENT_NAME
from utils.data_loader import load_ue
from utils.diagrams import render_diagram
from utils.html import html
from utils.illustrations import render_illustration
from utils.progress import mastery_ratio, record_quiz_result, render_hearts, render_stars
from utils.quiz_engine import run_quiz
from utils.theme import TINTS, inject_kawaii_theme


def render_ue_page(ue_id: str) -> None:
    ue_data = load_ue(ue_id)

    is_official_ue = ue_data["ue_id"].startswith("ue")
    heading = f"{ue_data['ue_id'].upper()} · {ue_data['ue_name']}" if is_official_ue else ue_data["ue_name"]

    st.set_page_config(page_title=heading, page_icon=ue_data["icon"])
    inject_kawaii_theme()

    html(f"""<div style="text-align:center; padding: .5rem 0 1rem;">
<div style="font-size:2.6rem;">{ue_data['icon']}</div>
<h1 style="margin:.2rem 0 .1rem;">{heading}</h1>
</div>""")

    chapters = ue_data["chapters"]
    chapter_titles = [c["title"] for c in chapters]
    choice = st.selectbox("Choisis un chapitre :", chapter_titles)
    chapter = next(c for c in chapters if c["title"] == choice)

    ratio = mastery_ratio(ue_id, chapter["id"])
    col1, col2 = st.columns([2, 1])
    with col1:
        html(render_stars(chapter["difficulty"]))
    with col2:
        html(render_hearts(ratio))

    if chapter.get("intro"):
        render_mascot_bubble(f"Dr. Mochi te souffle, {STUDENT_NAME} 🐱", chapter["intro"], mood="happy")

    tab_cours, tab_fiche, tab_exercices, tab_quiz, tab_ressources = st.tabs(
        ["📖 Cours", "📝 Fiche", "✏️ Exercices", "🧠 Quiz", "🔗 Ressources"]
    )

    with tab_cours:
        render_illustration(chapter["id"], chapter["title"])
        for block in chapter["course"]:
            render_course_block(block)

    with tab_fiche:
        if chapter.get("diagram"):
            st.markdown("#### 🗺️ Carte mentale")
            render_diagram(chapter["diagram"])
        render_fiche(chapter.get("fiche", []))

    with tab_exercices:
        render_exercises_section(chapter.get("exercises", {}), section_key=f"ex_{ue_id}_{chapter['id']}")

    with tab_quiz:
        quiz_key = f"quiz_{ue_id}_{chapter['id']}"

        def _on_finish(score: int, total: int, ue_id=ue_id, chapter_id=chapter["id"]):
            record_quiz_result(ue_id, chapter_id, score, total)

        run_quiz(chapter["quiz"], quiz_key, on_finish=_on_finish, title=chapter["title"])

    with tab_ressources:
        resources = chapter.get("resources", [])
        if not resources:
            st.info("Pas encore de ressources ici, reviens bientôt ! 🌸")
        for resource in resources:
            render_resource(resource)
