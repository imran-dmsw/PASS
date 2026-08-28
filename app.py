"""Page d'accueil : accueil, mascotte, message du jour, navigation vers les UE."""

import streamlit as st

from utils.components import render_mascot_bubble, render_ue_home_card
from utils.data_loader import AVAILABLE_UES, BONUS_MODULES, load_ue
from utils.html import html
from utils.mascot import pick_greeting
from utils.progress import init_progress, total_stars_earned
from utils.theme import inject_kawaii_theme

st.set_page_config(
    page_title="PASS Révision Kawaii",
    page_icon="🌸",
    layout="centered",
)

inject_kawaii_theme()
init_progress()

html("""<div style="text-align:center; padding: 1rem 0 1.5rem;">
<span class="kawaii-badge">✨ Révisions PASS</span>
<h1 style="margin:.6rem 0 .3rem;">Bienvenue dans ton cocon de révision 🌸</h1>
<p style="color:var(--text-soft);">Des fiches de cours toutes douces et des quiz pour cartonner au concours 💮</p>
</div>""")

render_mascot_bubble("Coucou, futur·e médecin ! 🐱", pick_greeting(), mood="happy")

stars = total_stars_earned()
html(f"""<div class="kawaii-card" style="text-align:center;">
<p style="margin:0; font-size:1.4rem;">⭐ {stars} chapitre(s) maîtrisé(s) à plus de 80%</p>
<p style="margin:.2rem 0 0; color:var(--text-soft); font-size:.85rem;">Continue comme ça, chaque quiz compte !</p>
</div>""")

st.markdown("### 📚 Choisis ton UE")
st.caption("Programme officiel Université Paris Cité — d'après les polys de pré-rentrée A2SUP 🎀")

PAGE_MAP = {
    "ue1": "pages/1_🧪_UE1_Chimie.py",
    "ue2": "pages/2_🧬_UE2_Biochimie.py",
    "ue3": "pages/3_🧠_UE3_BioCell.py",
    "ue4": "pages/4_⚛️_UE4_Physique.py",
}

for ue_id in AVAILABLE_UES:
    ue_data = load_ue(ue_id)
    render_ue_home_card(ue_data)
    st.page_link(PAGE_MAP[ue_id], label=f"Réviser {ue_data['ue_id'].upper()}", icon="➡️")
    st.write("")

if BONUS_MODULES:
    st.markdown("### 💮 Module bonus")
    st.caption("Pas de poly source pour cette matière : contenu basé sur mes connaissances générales + recherches web.")
    BONUS_PAGE_MAP = {"anatomie": "pages/8_💮_Bonus_Anatomie.py"}
    for bonus_id in BONUS_MODULES:
        bonus_data = load_ue(bonus_id)
        render_ue_home_card(bonus_data)
        st.page_link(BONUS_PAGE_MAP[bonus_id], label=f"Réviser {bonus_data['ue_name']}", icon="➡️")
        st.write("")

st.markdown("### 🎲 Envie de tout mélanger ?")
html("""<div class="kawaii-card">
<div class="kawaii-icon" style="background:var(--yellow-tint); color:#B98A1C;">🎲</div>
<h4 style="margin:0 0 .3rem;">Révision aléatoire</h4>
<p style="color:var(--text-soft); font-size:.9rem; margin:0;">Un quiz surprise qui pioche dans toutes les UE disponibles.</p>
</div>""")
st.page_link("pages/9_🎲_Revision_aleatoire.py", label="Lancer une révision aléatoire", icon="🎲")
