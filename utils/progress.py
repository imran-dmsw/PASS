"""Suivi de progression (cœurs/étoiles) stocké en st.session_state.

Volontairement en mémoire de session : pas de backend, l'appli reste simple
a déployer sur Streamlit Community Cloud. La progression se réinitialise
si l'onglet est fermé (comme dans un jeu sans compte).
"""

import streamlit as st

_KEY = "kawaii_progress"


def init_progress() -> None:
    if _KEY not in st.session_state:
        st.session_state[_KEY] = {}


def _chapter_key(ue_id: str, chapter_id: str) -> str:
    return f"{ue_id}__{chapter_id}"


def record_quiz_result(ue_id: str, chapter_id: str, score: int, total: int) -> None:
    init_progress()
    key = _chapter_key(ue_id, chapter_id)
    current = st.session_state[_KEY].get(key, {"best_score": 0, "total": total, "attempts": 0})
    st.session_state[_KEY][key] = {
        "best_score": max(current["best_score"], score),
        "total": total,
        "attempts": current["attempts"] + 1,
    }


def get_chapter_progress(ue_id: str, chapter_id: str) -> dict:
    init_progress()
    key = _chapter_key(ue_id, chapter_id)
    return st.session_state[_KEY].get(key, {"best_score": 0, "total": 0, "attempts": 0})


def mastery_ratio(ue_id: str, chapter_id: str) -> float:
    progress = get_chapter_progress(ue_id, chapter_id)
    if not progress["total"]:
        return 0.0
    return progress["best_score"] / progress["total"]


def render_stars(difficulty: int) -> str:
    difficulty = max(1, min(3, int(difficulty)))
    filled = "★" * difficulty
    empty = "☆" * (3 - difficulty)
    return f'<span class="kawaii-stars">{filled}<span class="off">{empty}</span></span>'


def render_hearts(ratio: float, count: int = 5) -> str:
    filled = round(ratio * count)
    hearts = "".join("💖" if i < filled else '<span style="opacity:.3;filter:grayscale(1)">🤍</span>' for i in range(count))
    return f'<div style="margin:.5rem 0;">{hearts}</div>'


def total_stars_earned() -> int:
    """Nombre de chapitres maitrisés a plus de 80% (pour un compteur global sympa)."""
    init_progress()
    return sum(1 for v in st.session_state[_KEY].values() if v["total"] and v["best_score"] / v["total"] >= 0.8)
