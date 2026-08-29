"""Petite bibliothèque d'illustrations SVG kawaii, choisies automatiquement
selon le sujet du chapitre (mots-clés dans le titre/id). Purement décoratif,
aucune dépendance externe, aucun réseau — tout est dessiné à la main en SVG
inline dans la palette du thème."""

from __future__ import annotations

from utils.html import html

_ATOM = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<circle cx="80" cy="80" r="14" fill="#FF9EC4"/>
<ellipse cx="80" cy="80" rx="65" ry="26" fill="none" stroke="#C9B6F5" stroke-width="3"/>
<ellipse cx="80" cy="80" rx="65" ry="26" fill="none" stroke="#7FD0EC" stroke-width="3" transform="rotate(60 80 80)"/>
<ellipse cx="80" cy="80" rx="65" ry="26" fill="none" stroke="#FFD873" stroke-width="3" transform="rotate(120 80 80)"/>
<circle cx="145" cy="80" r="6" fill="#C9B6F5"/>
<circle cx="47.5" cy="35.5" r="6" fill="#7FD0EC"/>
<circle cx="47.5" cy="124.5" r="6" fill="#FFD873"/>
</svg>"""

_DNA = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<path d="M50 10 C90 35 30 55 70 80 C90 92 90 92 70 105 C30 130 90 150 50 150" fill="none" stroke="#FF9EC4" stroke-width="5" stroke-linecap="round"/>
<path d="M110 10 C70 35 130 55 90 80 C70 92 70 92 90 105 C130 130 70 150 110 150" fill="none" stroke="#7FD0EC" stroke-width="5" stroke-linecap="round"/>
<line x1="62" y1="25" x2="98" y2="25" stroke="#FFD873" stroke-width="4"/>
<line x1="55" y1="47" x2="107" y2="47" stroke="#C9B6F5" stroke-width="4"/>
<line x1="80" y1="80" x2="80" y2="80" stroke="#FFD873" stroke-width="4"/>
<line x1="55" y1="113" x2="107" y2="113" stroke="#FFD873" stroke-width="4"/>
<line x1="62" y1="135" x2="98" y2="135" stroke="#C9B6F5" stroke-width="4"/>
</svg>"""

_CELL = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="80" cy="80" rx="70" ry="60" fill="#E4F7FD" stroke="#7FD0EC" stroke-width="3"/>
<ellipse cx="70" cy="70" rx="22" ry="18" fill="#F1EBFE" stroke="#C9B6F5" stroke-width="3"/>
<circle cx="70" cy="70" r="6" fill="#8862C7"/>
<ellipse cx="120" cy="60" rx="12" ry="7" fill="#FFE8F1" stroke="#FF9EC4" stroke-width="2"/>
<ellipse cx="115" cy="105" rx="10" ry="6" fill="#FFE8F1" stroke="#FF9EC4" stroke-width="2"/>
<ellipse cx="45" cy="110" rx="11" ry="7" fill="#FFF6DC" stroke="#FFD873" stroke-width="2"/>
<circle cx="35" cy="55" r="5" fill="#8FE3C7"/>
<circle cx="95" cy="115" r="4" fill="#8FE3C7"/>
</svg>"""

_MOLECULE = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<line x1="80" y1="80" x2="40" y2="45" stroke="#5B4368" stroke-width="3"/>
<line x1="80" y1="80" x2="120" y2="45" stroke="#5B4368" stroke-width="3"/>
<line x1="80" y1="80" x2="80" y2="128" stroke="#5B4368" stroke-width="3"/>
<line x1="80" y1="80" x2="130" y2="105" stroke="#5B4368" stroke-width="3"/>
<circle cx="80" cy="80" r="16" fill="#7FD0EC"/>
<circle cx="40" cy="45" r="12" fill="#FF9EC4"/>
<circle cx="120" cy="45" r="12" fill="#FF9EC4"/>
<circle cx="80" cy="128" r="12" fill="#FFD873"/>
<circle cx="130" cy="105" r="10" fill="#C9B6F5"/>
</svg>"""

_WAVE = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<path d="M10 80 Q35 20 60 80 T110 80 T160 80" fill="none" stroke="#7FD0EC" stroke-width="5" stroke-linecap="round"/>
<line x1="10" y1="80" x2="150" y2="80" stroke="#D9D2E9" stroke-width="2" stroke-dasharray="4 4"/>
<line x1="35" y1="80" x2="35" y2="30" stroke="#FFD873" stroke-width="3"/>
<text x="38" y="28" font-size="12" fill="#B98A1C" font-family="Quicksand,sans-serif">A</text>
</svg>"""

_HEART = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<path d="M80 135 C20 95 20 45 55 35 C70 30 80 45 80 55 C80 45 90 30 105 35 C140 45 140 95 80 135 Z" fill="#FF9EC4" stroke="#F7739F" stroke-width="3"/>
<path d="M35 80 L55 80 L65 60 L75 100 L85 75 L95 90 L110 90" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

_NEURON = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<circle cx="55" cy="75" r="22" fill="#C9B6F5" stroke="#8862C7" stroke-width="3"/>
<line x1="38" y1="60" x2="20" y2="40" stroke="#8862C7" stroke-width="3"/>
<line x1="35" y1="75" x2="12" y2="75" stroke="#8862C7" stroke-width="3"/>
<line x1="38" y1="90" x2="20" y2="110" stroke="#8862C7" stroke-width="3"/>
<line x1="77" y1="75" x2="130" y2="75" stroke="#5B4368" stroke-width="4"/>
<circle cx="95" cy="75" r="4" fill="white" stroke="#5B4368" stroke-width="2"/>
<circle cx="115" cy="75" r="4" fill="white" stroke="#5B4368" stroke-width="2"/>
<circle cx="145" cy="75" r="8" fill="#FFD873" stroke="#B98A1C" stroke-width="2"/>
<line x1="138" y1="68" x2="130" y2="60" stroke="#B98A1C" stroke-width="2"/>
<line x1="138" y1="82" x2="130" y2="90" stroke="#B98A1C" stroke-width="2"/>
</svg>"""

_LUNGS = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<line x1="80" y1="20" x2="80" y2="55" stroke="#7FD0EC" stroke-width="6" stroke-linecap="round"/>
<path d="M80 55 L55 65" stroke="#7FD0EC" stroke-width="4" fill="none"/>
<path d="M80 55 L105 65" stroke="#7FD0EC" stroke-width="4" fill="none"/>
<path d="M55 65 C20 70 15 130 45 140 C65 145 60 100 55 65 Z" fill="#E4F7FD" stroke="#7FD0EC" stroke-width="3"/>
<path d="M105 65 C140 70 145 130 115 140 C95 145 100 100 105 65 Z" fill="#E4F7FD" stroke="#7FD0EC" stroke-width="3"/>
</svg>"""

_FLASK = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<line x1="68" y1="20" x2="68" y2="60" stroke="#5B4368" stroke-width="4"/>
<line x1="92" y1="20" x2="92" y2="60" stroke="#5B4368" stroke-width="4"/>
<path d="M68 60 L35 130 Q30 140 42 140 L118 140 Q130 140 125 130 L92 60 Z" fill="#E4F7FD" stroke="#5B4368" stroke-width="4"/>
<path d="M45 125 L115 125 L125 130 Q130 140 118 140 L42 140 Q30 140 35 130 Z" fill="#8FE3C7" opacity="0.7"/>
<circle cx="70" cy="105" r="5" fill="white" opacity="0.8"/>
<circle cx="90" cy="115" r="4" fill="white" opacity="0.8"/>
<circle cx="80" cy="95" r="3" fill="white" opacity="0.8"/>
</svg>"""

_PROTEIN = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<path d="M20 50 C50 20 50 80 80 80 C110 80 110 20 140 50" fill="none" stroke="#FF9EC4" stroke-width="7" stroke-linecap="round"/>
<path d="M20 100 C50 70 50 130 80 130 C110 130 110 70 140 100" fill="none" stroke="#7FD0EC" stroke-width="7" stroke-linecap="round"/>
<line x1="35" y1="55" x2="35" y2="95" stroke="#D9D2E9" stroke-width="2" stroke-dasharray="3 3"/>
<line x1="80" y1="80" x2="80" y2="130" stroke="#D9D2E9" stroke-width="2" stroke-dasharray="3 3"/>
<line x1="125" y1="55" x2="125" y2="95" stroke="#D9D2E9" stroke-width="2" stroke-dasharray="3 3"/>
</svg>"""

_BODY = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<circle cx="80" cy="35" r="20" fill="#FFE8F1" stroke="#FF9EC4" stroke-width="3"/>
<path d="M55 60 Q80 50 105 60 L112 130 Q80 145 48 130 Z" fill="#E4F7FD" stroke="#7FD0EC" stroke-width="3"/>
<line x1="55" y1="70" x2="30" y2="110" stroke="#7FD0EC" stroke-width="6" stroke-linecap="round"/>
<line x1="105" y1="70" x2="130" y2="110" stroke="#7FD0EC" stroke-width="6" stroke-linecap="round"/>
<line x1="65" y1="130" x2="60" y2="155" stroke="#7FD0EC" stroke-width="7" stroke-linecap="round"/>
<line x1="95" y1="130" x2="100" y2="155" stroke="#7FD0EC" stroke-width="7" stroke-linecap="round"/>
</svg>"""

_BOOK = """<svg viewBox="0 0 160 160" width="140" height="140" xmlns="http://www.w3.org/2000/svg">
<path d="M80 40 C60 25 30 25 20 35 L20 120 C30 110 60 110 80 125 Z" fill="#FFE8F1" stroke="#FF9EC4" stroke-width="3"/>
<path d="M80 40 C100 25 130 25 140 35 L140 120 C130 110 100 110 80 125 Z" fill="#F1EBFE" stroke="#C9B6F5" stroke-width="3"/>
<line x1="80" y1="45" x2="80" y2="122" stroke="#D9D2E9" stroke-width="2"/>
</svg>"""

_LIBRARY = {
    "atom": _ATOM,
    "dna": _DNA,
    "cell": _CELL,
    "molecule": _MOLECULE,
    "wave": _WAVE,
    "heart": _HEART,
    "neuron": _NEURON,
    "lungs": _LUNGS,
    "flask": _FLASK,
    "protein": _PROTEIN,
    "body": _BODY,
    "book": _BOOK,
}

# Mots-clés (dans le titre ou l'id du chapitre) -> illustration. Ordre = priorité.
_KEYWORDS = [
    (("atomist", "atome", "electron", "quantique", "periodique"), "atom"),
    (("nucleique", "genome", "adn", "replication", "transcription", "traduction", "genetique", "variations_genome", "methodes_etude"), "dna"),
    (("cellule", "membrane", "cytosquelette", "noyau", "apoptose", "endomembran", "mitochondrie", "peroxysome", "jonction", "signalisation", "developpement", "endocytose"), "cell"),
    (("organique", "liaisons", "stereochimie", "hybridation",), "molecule"),
    (("proteine", "enzymo", "chaperonne", "peptide", "amine",), "protein"),
    (("onde", "acoustique", "electrostat", "energ", "force", "fluide", "gaz", "imagerie",), "wave"),
    (("cardio", "coeur", "circulat",), "heart"),
    (("nerveux", "neurone", "cerveau",), "neuron"),
    (("respirat", "poumon",), "lungs"),
    (("acide_base", "redox", "cinetique", "thermodynamique", "glucide", "lipide",), "flask"),
    (("cycle_cellulaire",), "cell"),
]


def pick_illustration(chapter_id: str, title: str) -> str:
    haystack = f"{chapter_id} {title}".lower()
    for keywords, key in _KEYWORDS:
        if any(kw in haystack for kw in keywords):
            return key
    return "book"


def render_illustration(chapter_id: str, title: str) -> None:
    key = pick_illustration(chapter_id, title)
    svg = _LIBRARY.get(key, _BOOK)
    html(
        f'<div style="text-align:center; margin-bottom:.5rem;">{svg}</div>'
    )
