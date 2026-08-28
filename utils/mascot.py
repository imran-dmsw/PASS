"""Dr. Mochi, la mascotte chat-étudiant. SVG inline (pas de fichier externe requis)."""

import random

_BASE_HEAD = """
<svg width="{size}" height="{size}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="60" cy="102" rx="30" ry="8" fill="#F7739F" opacity=".12"/>
  <path d="M34 40 L24 14 L48 32 Z" fill="#FFD873"/>
  <path d="M86 40 L96 14 L72 32 Z" fill="#FFD873"/>
  <path d="M38 42 L30 22 L50 34 Z" fill="#FFE8B0"/>
  <path d="M82 42 L90 22 L70 34 Z" fill="#FFE8B0"/>
  <circle cx="60" cy="62" r="38" fill="#FFF6DC"/>
  <ellipse cx="38" cy="70" rx="7" ry="5" fill="#FFC2D1"/>
  <ellipse cx="82" cy="70" rx="7" ry="5" fill="#FFC2D1"/>
  {face}
</svg>
"""

_FACES = {
    "happy": """
        <path d="M45 58 Q49 52 53 58" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M67 58 Q71 52 75 58" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M53 80 Q60 87 67 80" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <circle cx="60" cy="96" r="6" fill="#7FD0EC"/>
        <path d="M54 92 q6 8 12 0" stroke="#7FD0EC" stroke-width="3" fill="none"/>
    """,
    "bravo": """
        <path d="M44 55 a5 5 0 0 1 10 0" fill="#5B4368"/>
        <path d="M66 55 a5 5 0 0 1 10 0" fill="#5B4368"/>
        <path d="M50 84 Q60 92 70 84 Q60 98 50 84Z" fill="#5B4368"/>
        <g transform="translate(60 55) rotate(15)"><rect x="-16" y="-3" width="32" height="6" rx="3" fill="#FFD873"/></g>
    """,
    "encourage": """
        <ellipse cx="38" cy="72" rx="8" ry="6" fill="#FFC2D1"/>
        <ellipse cx="82" cy="72" rx="8" ry="6" fill="#FFC2D1"/>
        <path d="M46 62 Q50 68 54 62" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M66 62 Q70 68 74 62" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M52 84 Q60 80 68 84" stroke="#5B4368" stroke-width="3" fill="none" stroke-linecap="round"/>
        <circle cx="46" cy="78" r="3" fill="#7FD0EC" opacity=".8"/>
    """,
}


def mascot_svg(mood: str = "happy", size: int = 100) -> str:
    """mood: 'happy' | 'bravo' | 'encourage'

    Rendu sur une seule ligne : un SVG multi-lignes indenté, une fois
    interpolé dans un bloc HTML plus large passé à st.markdown, peut être
    coupé par le parseur Markdown (qui traite le texte indenté comme du
    code) et fuiter en texte brut au lieu de s'afficher comme une image.
    """
    face = _FACES.get(mood, _FACES["happy"])
    svg = _BASE_HEAD.format(size=size, face=face)
    return " ".join(svg.split())


GREETINGS = [
    "Prêt·e à faire fondre quelques neurones aujourd'hui ? 🌸🧠",
    "Un petit quiz par jour éloigne le trou de mémoire ! ✨",
    "Dr. Mochi a préparé des fiches toutes douces pour toi aujourd'hui 🐱💕",
    "Chaque révision est une étoile de plus dans ta collection ⭐",
    "Tu peux le faire, courage petit·e futur·e médecin ! 🌸",
    "Aujourd'hui, on avance pas à pas — même un petit quiz compte ! 🎀",
    "Respire, révise, ronronne. On y va en douceur 🐾",
]

CORRECT_MESSAGES = [
    ("Miaou-gnifique !", "Exactement ça, tu gères ! ✨"),
    ("Bravo !", "Une étoile de plus dans ta collection 🌟"),
    ("Parfait !", "Dr. Mochi ronronne de fierté 🐱💕"),
    ("Yatta !", "Cette notion, tu l'as maintenant dans la poche 🎀"),
]

WRONG_MESSAGES = [
    ("Oups, pas grave !", "On retente ensemble, tu vas y arriver 💪🐰"),
    ("Presque !", "C'est en se trompant qu'on retient le mieux, courage 🌸"),
    ("Pas tout à fait...", "Relis l'explication, elle va tout éclaircir 💡"),
    ("Ce n'est rien !", "Chaque erreur est une future bonne réponse au concours 🎗️"),
]


def pick_greeting() -> str:
    return random.choice(GREETINGS)


def pick_feedback(is_correct: bool):
    """Retourne (titre, message, mood) pour la bulle de feedback d'une question."""
    if is_correct:
        title, msg = random.choice(CORRECT_MESSAGES)
        return title, msg, "bravo"
    title, msg = random.choice(WRONG_MESSAGES)
    return title, msg, "encourage"


def score_reaction(ratio: float):
    """Retourne (titre, message, mood) pour l'écran de score final, selon le ratio de réussite."""
    if ratio >= 0.8:
        return (
            "Excellent·e ! 🎉",
            "Tu maîtrises ce chapitre à merveille, continue comme ça, futur·e médecin ! 🌸👩‍⚕️",
            "bravo",
        )
    if ratio >= 0.5:
        return (
            "Bon travail ! 💮",
            "Tu es sur la bonne voie, encore un peu de pratique et ce sera parfait ✨",
            "happy",
        )
    return (
        "Courage ! 💪",
        "Ce chapitre est corsé, relis la fiche de cours et retente le quiz, tu vas progresser 🐰💕",
        "encourage",
    )
