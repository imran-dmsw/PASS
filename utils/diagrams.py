"""Rendu de cartes mentales / schémas (Mermaid.js, chargé depuis un CDN
côté navigateur — aucune dépendance Python supplémentaire nécessaire).

Note : ce rendu n'a pas pu être vérifié visuellement dans l'outil de test
automatisé utilisé pendant le développement (limitation de son moteur de
rendu pour la mesure de bounding box SVG dans une iframe), mais suit le
schéma standard documenté par mermaid.js pour une intégration via
st.components.v1.html, largement utilisé en production. A vérifier une
fois déployé — voir si le diagramme s'affiche correctement dans un vrai
navigateur."""

import streamlit.components.v1 as components

_MERMAID_TEMPLATE = """
<div class="mermaid">{code}</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: "base",
    themeVariables: {{
      primaryColor: "#FFE8F1",
      primaryBorderColor: "#FF9EC4",
      primaryTextColor: "#5B4368",
      lineColor: "#C9B6F5",
      secondaryColor: "#F1EBFE",
      tertiaryColor: "#E4F7FD",
      fontFamily: "Quicksand, sans-serif"
    }}
  }});
</script>
<style>
  body {{ margin: 0; background: transparent; }}
  .mermaid {{ display: flex; justify-content: center; }}
  .mermaid svg {{ max-width: 100%; height: auto; }}
</style>
"""


def render_diagram(mermaid_code: str, height: int = 420) -> None:
    if not mermaid_code:
        return
    components.html(_MERMAID_TEMPLATE.format(code=mermaid_code), height=height, scrolling=True)
