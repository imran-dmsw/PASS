"""Petit helper pour injecter du HTML (cards, bulles mascotte, SVG inline).

On utilise st.markdown(unsafe_allow_html=True) plutôt que st.html() : ce
dernier passe le contenu dans DOMPurify côté frontend, qui supprime les
balises <svg> par défaut — or la mascotte Dr. Mochi est un SVG inline.
Les blocs HTML passés ici doivent rester flush-left et sans ligne vide
interne : Markdown peut couper un bloc HTML multi-lignes sur une ligne
vide et faire fuiter du texte brut (c'est pour ça que le CSS global, qui
a besoin de lignes vides pour rester lisible, est injecté séparément via
st.html() dans utils/theme.py)."""

import streamlit as st


def html(content: str) -> None:
    st.markdown(content, unsafe_allow_html=True)
