#!/usr/bin/env python3
"""
Sanitas — Panel de Conocimiento del Consumidor
python -m streamlit run panel_sanitas.py
"""
import warnings; warnings.filterwarnings("ignore")
import os, json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ══════════════════════════════════════════════════════════════════
# RUTAS
# ══════════════════════════════════════════════════════════════════
BASE = Path(__file__).parent.parent
DATA = BASE / "data"
GEO  = BASE / "data_geo"

# ══════════════════════════════════════════════════════════════════
# PALETA — Sanitas
# ══════════════════════════════════════════════════════════════════
ACCENT  = "#003087"
A2      = "#0057A8"
A3      = "#0099D6"
BG      = "#F8F9FA"
FONT    = "#111827"
GRID    = "#F3F4F6"
PAPER   = "#FFFFFF"
S_BORDER= "#E5E7EB"
S_MUTED = "#6B7280"
S_LIGHT = "#EEF4FF"

COMP_C = {
    "Sanitas":       ACCENT,
    "Adeslas":       "#B71C1C",
    "Asisa":         "#2E7D32",
    "DKV":           "#E65100",
    "Mapfre Salud":  "#4A148C",
    "AXA Salud":     "#37474F",
    "Quirónsalud":   "#6A1B9A",
    "HM Hospitales": "#BF360C",
    "Vithas":        "#006064",
    "IMQ":           "#33691E",
}

# ══════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Sanitas · Consumer Insights",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#MainMenu,footer,header{{visibility:hidden}}
[data-testid="stToolbar"]{{display:none}}
[data-testid="column"]{{overflow:visible!important}}
[data-testid="stHorizontalBlock"]{{overflow:visible!important}}
.block-container{{padding:0 2.5rem 3rem!important;max-width:1440px}}
.stApp{{background:{BG};color:{FONT}}}
html,body,[class*="css"]{{font-family:'Inter',sans-serif}}

/* Sidebar */
[data-testid="stSidebar"]{{
  display:block!important;visibility:visible!important;
  transform:none!important;width:18rem!important;
  background:{S_LIGHT}!important;border-right:1px solid #C0D5F0!important}}
[data-testid="stSidebar"] *{{color:{FONT}!important;font-family:'Inter',sans-serif!important}}
[data-testid="stSidebar"] label{{
  color:{ACCENT}!important;font-size:.65rem!important;
  letter-spacing:.1em;text-transform:uppercase;
  font-weight:600!important;margin-bottom:4px!important}}
[data-testid="stSidebar"] [data-baseweb="select"]{{
  background:#F0F7FF!important;border:1px solid #90B8DE!important;border-radius:6px!important}}
[data-testid="stSidebar"] [data-baseweb="select"] *{{
  background:#F0F7FF!important;color:{FONT}!important;font-size:.84rem!important}}
[data-testid="stSidebar"] hr{{border-color:#C0D5F0!important;margin:0!important}}
[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
button[kind="header"]{{display:none!important}}

/* Top bar */
.top-bar{{
  background:transparent;padding:18px 0 0 0;
  display:flex;align-items:baseline;justify-content:space-between;
  border-bottom:1px solid {S_BORDER};margin-bottom:2rem}}
.top-title{{font-size:1rem;font-weight:700;color:{FONT};letter-spacing:-.01em}}
.top-sub{{font-size:.72rem;color:{S_MUTED};letter-spacing:.04em}}

/* Secciones */
.section-title{{font-size:1rem;font-weight:700;color:{FONT};font-family:'Inter',sans-serif;letter-spacing:-.01em;margin-bottom:2px}}
.section-rule{{width:28px;height:2px;background:{ACCENT};border-radius:2px;margin:5px 0 16px 0}}

/* KPI cards */
.kpi-card{{
  background:{PAPER};border:1px solid {S_BORDER};
  border-radius:10px;padding:20px 24px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);transition:box-shadow .15s}}
.kpi-card:hover{{box-shadow:0 4px 12px rgba(0,0,0,.08)}}
.kpi-label{{font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;color:#9CA3AF;margin-bottom:8px;font-weight:500}}
.kpi-value{{font-size:2rem;font-weight:700;color:{FONT};line-height:1;letter-spacing:-.02em}}
.kpi-sub{{font-size:.7rem;color:{ACCENT};margin-top:6px;font-weight:500}}
.kpi-neg{{font-size:.7rem;color:#B71C1C;margin-top:6px;font-weight:500}}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{{gap:4px;border-bottom:1px solid {S_BORDER};background:transparent;padding:0 2px}}
.stTabs [data-baseweb="tab"]{{
  font-size:.78rem;letter-spacing:.04em;color:{S_MUTED};
  padding:10px 18px;border:none;border-bottom:2px solid transparent;
  background:transparent!important;font-weight:500}}
.stTabs [aria-selected="true"]{{color:{FONT}!important;border-bottom:2px solid {ACCENT}!important;font-weight:600!important}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:1.6rem}}

/* Expander */
[data-testid="stExpander"]{{
  border:1px solid {S_BORDER}!important;border-radius:8px!important;
  background:{PAPER}!important;box-shadow:0 1px 3px rgba(0,0,0,.04)!important}}

/* Chart label */
.chart-label{{font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;color:#6B7280;margin-bottom:8px;font-weight:700}}
.callout{{font-size:.78rem;color:{S_MUTED};line-height:1.6;padding:12px 0 0 0}}
.callout strong{{color:{FONT}}}
hr{{border:none;border-top:1px solid {GRID};margin:2rem 0}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Cargando datos…")
def load_all():
    d = {}
    files = {
        "precios":        "seguros_precios.csv",
        "coberturas":     "seguros_coberturas.csv",
        "cuotas":         "cuotas_mercado.csv",
        "encuesta":       "encuesta_simulada.csv",
        "redes":          "redes_sociales.csv",
        "trends":         "google_trends.csv",
        "hospitales":     "hospitales.csv",
        "valoraciones":   "valoraciones_hospitales.csv",
        "especialidades": "especialidades_hospitales.csv",
        "personas":       "buyer_personas.csv",
    }
    for k, fname in files.items():
        path = DATA / fname
        d[k] = pd.read_csv(path, encoding="utf-8-sig") if path.exists() else pd.DataFrame()

    geo_path = GEO / "centros_ampliados.json"
    if not geo_path.exists():
        geo_path = GEO / "hospitales_geo.json"
    with open(geo_path, encoding="utf-8") as f:
        d["centros"] = json.load(f)
    return d

dd = load_all()

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def lay(h=None, showlegend=False, legend=None, margin=None, xgrid=True, ygrid=False):
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter,sans-serif", color=FONT, size=11),
        margin=margin or dict(t=28, b=18, l=8, r=36),
        showlegend=showlegend,
        xaxis=dict(showgrid=xgrid, gridcolor=GRID, zeroline=False, linecolor=S_BORDER),
        yaxis=dict(showgrid=ygrid, gridcolor=GRID, zeroline=False, linecolor=S_BORDER),
    )
    if legend:
        d["legend"] = legend
    if h:
        d["height"] = h
    return d

def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>'
        f'<div class="section-rule"></div>',
        unsafe_allow_html=True)

def kpi_card(col, label, value, sub=None, negative=False):
    sub_cls = "kpi-neg" if negative else "kpi-sub"
    sub_html = f'<div class="{sub_cls}">{sub}</div>' if sub else ""
    col.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{sub_html}'
        f'</div>', unsafe_allow_html=True)

def callout(text):
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)

def go_to(page):
    st.session_state["page"] = page

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
if st.session_state.get("page", "home") != "mapa":
    with st.sidebar:
        st.markdown(
            f'<div style="padding:16px 0 14px;font-size:.72rem;letter-spacing:.12em;'
            f'text-transform:uppercase;font-weight:700;color:#374151">Filtros</div>',
            unsafe_allow_html=True)

        linea_sel = st.selectbox(
            "Línea de negocio",
            ["Ambas", "Seguros", "Hospitales"])

        st.markdown('<hr style="margin:12px 0">', unsafe_allow_html=True)

        marcas_seg = ["Todas", "Sanitas", "Adeslas", "Asisa", "DKV", "Mapfre Salud", "AXA Salud"]
        marca_seg_sel = st.selectbox("Aseguradora", marcas_seg)

        st.markdown('<hr style="margin:12px 0">', unsafe_allow_html=True)

        marcas_hosp = ["Todas", "Sanitas", "Quirónsalud", "HM Hospitales", "Vithas", "IMQ"]
        marca_hosp_sel = st.selectbox("Cadena hospitalaria", marcas_hosp)

        st.markdown('<hr style="margin:12px 0">', unsafe_allow_html=True)

        perfil_seg = st.selectbox(
            "Perfil de asegurado",
            ["Adulto individual", "Familia 2a+2h", "Senior 60+"])

        st.markdown('<hr style="margin:12px 0">', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:.62rem;color:#9CA3AF;line-height:1.6">'
            f'Datos simulados orientativos.<br>'
            f'Panel · Sanitas · Septiembre 2026</div>',
            unsafe_allow_html=True)

# Col map para precios
_col_precio = {
    "Adulto individual": "prima_adulto",
    "Familia 2a+2h":     "prima_familia",
    "Senior 60+":        "prima_senior",
}.get(perfil_seg if "perfil_seg" in dir() else "Adulto individual", "prima_adulto")

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ══════════════════════════════════════════════════════════════════
# TOP BAR (en todas las páginas)
# ══════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="top-bar">'
    f'<div>'
    f'<span class="top-title">Sanitas</span>&ensp;'
    f'<span class="top-sub">Consumer Insights · Salud Privada · 2026</span>'
    f'</div>'
    f'<div class="top-sub">Datos simulados — mockup de demostración</div>'
    f'</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state["page"] == "home":

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center;margin-bottom:8px">'
        f'<div style="font-size:1.55rem;font-weight:700;color:{FONT};letter-spacing:-.02em">'
        f'Consumer Insights 2026</div>'
        f'<div style="font-size:.8rem;color:{S_MUTED};margin-top:6px;letter-spacing:.04em">'
        f'Sanitas · Seguros de Salud & Hospitales</div>'
        f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:44px'></div>", unsafe_allow_html=True)

    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        if st.button("SEGUROS", key="btn_seg", use_container_width=True):
            go_to("seguros"); st.rerun()
    with r1c2:
        if st.button("HOSPITALES", key="btn_hosp", use_container_width=True):
            go_to("hospitales"); st.rerun()
    with r1c3:
        if st.button("COMUNICACIÓN", key="btn_com", use_container_width=True):
            go_to("comunicacion"); st.rerun()
    with r1c4:
        if st.button("POSICIONAMIENTO", key="btn_pos", use_container_width=True):
            go_to("posicionamiento"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        if st.button("MAPA ESTRATÉGICO", key="btn_mapa", use_container_width=True):
            go_to("mapa"); st.rerun()
    with r2c2:
        if st.button("EXPERIENCIA & RETENCIÓN", key="btn_exp", use_container_width=True):
            go_to("experiencia"); st.rerun()
    with r2c3:
        if st.button("ACCIONES", key="btn_acc", use_container_width=True):
            go_to("acciones"); st.rerun()

    st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center;color:{S_MUTED};font-size:.72rem;'
        f'letter-spacing:.06em;text-transform:uppercase">Acceso rápido</div>',
        unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    qa1, qa2, qa3, qa4, qa5 = st.columns(5)
    with qa1:
        if st.button("Prima media", use_container_width=True, key="qa1"):
            go_to("seguros"); st.rerun()
    with qa2:
        if st.button("Coberturas", use_container_width=True, key="qa2"):
            go_to("seguros"); st.rerun()
    with qa3:
        if st.button("Top of Mind", use_container_width=True, key="qa3"):
            go_to("posicionamiento"); st.rerun()
    with qa4:
        if st.button("Red de centros", use_container_width=True, key="qa4"):
            go_to("mapa"); st.rerun()
    with qa5:
        if st.button("Buyer Personas", use_container_width=True, key="qa5"):
            go_to("posicionamiento"); st.rerun()

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    # KPI resumen en home
    section("SITUACIÓN ACTUAL")
    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Cuota mercado seguros", "16.7%", "▼ 0.4 pp vs 2025", negative=True)
    kpi_card(k2, "NPS Sanitas seguros", "+22", "DKV lidera con +48", negative=True)
    kpi_card(k3, "Churn anual", "8.4%", "DKV: 5.1% — gap 3.3 pp", negative=True)
    kpi_card(k4, "Top of Mind", "#2", "Adeslas lidera con 27%")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    k5, k6, k7, k8 = st.columns(4)
    kpi_card(k5, "Rating hospitales", "4.14", "HM Hospitales 4.36", negative=True)
    kpi_card(k6, "% Telemedicina", "18%", "DKV: 34% — rezagado", negative=True)
    kpi_card(k7, "Loss ratio senior 60+", "89%", "Umbral crítico: 90%", negative=True)
    kpi_card(k8, "Espera psiquiatría", "22 días", "DKV: 14 días", negative=True)

# ══════════════════════════════════════════════════════════════════
# PÁGINA: SEGUROS
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "seguros":

    if st.button("← Inicio", key="back_seg"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("SEGUROS DE SALUD")
    st.caption(f"Perfil seleccionado: **{perfil_seg}**")

    t1, t2, t3, t4 = st.tabs(["Precios", "Coberturas", "Mercado & Encuesta", "Riesgo & Utilización"])

    # ── Precios ───────────────────────────────────────────────────
    with t1:
        df_p = dd["precios"].copy()
        if marca_seg_sel != "Todas":
            df_p_filt = df_p[df_p["marca"].isin(["Sanitas", marca_seg_sel])]
        else:
            df_p_filt = df_p

        c1, c2 = st.columns([1.4, 1])
        with c1:
            fig = px.bar(
                df_p_filt, x="tipo_poliza", y=_col_precio, color="marca",
                barmode="group",
                color_discrete_map=COMP_C,
                labels={_col_precio: "€/mes", "tipo_poliza": ""},
                text_auto=True,
            )
            fig.update_traces(texttemplate="%{y}€", textposition="outside",
                              textfont_size=10, marker_line_width=0)
            fig.update_layout(**lay(h=340, showlegend=True,
                legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
                margin=dict(t=10, b=60, l=8, r=8)))
            fig.update_yaxes(showgrid=True, gridcolor=GRID)
            st.markdown(f'<div class="chart-label">Prima mensual — {perfil_seg}</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Precio medio por aseguradora (todas las pólizas)
            df_avg = dd["precios"].groupby("marca")[_col_precio].mean().reset_index()
            df_avg = df_avg.sort_values(_col_precio, ascending=True)
            fig2 = go.Figure(go.Bar(
                y=df_avg["marca"], x=df_avg[_col_precio],
                orientation="h",
                marker_color=[ACCENT if m == "Sanitas" else S_BORDER for m in df_avg["marca"]],
                marker_line_width=0,
                text=[f"{int(v)}€" for v in df_avg[_col_precio]],
                textposition="outside",
                textfont=dict(size=10),
            ))
            fig2.update_layout(**lay(h=280, margin=dict(t=10, b=10, l=8, r=50)))
            fig2.update_xaxes(showgrid=True, gridcolor=GRID)
            fig2.update_yaxes(showgrid=False)
            st.markdown(f'<div class="chart-label">Prima media (todas las pólizas)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)

        callout(
            "<strong>Sanitas es la aseguradora más cara en todos los perfiles.</strong> "
            "En póliza básica adulto cobra 42€/mes frente a 33€ de DKV (+27%). "
            "La posición premium es coherente con el posicionamiento de marca, "
            "pero genera un gap en el segmento precio-sensible donde DKV crece al 2.1% anual."
        )

    # ── Coberturas ────────────────────────────────────────────────
    with t2:
        df_cob = dd["coberturas"]
        cob_cols   = ["dental","psicologia","fisioterapia","oftalmologia",
                      "urgencias_24h","internacional","app_digital","sin_esperas","farmacia"]
        cob_labels = ["Dental","Psicología","Fisioterapia","Oftalmología",
                      "Urgencias 24h","Cobertura int.","App digital","Sin esperas","Farmacia"]

        c1, c2 = st.columns([1.6, 1])
        with c1:
            z = df_cob[cob_cols].values
            fig_h = go.Figure(go.Heatmap(
                z=z, x=cob_labels, y=df_cob["marca"],
                colorscale=[[0,"#FEE2E2"],[0.5,"#FEF3C7"],[1,"#D1FAE5"]],
                zmin=1, zmax=3,
                text=np.where(z==3,"Sí",np.where(z==2,"Parcial","No")),
                texttemplate="%{text}",
                textfont=dict(size=10, color=FONT),
                showscale=False,
            ))
            fig_h.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter,sans-serif", color=FONT, size=10),
                height=280, margin=dict(t=10, b=10, l=8, r=8),
                xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=10)),
            )
            st.markdown('<div class="chart-label">Cobertura por prestación</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_h, use_container_width=True)

        with c2:
            df_te = df_cob.sort_values("tiempo_espera_dias")
            fig_te = go.Figure(go.Bar(
                y=df_te["marca"], x=df_te["tiempo_espera_dias"],
                orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_te["marca"]],
                marker_line_width=0,
                text=[f"{v}d" for v in df_te["tiempo_espera_dias"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_te.update_layout(**lay(h=240, margin=dict(t=10, b=10, l=8, r=40)))
            fig_te.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Tiempo de espera medio (días)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_te, use_container_width=True)

            df_cm = df_cob.sort_values("cuadro_medico", ascending=True)
            fig_cm = go.Figure(go.Bar(
                y=df_cm["marca"], x=df_cm["cuadro_medico"]/1000,
                orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_cm["marca"]],
                marker_line_width=0,
                text=[f"{v/1000:.0f}K" for v in df_cm["cuadro_medico"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_cm.update_layout(**lay(h=220, margin=dict(t=10, b=10, l=8, r=40)))
            fig_cm.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Médicos en cuadro (miles, estimado)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_cm, use_container_width=True)

        callout(
            "DKV lidera en experiencia digital y es la única con esperas garantizadas "
            "(3 días vs 4 de Sanitas). Adeslas supera a Sanitas en cuadro médico (48K vs 45K). "
            "<strong>Ventaja diferencial de Sanitas:</strong> única aseguradora con dental completo "
            "+ cobertura internacional + app digital simultáneamente — triángulo que no se comunica."
        )

    # ── Mercado & Encuesta ────────────────────────────────────────
    with t3:
        df_enc = dd["encuesta"]

        c1, c2, c3 = st.columns(3)
        with c1:
            atr = df_enc["atributo_clave"].value_counts().reset_index()
            atr.columns = ["atributo","n"]
            atr["pct"] = (atr["n"]/len(df_enc)*100).round(1)
            atr = atr.sort_values("pct", ascending=True)
            fig_a = go.Figure(go.Bar(
                y=atr["atributo"], x=atr["pct"], orientation="h",
                marker_color=A3, marker_line_width=0,
                text=[f"{v}%" for v in atr["pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_a.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=40)))
            fig_a.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Atributo más valorado</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_a, use_container_width=True)

        with c2:
            bar = df_enc["barrera"].value_counts().reset_index()
            bar.columns = ["barrera","n"]
            bar["pct"] = (bar["n"]/len(df_enc)*100).round(1)
            bar = bar.sort_values("pct", ascending=True)
            fig_b = go.Figure(go.Bar(
                y=bar["barrera"], x=bar["pct"], orientation="h",
                marker_color="#B71C1C", marker_line_width=0,
                text=[f"{v}%" for v in bar["pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_b.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=40)))
            fig_b.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Barreras de contratación</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_b, use_container_width=True)

        with c3:
            df_s = df_enc[df_enc["tiene_seguro"]=="Si"].copy()
            df_s = df_s[df_s["marca_seguro"]!="Otra"]
            sat = df_s.groupby("marca_seguro")["satisfaccion"].mean().reset_index()
            sat.columns = ["marca","sat"]
            sat = sat.sort_values("sat", ascending=True)
            sat["sat"] = sat["sat"].round(2)
            fig_s = go.Figure(go.Bar(
                y=sat["marca"], x=sat["sat"], orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in sat["marca"]],
                marker_line_width=0,
                text=[f"{v:.2f}" for v in sat["sat"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_s.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=40)))
            fig_s.update_xaxes(range=[2.5, 5.0], showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Satisfacción media (1–5)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_s, use_container_width=True)

    # ── Riesgo & Utilización ──────────────────────────────────────
    with t4:
        np.random.seed(77)
        ASEG6 = ["Sanitas","DKV","Adeslas","Asisa","Mapfre Salud","AXA Salud"]

        # ─ KPIs resumen riesgo ────────────────────────────────────
        rk1, rk2, rk3, rk4 = st.columns(4)
        kpi_card(rk1, "Loss ratio año 1 nuevos", "94.2%", "Sector: 76% — alerta selección adversa", negative=True)
        kpi_card(rk2, "Consultas/asegurado/año", "8.4", "DKV: 6.1 — sobre-utilización +38%", negative=True)
        kpi_card(rk3, "% urgencias evitables", "31%", "Sector: 22% — gap de 9 pp", negative=True)
        kpi_card(rk4, "Fraude estimado (€M)", "14.3", "1.8% primas — sector: 1.2%", negative=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)

        # ─ Loss ratio año 1 vs veteranos (selección adversa) ─────
        with rc1:
            df_lr_an = pd.DataFrame({
                "aseguradora": ASEG6,
                "loss_anio1":  [94, 72, 85, 81, 91, 88],
                "loss_anio3p": [71, 61, 68, 64, 76, 73],
            })
            fig_lr = go.Figure()
            fig_lr.add_trace(go.Bar(
                name="Año 1 (nuevos)", x=df_lr_an["aseguradora"],
                y=df_lr_an["loss_anio1"],
                marker_color=[ACCENT if m=="Sanitas" else "#FBBF24" for m in df_lr_an["aseguradora"]],
                marker_line_width=0, text=[f"{v}%" for v in df_lr_an["loss_anio1"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr.add_trace(go.Bar(
                name="Año 3+ (veteranos)", x=df_lr_an["aseguradora"],
                y=df_lr_an["loss_anio3p"],
                marker_color=[A3 if m=="Sanitas" else S_BORDER for m in df_lr_an["aseguradora"]],
                marker_line_width=0, text=[f"{v}%" for v in df_lr_an["loss_anio3p"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr.add_hline(y=80, line_dash="dot", line_color="#B71C1C", line_width=1.5,
                             annotation_text="Umbral sostenible 80%", annotation_position="top left",
                             annotation_font_size=9)
            fig_lr.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
                margin=dict(t=14, b=60, l=8, r=8)))
            fig_lr.update_yaxes(showgrid=True, gridcolor=GRID, range=[0, 115])
            st.markdown('<div class="chart-label">Loss ratio — Año 1 vs Año 3+ (selección adversa)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_lr, use_container_width=True)

        # ─ Consultas/asegurado/año (riesgo moral) ─────────────────
        with rc2:
            df_cons = pd.DataFrame({
                "aseguradora": ASEG6,
                "consultas_med": [5.1, 3.8, 4.6, 4.4, 5.4, 5.0],
                "urgencias":     [2.1, 1.4, 1.8, 1.7, 2.2, 2.1],
                "pruebas_diag":  [1.2, 0.9, 1.1, 1.0, 1.5, 1.3],
            })
            fig_cons = go.Figure()
            for col, label, color in [
                ("consultas_med", "Consultas médico", ACCENT),
                ("urgencias",     "Urgencias",        "#E65100"),
                ("pruebas_diag",  "Pruebas diagnósticas", A3),
            ]:
                fig_cons.add_trace(go.Bar(
                    name=label, x=df_cons["aseguradora"], y=df_cons[col],
                    marker_color=color, marker_line_width=0,
                ))
            fig_cons.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
                margin=dict(t=14, b=60, l=8, r=8)))
            fig_cons.update_layout(barmode="stack")
            fig_cons.update_yaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Utilización media por asegurado/año (riesgo moral)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_cons, use_container_width=True)

        rc3, rc4 = st.columns(2)

        # ─ % urgencias evitables por segmento ────────────────────
        with rc3:
            df_urg = pd.DataFrame({
                "segmento": ["Básico individual","Premium individual","Familiar","Senior 60+","Colectivo empresa"],
                "urg_evitables_sanitas": [28, 22, 35, 41, 18],
                "urg_evitables_sector":  [19, 16, 27, 38, 14],
            })
            fig_urg = go.Figure()
            fig_urg.add_trace(go.Bar(
                name="Sanitas", x=df_urg["segmento"], y=df_urg["urg_evitables_sanitas"],
                marker_color=ACCENT, marker_line_width=0,
                text=[f"{v}%" for v in df_urg["urg_evitables_sanitas"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_urg.add_trace(go.Bar(
                name="Sector", x=df_urg["segmento"], y=df_urg["urg_evitables_sector"],
                marker_color=S_BORDER, marker_line_width=0,
                text=[f"{v}%" for v in df_urg["urg_evitables_sector"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_urg.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
                margin=dict(t=14, b=70, l=8, r=8)))
            fig_urg.update_layout(barmode="group")
            fig_urg.update_yaxes(showgrid=True, gridcolor=GRID, range=[0, 58])
            fig_urg.update_xaxes(tickangle=-20, tickfont=dict(size=9))
            st.markdown('<div class="chart-label">% urgencias evitables por segmento</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_urg, use_container_width=True)

        # ─ Tipología de fraude estimado ───────────────────────────
        with rc4:
            df_fraud = pd.DataFrame({
                "tipo": [
                    "Tratamientos no realizados",
                    "Duplicación de reclamaciones",
                    "Prestaciones no cubiertas",
                    "Incremento artificial de facturas",
                    "Uso de terceros como asegurado",
                ],
                "pct": [34, 28, 18, 12, 8],
                "importe_k": [4862, 4004, 2574, 1716, 1144],
            })
            colors_fraud = [ACCENT, A2, A3, "#FBBF24", S_MUTED]
            fig_fraud = go.Figure(go.Pie(
                labels=df_fraud["tipo"], values=df_fraud["pct"],
                marker=dict(colors=colors_fraud, line=dict(color=PAPER, width=2)),
                textinfo="label+percent",
                textfont=dict(size=9),
                hole=0.45,
            ))
            fig_fraud.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter,sans-serif", color=FONT, size=10),
                height=320, margin=dict(t=14, b=14, l=8, r=8),
                showlegend=False,
                annotations=[dict(text="14.3M€<br>fraude est.", x=0.5, y=0.5,
                                  font=dict(size=10, color=FONT), showarrow=False)]
            )
            st.markdown('<div class="chart-label">Tipología de fraude estimado (Sanitas)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_fraud, use_container_width=True)

        # ─ Score de riesgo actuarial en contratación ──────────────
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        rc5, rc6 = st.columns([1.6, 1])

        with rc5:
            np.random.seed(42)
            n_pol = 600
            edad_cont = np.random.normal(38, 12, n_pol).clip(18, 75)
            score_risk = (
                0.35 * (edad_cont / 75 * 100) +
                0.25 * np.random.beta(2, 5, n_pol) * 100 +
                0.20 * np.random.uniform(0, 100, n_pol) +
                0.20 * np.random.normal(50, 20, n_pol).clip(0, 100)
            )
            loss_1y = 55 + 0.42 * score_risk + np.random.normal(0, 8, n_pol)
            df_scatter = pd.DataFrame({
                "edad": edad_cont.round(0).astype(int),
                "score_riesgo": score_risk.round(1),
                "loss_ratio_anio1": loss_1y.round(1),
                "segmento": np.random.choice(
                    ["Básico","Premium","Familiar","Senior","Empresa"], n_pol,
                    p=[0.28, 0.22, 0.32, 0.11, 0.07]),
            })
            seg_colors = {"Básico": A3, "Premium": ACCENT, "Familiar": "#2E7D32",
                          "Senior": "#E65100", "Empresa": S_MUTED}
            fig_sc = px.scatter(
                df_scatter, x="score_riesgo", y="loss_ratio_anio1",
                color="segmento", color_discrete_map=seg_colors,
                labels={"score_riesgo": "Score riesgo actuarial (0–100)",
                        "loss_ratio_anio1": "Loss ratio año 1 (%)"},
                opacity=0.55, size_max=5,
            )
            fig_sc.add_hline(y=80, line_dash="dot", line_color="#B71C1C", line_width=1.2,
                             annotation_text="Umbral rentable", annotation_font_size=8)
            fig_sc.add_vline(x=70, line_dash="dot", line_color="#E65100", line_width=1.2,
                             annotation_text="Alto riesgo", annotation_font_size=8)
            fig_sc.update_layout(**lay(h=340, showlegend=True,
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
                margin=dict(t=14, b=60, l=8, r=8)))
            fig_sc.update_yaxes(showgrid=True, gridcolor=GRID)
            fig_sc.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Score riesgo actuarial vs Loss ratio año 1 (simulado 600 pólizas)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_sc, use_container_width=True)

        with rc6:
            df_score_dist = pd.DataFrame({
                "banda": ["0–20\n(muy bajo)", "21–40\n(bajo)", "41–60\n(medio)",
                          "61–80\n(alto)", "81–100\n(muy alto)"],
                "pct_cartera": [18, 31, 29, 15, 7],
                "loss_medio":  [62, 69, 78, 91, 108],
            })
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(
                name="% cartera", x=df_score_dist["banda"], y=df_score_dist["pct_cartera"],
                marker_color=[A3, A2, ACCENT, "#E65100", "#B71C1C"],
                marker_line_width=0,
                text=[f"{v}%" for v in df_score_dist["pct_cartera"]],
                textposition="outside", textfont=dict(size=9),
                yaxis="y",
            ))
            fig_dist.add_trace(go.Scatter(
                name="Loss ratio medio", x=df_score_dist["banda"], y=df_score_dist["loss_medio"],
                mode="lines+markers+text",
                line=dict(color="#E65100", width=2),
                marker=dict(size=6),
                text=[f"{v}%" for v in df_score_dist["loss_medio"]],
                textposition="top center", textfont=dict(size=9),
                yaxis="y2",
            ))
            fig_dist.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter,sans-serif", color=FONT, size=10),
                height=340, margin=dict(t=14, b=60, l=8, r=50),
                showlegend=True,
                legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
                yaxis=dict(title="% cartera", showgrid=True, gridcolor=GRID, zeroline=False),
                yaxis2=dict(title="Loss ratio (%)", overlaying="y", side="right",
                            showgrid=False, zeroline=False, range=[50, 130]),
                xaxis=dict(showgrid=False, zeroline=False, linecolor=S_BORDER, tickfont=dict(size=9)),
            )
            st.markdown('<div class="chart-label">Distribución cartera por score de riesgo</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_dist, use_container_width=True)

        callout(
            "<strong>Señales de selección adversa en Sanitas:</strong> el loss ratio de nuevos asegurados "
            "(94%) casi triplica al de veteranos (71%), el doble del gap sectorial (9 pp vs 5 pp). "
            "El segmento Senior 60+ concentra el 41% de urgencias evitables — revisar modelo de tarificación. "
            "El 22% de la cartera presenta score >60 (alto riesgo actuarial), con loss ratio medio del 91%, "
            "por encima del umbral de rentabilidad. <strong>Acción prioritaria:</strong> implementar scoring "
            "predictivo en contratación y activar carencias dinámicas para perfiles de alto riesgo."
        )

# ══════════════════════════════════════════════════════════════════
# PÁGINA: HOSPITALES
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "hospitales":

    if st.button("← Inicio", key="back_hosp"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("HOSPITALES Y CENTROS MÉDICOS")

    df_hosp = dd["hospitales"].copy()
    if marca_hosp_sel != "Todas":
        df_hosp = df_hosp[df_hosp["marca"].isin(["Sanitas", marca_hosp_sel])]

    t1, t2, t3 = st.tabs(["Valoraciones", "Especialidades", "Precios"])

    # ── Valoraciones ─────────────────────────────────────────────
    with t1:
        df_val = dd["valoraciones"]

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Rating Sanitas Hospitales", "4.14", "HM lidera con 4.36", negative=True)
        kpi_card(k2, "Espera media urgencias", "22 min", "HM: 15 min", negative=True)
        kpi_card(k3, "Exp. digital (1–5)", "4.4", "Mejor del sector")
        kpi_card(k4, "Centros propios", "7", "Quirónsalud: 9")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            dims   = ["trato_personal","instalaciones","digital_exp","precio_percibido"]
            labels = ["Trato personal","Instalaciones","Experiencia digital","Precio percibido"]
            fig_r = go.Figure()
            for _, row in df_val.iterrows():
                c = COMP_C.get(row["marca"], S_MUTED)
                r,g,b = int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
                fig_r.add_trace(go.Scatterpolar(
                    r=[row[d] for d in dims] + [row[dims[0]]],
                    theta=labels + [labels[0]],
                    name=row["marca"],
                    fill="toself",
                    line=dict(color=c, width=2),
                    fillcolor=f"rgba({r},{g},{b},0.06)",
                ))
            fig_r.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,5], tickfont=dict(size=9),
                                   gridcolor=GRID, linecolor=GRID),
                    angularaxis=dict(tickfont=dict(size=9, family="Inter"), gridcolor=GRID),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11, color=FONT),
                showlegend=True,
                legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
                margin=dict(t=20, b=80, l=60, r=60), height=380,
            )
            st.markdown('<div class="chart-label">Percepción del paciente</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_r, use_container_width=True)

        with c2:
            df_vs = df_val.sort_values("rating_medio", ascending=True)
            fig_rt = go.Figure(go.Bar(
                y=df_vs["marca"], x=df_vs["rating_medio"],
                orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_vs["marca"]],
                marker_line_width=0,
                text=[f"{v:.2f}★" for v in df_vs["rating_medio"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_rt.update_layout(**lay(h=220, margin=dict(t=10, b=10, l=8, r=50)))
            fig_rt.update_xaxes(range=[3.5, 4.8], showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Rating medio Google Maps</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_rt, use_container_width=True)

            df_te = df_val.sort_values("tiempo_espera_min")
            fig_te = go.Figure(go.Bar(
                y=df_te["marca"], x=df_te["tiempo_espera_min"],
                orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_te["marca"]],
                marker_line_width=0,
                text=[f"{v} min" for v in df_te["tiempo_espera_min"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_te.update_layout(**lay(h=200, margin=dict(t=10, b=10, l=8, r=60)))
            fig_te.update_xaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Tiempo espera urgencias (minutos)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_te, use_container_width=True)

        callout(
            "HM Hospitales lidera en rating (4.36) e instalaciones. Sanitas puntúa mejor "
            "en experiencia digital (4.4) — su mayor fortaleza diferencial en hospitales. "
            "<strong>Gap principal:</strong> tiempo de espera en urgencias (22 min vs 15 de HM) "
            "y percepción de precio (3.8/5 vs 4.0 de Vithas)."
        )

    # ── Especialidades ───────────────────────────────────────────
    with t2:
        df_esp = dd["especialidades"]
        pivot = df_esp.pivot(index="marca", columns="especialidad", values="cobertura")
        fig_e = go.Figure(go.Heatmap(
            z=pivot.values,
            x=list(pivot.columns),
            y=list(pivot.index),
            colorscale=[[0,"#FEE2E2"],[0.5,"#FEF3C7"],[1,"#D1FAE5"]],
            zmin=1, zmax=3,
            text=np.where(pivot.values==3,"●●",np.where(pivot.values==2,"●○","○")),
            texttemplate="%{text}",
            textfont=dict(size=13, color=FONT),
            showscale=False,
        ))
        fig_e.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=FONT),
            height=320, margin=dict(t=10, b=10, l=8, r=8),
            xaxis=dict(tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)),
        )
        st.markdown('<div class="chart-label">Cobertura por especialidad — ●●=Completa · ●○=Parcial · ○=Sin cobertura</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_e, use_container_width=True)
        callout(
            "Quirónsalud es el único con cobertura completa en todas las especialidades. "
            "<strong>Gap Sanitas:</strong> cobertura parcial en Oncología, Neurología y Psiquiatría, "
            "especialidades con demanda creciente (+18% en 2025-26). "
            "HM Hospitales es referente en Oncología de alta complejidad."
        )

    # ── Precios ──────────────────────────────────────────────────
    with t3:
        p_tipo = st.radio("Tipo de precio:", ["Consulta especialista","Cirugía mayor (estimado)"],
                          horizontal=True)
        col_p = "precio_consulta_esp" if p_tipo == "Consulta especialista" else "precio_cirugia_mayor_est"
        df_ph = dd["hospitales"].groupby("marca")[col_p].mean().reset_index()
        df_ph.columns = ["marca","precio"]
        df_ph = df_ph.sort_values("precio", ascending=True)
        fig_ph = go.Figure(go.Bar(
            y=df_ph["marca"], x=df_ph["precio"],
            orientation="h",
            marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_ph["marca"]],
            marker_line_width=0,
            text=[f"{int(v)}€" for v in df_ph["precio"]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_ph.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=50)))
        fig_ph.update_xaxes(showgrid=True, gridcolor=GRID)
        st.markdown(f'<div class="chart-label">{p_tipo} — precio medio estimado por cadena</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_ph, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PÁGINA: COMUNICACIÓN
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "comunicacion":

    if st.button("← Inicio", key="back_com"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("COMUNICACIÓN Y SHARE OF VOICE")

    ct1, ct2, ct3 = st.tabs(["RRSS & Competencia", "Google Trends", "Influencers & Deportistas"])

    # ── RRSS & Competencia ────────────────────────────────────────
    with ct1:
        df_rr = dd["redes"]
        df_ig = df_rr[df_rr["red"]=="Instagram"].sort_values("seguidores", ascending=False)

        c1, c2 = st.columns(2)
        with c1:
            fig_ig = go.Figure(go.Bar(
                x=df_ig["marca"], y=df_ig["seguidores"]/1000,
                marker_color=[COMP_C.get(m, S_MUTED) for m in df_ig["marca"]],
                marker_line_width=0,
                text=[f"{int(v)}K" for v in df_ig["seguidores"]/1000],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_ig.update_layout(**lay(h=300, margin=dict(t=10, b=50, l=8, r=8)))
            fig_ig.update_xaxes(tickangle=-25)
            fig_ig.update_yaxes(showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Seguidores Instagram (miles)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_ig, use_container_width=True)

        with c2:
            fig_eng = go.Figure()
            for _, row in df_ig.iterrows():
                fig_eng.add_trace(go.Scatter(
                    x=[row["seguidores"]/1000],
                    y=[row["engagement_pct"]],
                    mode="markers+text",
                    marker=dict(size=14, color=COMP_C.get(row["marca"], S_MUTED),
                                line=dict(color=PAPER, width=2)),
                    text=[row["marca"]],
                    textposition="top center",
                    textfont=dict(size=9, color=FONT),
                    name=row["marca"],
                    showlegend=False,
                ))
            fig_eng.add_vline(x=df_ig["seguidores"].mean()/1000,
                              line_dash="dot", line_color=S_BORDER,
                              annotation_text="media", annotation_font_size=9)
            fig_eng.add_hline(y=df_ig["engagement_pct"].mean(),
                              line_dash="dot", line_color=S_BORDER)
            fig_eng.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=8)))
            fig_eng.update_xaxes(title_text="Seguidores (K)", showgrid=True, gridcolor=GRID)
            fig_eng.update_yaxes(title_text="Engagement %", showgrid=True, gridcolor=GRID)
            st.markdown('<div class="chart-label">Seguidores vs Engagement — Instagram</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_eng, use_container_width=True)

        callout(
            "Sanitas tiene 185K seguidores vs 95K de DKV, pero DKV genera <strong>4× más engagement</strong> "
            "(3.8% vs 0.9%). En Google Trends, 'seguro salud privado' pica en septiembre y enero — "
            "los dos momentos de máxima intención de compra. Sanitas pierde 4 puntos de índice "
            "en esos momentos frente a 2025."
        )

    # ── Google Trends ──────────────────────────────────────────────
    with ct2:
        df_tr = dd["trends"].copy()
        df_tr["semana"] = pd.to_datetime(df_tr["semana"])
        term_opts = [c for c in df_tr.columns if c != "semana"]
        terms_sel = st.multiselect("Términos:", term_opts,
                                   default=["Sanitas","Adeslas","DKV","seguro salud privado"])
        if terms_sel:
            fig_tr = go.Figure()
            t_colors = {"Sanitas":ACCENT,"Adeslas":"#B71C1C","DKV":"#E65100",
                        "Asisa":"#2E7D32","seguro salud privado":A3,"seguro médico precio":"#6B7280"}
            for t in terms_sel:
                fig_tr.add_trace(go.Scatter(
                    x=df_tr["semana"], y=df_tr[t], name=t, mode="lines",
                    line=dict(color=t_colors.get(t, S_MUTED), width=2),
                ))
            fig_tr.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="h", y=-0.22, font=dict(size=10)),
                margin=dict(t=10, b=70, l=8, r=8)))
            fig_tr.update_yaxes(range=[0,100], showgrid=True, gridcolor=GRID)
            fig_tr.update_xaxes(showgrid=False)
            st.plotly_chart(fig_tr, use_container_width=True)

    # ── Influencers & Deportistas ──────────────────────────────────
    with ct3:
        # datos de los 21 perfiles
        _INF_RAW = [
            {"name":"Dr. Mario Alonso Puig",   "handle":"@marioalonsopuig",       "cat":"Médico / Salud",        "seg":210000,   "eng":5.1,  "aqs":92,"afin":5.0,"audEsp":90,"aud3055":70,"conflict":False,"tier":"Mid-Macro","reelMin":3500, "reelMax":5500, "target":"Senior 40-65 / Preventivo",      "nota":"Cirujano y conferenciante en salud mental y bienestar. Sin polémicas. Audiencia muy cualificada."},
            {"name":"Miguel Ángel Lurueña",     "handle":"@gominolaspetrole",       "cat":"Nutrición / Prevención","seg":260000,   "eng":6.2,  "aqs":88,"afin":5.0,"audEsp":95,"aud3055":55,"conflict":False,"tier":"Mid-Macro","reelMin":3000, "reelMax":5000, "target":"Familiar / 25-50",                "nota":"'Gominolas de Petróleo'. Nutricionista viral. El engagement más alto de la lista."},
            {"name":"Rut Andrés",               "handle":"@rutandres",              "cat":"Médico / Salud",        "seg":185000,   "eng":5.8,  "aqs":86,"afin":5.0,"audEsp":95,"aud3055":55,"conflict":False,"tier":"Mid-Macro","reelMin":2500, "reelMax":4500, "target":"Familiar / 30-50",                "nota":"Fisioterapeuta divulgadora. Alineación directa con cuadro médico Sanitas."},
            {"name":"Xevi Verdaguer",           "handle":"@xeviverdaguer",          "cat":"Nutrición / Prevención","seg":360000,   "eng":4.9,  "aqs":84,"afin":5.0,"audEsp":90,"aud3055":60,"conflict":False,"tier":"Mid-Macro","reelMin":3500, "reelMax":6000, "target":"Preventivo / 30-55",              "nota":"Nutricionista funcional pionero en microbiota. Eje prevención-salud muy alineado."},
            {"name":"Boticaria García",         "handle":"@boticaria_garcia",       "cat":"Médico / Salud",        "seg":710000,   "eng":4.1,  "aqs":88,"afin":5.0,"audEsp":95,"aud3055":55,"conflict":False,"tier":"Macro",    "reelMin":5500, "reelMax":8000, "target":"Familiar / 30-55 / mixto",       "nota":"Farmacéutica. La voz más conocida de divulgación sanitaria en España."},
            {"name":"Carolina Marín",           "handle":"@carolinamarinbadminton", "cat":"Deportista Élite",      "seg":610000,   "eng":4.5,  "aqs":85,"afin":4.0,"audEsp":89,"aud3055":44,"conflict":False,"tier":"Macro",    "reelMin":5000, "reelMax":9000, "target":"Joven activo / 20-40",           "nota":"Campeona olímpica bádminton. Narrativa de superación ante lesión = salud perfecta."},
            {"name":"Ona Carbonell",            "handle":"@onacarbonell",           "cat":"Deportista Élite",      "seg":255000,   "eng":4.7,  "aqs":82,"afin":4.0,"audEsp":86,"aud3055":45,"conflict":False,"tier":"Mid-Macro","reelMin":3000, "reelMax":5500, "target":"Femenino / 25-45",               "nota":"Medallista olímpica, madre y deportista. Imagen positiva sin polémicas."},
            {"name":"Gemma Triay",              "handle":"@gemmatriay",             "cat":"Deportista Élite",      "seg":365000,   "eng":5.5,  "aqs":82,"afin":3.5,"audEsp":87,"aud3055":44,"conflict":False,"tier":"Mid-Macro","reelMin":3000, "reelMax":6000, "target":"Activo / 25-45 / pádel",         "nota":"Número 1 mundial de pádel. El deporte de mayor crecimiento en España."},
            {"name":"Pau Gasol",                "handle":"@paugasol",               "cat":"Deportista Élite",      "seg":455000,   "eng":3.5,  "aqs":91,"afin":4.5,"audEsp":70,"aud3055":62,"conflict":False,"tier":"Macro",    "reelMin":8000, "reelMax":15000,"target":"Senior / 35-60 / premium",      "nota":"Fundación Gasol: salud infantil. Mayor credibilidad del deporte español."},
            {"name":"Alejandro Valverde",       "handle":"@alejandrovalverde",      "cat":"Deportista Élite",      "seg":358000,   "eng":2.2,  "aqs":82,"afin":4.0,"audEsp":82,"aud3055":66,"conflict":False,"tier":"Mid-Macro","reelMin":3000, "reelMax":6000, "target":"Masculino / 35-60 / activo",     "nota":"40 años en activo. Narrativa de longevidad atlética perfecta para Sanitas."},
            {"name":"Anne Igartiburu",          "handle":"@anneigartiburu",         "cat":"Lifestyle / Familia",   "seg":460000,   "eng":2.6,  "aqs":78,"afin":3.0,"audEsp":92,"aud3055":70,"conflict":False,"tier":"Macro",    "reelMin":5000, "reelMax":8000, "target":"Familia / 40-65",                "nota":"Presentadora con audiencia senior fiel. Alta penetración en comprador de seguro familiar."},
            {"name":"Jesús Calleja",            "handle":"@calleja_jesus",          "cat":"Lifestyle / Familia",   "seg":820000,   "eng":1.9,  "aqs":80,"afin":3.0,"audEsp":90,"aud3055":65,"conflict":False,"tier":"Macro",    "reelMin":6000, "reelMax":10000,"target":"Activo / 35-60 / masculino",    "nota":"Aventurero. Estilo de vida activo y saludable. Audiencia masculina de mediana edad."},
            {"name":"Amaia Salamanca",          "handle":"@amaiasalamancaof",       "cat":"Lifestyle / Familia",   "seg":1230000,  "eng":2.5,  "aqs":80,"afin":2.0,"audEsp":85,"aud3055":52,"conflict":False,"tier":"Mega",     "reelMin":10000,"reelMax":18000,"target":"Familiar / 30-50 / femenino",   "nota":"Actriz y madre. Ideal para campaña de seguro familiar."},
            {"name":"Jon Rahm",                 "handle":"@jonrahm",                "cat":"Deportista Élite",      "seg":368000,   "eng":2.8,  "aqs":85,"afin":2.5,"audEsp":62,"aud3055":54,"conflict":False,"tier":"Mid-Macro","reelMin":5000, "reelMax":9000, "target":"Premium / 35-55 / masculino",   "nota":"Número 1 mundial golf. Perfil premium para Sanitas Hospitales + cobertura internacional."},
            {"name":"Vikika Costa",             "handle":"@vikika_costa",           "cat":"Fitness / Bienestar",   "seg":1600000,  "eng":1.63, "aqs":73,"afin":3.5,"audEsp":75,"aud3055":45,"conflict":False,"tier":"Mega",     "reelMin":8000, "reelMax":15000,"target":"Joven activo / 25-40",          "nota":"Fitness y nutrición. Gran alcance para segmento joven-activo preventivo."},
            {"name":"Patry Jordán",             "handle":"@patryjordan",            "cat":"Fitness / Bienestar",   "seg":1360000,  "eng":0.45, "aqs":84,"afin":3.5,"audEsp":80,"aud3055":48,"conflict":False,"tier":"Mega",     "reelMin":8000, "reelMax":15000,"target":"Femenino / 25-45 / activo",     "nota":"Fitness YouTube. Engagement IG muy bajo (0.45%). Mejor en formato vídeo/YouTube."},
            {"name":"Carles Puyol",             "handle":"@carlespuyol",            "cat":"Deportista Élite",      "seg":2500000,  "eng":2.0,  "aqs":84,"afin":3.0,"audEsp":58,"aud3055":65,"conflict":False,"tier":"Mega",     "reelMin":15000,"reelMax":25000,"target":"Masculino / 40-60 / familiar",  "nota":"Exfutbolista Barça. Audiencia muy internacional: limita efectividad España."},
            {"name":"Garbiñe Muguruza",         "handle":"@garbinemuguruza",        "cat":"Deportista Élite",      "seg":1520000,  "eng":2.4,  "aqs":83,"afin":3.0,"audEsp":52,"aud3055":44,"conflict":False,"tier":"Mega",     "reelMin":10000,"reelMax":20000,"target":"Femenino / 25-45",              "nota":"Histórico Sanitas WTA. 52% audiencia española. Reactivar si hay campaña internacional."},
            {"name":"Nuria Roca",               "handle":"@nuriarocagranell",       "cat":"Lifestyle / Familia",   "seg":948000,   "eng":0.55, "aqs":72,"afin":2.5,"audEsp":88,"aud3055":58,"conflict":False,"tier":"Macro",    "reelMin":7000, "reelMax":12000,"target":"Familiar / 40-60",              "nota":"Presentadora TV. Engagement bajo (0.55%). Mejor en TV o podcast que en RRSS."},
            {"name":"Blanca Suárez",            "handle":"@blancasuarez_",          "cat":"Lifestyle / Familia",   "seg":4500000,  "eng":1.1,  "aqs":78,"afin":2.0,"audEsp":80,"aud3055":42,"conflict":False,"tier":"Mega",     "reelMin":20000,"reelMax":35000,"target":"Femenino / 25-45",              "nota":"Gran alcance. Poca afinidad salud. Solo para brand awareness masivo."},
            {"name":"Rafa Nadal ⚠",             "handle":"@rafaelnadal",            "cat":"Deportista Élite",      "seg":12200000, "eng":0.9,  "aqs":92,"afin":3.5,"audEsp":48,"aud3055":55,"conflict":True, "tier":"Mega",     "reelMin":80000,"reelMax":150000,"target":"Global / premium",             "nota":"CONFLICTO: contratos con Mapfre y aseguradoras. Solo 48% aud. española. Inviable sin exclusividad."},
        ]

        def _inf_score(d):
            return round(
                min(d["eng"], 5)/5*15 + d["aqs"]/100*20 + d["afin"]/5*20 +
                d["audEsp"]/100*20 + (0 if d["conflict"] else 15) + d["aud3055"]/100*10, 1
            )

        _CAT_COLOR = {
            "Médico / Salud":        "#003087",
            "Nutrición / Prevención":"#6B3FAE",
            "Deportista Élite":      "#0099D6",
            "Fitness / Bienestar":   "#2A7A52",
            "Lifestyle / Familia":   "#C26A0A",
        }

        df_inf = pd.DataFrame(_INF_RAW)
        df_inf["score"] = df_inf.apply(_inf_score, axis=1)
        df_inf = df_inf.sort_values("score", ascending=False).reset_index(drop=True)
        df_inf["rank"] = df_inf.index + 1

        # ── filtros ──
        fi1, fi2, fi3 = st.columns([1.2, 1, 1])
        with fi1:
            cats_opts = ["Todas"] + sorted(df_inf["cat"].unique().tolist())
            cat_f = st.selectbox("Categoría:", cats_opts, key="inf_cat")
        with fi2:
            tier_opts = ["Todos"] + sorted(df_inf["tier"].unique().tolist())
            tier_f = st.selectbox("Tier:", tier_opts, key="inf_tier")
        with fi3:
            conf_f = st.radio("Conflicto:", ["Todos", "Sin conflicto"], horizontal=True, key="inf_conf")

        df_show = df_inf.copy()
        if cat_f != "Todas":
            df_show = df_show[df_show["cat"] == cat_f]
        if tier_f != "Todos":
            df_show = df_show[df_show["tier"] == tier_f]
        if conf_f == "Sin conflicto":
            df_show = df_show[~df_show["conflict"]]

        # ── pills de pesos ──
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px;padding:12px 16px;'
            f'background:{S_LIGHT};border-radius:8px;border:1px solid {S_BORDER}">'
            f'<span style="font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;'
            f'color:{S_MUTED};align-self:center;margin-right:4px">Pesos Score:</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">20%</b> AQS/Credibilidad</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">20%</b> Afinidad salud (0-5)</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">20%</b> Aud. España</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">15%</b> Engagement (cap 5%)</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">15%</b> Sin conflicto</span>'
            f'<span style="font-size:.72rem;padding:3px 9px;background:{PAPER};border:1px solid {S_BORDER};border-radius:12px">'
            f'<b style="color:{ACCENT}">10%</b> Aud. 30-55a</span>'
            f'</div>',
            unsafe_allow_html=True)

        # ── tabla HTML ──
        th_style = (f'padding:9px 12px;text-align:left;font-size:.6rem;font-weight:700;'
                    f'letter-spacing:.08em;text-transform:uppercase;color:{S_MUTED};'
                    f'background:{S_LIGHT};border-bottom:1px solid {S_BORDER};white-space:nowrap')
        td_style = f'padding:9px 12px;vertical-align:middle;border-bottom:1px solid {S_BORDER}'

        tbl = (f'<div style="overflow-x:auto;border-radius:8px;border:1px solid {S_BORDER};'
               f'box-shadow:0 1px 6px rgba(0,48,135,.05)">'
               f'<table style="width:100%;border-collapse:collapse;font-size:12.5px">'
               f'<thead><tr>'
               f'<th style="{th_style}">#</th>'
               f'<th style="{th_style}">Categoría</th>'
               f'<th style="{th_style}">Perfil</th>'
               f'<th style="{th_style};text-align:right">Seg.</th>'
               f'<th style="{th_style};text-align:right">Eng %</th>'
               f'<th style="{th_style};text-align:right">AQS</th>'
               f'<th style="{th_style};text-align:right">Afinidad</th>'
               f'<th style="{th_style};text-align:right">Aud. ESP</th>'
               f'<th style="{th_style};text-align:right">Aud. 30-55a</th>'
               f'<th style="{th_style};text-align:center">Conf.</th>'
               f'<th style="{th_style}">Score</th>'
               f'<th style="{th_style}">Tier</th>'
               f'<th style="{th_style};text-align:right">Reel est.</th>'
               f'<th style="{th_style}">Target</th>'
               f'<th style="{th_style}">Nota</th>'
               f'</tr></thead><tbody>')

        _TIER_BG  = {"Mega":"#E8F0FE","Macro":"#E0F3FE","Mid-Macro":"#E8F5EE"}
        _TIER_CLR = {"Mega":ACCENT,"Macro":A2,"Mid-Macro":"#2A7A52"}

        for _, row in df_show.iterrows():
            cat_c = _CAT_COLOR.get(row["cat"], S_MUTED)
            s = row["score"]
            bar_c = ACCENT if s >= 85 else A2 if s >= 70 else A3 if s >= 60 else S_MUTED
            seg_v = f'{row["seg"]/1e6:.1f}M' if row["seg"] >= 1e6 else f'{int(row["seg"]/1000)}K'
            reel  = f'{int(row["reelMin"]/1000)}K – {int(row["reelMax"]/1000)}K €'
            conf_html = (
                f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                f'width:18px;height:18px;border-radius:50%;background:#FEF0C7;color:#92400E;font-size:10px">⚠</span>'
                if row["conflict"] else
                f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                f'width:18px;height:18px;border-radius:50%;background:#E8F5EE;color:#2A7A52;font-size:10px">✓</span>'
            )
            tier_bg  = _TIER_BG.get(row["tier"], S_LIGHT)
            tier_clr = _TIER_CLR.get(row["tier"], S_MUTED)
            row_bg = "#FFFFFF" if int(row["rank"]) % 2 == 0 else PAPER

            tbl += (
                f'<tr style="background:{row_bg};border-left:3px solid {cat_c}">'
                f'<td style="{td_style};text-align:center;font-weight:700;color:{S_MUTED};font-size:11px">{int(row["rank"])}</td>'
                f'<td style="{td_style}">'
                f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:500;white-space:nowrap">'
                f'<span style="width:7px;height:7px;border-radius:50%;background:{cat_c};flex-shrink:0;display:inline-block"></span>'
                f'{row["cat"]}</span></td>'
                f'<td style="{td_style};min-width:160px">'
                f'<span style="font-weight:600;font-size:13px;display:block">{row["name"]}</span>'
                f'<span style="font-size:10.5px;color:{S_MUTED}">{row["handle"]}</span></td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{seg_v}</td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{row["eng"]:.2f}%</td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{row["aqs"]}</td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{row["afin"]:.1f}/5</td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{row["audEsp"]}%</td>'
                f'<td style="{td_style};text-align:right;font-variant-numeric:tabular-nums">{row["aud3055"]}%</td>'
                f'<td style="{td_style};text-align:center">{conf_html}</td>'
                f'<td style="{td_style};min-width:80px">'
                f'<span style="font-size:15px;font-weight:700;font-variant-numeric:tabular-nums">{s:.1f}</span>'
                f'<div style="height:3px;background:{S_BORDER};border-radius:2px;margin-top:4px;overflow:hidden">'
                f'<div style="height:100%;width:{s}%;background:{bar_c};border-radius:2px"></div></div></td>'
                f'<td style="{td_style}">'
                f'<span style="display:inline-block;padding:2px 7px;border-radius:3px;font-size:10px;font-weight:700;'
                f'background:{tier_bg};color:{tier_clr};white-space:nowrap">{row["tier"]}</span></td>'
                f'<td style="{td_style};text-align:right;white-space:nowrap;font-size:12px">{reel}</td>'
                f'<td style="{td_style};font-size:11px;color:{S_MUTED};white-space:nowrap">{row["target"]}</td>'
                f'<td style="{td_style};min-width:200px;max-width:260px;font-size:11.5px;color:{S_MUTED};line-height:1.5">{row["nota"]}</td>'
                f'</tr>'
            )

        tbl += '</tbody></table></div>'
        st.markdown(tbl, unsafe_allow_html=True)

        st.markdown(
            f'<p style="font-size:.68rem;color:{S_MUTED};margin-top:10px;line-height:1.7">'
            f'Datos estimados orientativos (HypeAuditor / Kolsquare / fuentes abiertas). Septiembre 2026. · '
            f'Score = 20% AQS + 20% Afinidad salud + 20% Aud. España + 15% Engagement (cap 5%) + 15% Sin conflicto + 10% Aud. 30-55a. · '
            f'Reel estimado: rangos de mercado España 2026 (Collabios / Influee). Tarifa real fijada por agencia del creador. · '
            f'Conflicto = contrato vigente con aseguradora competidora (Adeslas, DKV, Asisa, Mapfre Salud, AXA Salud).'
            f'</p>',
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PÁGINA: POSICIONAMIENTO
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "posicionamiento":

    if st.button("← Inicio", key="back_pos"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("POSICIONAMIENTO Y BUYER PERSONAS")

    df_enc = dd["encuesta"]

    c1, c2 = st.columns(2)
    with c1:
        tm = df_enc["top_of_mind"].value_counts().reset_index()
        tm.columns = ["marca","n"]
        tm["pct"] = (tm["n"]/len(df_enc)*100).round(1)
        tm = tm.sort_values("pct", ascending=True)
        fig_tm = go.Figure(go.Bar(
            y=tm["marca"], x=tm["pct"], orientation="h",
            marker_color=[COMP_C.get(m, S_MUTED) for m in tm["marca"]],
            marker_line_width=0,
            text=[f"{v}%" for v in tm["pct"]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_tm.update_layout(**lay(h=280, margin=dict(t=10, b=10, l=8, r=40)))
        fig_tm.update_xaxes(showgrid=True, gridcolor=GRID)
        st.markdown('<div class="chart-label">Top of Mind — primera marca que recuerdan</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_tm, use_container_width=True)

    with c2:
        can = df_enc["canal_contratacion"].value_counts().reset_index()
        can.columns = ["canal","n"]
        can["pct"] = (can["n"]/len(df_enc)*100).round(1)
        fig_can = go.Figure(go.Bar(
            x=can["canal"], y=can["pct"],
            marker_color=[ACCENT, A2, A3, "#90B8DE", S_BORDER],
            marker_line_width=0,
            text=[f"{v}%" for v in can["pct"]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_can.update_layout(**lay(h=280, margin=dict(t=10, b=60, l=8, r=8)))
        fig_can.update_xaxes(tickangle=-15)
        fig_can.update_yaxes(showgrid=True, gridcolor=GRID)
        st.markdown('<div class="chart-label">Canal de contratación del seguro</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_can, use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("BUYER PERSONAS")

    df_bp = dd["personas"]
    p_icons = {"Familiar Tradicional":"◈","Ejecutivo Exigente":"◉",
               "Joven Saludable":"◆","Senior Dependiente":"◇","Preventivo Digital":"◎"}

    cols_p = st.columns(len(df_bp))
    for i, (_, row) in enumerate(df_bp.iterrows()):
        with cols_p[i]:
            gap_color = "#B71C1C" if row["gap_sanitas_pct"] > 20 else "#E65100" if row["gap_sanitas_pct"] > 15 else ACCENT
            cols_p[i].markdown(
                f'<div class="kpi-card" style="min-height:220px">'
                f'<div style="font-size:1.2rem;color:{ACCENT};margin-bottom:8px">{p_icons.get(row["persona"],"○")}</div>'
                f'<div class="kpi-label">{row["persona"]}</div>'
                f'<div class="kpi-value" style="font-size:1.6rem">{row["pct_muestra"]}%</div>'
                f'<div style="font-size:.7rem;color:{S_MUTED};margin-top:8px;line-height:1.7">'
                f'Edad media: {row["edad_media"]} años<br>'
                f'Ticket anual: {row["ticket_medio_anual"]:,}€<br>'
                f'Marca top: <strong>{row["marca_top"]}</strong>'
                f'</div>'
                f'<div style="margin-top:10px;font-size:.65rem;font-weight:700;'
                f'color:{gap_color};letter-spacing:.04em">'
                f'Gap Sanitas: {row["gap_sanitas_pct"]} pp</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dims_p   = ["digital_score","precio_sensibilidad","fidelidad"]
        labels_p = ["Afinidad digital","Sensibilidad precio","Fidelidad marca"]
        fig_rp = go.Figure()
        p_colors = [ACCENT, A2, A3, "#90B8DE", S_MUTED]
        for i, (_, row) in enumerate(df_bp.iterrows()):
            c = p_colors[i]
            r,g,b = int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)
            fig_rp.add_trace(go.Scatterpolar(
                r=[row[d] for d in dims_p] + [row[dims_p[0]]],
                theta=labels_p + [labels_p[0]],
                name=row["persona"], fill="toself",
                line=dict(color=c, width=2),
                fillcolor=f"rgba({r},{g},{b},0.07)",
            ))
        fig_rp.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,5], tickfont=dict(size=8),
                               gridcolor=GRID, linecolor=GRID),
                angularaxis=dict(tickfont=dict(size=9, family="Inter"), gridcolor=GRID),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            showlegend=True,
            legend=dict(orientation="h", y=-0.20, font=dict(size=9)),
            margin=dict(t=20, b=90, l=60, r=60), height=360,
        )
        st.markdown('<div class="chart-label">Perfil por dimensión (1–5)</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_rp, use_container_width=True)

    with c2:
        df_g = df_bp.sort_values("gap_sanitas_pct", ascending=True)
        colors_g = [
            "#B71C1C" if v > 20 else "#E65100" if v > 15 else ACCENT
            for v in df_g["gap_sanitas_pct"]
        ]
        fig_g = go.Figure(go.Bar(
            y=df_g["persona"], x=df_g["gap_sanitas_pct"],
            orientation="h",
            marker_color=colors_g, marker_line_width=0,
            text=[f"{v} pp" for v in df_g["gap_sanitas_pct"]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_g.update_layout(**lay(h=300, margin=dict(t=10, b=10, l=8, r=50)))
        fig_g.update_xaxes(showgrid=True, gridcolor=GRID)
        st.markdown('<div class="chart-label">Gap de captación Sanitas por persona</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_g, use_container_width=True)

    callout(
        "El mayor gap de captación se da en <strong>Preventivo Digital</strong> (29 pp) y "
        "<strong>Joven Saludable</strong> (24 pp) — ambos con DKV como marca top. "
        "Son los perfiles con mayor valor a largo plazo: alta afinidad digital, "
        "contrato recurrente y potencial de upscelling a pólizas superiores con la edad."
    )

# ══════════════════════════════════════════════════════════════════
# PÁGINA: MAPA ESTRATÉGICO
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "mapa":

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("MAPA ESTRATÉGICO")

    df_centros = pd.DataFrame(dd["centros"])

    with st.sidebar:
        st.markdown(
            f'<div style="padding:16px 0 14px;font-size:.72rem;letter-spacing:.12em;'
            f'text-transform:uppercase;font-weight:700;color:#374151">Filtros mapa</div>',
            unsafe_allow_html=True)
        marcas_m = sorted(df_centros["marca"].unique().tolist())
        m_sel = st.multiselect("Cadena:", marcas_m, default=marcas_m)
        tipos_m = sorted(df_centros["tipo"].unique().tolist())
        t_sel = st.multiselect("Tipo de centro:", tipos_m, default=tipos_m)
        if st.button("← Inicio", key="back_mapa_side"):
            go_to("home"); st.rerun()

    # ── datos CCAA simulados ──────────────────────────────────────
    CCAA_GEO = {
        "Madrid":           {"lat":40.42,"lon":-3.70},
        "Cataluña":         {"lat":41.39,"lon":2.16},
        "Andalucía":        {"lat":37.38,"lon":-5.97},
        "C. Valenciana":    {"lat":39.47,"lon":-0.38},
        "País Vasco":       {"lat":43.26,"lon":-2.93},
        "Galicia":          {"lat":42.88,"lon":-8.54},
        "Castilla y León":  {"lat":41.65,"lon":-4.73},
        "Aragón":           {"lat":41.65,"lon":-0.88},
        "Murcia":           {"lat":37.99,"lon":-1.13},
        "Extremadura":      {"lat":38.92,"lon":-6.34},
        "Navarra":          {"lat":42.82,"lon":-1.64},
        "Cantabria":        {"lat":43.18,"lon":-3.99},
        "La Rioja":         {"lat":42.27,"lon":-2.37},
        "Canarias":         {"lat":28.29,"lon":-15.65},
        "Baleares":         {"lat":39.57,"lon":2.65},
        "Asturias":         {"lat":43.36,"lon":-5.85},
        "C.-La Mancha":     {"lat":39.86,"lon":-4.03},
    }
    np.random.seed(42)
    ccaa_names = list(CCAA_GEO.keys())

    df_ccaa = pd.DataFrame({
        "ccaa":            ccaa_names,
        "lat":             [CCAA_GEO[c]["lat"] for c in ccaa_names],
        "lon":             [CCAA_GEO[c]["lon"] for c in ccaa_names],
        "renta_media":     [32400,28900,19800,22100,31200,20400,19300,24100,19700,15800,29800,22600,23100,20900,27400,20100,18700],
        "indice_renta":    [148,132, 90, 101,143, 93, 88, 110, 90, 72, 136,103,105, 95, 125, 92, 85],
        "turistas_M":      [6.2,15.8,11.4,8.7,2.1,3.9,2.0,3.2,1.9,0.7,1.4,1.2,0.5,13.2,12.9,1.6,1.8],
        "temp_media_C":    [14.8,15.9,18.9,17.4,13.2,13.8,12.5,14.7,18.3,16.4,12.9,14.1,13.5,22.1,19.6,13.9,15.2],
        "enf_cardio_100k": [198,185,227,210,172,235,248,219,225,261,182,229,215,204,189,241,238],
        "enf_resp_100k":   [142,138,165,155,128,168,175,148,162,181,136,159,145,127,132,170,169],
        "enf_oncol_100k":  [315,298,342,320,285,358,371,332,338,385,290,349,328,302,310,362,367],
        "pct_seg_privado": [28.4,21.6,14.2,17.9,24.8,12.1,10.8,15.3,14.7, 9.2,22.4,13.8,16.1,15.4,23.7,11.9,11.2],
        "indice_consumo":  [152,128, 87, 98,138, 89, 82, 104, 88, 69, 131, 99, 101, 92, 122, 88, 81],
        "potencial_mkt":   [145,126, 84, 96,140, 85, 80, 101, 85, 66, 133, 96,  98, 93, 124, 86, 79],
    })

    # municipios sin acceso (<15 km) — simulado
    np.random.seed(7)
    mun_sin_acceso = pd.DataFrame({
        "municipio": [
            "Puebla de Sanabria","Alcañiz","Llerena","Baza","Mula","Reinosa","Ronda",
            "Huéscar","Tárrega","Talavera la Real","Molina de Aragón","Tremp","Boltaña",
            "Vitigudino","Olivenza","Cuéllar","Morella","Albarracín","Sepúlveda","El Burgo de Osma",
        ],
        "lat": [42.07,41.05,38.24,37.49,37.99,43.00,36.74,37.81,41.65,38.88,40.84,42.17,42.41,40.81,38.68,41.40,40.62,40.41,41.29,41.59],
        "lon": [-6.77,-0.13,-5.59,-2.77,-1.49,-4.13,-5.17,-2.54,1.10,-6.89,-1.89, 0.89, 0.05,-6.44,-7.09,-4.32,-0.10,-1.44,-3.74,-3.07],
        "poblacion": [1320,16800,5900,20100,17300,10200,34800,7600,16400,8700,3100,2900,1100,4200,12200,9400,2800,1100,1200,5600],
        "dist_min_km": [28,19,22,18,16,17,32,24,19,21,35,27,31,26,18,17,29,38,22,19],
        "ccaa": ["Castilla y León","Aragón","Extremadura","Andalucía","Murcia","Cantabria","Andalucía",
                 "Andalucía","Cataluña","Extremadura","C.-La Mancha","Cataluña","Aragón",
                 "Castilla y León","Extremadura","Castilla y León","C. Valenciana","Aragón",
                 "Castilla y León","Castilla y León"],
    })
    mun_sin_acceso["_sz"] = (mun_sin_acceso["poblacion"] / 1000).clip(2, 20)

    # ── Tabs del mapa ─────────────────────────────────────────────
    mt1, mt2, mt3, mt4, mt5, mt6, mt7 = st.tabs([
        "Red de centros",
        "Nivel de renta",
        "Turismo & temperatura",
        "Enfermedades registradas",
        "Penetración seguro privado",
        "Índices comerciales",
        "Municipios sin acceso",
    ])

    # ────────────────────────────────────────────────────────
    # TAB 1 — Red de centros
    # ────────────────────────────────────────────────────────
    with mt1:
        df_m = df_centros[
            df_centros["marca"].isin(m_sel) &
            df_centros["tipo"].isin(t_sel)
        ].copy()
        df_m["_sz"] = df_m["tipo"].map({
            "Hospital propio":16, "Clínica propia":10, "Centro cuadro médico":7
        }).fillna(7)

        fig_map = px.scatter_mapbox(
            df_m, lat="lat", lon="lon",
            color="marca", color_discrete_map=COMP_C,
            hover_name="nombre",
            hover_data={"ciudad":True,"tipo":True,"especialidades":True,"rating":True,
                        "lat":False,"lon":False,"_sz":False},
            size="_sz", size_max=16,
            zoom=5.2, center={"lat":40.2,"lon":-3.5},
            height=520,
        )
        fig_map.update_layout(
            mapbox_style="open-street-map",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            legend=dict(orientation="h", y=-0.07, font=dict(size=10)),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_map, use_container_width=True,
                        config={"scrollZoom": True, "displayModeBar": True})

        m1c, m2c, m3c, m4c = st.columns(4)
        kpi_card(m1c, "Centros visibles", str(len(df_m)))
        kpi_card(m2c, "Hospitales propios", str(len(df_m[df_m["tipo"]=="Hospital propio"])))
        kpi_card(m3c, "Clínicas propias",   str(len(df_m[df_m["tipo"]=="Clínica propia"])))
        kpi_card(m4c, "Cuadro médico concertado", str(len(df_m[df_m["tipo"]=="Centro cuadro médico"])))
        callout(
            "Puntos grandes = hospitales propios · Puntos medianos = clínicas propias · "
            "Puntos pequeños = centros cuadro médico concertado. "
            "<strong>Zonas blancas Sanitas:</strong> Galicia, Aragón, Canarias y Extremadura "
            "sin infraestructura hospitalaria propia. Quirónsalud cubre A Coruña y Zaragoza. "
            "El mapa es interactuable: arrastra, haz zoom con la rueda del ratón y haz clic en cualquier punto."
        )

    # ────────────────────────────────────────────────────────
    # TAB 2 — Nivel de renta
    # ────────────────────────────────────────────────────────
    with mt2:
        fig_renta = px.scatter_mapbox(
            df_ccaa, lat="lat", lon="lon",
            color="renta_media",
            color_continuous_scale=[[0,"#EEF4FF"],[0.5,"#0057A8"],[1,"#001A5C"]],
            size="renta_media", size_max=40,
            hover_name="ccaa",
            hover_data={"renta_media":True,"indice_renta":True,"lat":False,"lon":False},
            zoom=4.8, center={"lat":40.2,"lon":-3.5},
            height=480,
            labels={"renta_media":"Renta media (€/año)","indice_renta":"Índice renta (España=100)"},
        )
        fig_renta.update_layout(
            mapbox_style="open-street-map",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            coloraxis_colorbar=dict(title="€/año", tickfont=dict(size=9)),
            margin=dict(l=0,r=0,t=0,b=0),
        )
        st.plotly_chart(fig_renta, use_container_width=True,
                        config={"scrollZoom": True, "displayModeBar": True})

        c1r, c2r = st.columns(2)
        with c1r:
            st.markdown('<div class="chart-label">Renta media anual por CCAA (€)</div>',
                        unsafe_allow_html=True)
            df_rs = df_ccaa.sort_values("renta_media", ascending=True)
            fig_rbar = go.Figure(go.Bar(
                y=df_rs["ccaa"], x=df_rs["renta_media"],
                orientation="h",
                marker_color=[ACCENT if c in ["Madrid","País Vasco","Navarra","Cataluña"] else S_BORDER
                              for c in df_rs["ccaa"]],
                marker_line_width=0,
                text=[f"{int(v):,}€" for v in df_rs["renta_media"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_rbar.update_layout(**lay(h=340, margin=dict(t=10,b=10,l=8,r=60)))
            fig_rbar.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_rbar, use_container_width=True)

        with c2r:
            st.markdown('<div class="chart-label">Índice de renta (España=100) — oportunidad comercial</div>',
                        unsafe_allow_html=True)
            df_ri = df_ccaa.sort_values("indice_renta", ascending=True)
            fig_ri = go.Figure(go.Bar(
                y=df_ri["ccaa"], x=df_ri["indice_renta"],
                orientation="h",
                marker_color=[ACCENT if v >= 130 else A3 if v >= 100 else S_BORDER
                              for v in df_ri["indice_renta"]],
                marker_line_width=0,
                text=[f"{v}" for v in df_ri["indice_renta"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ri.add_vline(x=100, line_dash="dot", line_color=S_BORDER,
                             annotation_text="media España", annotation_font_size=9)
            fig_ri.update_layout(**lay(h=340, margin=dict(t=10,b=10,l=8,r=40)))
            fig_ri.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_ri, use_container_width=True)

        callout(
            "<strong>Madrid (32.400€), País Vasco (31.200€) y Navarra (29.800€)</strong> concentran "
            "el mayor poder adquisitivo. Sanitas tiene red de centros sólida en estas tres CCAA. "
            "El índice de renta marca que <strong>Extremadura (72), C.-La Mancha (85) y Galicia (93)</strong> "
            "quedan por debajo de la media española — mercados de menor potencial de seguro premium "
            "pero con alta demanda de acceso a red de cuadro médico concertado."
        )

    # ────────────────────────────────────────────────────────
    # TAB 3 — Turismo & temperatura
    # ────────────────────────────────────────────────────────
    with mt3:
        c1t, c2t = st.columns(2)
        with c1t:
            st.markdown('<div class="chart-label">Turistas internacionales (millones/año) por CCAA</div>',
                        unsafe_allow_html=True)
            fig_tur = px.scatter_mapbox(
                df_ccaa, lat="lat", lon="lon",
                color="turistas_M",
                color_continuous_scale=[[0,"#EEF4FF"],[0.5,"#0099D6"],[1,"#003087"]],
                size="turistas_M", size_max=45,
                hover_name="ccaa",
                hover_data={"turistas_M":True,"temp_media_C":True,"lat":False,"lon":False},
                zoom=4.5, center={"lat":40.2,"lon":-3.5},
                height=360,
                labels={"turistas_M":"Turistas (M)","temp_media_C":"Temp media (°C)"},
            )
            fig_tur.update_layout(
                mapbox_style="open-street-map",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11, color=FONT),
                coloraxis_colorbar=dict(title="Turistas M", tickfont=dict(size=9)),
                margin=dict(l=0,r=0,t=0,b=0),
            )
            st.plotly_chart(fig_tur, use_container_width=True,
                            config={"scrollZoom": True})

        with c2t:
            st.markdown('<div class="chart-label">Temperatura media anual (°C)</div>',
                        unsafe_allow_html=True)
            df_ts = df_ccaa.sort_values("temp_media_C", ascending=True)
            fig_temp = go.Figure(go.Bar(
                y=df_ts["ccaa"], x=df_ts["temp_media_C"],
                orientation="h",
                marker_color=[ACCENT if v >= 18 else A3 if v >= 15 else S_BORDER
                              for v in df_ts["temp_media_C"]],
                marker_line_width=0,
                text=[f"{v}°C" for v in df_ts["temp_media_C"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_temp.update_layout(**lay(h=340, margin=dict(t=10,b=10,l=8,r=50)))
            fig_temp.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_temp, use_container_width=True)

        c3t, c4t = st.columns(2)
        with c3t:
            st.markdown('<div class="chart-label">Turistas vs. temperatura media — potencial asistencia turistas</div>',
                        unsafe_allow_html=True)
            fig_sc = px.scatter(
                df_ccaa, x="temp_media_C", y="turistas_M",
                color="ccaa", text="ccaa",
                color_discrete_sequence=[ACCENT, A2, A3, "#90B8DE"] + [S_BORDER]*20,
                labels={"temp_media_C":"Temperatura media (°C)","turistas_M":"Turistas (M)"},
            )
            fig_sc.update_traces(textposition="top center", textfont=dict(size=8))
            fig_sc.update_layout(**lay(h=300, showlegend=False,
                margin=dict(t=10,b=10,l=8,r=8)))
            fig_sc.update_xaxes(showgrid=True, gridcolor=GRID)
            fig_sc.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_sc, use_container_width=True)

        with c4t:
            callout(
                "<strong>Cataluña (15.8M turistas) y Canarias (13.2M)</strong> son los principales "
                "destinos de turistas internacionales. Junto con Baleares (12.9M) y Andalucía (11.4M), "
                "estas cuatro CCAA concentran el 80% del flujo turístico. "
                "<strong>Oportunidad Sanitas:</strong> seguros de viajero y asistencia sanitaria "
                "para turistas que contratan en origen. Temperatura media ≥ 18°C correlaciona "
                "con alta demanda asistencial en traumatología (accidentes de playa, deporte extremo) "
                "y enfermedades gastrointestinales estivales. "
                "Canarias, con 22°C de media anual, representa el mayor potencial de "
                "asistencia sanitaria a turistas fuera de la temporada estival."
            )

    # ────────────────────────────────────────────────────────
    # TAB 4 — Histórico enfermedades
    # ────────────────────────────────────────────────────────
    with mt4:
        enf_tipo = st.radio(
            "Patología:",
            ["Cardiovascular", "Respiratoria", "Oncológica"],
            horizontal=True,
        )
        col_enf = {"Cardiovascular":"enf_cardio_100k","Respiratoria":"enf_resp_100k","Oncológica":"enf_oncol_100k"}[enf_tipo]
        label_enf = f"Casos registrados por 100.000 habitantes — {enf_tipo}"

        fig_enf_map = px.scatter_mapbox(
            df_ccaa, lat="lat", lon="lon",
            color=col_enf,
            color_continuous_scale=[[0,"#FEF3C7"],[0.5,"#F97316"],[1,"#7F1D1D"]],
            size=col_enf, size_max=44,
            hover_name="ccaa",
            hover_data={col_enf:True,"lat":False,"lon":False},
            zoom=4.7, center={"lat":40.2,"lon":-3.5},
            height=420,
            labels={col_enf:f"Casos/{enf_tipo}"},
        )
        fig_enf_map.update_layout(
            mapbox_style="open-street-map",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            coloraxis_colorbar=dict(title="Casos/100K", tickfont=dict(size=9)),
            margin=dict(l=0,r=0,t=0,b=0),
        )
        st.plotly_chart(fig_enf_map, use_container_width=True,
                        config={"scrollZoom": True, "displayModeBar": True})

        c1e, c2e = st.columns(2)
        with c1e:
            st.markdown(f'<div class="chart-label">{label_enf}</div>', unsafe_allow_html=True)
            df_es = df_ccaa.sort_values(col_enf, ascending=True)
            ebar_colors = [
                "#7F1D1D" if v >= df_ccaa[col_enf].quantile(.75)
                else "#F97316" if v >= df_ccaa[col_enf].median()
                else S_BORDER
                for v in df_es[col_enf]
            ]
            fig_ebar = go.Figure(go.Bar(
                y=df_es["ccaa"], x=df_es[col_enf],
                orientation="h",
                marker_color=ebar_colors, marker_line_width=0,
                text=[str(v) for v in df_es[col_enf]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ebar.update_layout(**lay(h=340, margin=dict(t=10,b=10,l=8,r=40)))
            fig_ebar.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_ebar, use_container_width=True)

        with c2e:
            st.markdown('<div class="chart-label">Las tres patologías comparadas — media España</div>',
                        unsafe_allow_html=True)
            df_3p = pd.DataFrame({
                "Patología": ["Cardiovascular","Respiratoria","Oncológica"],
                "Media": [int(df_ccaa[c].mean()) for c in ["enf_cardio_100k","enf_resp_100k","enf_oncol_100k"]],
                "Max":   [int(df_ccaa[c].max())  for c in ["enf_cardio_100k","enf_resp_100k","enf_oncol_100k"]],
            })
            fig_3p = go.Figure()
            fig_3p.add_trace(go.Bar(
                x=df_3p["Patología"], y=df_3p["Media"], name="Media",
                marker_color=ACCENT, marker_line_width=0,
            ))
            fig_3p.add_trace(go.Bar(
                x=df_3p["Patología"], y=df_3p["Max"], name="Máximo CCAA",
                marker_color=S_BORDER, marker_line_width=0,
            ))
            fig_3p.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="h", y=-0.20, font=dict(size=10)),
                margin=dict(t=10,b=60,l=8,r=8)))
            fig_3p.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_3p, use_container_width=True)

        callout(
            "La <strong>patología oncológica</strong> presenta la mayor incidencia "
            "(media 330/100K) y la mayor variabilidad geográfica: Extremadura, Castilla y León "
            "y Galicia superan los 358 casos/100K. "
            "Estas tres CCAA tienen <strong>escasa presencia de centros de oncología privada Sanitas</strong> "
            "— un gap crítico dado que el ticket oncológico privado es 4-6× superior al de una consulta estándar. "
            "La enfermedad cardiovascular concentra mayor incidencia en CCAA de interior y con envejecimiento poblacional acelerado."
        )

    # ────────────────────────────────────────────────────────
    # TAB 5 — Penetración seguro privado
    # ────────────────────────────────────────────────────────
    with mt5:
        fig_seg_map = px.scatter_mapbox(
            df_ccaa, lat="lat", lon="lon",
            color="pct_seg_privado",
            color_continuous_scale=[[0,"#EEF4FF"],[0.5,"#0057A8"],[1,"#001A5C"]],
            size="pct_seg_privado", size_max=44,
            hover_name="ccaa",
            hover_data={"pct_seg_privado":True,"renta_media":True,"lat":False,"lon":False},
            zoom=4.7, center={"lat":40.2,"lon":-3.5},
            height=420,
            labels={"pct_seg_privado":"% con seguro privado"},
        )
        fig_seg_map.update_layout(
            mapbox_style="open-street-map",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            coloraxis_colorbar=dict(title="% pob.", tickfont=dict(size=9)),
            margin=dict(l=0,r=0,t=0,b=0),
        )
        st.plotly_chart(fig_seg_map, use_container_width=True,
                        config={"scrollZoom": True, "displayModeBar": True})

        c1s, c2s, c3s = st.columns(3)
        with c1s:
            st.markdown('<div class="chart-label">% Población con seguro privado por CCAA</div>',
                        unsafe_allow_html=True)
            df_ss = df_ccaa.sort_values("pct_seg_privado", ascending=True)
            fig_ss = go.Figure(go.Bar(
                y=df_ss["ccaa"], x=df_ss["pct_seg_privado"],
                orientation="h",
                marker_color=[ACCENT if v >= 24 else A3 if v >= 18 else S_BORDER
                              for v in df_ss["pct_seg_privado"]],
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in df_ss["pct_seg_privado"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ss.update_layout(**lay(h=360, margin=dict(t=10,b=10,l=8,r=50)))
            fig_ss.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_ss, use_container_width=True)

        with c2s:
            st.markdown('<div class="chart-label">Renta media vs. penetración seguro privado</div>',
                        unsafe_allow_html=True)
            fig_rv = px.scatter(
                df_ccaa, x="renta_media", y="pct_seg_privado",
                color="ccaa", text="ccaa",
                color_discrete_sequence=[ACCENT, A2, A3] + [S_BORDER]*20,
                labels={"renta_media":"Renta media (€/año)","pct_seg_privado":"% seguro privado"},
            )
            fig_rv.update_traces(textposition="top center", textfont=dict(size=8))
            fig_rv.update_layout(**lay(h=360, showlegend=False,
                margin=dict(t=10,b=10,l=8,r=8)))
            fig_rv.update_xaxes(showgrid=True, gridcolor=GRID)
            fig_rv.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_rv, use_container_width=True)

        with c3s:
            media_esp = df_ccaa["pct_seg_privado"].mean()
            top3 = df_ccaa.nlargest(3,"pct_seg_privado")["ccaa"].tolist()
            gap_ccaa = df_ccaa.sort_values("pct_seg_privado").head(5)
            callout(
                f"La media española de penetración de seguro privado es <strong>{media_esp:.1f}%</strong>. "
                f"<strong>Madrid (28.4%), País Vasco (24.8%) y Navarra (22.4%)</strong> lideran. "
                f"La correlación renta-penetración es directa (r≈0.87): "
                f"a mayor renta disponible, mayor predisposición al seguro privado. "
                f"<strong>Extremadura (9.2%), Galicia (12.1%) y Castilla y León (10.8%)</strong> "
                f"son mercados con baja penetración actual pero con incidencia de enfermedad "
                f"por encima de la media — perfil de cliente que más necesita el seguro "
                f"pero que menos accede. "
                f"Línea de acción: seguro básico o plan de empresa en colaboración "
                f"con administraciones regionales."
            )

    # ────────────────────────────────────────────────────────
    # TAB 6 — Índices comerciales
    # ────────────────────────────────────────────────────────
    with mt6:
        section("ÍNDICES COMERCIALES POR CCAA")

        st.markdown(
            f'<div style="font-size:.78rem;color:{S_MUTED};margin-bottom:16px;line-height:1.65">'
            f'Los índices se calculan sobre base 100 = media España. '
            f'<strong>Índice de Renta</strong>: renta disponible per cápita relativa. '
            f'<strong>Índice de Consumo</strong>: gasto en servicios de salud privada per cápita relativo. '
            f'<strong>Potencial de Mercado</strong>: media ponderada de renta, consumo salud y penetración seguro privado. '
            f'Datos simulados orientativos — fuente metodología panel.'
            f'</div>',
            unsafe_allow_html=True)

        df_idx = df_ccaa[["ccaa","indice_renta","indice_consumo","potencial_mkt","pct_seg_privado","renta_media"]].copy()
        df_idx = df_idx.sort_values("potencial_mkt", ascending=False).reset_index(drop=True)
        df_idx.index = df_idx.index + 1

        c1i, c2i = st.columns([1.3, 1])
        with c1i:
            st.markdown('<div class="chart-label">Potencial de mercado vs. Índice de consumo salud</div>',
                        unsafe_allow_html=True)
            fig_idx_s = px.scatter(
                df_idx, x="indice_consumo", y="potencial_mkt",
                color="indice_renta",
                color_continuous_scale=[[0,"#90B8DE"],[0.5,"#0057A8"],[1,"#001A5C"]],
                size="pct_seg_privado", size_max=28,
                text="ccaa",
                labels={
                    "indice_consumo":"Índice consumo salud privada",
                    "potencial_mkt":"Índice potencial de mercado",
                    "indice_renta":"Índice renta",
                    "pct_seg_privado":"% Seg. privado",
                },
                height=400,
            )
            fig_idx_s.update_traces(textposition="top center", textfont=dict(size=8, color=FONT))
            fig_idx_s.add_vline(x=100, line_dash="dot", line_color=S_BORDER,
                                annotation_text="consumo medio", annotation_font_size=9)
            fig_idx_s.add_hline(y=100, line_dash="dot", line_color=S_BORDER,
                                annotation_text="potencial medio", annotation_font_size=9)
            fig_idx_s.update_layout(**lay(h=400, showlegend=False,
                margin=dict(t=10,b=10,l=8,r=8)))
            fig_idx_s.update_xaxes(showgrid=True, gridcolor=GRID)
            fig_idx_s.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_idx_s, use_container_width=True)

        with c2i:
            st.markdown('<div class="chart-label">Ranking potencial de mercado por CCAA</div>',
                        unsafe_allow_html=True)
            colors_idx = [ACCENT if v >= 130 else A3 if v >= 100 else S_BORDER
                          for v in df_idx["potencial_mkt"]]
            fig_idx_bar = go.Figure(go.Bar(
                y=df_idx["ccaa"][::-1], x=df_idx["potencial_mkt"][::-1],
                orientation="h",
                marker_color=colors_idx[::-1], marker_line_width=0,
                text=[str(v) for v in df_idx["potencial_mkt"][::-1]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_idx_bar.add_vline(x=100, line_dash="dot", line_color=S_BORDER)
            fig_idx_bar.update_layout(**lay(h=400, margin=dict(t=10,b=10,l=8,r=40)))
            fig_idx_bar.update_xaxes(range=[50, 175], showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_idx_bar, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="chart-label">Tabla resumen de índices comerciales</div>',
                    unsafe_allow_html=True)

        def color_idx(val):
            if val >= 130: return f"color:{ACCENT};font-weight:700"
            if val >= 100: return f"color:{A3};font-weight:600"
            return f"color:{S_MUTED}"

        tabla_html = '<table style="width:100%;border-collapse:collapse;font-size:12.5px">'
        tabla_html += f'<thead><tr style="border-bottom:1px solid {S_BORDER};background:{S_LIGHT}">'
        for col in ["CCAA","Renta media","Í. Renta","Í. Consumo","Potencial Mkt","% Seg. Privado"]:
            tabla_html += f'<th style="padding:8px 12px;text-align:left;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:{S_MUTED}">{col}</th>'
        tabla_html += '</tr></thead><tbody>'
        for i, row in df_idx.iterrows():
            bg = PAPER if i % 2 == 0 else "#F8FAFE"
            tabla_html += f'<tr style="background:{bg};border-bottom:1px solid {S_BORDER}">'
            tabla_html += f'<td style="padding:8px 12px;font-weight:600">{row["ccaa"]}</td>'
            tabla_html += f'<td style="padding:8px 12px">{int(row["renta_media"]):,}€</td>'
            tabla_html += f'<td style="padding:8px 12px;{color_idx(row["indice_renta"])}">{row["indice_renta"]}</td>'
            tabla_html += f'<td style="padding:8px 12px;{color_idx(row["indice_consumo"])}">{row["indice_consumo"]}</td>'
            tabla_html += f'<td style="padding:8px 12px;{color_idx(row["potencial_mkt"])}">{row["potencial_mkt"]}</td>'
            tabla_html += f'<td style="padding:8px 12px">{row["pct_seg_privado"]:.1f}%</td>'
            tabla_html += '</tr>'
        tabla_html += '</tbody></table>'
        st.markdown(tabla_html, unsafe_allow_html=True)

        callout(
            "<strong>Top 3 por potencial de mercado: Madrid (145), País Vasco (140) y Navarra (133)</strong>. "
            "Son los únicos mercados con índice de potencial ≥ 130, todos por encima de la media España "
            "en las tres dimensiones (renta, consumo salud y penetración seguro). "
            "Oportunidad de crecimiento orgánico en Baleares (124) con el componente turístico. "
            "Cataluña (126) es el segundo mercado en volumen absoluto pero con potencial relativo inferior a Madrid "
            "por mayor fragmentación entre aseguradoras y menor ventaja competitiva Sanitas."
        )

    # ────────────────────────────────────────────────────────
    # TAB 7 — Municipios sin acceso
    # ────────────────────────────────────────────────────────
    with mt7:
        section("MUNICIPIOS CON CENTRO MÉDICO A MÁS DE 15 KM")
        callout(
            "Municipios donde el ciudadano más cercano al área tiene el centro médico privado más próximo "
            "a más de 15 km. Tamaño del punto proporcional a la población del municipio. "
            "Dato orientativo simulado sobre municipios rurales de interior con menor cobertura sanitaria privada."
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        fig_mun_map = px.scatter_mapbox(
            mun_sin_acceso, lat="lat", lon="lon",
            color="dist_min_km",
            color_continuous_scale=[[0,"#FEF3C7"],[0.5,"#F97316"],[1,"#7F1D1D"]],
            size="_sz", size_max=28,
            hover_name="municipio",
            hover_data={"ccaa":True,"poblacion":True,"dist_min_km":True,
                        "lat":False,"lon":False,"_sz":False},
            zoom=4.9, center={"lat":40.2,"lon":-3.5},
            height=440,
            labels={"dist_min_km":"Dist. mín. (km)","poblacion":"Población"},
        )
        fig_mun_map.update_layout(
            mapbox_style="open-street-map",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color=FONT),
            coloraxis_colorbar=dict(title="km al centro", tickfont=dict(size=9)),
            margin=dict(l=0,r=0,t=0,b=0),
        )
        st.plotly_chart(fig_mun_map, use_container_width=True,
                        config={"scrollZoom": True, "displayModeBar": True})

        c1m, c2m = st.columns(2)
        with c1m:
            st.markdown('<div class="chart-label">Municipios sin acceso por CCAA</div>',
                        unsafe_allow_html=True)
            cnt_ccaa = mun_sin_acceso.groupby("ccaa").size().reset_index(name="n")
            cnt_ccaa = cnt_ccaa.sort_values("n", ascending=True)
            fig_cnt = go.Figure(go.Bar(
                y=cnt_ccaa["ccaa"], x=cnt_ccaa["n"],
                orientation="h",
                marker_color=[ACCENT if v >= 4 else A3 if v >= 2 else S_BORDER
                              for v in cnt_ccaa["n"]],
                marker_line_width=0,
                text=[str(v) for v in cnt_ccaa["n"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_cnt.update_layout(**lay(h=280, margin=dict(t=10,b=10,l=8,r=30)))
            fig_cnt.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_cnt, use_container_width=True)

        with c2m:
            st.markdown('<div class="chart-label">Distancia mínima al centro médico privado</div>',
                        unsafe_allow_html=True)
            df_ms = mun_sin_acceso.sort_values("dist_min_km", ascending=True)
            fig_dist = go.Figure(go.Bar(
                x=df_ms["municipio"], y=df_ms["dist_min_km"],
                marker_color=["#7F1D1D" if v >= 30 else "#F97316" if v >= 22 else S_BORDER
                              for v in df_ms["dist_min_km"]],
                marker_line_width=0,
                text=[f"{v} km" for v in df_ms["dist_min_km"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_dist.update_layout(**lay(h=280, margin=dict(t=10,b=60,l=8,r=8)))
            fig_dist.update_xaxes(tickangle=-35, tickfont=dict(size=8))
            fig_dist.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_dist, use_container_width=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        section("CONCLUSIONES ESTRATÉGICAS DEL MAPA")

        CONCLUSIONES_MAPA = [
            {
                "num": "01",
                "area": "Red de centros",
                "titulo": "Sanitas opera en 5 zonas blancas con 3.8M de asegurados potenciales sin centro propio",
                "cuerpo": (
                    "Galicia, Aragón, Canarias, Extremadura y Cantabria interior carecen de hospital o clínica propia Sanitas. "
                    "La población combinada de estas CCAA supera los 5.2M de habitantes, de los cuales un 12–15% (618K–780K personas) "
                    "tiene o tendría capacidad económica para un seguro privado. "
                    "Sin presencia hospitalaria propia, el asegurado acude a red concertada: NPS 12 puntos inferior, "
                    "mayor tasa de abandono (-18%) y nula diferenciación de marca en el punto de contacto crítico."
                ),
                "accion": "Prioridad clínica ambulatoria: A Coruña (Galicia, 2.7M hab., renta 93% media España) y Zaragoza (Aragón, 1.3M hab., renta 110%).",
            },
            {
                "num": "02",
                "area": "Índices comerciales",
                "titulo": "Madrid, País Vasco y Navarra concentran el 52% del potencial de mercado de seguro privado",
                "cuerpo": (
                    "El índice de potencial de mercado de Madrid (145) es 2.1× el de Extremadura (66). "
                    "País Vasco (140) y Navarra (133) son los mercados con mayor propensión de compra por renta combinada "
                    "con alta cultura de seguro. En País Vasco, sin embargo, IMQ captura el 38% de la cuota "
                    "de seguro privado — un competidor local con fuerte arraigo que Sanitas no bate con su "
                    "propuesta actual de valor. "
                    "En Navarra, la ausencia de hospital propio Sanitas obliga a trabajar solo a través del canal correduría."
                ),
                "accion": "En PV: activar campaña B2B específica frente a IMQ con el argumento 'red nacional + cobertura internacional'. En Navarra: acuerdo con Clínica Universidad de Navarra para ampliar red concertada premium.",
            },
            {
                "num": "03",
                "area": "Enfermedades & turismo",
                "titulo": "Canarias y Baleares: la demanda turística exige cobertura de asistencia diferenciada",
                "cuerpo": (
                    "Canarias recibe 13.2M de turistas/año con temperatura media de 22°C — la más alta de España. "
                    "La incidencia de traumatología estival (caídas, accidentes náuticos) y gastroenteritis "
                    "en turistas internacionales genera 140K–180K episodios asistenciales/año. "
                    "Sanitas no tiene hospital propio en Canarias: toda la asistencia pasa por concertado. "
                    "Baleares (12.9M turistas, 19.6°C) presenta el mismo patrón con el añadido de alta incidencia "
                    "cardiológica en turistas senior (perfil 55+). "
                    "Ambos archipiélagos tienen índice de potencial relativo elevado (93–124) y alta penetración de seguro privado."
                ),
                "accion": "Producto 'Sanitas Islas': combinación seguro residentes + cobertura de asistencia a turistas en centros concertados con SLA garantizado. Convenio con aerolíneas y touroperadores.",
            },
            {
                "num": "04",
                "area": "Acceso rural",
                "titulo": "20 municipios con más de 1.000 habitantes a más de 15 km del centro privado más cercano",
                "cuerpo": (
                    "Albarracín (38 km), Boltaña (31 km) y Molina de Aragón (35 km) encabezan la lista "
                    "de municipios con peor acceso a medicina privada. El 65% de los municipios identificados "
                    "pertenecen a Castilla y León, Aragón y Extremadura — las tres CCAA con índice de potencial "
                    "más bajo pero con incidencia de enfermedad crónica por encima de la media. "
                    "La solución no es apertura de centros físicos (rentabilidad insuficiente) sino "
                    "digitalización: telemedicina + consulta online + envío a domicilio de pruebas diagnósticas básicas."
                ),
                "accion": "Sanitas Digital Rural: póliza con app-first, primera consulta siempre por videollamada, desplazamiento cubierto hasta centro físico para urgencias. Precio 20% inferior a póliza estándar.",
            },
            {
                "num": "05",
                "area": "Oncología",
                "titulo": "Extremadura, Castilla y León y Galicia: alta carga oncológica sin red Sanitas",
                "cuerpo": (
                    "Las tres CCAA con mayor incidencia oncológica registrada (≥358 casos/100K) son "
                    "precisamente aquellas donde Sanitas no tiene hospital propio. "
                    "El perfil de asegurado con cáncer genera un ticket anual de 12.000–25.000€ vs. 900€ "
                    "de un asegurado estándar. Capturar el 1% de los casos oncológicos privados de "
                    "estas tres CCAA representaría un incremento de facturación de 18–30M€/año. "
                    "Hoy esa demanda va a HM Hospitales (referente oncológico nacional) y a hospitales universitarios concertados."
                ),
                "accion": "Alianza estratégica con red hospitalaria en Galicia para oncología de alto nivel concertado. Desarrollar unidad de oncología de alta complejidad en Hospital La Moraleja para captar derivaciones nacionales.",
            },
        ]

        for conc in CONCLUSIONES_MAPA:
            color_area = {
                "Red de centros": ACCENT,
                "Índices comerciales": A2,
                "Enfermedades & turismo": A3,
                "Acceso rural": "#2E7D32",
                "Oncología": "#B71C1C",
            }.get(conc["area"], ACCENT)
            with st.expander(f"{conc['num']} · {conc['titulo']}", expanded=(conc['num']=="01")):
                ca, cb = st.columns([1, 2])
                with ca:
                    st.markdown(
                        f'<div style="font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;'
                        f'font-weight:700;color:{color_area};margin-bottom:8px">{conc["area"]}</div>'
                        f'<div style="font-size:.78rem;color:{S_MUTED};line-height:1.65">'
                        f'{conc["cuerpo"]}'
                        f'</div>',
                        unsafe_allow_html=True)
                with cb:
                    st.markdown(
                        f'<div style="background:{S_LIGHT};border-left:3px solid {color_area};'
                        f'padding:14px 16px;border-radius:0 6px 6px 0">'
                        f'<div style="font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;'
                        f'font-weight:700;color:{color_area};margin-bottom:6px">Acción recomendada</div>'
                        f'<div style="font-size:.78rem;color:{FONT};line-height:1.65">{conc["accion"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PÁGINA: EXPERIENCIA & RETENCIÓN
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "experiencia":

    if st.button("← Inicio", key="back_exp"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("EXPERIENCIA DEL ASEGURADO & RETENCIÓN")

    # ── datos simulados ───────────────────────────────────────────
    ASEG = ["Sanitas","DKV","Asisa","Adeslas","Mapfre Salud","AXA Salud"]

    df_nps = pd.DataFrame({
        "marca":       ASEG,
        "promotores":  [38, 62, 45, 36, 28, 25],
        "pasivos":     [46, 30, 40, 46, 50, 52],
        "detractores": [16,  8, 15, 18, 22, 23],
        "nps":         [22, 54, 30, 18, 6,  2],
    })

    df_churn = pd.DataFrame({
        "marca":       ASEG,
        "churn_pct":   [8.4, 5.1, 6.8, 7.2, 9.1, 9.8],
        "vida_media_anos": [5.8, 9.2, 7.1, 6.6, 5.3, 4.9],
    })

    df_motivos = pd.DataFrame({
        "motivo": ["Precio demasiado alto","Tiempo de espera","Calidad de atención",
                   "Falta especialista próximo","Mejor oferta competidor"],
        "pct":    [42, 21, 15, 12, 10],
    })

    df_digital = pd.DataFrame({
        "marca":          ["DKV","Sanitas","Adeslas","Asisa","Mapfre Salud","AXA Salud"],
        "citas_online":   [87, 71, 68, 62, 55, 52],
        "telemedicina":   [34, 18, 15, 12,  9,  8],
        "claims_online":  [91, 73, 70, 65, 58, 54],
        "app_rating":     [4.6, 4.2, 3.9, 3.8, 3.5, 3.4],
    })

    ESPECIALIDADES = ["Médico general","Dermatología","Traumatología","Cardiología",
                      "Ginecología","Neurología","Psiquiatría","Oncología"]
    df_espera = pd.DataFrame({
        "especialidad": ESPECIALIDADES,
        "Sanitas":  [ 2,  8, 10, 12,  7, 15, 22, 18],
        "DKV":      [ 1,  5,  7,  9,  5, 11, 14, 21],
        "Adeslas":  [ 2,  9, 11, 14,  8, 17, 28, 21],
        "HM Hosp.": [ 3,  6,  9,  8,  6, 13, 16, 12],
        "Sector":   [ 2,  8, 11, 12,  7, 15, 24, 18],
    })

    SEGMENTOS = ["Básico individual","Premium individual","Familiar","Senior 60+","Colectivo empresa"]
    df_loss = pd.DataFrame({
        "segmento":          SEGMENTOS,
        "loss_sanitas":      [72, 61, 78, 89, 67],
        "loss_sector":       [68, 64, 75, 91, 66],
        "primas_peso":       [28, 22, 32, 11, 7],
    })

    df_rec = pd.DataFrame({
        "marca":         ASEG,
        "reclamaciones": [2.8, 1.4, 1.9, 2.1, 3.4, 3.1],
    })

    ex1, ex2, ex3, ex4 = st.tabs(["NPS & Lealtad","Churn & Motivos","Digitalización","Siniestralidad & Esperas"])

    # ──────────────────────────────────────────────────────────────
    # TAB 1 — NPS & Lealtad
    # ──────────────────────────────────────────────────────────────
    with ex1:
        k1e, k2e, k3e, k4e = st.columns(4)
        kpi_card(k1e, "NPS Sanitas", "+22", "Sector medio: +22")
        kpi_card(k2e, "NPS DKV (líder)", "+54", "Gap vs Sanitas: 32 pp", negative=True)
        kpi_card(k3e, "Promotores Sanitas", "38%", "DKV: 62%", negative=True)
        kpi_card(k4e, "Detractores Sanitas", "16%", "DKV: 8%", negative=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        c1n, c2n = st.columns(2)
        with c1n:
            st.markdown('<div class="chart-label">NPS por aseguradora</div>', unsafe_allow_html=True)
            df_ns = df_nps.sort_values("nps", ascending=True)
            bar_colors_nps = [
                ACCENT if v >= 20 else A3 if v >= 0 else "#B71C1C"
                for v in df_ns["nps"]
            ]
            fig_nps = go.Figure(go.Bar(
                y=df_ns["marca"], x=df_ns["nps"], orientation="h",
                marker_color=bar_colors_nps, marker_line_width=0,
                text=[f"+{v}" if v >= 0 else str(v) for v in df_ns["nps"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_nps.add_vline(x=0, line_color=S_BORDER, line_width=1)
            fig_nps.update_layout(**lay(h=280, margin=dict(t=10,b=10,l=8,r=50)))
            fig_nps.update_xaxes(range=[-10, 70], showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_nps, use_container_width=True)

        with c2n:
            st.markdown('<div class="chart-label">Desglose NPS Sanitas — Promotores / Pasivos / Detractores</div>',
                        unsafe_allow_html=True)
            san_row = df_nps[df_nps["marca"]=="Sanitas"].iloc[0]
            dkv_row = df_nps[df_nps["marca"]=="DKV"].iloc[0]
            fig_stack = go.Figure()
            for marca, row in [("Sanitas", san_row), ("DKV", dkv_row)]:
                fig_stack.add_trace(go.Bar(
                    name="Promotores", x=[marca], y=[row["promotores"]],
                    marker_color="#2A7A52" if marca=="DKV" else ACCENT,
                    text=[f'{row["promotores"]}%'], textposition="inside",
                    textfont=dict(size=10, color="white"),
                    showlegend=(marca=="Sanitas"),
                ))
                fig_stack.add_trace(go.Bar(
                    name="Pasivos", x=[marca], y=[row["pasivos"]],
                    marker_color=S_BORDER if marca=="DKV" else "#90B8DE",
                    text=[f'{row["pasivos"]}%'], textposition="inside",
                    textfont=dict(size=10, color=FONT),
                    showlegend=(marca=="Sanitas"),
                ))
                fig_stack.add_trace(go.Bar(
                    name="Detractores", x=[marca], y=[row["detractores"]],
                    marker_color="#FECACA" if marca=="DKV" else "#FCA5A5",
                    text=[f'{row["detractores"]}%'], textposition="inside",
                    textfont=dict(size=10, color="#7F1D1D"),
                    showlegend=(marca=="Sanitas"),
                ))
            fig_stack.update_layout(
                barmode="stack",
                **lay(h=280, showlegend=True,
                      legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
                      margin=dict(t=10,b=60,l=8,r=8))
            )
            fig_stack.update_yaxes(range=[0,105], showgrid=False)
            st.plotly_chart(fig_stack, use_container_width=True)

        c3n, c4n = st.columns(2)
        with c3n:
            st.markdown('<div class="chart-label">Reclamaciones al regulador (DGSFP) por 1.000 asegurados</div>',
                        unsafe_allow_html=True)
            df_rs = df_rec.sort_values("reclamaciones", ascending=True)
            fig_rec = go.Figure(go.Bar(
                y=df_rs["marca"], x=df_rs["reclamaciones"], orientation="h",
                marker_color=["#2A7A52" if v <= 1.5 else ACCENT if v <= 2.5 else "#F97316" if v <= 3.0 else "#B71C1C"
                              for v in df_rs["reclamaciones"]],
                marker_line_width=0,
                text=[f"{v:.1f}" for v in df_rs["reclamaciones"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_rec.update_layout(**lay(h=250, margin=dict(t=10,b=10,l=8,r=40)))
            fig_rec.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_rec, use_container_width=True)

        with c4n:
            callout(
                "DKV lidera el NPS sectorial con <strong>+54</strong>, "
                "32 puntos por encima de Sanitas (+22). La brecha se explica principalmente "
                "por la experiencia digital y los tiempos de espera. "
                "<strong>Detractores de Sanitas (16%)</strong> generan erosión de cartera "
                "vía boca-oído: cada detractor comparte su experiencia con una media de 4.2 contactos. "
                "Reducir detractores del 16% al 10% equivale a evitar la pérdida de "
                "~28.000 pólizas en los próximos 24 meses. "
                "Sanitas supera a Adeslas (+18) y duplica a Mapfre Salud (+6) — "
                "posición defensiva razonable pero muy alejada del líder."
            )

    # ──────────────────────────────────────────────────────────────
    # TAB 2 — Churn & Motivos
    # ──────────────────────────────────────────────────────────────
    with ex2:
        k1c, k2c, k3c, k4c = st.columns(4)
        kpi_card(k1c, "Churn Sanitas", "8.4%", "▼ mejor que Mapfre (9.1%)")
        kpi_card(k2c, "Vida media asegurado", "5.8 años", "DKV: 9.2 años", negative=True)
        kpi_card(k3c, "Churn evitable est.", "4.8 pp", "Motivos controlables (espera + calidad)")
        kpi_card(k4c, "Coste churn anual est.", "~42 M€", "CAC medio nuevo cliente: 380€", negative=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        c1c, c2c = st.columns(2)
        with c1c:
            st.markdown('<div class="chart-label">Tasa de churn anual por aseguradora (%)</div>',
                        unsafe_allow_html=True)
            df_cs = df_churn.sort_values("churn_pct", ascending=True)
            fig_churn = go.Figure(go.Bar(
                y=df_cs["marca"], x=df_cs["churn_pct"], orientation="h",
                marker_color=["#2A7A52" if v <= 6 else ACCENT if v <= 8.4 else "#F97316" if v <= 9 else "#B71C1C"
                              for v in df_cs["churn_pct"]],
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in df_cs["churn_pct"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_churn.update_layout(**lay(h=260, margin=dict(t=10,b=10,l=8,r=50)))
            fig_churn.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_churn, use_container_width=True)

        with c2c:
            st.markdown('<div class="chart-label">Vida media del asegurado (años)</div>',
                        unsafe_allow_html=True)
            df_vm = df_churn.sort_values("vida_media_anos", ascending=True)
            fig_vida = go.Figure(go.Bar(
                y=df_vm["marca"], x=df_vm["vida_media_anos"], orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_vm["marca"]],
                marker_line_width=0,
                text=[f"{v:.1f}a" for v in df_vm["vida_media_anos"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_vida.update_layout(**lay(h=260, margin=dict(t=10,b=10,l=8,r=50)))
            fig_vida.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_vida, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c3c, c4c = st.columns(2)
        with c3c:
            st.markdown('<div class="chart-label">Motivos de baja en Sanitas (% sobre total bajas)</div>',
                        unsafe_allow_html=True)
            df_mv = df_motivos.sort_values("pct", ascending=True)
            mot_colors = [
                "#B71C1C" if v >= 35 else "#F97316" if v >= 18 else S_BORDER
                for v in df_mv["pct"]
            ]
            fig_mot = go.Figure(go.Bar(
                y=df_mv["motivo"], x=df_mv["pct"], orientation="h",
                marker_color=mot_colors, marker_line_width=0,
                text=[f"{v}%" for v in df_mv["pct"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_mot.update_layout(**lay(h=260, margin=dict(t=10,b=10,l=8,r=50)))
            fig_mot.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_mot, use_container_width=True)

        with c4c:
            # Funnel de retención simulado
            st.markdown('<div class="chart-label">Embudo retención: de baja declarada a baja efectiva</div>',
                        unsafe_allow_html=True)
            funnel_labels = ["Solicitudes de baja","Contactados por retención",
                             "Oferta presentada","Retenidos","Bajas efectivas"]
            funnel_vals   = [100, 82, 61, 34, 66]
            fig_fun = go.Figure(go.Funnel(
                y=funnel_labels, x=funnel_vals,
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(color=[A2, ACCENT, A3, "#2A7A52", "#B71C1C"]),
                connector=dict(line=dict(color=S_BORDER, width=1)),
            ))
            fig_fun.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=10, color=FONT),
                margin=dict(t=10,b=10,l=8,r=8), height=260,
            )
            st.plotly_chart(fig_fun, use_container_width=True)

        callout(
            "El <strong>42% de las bajas</strong> se debe al precio — un motivo estructural difícil de atacar "
            "sin tocar la propuesta de valor. Pero el <strong>48% restante</strong> "
            "(espera + calidad + falta de especialista) es directamente controlable. "
            "El embudo de retención revela que solo el <strong>34% de quienes piden la baja "
            "son finalmente retenidos</strong>. Aumentar esa tasa del 34% al 45% "
            "equivale a ~1.100 pólizas adicionales retenidas/año (~3.4M€ en primas anuales). "
            "Cada año de retraso en reducir churn del 8.4% al 6% equivale "
            "a una pérdida acumulada estimada de <strong>~87M€ en valor de cartera</strong>."
        )

    # ──────────────────────────────────────────────────────────────
    # TAB 3 — Digitalización
    # ──────────────────────────────────────────────────────────────
    with ex3:
        k1d, k2d, k3d, k4d = st.columns(4)
        kpi_card(k1d, "Citas online Sanitas", "71%", "DKV: 87% — gap 16 pp", negative=True)
        kpi_card(k2d, "Telemedicina Sanitas", "18%", "DKV: 34% — gap 16 pp", negative=True)
        kpi_card(k3d, "App Store rating", "4.2 ★", "DKV: 4.6 ★", negative=True)
        kpi_card(k4d, "Reclamaciones online", "73%", "DKV: 91% — gap 18 pp", negative=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        c1d, c2d = st.columns(2)
        with c1d:
            st.markdown('<div class="chart-label">Madurez digital — comparativa aseguradoras</div>',
                        unsafe_allow_html=True)
            dims_d   = ["citas_online","telemedicina","claims_online"]
            labels_d = ["Citas online %","Telemedicina %","Gestión online %"]
            fig_rad_d = go.Figure()
            d_colors = [A3, ACCENT, S_BORDER, "#C26A0A", "#6B3FAE", "#2A7A52"]
            for i, (_, row) in enumerate(df_digital.iterrows()):
                c = d_colors[i]
                r, g, b = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
                vals = [row[d] for d in dims_d]
                fig_rad_d.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=labels_d + [labels_d[0]],
                    name=row["marca"], fill="toself",
                    line=dict(color=c, width=2),
                    fillcolor=f"rgba({r},{g},{b},0.06)",
                ))
            fig_rad_d.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,100],
                                   tickfont=dict(size=8), gridcolor=GRID, linecolor=GRID),
                    angularaxis=dict(tickfont=dict(size=9, family="Inter"), gridcolor=GRID),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11, color=FONT),
                showlegend=True,
                legend=dict(orientation="h", y=-0.20, font=dict(size=9)),
                margin=dict(t=20,b=90,l=60,r=60), height=360,
            )
            st.plotly_chart(fig_rad_d, use_container_width=True)

        with c2d:
            st.markdown('<div class="chart-label">App Store rating por aseguradora</div>',
                        unsafe_allow_html=True)
            df_ds = df_digital.sort_values("app_rating", ascending=True)
            fig_app = go.Figure(go.Bar(
                y=df_ds["marca"], x=df_ds["app_rating"], orientation="h",
                marker_color=["#2A7A52" if v >= 4.5 else ACCENT if v >= 4.0 else "#F97316" if v >= 3.7 else "#B71C1C"
                              for v in df_ds["app_rating"]],
                marker_line_width=0,
                text=[f"{v:.1f} ★" for v in df_ds["app_rating"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_app.update_layout(**lay(h=240, margin=dict(t=10,b=10,l=8,r=60)))
            fig_app.update_xaxes(range=[3.0, 5.0], showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_app, use_container_width=True)

            st.markdown('<div class="chart-label">% Telemedicina sobre total consultas</div>',
                        unsafe_allow_html=True)
            df_tele = df_digital.sort_values("telemedicina", ascending=True)
            fig_tele = go.Figure(go.Bar(
                y=df_tele["marca"], x=df_tele["telemedicina"], orientation="h",
                marker_color=[ACCENT if m=="Sanitas" else S_BORDER for m in df_tele["marca"]],
                marker_line_width=0,
                text=[f"{v}%" for v in df_tele["telemedicina"]],
                textposition="outside", textfont=dict(size=10),
            ))
            fig_tele.update_layout(**lay(h=220, margin=dict(t=10,b=10,l=8,r=50)))
            fig_tele.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_tele, use_container_width=True)

        callout(
            "DKV tiene una ventaja digital estructural en todos los indicadores: "
            "<strong>+16 pp en telemedicina</strong>, +16 pp en citas online, +18 pp en gestión de reclamaciones. "
            "La telemedicina no es solo un canal de conveniencia — "
            "reduce el coste de cada consulta un 62% y aumenta la frecuencia de contacto, "
            "lo que mejora la detección precoz y reduce la siniestralidad. "
            "Si Sanitas alcanzara el 30% de telemedicina, liberaría ~120.000 consultas presenciales/año "
            "en sus centros propios, reduciendo tiempos de espera y mejorando NPS en 8-12 puntos."
        )

    # ──────────────────────────────────────────────────────────────
    # TAB 4 — Siniestralidad & Esperas
    # ──────────────────────────────────────────────────────────────
    with ex4:
        k1s, k2s, k3s, k4s = st.columns(4)
        kpi_card(k1s, "Loss ratio familiar", "78%", "Umbral alert.: >80%", negative=True)
        kpi_card(k2s, "Loss ratio senior 60+", "89%", "Umbral crítico: 90%", negative=True)
        kpi_card(k3s, "Loss ratio premium", "61%", "Margen más saludable")
        kpi_card(k4s, "Espera oncología Sanitas", "18 días", "HM Hosp.: 12 días", negative=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        c1s, c2s = st.columns(2)
        with c1s:
            st.markdown('<div class="chart-label">Loss ratio Sanitas vs sector por segmento (%)</div>',
                        unsafe_allow_html=True)
            fig_lr = go.Figure()
            fig_lr.add_trace(go.Bar(
                x=df_loss["segmento"], y=df_loss["loss_sanitas"],
                name="Sanitas", marker_color=ACCENT, marker_line_width=0,
                text=[f"{v}%" for v in df_loss["loss_sanitas"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr.add_trace(go.Bar(
                x=df_loss["segmento"], y=df_loss["loss_sector"],
                name="Media sector", marker_color=S_BORDER, marker_line_width=0,
                text=[f"{v}%" for v in df_loss["loss_sector"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr.add_hline(y=80, line_dash="dot", line_color="#F97316",
                             annotation_text="80% alerta", annotation_font_size=9,
                             annotation_font_color="#F97316")
            fig_lr.add_hline(y=90, line_dash="dash", line_color="#B71C1C",
                             annotation_text="90% crítico", annotation_font_size=9,
                             annotation_font_color="#B71C1C")
            fig_lr.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=-0.20, font=dict(size=10)),
                margin=dict(t=10,b=70,l=8,r=8)))
            fig_lr.update_xaxes(tickangle=-15)
            fig_lr.update_yaxes(range=[50, 100], showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_lr, use_container_width=True)

        with c2s:
            st.markdown('<div class="chart-label">Peso en cartera (% primas) por segmento</div>',
                        unsafe_allow_html=True)
            fig_peso = go.Figure(go.Pie(
                labels=df_loss["segmento"],
                values=df_loss["primas_peso"],
                marker_colors=[ACCENT, A2, A3, "#F97316", "#90B8DE"],
                textinfo="label+percent",
                textfont=dict(size=10, family="Inter"),
                hole=0.45,
            ))
            fig_peso.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11, color=FONT),
                showlegend=False,
                margin=dict(t=10,b=10,l=8,r=8), height=280,
            )
            st.plotly_chart(fig_peso, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="chart-label">Tiempo de espera por especialidad — días (menos = mejor)</div>',
                    unsafe_allow_html=True)

        espera_sel = st.multiselect(
            "Aseguradoras a comparar:",
            ["Sanitas","DKV","Adeslas","HM Hosp.","Sector"],
            default=["Sanitas","DKV","HM Hosp."],
            key="esp_sel",
        )
        if espera_sel:
            fig_esp = go.Figure()
            esp_colors_map = {"Sanitas":ACCENT,"DKV":A3,"Adeslas":"#B71C1C",
                              "HM Hosp.":"#6A1B9A","Sector":S_MUTED}
            for col in espera_sel:
                fig_esp.add_trace(go.Scatter(
                    x=df_espera["especialidad"], y=df_espera[col],
                    name=col, mode="lines+markers",
                    line=dict(color=esp_colors_map.get(col, S_MUTED),
                              width=2 if col=="Sanitas" else 1.5,
                              dash="dot" if col=="Sector" else "solid"),
                    marker=dict(size=7 if col=="Sanitas" else 5),
                ))
            fig_esp.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="h", y=-0.22, font=dict(size=10)),
                margin=dict(t=10,b=70,l=8,r=8)))
            fig_esp.update_xaxes(tickangle=-20, showgrid=False)
            fig_esp.update_yaxes(showgrid=True, gridcolor=GRID,
                                  title_text="Días de espera")
            st.plotly_chart(fig_esp, use_container_width=True)

        callout(
            "El <strong>loss ratio senior 60+ (89%)</strong> roza el umbral crítico del 90% "
            "— cualquier incremento en siniestralidad de este segmento convierte la cartera en no rentable. "
            "Con el envejecimiento poblacional (España +65: 19.8% en 2026 → 26.4% en 2040), "
            "el peso de este segmento crecerá estructuralmente. "
            "<strong>Psiquiatría (22 días) y Oncología (18 días)</strong> son los cuellos de botella "
            "de espera que más daño hacen al NPS. DKV resuelve psiquiatría en 14 días "
            "gracias a la telemedicina — el canal digital como solución directa al gap de espera. "
            "El segmento <strong>Premium individual</strong> (LR 61%) es el más rentable: "
            "priorizar su captación y retención tiene doble impacto positivo — NPS alto + margen sano."
        )

# ══════════════════════════════════════════════════════════════════
# PÁGINA: ACCIONES RECOMENDADAS
# ══════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "acciones":

    if st.button("← Inicio", key="back_acc"):
        go_to("home"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section("ACCIONES RECOMENDADAS")
    st.caption("Cada acción señala el dato que la sustenta y la métrica con la que se evalúa.")

    ACCIONES = [
        {
            "area": "Seguros",
            "titulo": "Crear póliza Sanitas Young para el segmento 18–30",
            "dato": "El 22% de la muestra son Jóvenes Saludables con DKV como marca top. Gap de captación Sanitas: 24 pp. Precio máximo declarado: 35€/mes.",
            "urgencia": "DKV crece al 2.1% anual en este segmento con esperas garantizadas y app-first. Sin una respuesta, el segmento se consolida fuera de Sanitas.",
            "inversion": "Desarrollo de producto digital-first. 4–6 meses.",
            "metrica": "Contratos nuevos 18–30 años +35% en 12 meses. Prima media segmento: 33€/mes.",
        },
        {
            "area": "Seguros",
            "titulo": "Comunicar el triángulo diferencial: dental + internacional + app",
            "dato": "Sanitas es la única aseguradora con dental completo + cobertura internacional + app digital simultáneamente. El diferencial no está en la comunicación principal.",
            "urgencia": "El 12% de los encuestados valora cobertura dental como atributo decisivo. Ningún competidor ofrece los tres a la vez en gama completa.",
            "inversion": "Campaña de comunicación. Sin desarrollo de producto nuevo. Bajo coste.",
            "metrica": "Top of Mind sube de #2 a #1 en segmento 35–50 en 18 meses.",
        },
        {
            "area": "Hospitales",
            "titulo": "Abrir clínica Sanitas en A Coruña — zona blanca prioritaria",
            "dato": "Galicia es zona blanca de Sanitas hospitales. Quirónsalud captura ese flujo. Galicia: 2.7M habitantes, renta media, asegurado Sanitas sin infraestructura de marca propia.",
            "urgencia": "Sin centro propio, el asegurado acude al cuadro concertado: menor control de experiencia, menor fidelidad y NPS más bajo.",
            "inversion": "Clínica ambulatoria 15–20 especialidades. 8–14M€ o acuerdo de colaboración con clínica local.",
            "metrica": "Satisfacción asegurados Galicia +0.4 puntos en 24 meses. NPS regional +12.",
        },
        {
            "area": "Hospitales",
            "titulo": "Invertir en Oncología de alta complejidad en La Moraleja y CIMA",
            "dato": "Sanitas tiene cobertura parcial en Oncología. La demanda de oncología privada creció un 18% en 2025. HM Montepríncipe es el referente actual.",
            "urgencia": "El paciente oncológico privado genera un ticket anual 4–6× superior y fideliza todo el grupo familiar.",
            "inversion": "Equipamiento y captación de talento oncológico. 5–8M€ en 12–18 meses.",
            "metrica": "Pacientes oncológicos propios +40% en 24 meses. Rating Oncología Google ≥ 4.4.",
        },
        {
            "area": "Comunicación",
            "titulo": "Pasar de estrategia de alcance a estrategia de engagement",
            "dato": "Sanitas 185K seguidores, engagement 0.9%. DKV 95K seguidores, engagement 3.8%. La audiencia de Sanitas no interacciona: el algoritmo penaliza la distribución orgánica.",
            "urgencia": "Sanitas pierde 4 puntos de índice Google Trends en septiembre y enero, los dos momentos de máxima intención de compra.",
            "inversion": "Rediseño de estrategia de contenido. 3 meses. Recursos internos + agencia.",
            "metrica": "Engagement rate ≥ 2.5% en 6 meses. Alcance orgánico +30%.",
        },
        {
            "area": "B2B / Geo",
            "titulo": "Activar seguro colectivo en PYMES del País Vasco frente a IMQ",
            "dato": "PV tiene la renta per cápita más alta de España y alta penetración de seguro privado de empresa. IMQ es el competidor local con alta fidelidad. Sanitas tiene clínica en Bilbao sin red hospitalaria propia.",
            "urgencia": "El canal colectivo empresa (22% de la contratación total) genera contratos multianuales con menor churn que el canal individual.",
            "inversion": "Reasignación de fuerza comercial existente. Acuerdos con clúster empresarial vasco.",
            "metrica": "Contratos colectivos PV +20% en 12 meses. Penetración Sanitas en PV +1.5 pp.",
        },
    ]

    area_cols = {"Seguros": ACCENT, "Hospitales": A2, "Comunicación": A3, "B2B / Geo": S_MUTED}

    for i, acc in enumerate(ACCIONES):
        color = area_cols.get(acc["area"], ACCENT)
        with st.expander(f"{acc['area']}  ·  {acc['titulo']}", expanded=(i==0)):
            ca, cb = st.columns([1, 2])
            with ca:
                st.markdown(
                    f'<div style="font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;'
                    f'color:{color};font-weight:700;margin-bottom:4px">{acc["area"]}</div>'
                    f'<div style="font-size:.8rem;color:{S_MUTED};line-height:1.6">'
                    f'<strong style="color:{FONT}">Dato:</strong> {acc["dato"]}'
                    f'</div>', unsafe_allow_html=True)
            with cb:
                st.markdown(
                    f'<div style="font-size:.8rem;color:{S_MUTED};line-height:1.6">'
                    f'<strong style="color:{FONT}">Por qué ahora:</strong> {acc["urgencia"]}<br>'
                    f'<strong style="color:{FONT}">Inversión/esfuerzo:</strong> {acc["inversion"]}<br>'
                    f'<strong style="color:{color}">Métrica de éxito:</strong> {acc["metrica"]}'
                    f'</div>', unsafe_allow_html=True)
