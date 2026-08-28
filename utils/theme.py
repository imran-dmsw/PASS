"""Injection du thème visuel kawaii (CSS custom) pour toute l'application."""

import streamlit as st

# Palette validée dans la charte (voir aperçu partagé avec l'utilisateur)
PINK = "#FF9EC4"
PINK_DEEP = "#F7739F"
PINK_TINT = "#FFE8F1"
LAVENDER = "#C9B6F5"
LAVENDER_TINT = "#F1EBFE"
SKY = "#7FD0EC"
SKY_TINT = "#E4F7FD"
YELLOW = "#FFD873"
YELLOW_TINT = "#FFF6DC"
CREAM = "#FFFBF4"
TEXT = "#5B4368"
TEXT_SOFT = "#9683A3"
SUCCESS = "#3FAE6A"
SUCCESS_TINT = "#DFF6E6"
ERROR = "#E85D8A"
ERROR_TINT = "#FFE3EC"

# Une teinte de fond par UE, pour varier les cards sans sortir de la palette
TINTS = {
    "pink": (PINK_TINT, PINK_DEEP),
    "lavender": (LAVENDER_TINT, "#8862C7"),
    "sky": (SKY_TINT, "#2B8FB0"),
    "yellow": (YELLOW_TINT, "#B98A1C"),
}


def inject_kawaii_theme() -> None:
    """A appeler en tout début de page (une seule fois suffit par page)."""
    st.html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
        :root {{
            --pink: {PINK}; --pink-deep: {PINK_DEEP}; --pink-tint: {PINK_TINT};
            --lavender: {LAVENDER}; --lavender-tint: {LAVENDER_TINT};
            --sky: {SKY}; --sky-tint: {SKY_TINT};
            --yellow: {YELLOW}; --yellow-tint: {YELLOW_TINT};
            --cream: {CREAM}; --text: {TEXT}; --text-soft: {TEXT_SOFT};
            --success: {SUCCESS}; --success-tint: {SUCCESS_TINT};
            --error: {ERROR}; --error-tint: {ERROR_TINT};
        }}

        html, body, [class*="css"] {{
            font-family: "Quicksand", ui-rounded, "Nunito", sans-serif;
        }}

        [data-testid="stAppViewContainer"], .stApp {{
            background:
                radial-gradient(circle at 6% 8%, var(--sky-tint) 0%, transparent 38%),
                radial-gradient(circle at 96% 10%, var(--yellow-tint) 0%, transparent 35%),
                radial-gradient(circle at 92% 92%, var(--lavender-tint) 0%, transparent 40%),
                var(--cream);
        }}

        [data-testid="stHeader"] {{ background: transparent; }}

        h1, h2, h3, h4 {{
            font-family: "Baloo 2", ui-rounded, sans-serif !important;
            color: var(--text) !important;
        }}

        p, li, span, label, div {{ color: var(--text); }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #FFF6FB 0%, var(--pink-tint) 100%);
            border-right: 2px dashed #F3D3E4;
        }}
        [data-testid="stSidebar"] * {{ font-family: "Quicksand", sans-serif; }}

        /* Boutons */
        .stButton > button, .stDownloadButton > button {{
            font-family: "Quicksand", sans-serif;
            font-weight: 700;
            border: none;
            border-radius: 999px;
            padding: 0.55rem 1.4rem;
            background: var(--pink);
            color: white;
            box-shadow: 0 6px 14px rgba(247,115,159,0.35);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 18px rgba(247,115,159,0.42);
            color: white;
        }}
        .stButton > button:focus:not(:active) {{ color: white; }}

        /* Radios / choix de quiz */
        [data-testid="stRadio"] label {{
            background: white;
            border: 2px solid var(--pink-tint);
            border-radius: 16px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.4rem;
            font-weight: 600;
        }}

        /* Barre de progression native -> cœurs de couleur */
        div[data-testid="stProgress"] div[role="progressbar"] > div {{
            background-image: linear-gradient(90deg, var(--pink), var(--lavender)) !important;
        }}

        /* Onglets */
        button[data-baseweb="tab"] {{
            font-family: "Quicksand", sans-serif;
            font-weight: 700;
            border-radius: 999px 999px 0 0;
        }}

        /* Cards kawaii custom (rendues via st.markdown) */
        .kawaii-card {{
            background: white;
            border-radius: 26px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 8px 22px rgba(180,120,160,0.15);
            margin-bottom: 1.1rem;
            position: relative;
            overflow: hidden;
        }}
        .kawaii-card .kawaii-icon {{
            width: 48px; height: 48px; border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; margin-bottom: 0.7rem;
        }}
        .kawaii-badge {{
            display: inline-flex; align-items: center; gap: 0.35rem;
            font-family: "Quicksand", sans-serif; font-weight: 700; font-size: 0.78rem;
            letter-spacing: 0.04em; text-transform: uppercase;
            background: var(--pink-tint); color: var(--pink-deep);
            padding: 0.3rem 0.8rem; border-radius: 999px;
        }}
        .kawaii-stars {{ color: var(--yellow); letter-spacing: 2px; font-size: 1.05rem; }}
        .kawaii-stars .off {{ color: #F0E4D0; }}

        .mascot-bubble {{
            display: flex; gap: 0.8rem; align-items: flex-start;
            background: var(--lavender-tint);
            border-radius: 20px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }}
        .mascot-bubble b {{
            display: block; font-family: "Baloo 2", sans-serif; font-size: 1rem;
            margin-bottom: 0.2rem; color: var(--text);
        }}
        .mascot-bubble.success {{ background: var(--success-tint); }}
        .mascot-bubble.oops {{ background: var(--error-tint); }}

        .quiz-option-correct {{
            background: var(--success-tint) !important;
            border-color: var(--success) !important;
        }}
        .quiz-option-wrong {{
            background: var(--error-tint) !important;
            border-color: var(--error) !important;
        }}

        footer, #MainMenu {{ visibility: hidden; }}
        </style>
        """
    )
