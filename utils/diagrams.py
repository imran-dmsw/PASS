"""Cartes mentales : rendu 100% SVG statique généré côté serveur (aucun
JavaScript, aucune dépendance externe). Beaucoup plus fiable qu'une lib
JS (mermaid.js) chargée dans une iframe de composant Streamlit : pas de
mesure de bounding box côté navigateur, donc pas de bug de rendu possible
quel que soit le navigateur de l'utilisateur (confirmé cassé en prod).

Les chaînes "diagram" stockées dans les JSON restent au format mermaid
"flowchart TD" (A[Texte] --> B[Texte]) : on les parse nous-mêmes ici pour
en extraire un arbre (racine -> branches -> sous-branches), rendu en
colonnes façon organigramme (une colonne par branche, ses sous-nœuds
empilés verticalement en dessous) plutôt qu'en lignes complètes - ça
borne la largeur au nombre de branches (4-6) au lieu du nombre total de
feuilles (15-20), qui donnait un diagramme illisible en le compressant
dans une carte de largeur normale."""

from __future__ import annotations

import re
import textwrap

from utils.html import html

_EDGE_RE = re.compile(r"^\s*([A-Za-z0-9_]+)(\[[^\[\]]*\])?\s*-->\s*([A-Za-z0-9_]+)(\[[^\[\]]*\])?\s*$")

_PALETTE = ["#FF9EC4", "#C9B6F5", "#7FD0EC", "#FFD873", "#8FE3C7", "#F7B4D6"]

_NODE_W = 168
_COL_GAP = 18
_LINE_H = 14
_PAD_Y = 10
_ROOT_H = 46
_ROOT_GAP = 46
_CHILD_GAP = 14


def _parse(mermaid_code: str):
    labels: dict[str, str] = {}
    children: dict[str, list[str]] = {}
    parents: dict[str, str] = {}
    order: list[str] = []

    for line in mermaid_code.strip().split("\n")[1:]:
        m = _EDGE_RE.match(line)
        if not m:
            continue
        src, src_label, dst, dst_label = m.groups()
        for node_id, node_label in ((src, src_label), (dst, dst_label)):
            if node_id not in labels:
                order.append(node_id)
            if node_label:
                labels[node_id] = node_label[1:-1]
            elif node_id not in labels:
                labels[node_id] = node_id
        children.setdefault(src, []).append(dst)
        parents[dst] = src

    if not order:
        return None, {}, {}
    root = next((n for n in order if n not in parents), order[0])
    return root, labels, children


def _wrap(text: str, width: int = 15) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False) or [text]


def _node_block(cx: float, top: float, lines: list[str], color: str, filled: bool) -> tuple[str, float]:
    """Retourne (svg, hauteur_du_bloc) pour un nœud centré en x=cx, sommet en y=top."""
    h = _PAD_Y * 2 + len(lines) * _LINE_H
    rx = cx - _NODE_W / 2
    fill = color if filled else "white"
    text_color = "white" if filled else "#5B4368"
    weight = "700" if filled else "600"
    parts = [
        f'<rect x="{rx:.1f}" y="{top:.1f}" width="{_NODE_W}" height="{h:.1f}" rx="14" '
        f'fill="{fill}" stroke="{color}" stroke-width="2"/>'
    ]
    start_y = top + h / 2 - (len(lines) - 1) * _LINE_H / 2 + 5
    for j, line in enumerate(lines):
        parts.append(
            f'<text x="{cx:.1f}" y="{start_y + j * _LINE_H:.1f}" text-anchor="middle" '
            f'font-size="12.5" font-weight="{weight}" fill="{text_color}">{line}</text>'
        )
    return "".join(parts), h


def _svg_diagram(mermaid_code: str) -> str | None:
    root, labels, children = _parse(mermaid_code)
    if root is None:
        return None

    branches = children.get(root, [])
    if not branches:
        branches = [root]
        children = {}

    n_cols = len(branches)
    total_width = n_cols * _NODE_W + (n_cols - 1) * _COL_GAP + 40
    root_cx = total_width / 2

    body_parts = []
    edge_parts = []

    root_lines = _wrap(labels.get(root, root), width=18)
    root_top = 20
    root_svg, root_h = _node_block(root_cx, root_top, root_lines, _PALETTE[0], filled=True)
    body_parts.append(root_svg)

    col_bottom_y = root_top + root_h + _ROOT_GAP
    max_col_height = 0
    x = 20 + _NODE_W / 2

    for i, branch in enumerate(branches):
        color = _PALETTE[(i + 1) % len(_PALETTE)]
        branch_lines = _wrap(labels.get(branch, branch))
        branch_svg, branch_h = _node_block(x, col_bottom_y, branch_lines, color, filled=True)
        body_parts.append(branch_svg)
        edge_parts.append(
            f'<path d="M{root_cx:.1f},{root_top + root_h:.1f} C{root_cx:.1f},{root_top + root_h + 24:.1f} '
            f'{x:.1f},{col_bottom_y - 24:.1f} {x:.1f},{col_bottom_y:.1f}" '
            f'stroke="#D9D2E9" stroke-width="2" fill="none"/>'
        )

        y = col_bottom_y + branch_h + _CHILD_GAP
        prev_bottom = col_bottom_y + branch_h
        for child in children.get(branch, []):
            child_lines = _wrap(labels.get(child, child))
            child_svg, child_h = _node_block(x, y, child_lines, color, filled=False)
            body_parts.append(child_svg)
            edge_parts.append(
                f'<path d="M{x:.1f},{prev_bottom:.1f} L{x:.1f},{y:.1f}" '
                f'stroke="{color}" stroke-width="2" fill="none" opacity="0.5"/>'
            )
            prev_bottom = y + child_h
            y += child_h + _CHILD_GAP

        max_col_height = max(max_col_height, prev_bottom - col_bottom_y)
        x += _NODE_W + _COL_GAP

    total_height = col_bottom_y + max_col_height + 20

    svg = (
        f'<svg viewBox="0 0 {total_width:.0f} {total_height:.0f}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;height:auto;font-family:Quicksand,sans-serif;">'
        + "".join(edge_parts)
        + "".join(body_parts)
        + "</svg>"
    )
    return svg


def render_diagram(mermaid_code: str) -> None:
    if not mermaid_code:
        return
    svg = _svg_diagram(mermaid_code)
    if not svg:
        return
    html(f'<div class="kawaii-card" style="padding:1.2rem; overflow-x:auto;">{svg}</div>')
