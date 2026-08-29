"""Chargement (avec cache) des fichiers JSON de contenu par UE."""

from __future__ import annotations

import json
import os

import streamlit as st

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# UE officielles de Paris Cité, remplies a partir des vrais polys de pre-rentree A2SUP.
# A completer au fur et a mesure si d'autres UE (SHS, ...) sont fournies.
AVAILABLE_UES = ["ue1", "ue2", "ue3", "ue4", "ue5", "ue6", "ue7"]

# Module bonus hors numerotation officielle (pas de poly source pour le valider).
BONUS_MODULES = ["anatomie"]


@st.cache_data(show_spinner=False)
def load_ue(ue_id: str) -> dict:
    path = os.path.join(_DATA_DIR, f"{ue_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_all_ues() -> list:
    return [load_ue(ue_id) for ue_id in AVAILABLE_UES]


def get_chapter(ue_data: dict, chapter_id: str) -> dict | None:
    for chapter in ue_data["chapters"]:
        if chapter["id"] == chapter_id:
            return chapter
    return None
