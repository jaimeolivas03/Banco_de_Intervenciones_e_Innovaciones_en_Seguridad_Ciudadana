"""Estilos mínimos para reproducir la identidad cromática de la PPT."""

from html import escape
import streamlit as st

from banco.config import COLORES


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
        /* Interfaz clara, roja y gris inspirada en la PPT. */
        .stApp { background: #FFFFFF; color: #111111; }
        .block-container { max-width: 1230px; padding-top: 1.5rem; padding-bottom: 3.5rem; }
        section[data-testid="stSidebar"] { background: #F3F3F3; border-right: 1px solid #E4E4E4; }
        h1, h2, h3 { color: #111111; letter-spacing: -.025em; }
        div[data-testid="stMetric"] { background: #F8F8F8; border: 1px solid #E7E7E7; border-left: 4px solid #CF0000; border-radius: 12px; padding: 12px 16px; }
        div[data-testid="stMetricLabel"] { color: #5B5B5B; }
        .bii-hero { position:relative; overflow:hidden; background:#CF0000; color:white; border-radius:18px; padding:38px 42px; margin: 4px 0 26px; }
        .bii-hero:after { content:""; position:absolute; width:260px; height:260px; right:-50px; top:-96px; border:26px solid rgba(255,255,255,.11); border-radius:50%; }
        .bii-eyebrow { font-size:.78rem; text-transform:uppercase; letter-spacing:.16em; font-weight:700; opacity:.9; margin-bottom:10px; }
        .bii-hero h1 { color:#fff; font-size:clamp(1.65rem,3.4vw,2.6rem); line-height:1.15; margin: 0 0 10px; max-width:760px; }
        .bii-hero p { color:#fff; opacity:.93; margin:0; max-width:790px; font-size:1.01rem; line-height:1.58; }
        .bii-tag { display:inline-block; padding:5px 9px; font-size:.73rem; font-weight:700; background:#FDEAEA; color:#A90000; border-radius:8px; margin:4px 8px 8px 0; }
        .bii-step { padding:18px 14px; background:#F3F3F3; border-top:4px solid #CF0000; border-radius:12px; min-height:106px; }
        .bii-step strong { color:#CF0000; font-size:.8rem; letter-spacing:.09em; }
        .bii-step h4 { margin:8px 0 5px; color:#111111; font-size:1.0rem; }
        .bii-step p { color:#5B5B5B; margin:0; font-size:.82rem; line-height:1.4; }
        .bii-subtle { color:#5B5B5B; font-size:.90rem; }
        [data-testid="stSidebar"] .stRadio label { font-weight:600; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(titulo: str, subtitulo: str, etiqueta: str = "Piloto conceptual · versión 0.1") -> None:
    st.markdown(
        f'<div class="bii-hero"><div class="bii-eyebrow">{escape(etiqueta)}</div>'
        f'<h1>{escape(titulo)}</h1><p>{escape(subtitulo)}</p></div>',
        unsafe_allow_html=True,
    )


def paso(numero: str, titulo: str, descripcion: str) -> None:
    st.markdown(
        f'<div class="bii-step"><strong>{escape(numero)}</strong>'
        f'<h4>{escape(titulo)}</h4><p>{escape(descripcion)}</p></div>',
        unsafe_allow_html=True,
    )


def etiqueta_piloto() -> None:
    st.caption(
        "Diseño preliminar. Los registros demostrativos son ficticios y no acreditan "
        "resultados ni eficacia de intervenciones reales."
    )
