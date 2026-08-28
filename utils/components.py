"""Petits helpers de rendu HTML kawaii, réutilisés par app.py et les pages UE.

Les blocs HTML sont écrits sans indentation (flush-left) : Markdown convertit
tout texte indenté de 4+ espaces en bloc de code, ce qui casserait le rendu
si on gardait l'indentation Python habituelle à l'intérieur des f-strings.
"""

from utils.html import html
from utils.mascot import mascot_svg
from utils.progress import mastery_ratio, render_hearts, render_stars
from utils.theme import TINTS


def render_mascot_bubble(title: str, message: str, mood: str = "happy", style: str = "") -> None:
    css_class = "mascot-bubble"
    if style:
        css_class += f" {style}"
    html(f"""<div class="{css_class}">
<div>{mascot_svg(mood, size=64)}</div>
<div><b>{title}</b>{message}</div>
</div>""")


def render_chapter_summary_card(ue_id: str, chapter: dict) -> None:
    tint_bg, tint_text = TINTS.get("pink")
    ratio = mastery_ratio(ue_id, chapter["id"])
    html(f"""<div class="kawaii-card">
<div class="kawaii-icon" style="background:{tint_bg}; color:{tint_text};">📖</div>
<h4 style="margin:0 0 .2rem;">{chapter['title']}</h4>
<p style="color:var(--text-soft); margin:0 0 .5rem; font-size:.9rem;">{chapter.get('intro', '')}</p>
{render_stars(chapter['difficulty'])}
{render_hearts(ratio)}
</div>""")


def render_course_block(block: dict) -> None:
    html(f"""<div class="kawaii-card">
<div class="kawaii-icon" style="background:var(--pink-tint); color:var(--pink-deep);">{block['icon']}</div>
<h4 style="margin:0 0 .4rem;">{block['title']}</h4>
<p style="margin:0; font-size:.98rem; line-height:1.6;">{block['content']}</p>
</div>""")


def render_ue_home_card(ue_data: dict) -> None:
    tint_bg, tint_text = TINTS.get(ue_data.get("tint", "pink"), TINTS["pink"])
    n_chapters = len(ue_data["chapters"])
    n_questions = sum(len(c["quiz"]) for c in ue_data["chapters"])
    is_official_ue = ue_data["ue_id"].startswith("ue")
    heading = f"{ue_data['ue_id'].upper()} · {ue_data['ue_name']}" if is_official_ue else ue_data["ue_name"]
    html(f"""<div class="kawaii-card">
<div class="kawaii-icon" style="background:{tint_bg}; color:{tint_text};">{ue_data['icon']}</div>
<h3 style="margin:0 0 .2rem;">{heading}</h3>
<p style="color:var(--text-soft); font-size:.88rem; margin:0;">{n_chapters} chapitres · {n_questions} questions de quiz</p>
</div>""")
