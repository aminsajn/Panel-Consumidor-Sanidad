#!/usr/bin/env python3
"""
Sanitas — Plataforma de Inteligencia Corporativa
Vista Ejecutiva · Retención & Cartera · Optimización Operativa · Inteligencia Comercial
python -m streamlit run panel_sanitas.py
"""
import warnings; warnings.filterwarnings("ignore")
import base64
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def _img_b64(p):
    try:
        return base64.b64encode(Path(p).read_bytes()).decode()
    except Exception:
        return ""

_LOGO_DIR = Path(__file__).parent.parent
SANITAS_B64 = _img_b64(_LOGO_DIR / "logo-sanitas.png")
MINSAIT_B64  = _img_b64(_LOGO_DIR / "Logo-Minsait.png")
_SAN_IMG = f'<img src="data:image/png;base64,{SANITAS_B64}" height="52" style="object-fit:contain;display:block">' if SANITAS_B64 else ""
_MIN_IMG = f'<img src="data:image/png;base64,{MINSAIT_B64}" style="height:52px;max-width:140px;object-fit:contain;display:block;margin-left:auto">' if MINSAIT_B64 else ""

# ══════════════════════════════════════════════════════════════════
# PALETA
# ══════════════════════════════════════════════════════════════════
ACCENT  = "#003087"
A2      = "#0057A8"
A3      = "#0099D6"
BG      = "#F5F5F7"
FONT    = "#1D1D1F"
GRID    = "#E8E8ED"
PAPER   = "#FFFFFF"
S_BORDER= "rgba(0,0,0,0.08)"
S_MUTED = "#86868B"

COMP_C = {"Sanitas": ACCENT, "Adeslas": "#B71C1C", "Asisa": "#2E7D32",
           "DKV": "#E65100", "Mapfre Salud": "#4A148C", "AXA Salud": "#37474F"}

# ══════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Sanitas · Inteligencia Corporativa",
    page_icon=None, layout="wide", initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# CSS — Apple HIG
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#MainMenu,footer,header{{visibility:hidden}}
[data-testid="stToolbar"]{{display:none}}
[data-testid="column"]{{overflow:visible!important}}
[data-testid="stHorizontalBlock"]{{overflow:visible!important}}
.block-container{{padding:0 2.8rem 4rem!important;max-width:1400px}}
.stApp{{background:#F5F5F7;color:#1D1D1F}}
html,body,[class*="css"]{{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif}}
[data-testid="stSidebar"]{{display:block!important;visibility:visible!important;transform:none!important;
  width:17rem!important;background:#EEF4FF!important;border-right:1px solid #C0D5F0!important;
  box-shadow:2px 0 12px rgba(0,48,135,.06)!important}}
[data-testid="stSidebar"] *:not(button):not(button *){{color:#1D1D1F!important;font-family:'Inter',sans-serif!important}}
[data-testid="stSidebar"] button{{font-family:'Inter',sans-serif!important}}
[data-testid="stSidebar"] label{{color:{ACCENT}!important;font-size:.62rem!important;
  letter-spacing:.08em;text-transform:uppercase;font-weight:600!important;margin-bottom:4px!important}}
[data-testid="stSidebar"] [data-baseweb="select"]{{background:#DEEAF8!important;
  border:1px solid #A8C4E0!important;border-radius:8px!important}}
[data-testid="stSidebar"] [data-baseweb="select"] *{{background:#DEEAF8!important;
  color:#1D1D1F!important;font-size:.84rem!important}}
[data-testid="stSidebar"] hr{{border-color:#C0D5F0!important;margin:0!important}}
[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
button[kind="header"]{{display:none!important}}
.stButton>button{{background:#FFFFFF;color:#1D1D1F;border:1px solid rgba(0,0,0,.12);
  border-radius:980px;padding:9px 20px;font-size:.8rem;font-weight:500;letter-spacing:.01em;
  box-shadow:0 1px 3px rgba(0,0,0,.06);transition:all .18s ease}}
.stButton>button:hover{{background:#F5F5F7;box-shadow:0 3px 8px rgba(0,0,0,.1);
  border-color:rgba(0,0,0,.18)}}
.stButton>button:active{{transform:scale(.98)}}
[data-testid="stSidebar"] .stButton>button{{
  background:transparent!important;color:#374151!important;border:1px solid transparent!important;
  border-radius:10px!important;width:100%!important;text-align:left!important;
  padding:10px 14px!important;font-size:.84rem!important;font-weight:500!important;
  box-shadow:none!important;letter-spacing:.01em!important;margin-bottom:2px!important;
  transition:all .15s ease!important}}
[data-testid="stSidebar"] .stButton>button:hover{{
  background:rgba(0,48,135,.1)!important;color:{ACCENT}!important;
  border-color:rgba(0,48,135,.2)!important;box-shadow:none!important}}
.top-bar{{background:transparent;padding:20px 0 0;display:grid;
  grid-template-columns:1fr auto 1fr;align-items:center;
  border-bottom:1px solid rgba(0,0,0,.06);margin-bottom:2.4rem}}
.top-bar-center{{text-align:center}}
.top-title{{font-size:1.15rem;font-weight:600;color:#1D1D1F;letter-spacing:-.01em}}
.top-sub{{font-size:.78rem;color:#86868B;letter-spacing:.02em}}
.section-title{{font-size:.68rem;font-weight:600;color:#86868B;letter-spacing:.1em;
  text-transform:uppercase;margin-bottom:14px;margin-top:4px}}
.kpi-card{{background:#FFFFFF;border:none;border-radius:16px;padding:22px 24px;
  box-shadow:0 2px 12px rgba(0,0,0,.07),0 0 0 0.5px rgba(0,0,0,.04);
  transition:box-shadow .2s ease,transform .2s ease}}
.kpi-card:hover{{box-shadow:0 6px 20px rgba(0,0,0,.1),0 0 0 0.5px rgba(0,0,0,.04);
  transform:translateY(-1px)}}
.kpi-label{{font-size:.62rem;letter-spacing:.07em;text-transform:uppercase;
  color:#86868B;margin-bottom:10px;font-weight:500}}
.kpi-value{{font-size:2.1rem;font-weight:700;color:#1D1D1F;line-height:1;letter-spacing:-.03em}}
.kpi-sub{{font-size:.72rem;color:{ACCENT};margin-top:8px;font-weight:500}}
.kpi-neg{{font-size:.72rem;color:#FF3B30;margin-top:8px;font-weight:500}}
.stTabs [data-baseweb="tab-list"]{{gap:0;border-bottom:1px solid #C0D5F0;
  background:transparent;padding:0 2px;margin-bottom:1.6rem}}
.stTabs [data-baseweb="tab"]{{font-size:.78rem;color:#86868B;padding:10px 18px;
  border:none;border-bottom:2px solid transparent;background:transparent!important;
  font-weight:500;letter-spacing:.01em;transition:color .15s,border-color .15s;margin-bottom:-1px}}
.stTabs [aria-selected="true"]{{color:{ACCENT}!important;background:transparent!important;
  font-weight:600!important;border-bottom:2px solid {ACCENT}!important;box-shadow:none!important}}
.stTabs [data-baseweb="tab-panel"]{{padding-top:1.4rem}}
[data-testid="stExpander"]{{border:none!important;border-radius:14px!important;
  background:#FFFFFF!important;box-shadow:0 2px 10px rgba(0,0,0,.06),0 0 0 0.5px rgba(0,0,0,.04)!important;
  margin-bottom:10px!important}}
[data-testid="stExpander"] summary{{font-size:.85rem;font-weight:500;color:#1D1D1F;padding:14px 18px}}
.chart-label{{font-size:.64rem;letter-spacing:.07em;text-transform:uppercase;
  color:#86868B;margin-bottom:8px;font-weight:600}}
.callout{{background:#EEF4FF;border-radius:12px;border-left:3px solid {ACCENT};
  padding:14px 18px;margin:14px 0 4px;font-size:.79rem;color:#1D1D1F;line-height:1.65;
  box-shadow:0 1px 6px rgba(0,0,0,.06),0 0 0 0.5px rgba(0,0,0,.04)}}
.callout strong{{color:#1D1D1F}}
hr{{border:none;border-top:1px solid rgba(0,0,0,.06);margin:2rem 0}}
[data-baseweb="select"] [data-baseweb="input"]{{border-radius:10px!important}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def lay(h=None, showlegend=False, legend=None, margin=None):
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter,-apple-system,sans-serif", color=FONT, size=11),
        margin=margin or dict(t=28, b=18, l=8, r=36),
        showlegend=showlegend,
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False),
        yaxis=dict(showgrid=False, gridcolor=GRID, zeroline=False),
    )
    if legend: d["legend"] = legend
    if h:      d["height"] = h
    return d

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def kpi_card(col, label, value, sub=None, negative=False):
    sub_cls = "kpi-neg" if negative else "kpi-sub"
    sub_html = f'<div class="{sub_cls}">{sub}</div>' if sub else ""
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True)

def callout(text):
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)

def go_to(page):
    st.session_state["page"] = page

# ══════════════════════════════════════════════════════════════════
# DATOS FICTICIOS
# ══════════════════════════════════════════════════════════════════
np.random.seed(42)
MESES = pd.date_range("2025-01", "2026-09", freq="MS")
CCAA_LIST = ["Madrid","Cataluña","Andalucía","C. Valenciana","País Vasco",
             "Galicia","Aragón","Murcia","Navarra","Baleares","Canarias",
             "Castilla y León","Castilla-La Mancha","Extremadura","La Rioja",
             "Asturias","Cantabria"]

# ── Ejecutiva ──────────────────────────────────────────────────
df_cr = pd.DataFrame({
    "mes": MESES,
    "loss_ratio": [80.2,79.8,81.1,78.9,80.5,79.2,82.3,78.6,79.8,81.2,
                   80.1,79.5,78.9,79.8,80.2,79.1,78.8,79.3,80.1,78.9,79.3],
    "expense_ratio": [15.2,15.1,14.9,15.0,14.8,14.9,15.1,14.8,14.9,15.0,
                      14.8,14.7,14.9,14.8,15.0,14.8,14.7,14.9,14.8,14.7,14.9],
})
df_cr["combined"] = df_cr["loss_ratio"] + df_cr["expense_ratio"]

df_ebitda = pd.DataFrame({
    "linea":  ["Seguros Salud","Hospitales","Dental","Residencias","Blua Digital"],
    "ebitda": [98, 62, 18, 12, -4],
    "margen": [8.2, 12.4, 15.6, 6.8, -12.1],
    "color":  [ACCENT, A2, A3, "#2E7D32", "#E65100"],
})

df_port = pd.DataFrame({
    "mes": MESES,
    "altas": np.random.randint(18000, 28000, len(MESES)),
    "bajas": np.random.randint(14000, 22000, len(MESES)),
})
df_port["neto"] = df_port["altas"] - df_port["bajas"]

df_cuotas = pd.DataFrame({
    # Fuente: UNESPA — primas emitidas ramo salud, cierre diciembre 2025 (El Español / Invertia, feb 2026)
    # Adeslas 4.127M€ (+16.3%), Sanitas 2.242M€ (+11.2%), Asisa 1.835M€ (+21.2%), Mapfre 858M€, DKV 835M€ (-9.4% Muface)
    "aseguradora": ["Adeslas","Sanitas","Asisa","DKV","Mapfre Salud","AXA Salud","Otros"],
    "cuota":       [30.7, 16.7, 13.7, 6.2, 6.4, 5.7, 20.6],
    "color":       ["#B71C1C", ACCENT,"#2E7D32","#E65100","#4A148C","#37474F","#9E9E9E"],
})

df_nps = pd.DataFrame({
    "segmento": ["Premium 500K","Profesionales","Más Salud","Familiar","Básica","Senior Único"],
    "nps":      [71, 58, 46, 43, 35, 28],
    "n_miles":  [12.4, 38.6, 284, 510, 342, 98],
})

# ── Retención ─────────────────────────────────────────────────
df_tipos = pd.DataFrame({
    "tipo":       ["Completa","Familiar","Básica","Autónomo","Reembolso","Senior"],
    "asegurados": [890000, 510000, 342000, 168000, 134000, 98000],
    "loss_ratio": [71, 72, 58, 65, 52, 88],
    "margen":     [71, 65, 62, 74, 78, 44],
    "color":      [ACCENT, "#2E7D32", A3, "#6A1B9A", "#BF360C", "#E65100"],
})

df_antiguedad = pd.DataFrame({
    "rango":       ["< 1 año","1-3 años","3-5 años","5-10 años","> 10 años"],
    "asegurados":  [285000, 412000, 380000, 520000, 545000],
    "churn_rate":  [18.2, 12.4, 7.8, 4.2, 1.8],
})

df_razones = pd.DataFrame({
    "razon": ["Subida precio en renovación","Médico favorito abandonó cuadro",
              "Mudanza — red insuficiente en destino","Oferta más económica competencia",
              "Mala experiencia de servicio","Reducción de ingresos (económico)","Otros"],
    "pct": [34.2, 18.6, 14.8, 13.4, 10.2, 6.4, 2.4],
}).sort_values("pct")

scores_raw = np.concatenate([
    np.random.normal(18, 9, 1392),
    np.random.normal(55, 11, 535),
    np.random.normal(83, 7, 215),
])
scores_raw = np.clip(scores_raw, 0, 100)

COHORT_YEARS = ["2020","2021","2022","2023","2024","2025"]
COHORT_M     = ["Mes 1","Mes 3","Mes 6","Mes 12","Mes 24","Mes 36"]
cohort_ret   = np.array([
    [100, 94, 91, 88, 83, 79],
    [100, 93, 90, 86, 81, np.nan],
    [100, 94, 91, 87, 82, np.nan],
    [100, 92, 88, 84, np.nan, np.nan],
    [100, 93, 89, np.nan, np.nan, np.nan],
    [100, 91, np.nan, np.nan, np.nan, np.nan],
], dtype=float)

df_rentab = pd.DataFrame({
    "segmento":   ["Senior Único","Básica","Completa","Familiar","Autónomo","Reembolso"],
    "loss_ratio": [88, 58, 71, 72, 65, 52],
    "precio_med": [48.10, 27.85, 58.15, 60.53, 57.10, 85.22],
    "margen_idx": [44, 62, 71, 65, 74, 78],
})

# ── Operaciones ───────────────────────────────────────────────
PROD_LIST = ["Accede","Avanza","Más Salud Óptima","Más Salud Plus","Más Salud",
             "Familiar","Autónomo Óptima","Senior Único","Reembolso"]
lr_base   = np.array([42, 50, 62, 65, 68, 72, 58, 88, 54])
lr_matrix = np.clip(
    np.array([lr_base + np.random.normal(0, 4, len(PROD_LIST)) for _ in CCAA_LIST]),
    28, 108
)

df_centros = pd.DataFrame({
    "centro":         ["H. La Zarzuela (MAD)","H. La Moraleja (MAD)","H. Cima (BCN)",
                       "H. Ntra. Sra. Rosario (MAD)","H. Vitoria"],
    "camas_pct":      [87, 79, 82, 74, 71],
    "qx_pct":         [92, 84, 88, 78, 73],
    "espera_dias":    [8, 11, 9, 14, 12],
    "readmision_pct": [4.2, 3.8, 4.1, 5.2, 4.8],
})

df_espera = pd.DataFrame({
    "especialidad":   ["Traumatología","Cardiología","Dermatología","Ginecología",
                       "Neurología","Oftalmología","Oncología","Pediatría","Psiquiatría","Urología"],
    "sanitas":        [8, 12, 21, 6, 18, 15, 4, 3, 35, 9],
    "sector":         [12, 18, 28, 9, 24, 20, 6, 5, 42, 13],
    "objetivo":       [7, 10, 15, 5, 15, 12, 3, 3, 28, 8],
})

df_deriv = pd.DataFrame({
    "especialidad":   ["Neurocirugía","Cirugía robótica","Medicina nuclear",
                       "Radioterapia","Genética clínica","Otros"],
    "volumen_mes":    [340, 128, 89, 212, 67, 890],
    "coste_medio":    [4800, 6200, 1800, 3400, 2200, 890],
})
df_deriv["coste_total"] = df_deriv["volumen_mes"] * df_deriv["coste_medio"] / 1000

df_fraude = pd.DataFrame({
    "tipo":       ["Actos no realizados","Duplicidad de reclamación","Inflado de costes",
                   "Identidad suplantada","Proveedor ficticio","Otros"],
    "casos":      [23, 18, 31, 8, 4, 12],
    "importe_k":  [27.6, 15.3, 86.8, 27.2, 35.6, 7.8],
    "color":      [A2, A3, ACCENT, "#B71C1C", "#E65100", S_MUTED],
})

# ── Comercial ─────────────────────────────────────────────────
VEC = pd.DataFrame([
    # renta: INE Contabilidad Regional 2024 — PIB per cápita euros/hab, índice PV=100 (Madrid 44.755€, PV 41.016€)
    # penetracion: IDIS Observatorio Sector Sanitario Privado 2026 (datos 2025, % pobl. con seguro privado)
    # autonomo: INE EPA 2024 (% activos que son autónomos)
    {"ccaa":"Madrid",           "renta":109,"penetracion":37,"enfermedad":58,"acceso":82,"turismo":82,"deporte":68,"autonomo":21,"lat":40.42,"lon":-3.70},
    {"ccaa":"Cataluña",         "renta":91, "penetracion":31,"enfermedad":61,"acceso":78,"turismo":98,"deporte":72,"autonomo":20,"lat":41.39,"lon":2.16},
    {"ccaa":"País Vasco",       "renta":100,"penetracion":24,"enfermedad":54,"acceso":84,"turismo":48,"deporte":74,"autonomo":14,"lat":43.26,"lon":-2.93},
    {"ccaa":"Navarra",          "renta":95, "penetracion":20,"enfermedad":52,"acceso":80,"turismo":36,"deporte":76,"autonomo":14,"lat":42.82,"lon":-1.64},
    {"ccaa":"Baleares",         "renta":88, "penetracion":30,"enfermedad":50,"acceso":74,"turismo":94,"deporte":70,"autonomo":22,"lat":39.57,"lon":2.65},
    {"ccaa":"Aragón",           "renta":89, "penetracion":18,"enfermedad":56,"acceso":62,"turismo":30,"deporte":62,"autonomo":14,"lat":41.65,"lon":-0.88},
    {"ccaa":"C. Valenciana",    "renta":67, "penetracion":20,"enfermedad":60,"acceso":72,"turismo":86,"deporte":61,"autonomo":18,"lat":39.47,"lon":-0.38},
    {"ccaa":"Andalucía",        "renta":60, "penetracion":16,"enfermedad":64,"acceso":60,"turismo":72,"deporte":55,"autonomo":16,"lat":37.38,"lon":-5.97},
    {"ccaa":"Murcia",           "renta":65, "penetracion":13,"enfermedad":62,"acceso":64,"turismo":52,"deporte":57,"autonomo":16,"lat":37.99,"lon":-1.13},
    {"ccaa":"Canarias",         "renta":63, "penetracion":22,"enfermedad":58,"acceso":58,"turismo":96,"deporte":58,"autonomo":17,"lat":28.29,"lon":-15.65},
    {"ccaa":"Galicia",          "renta":74, "penetracion":17,"enfermedad":68,"acceso":60,"turismo":42,"deporte":54,"autonomo":15,"lat":42.88,"lon":-8.54},
    {"ccaa":"Castilla y León",  "renta":75, "penetracion":14,"enfermedad":70,"acceso":54,"turismo":28,"deporte":52,"autonomo":13,"lat":41.65,"lon":-4.73},
    {"ccaa":"Castilla-La Mancha","renta":64,"penetracion":11,"enfermedad":66,"acceso":50,"turismo":18,"deporte":48,"autonomo":13,"lat":39.86,"lon":-4.03},
    {"ccaa":"Extremadura",      "renta":62, "penetracion":9, "enfermedad":62,"acceso":44,"turismo":14,"deporte":44,"autonomo":12,"lat":38.92,"lon":-6.34},
    {"ccaa":"La Rioja",         "renta":83, "penetracion":17,"enfermedad":54,"acceso":70,"turismo":22,"deporte":64,"autonomo":15,"lat":42.27,"lon":-2.37},
    {"ccaa":"Asturias",         "renta":72, "penetracion":15,"enfermedad":72,"acceso":64,"turismo":30,"deporte":60,"autonomo":13,"lat":43.36,"lon":-5.85},
    {"ccaa":"Cantabria",        "renta":73, "penetracion":16,"enfermedad":60,"acceso":68,"turismo":32,"deporte":63,"autonomo":13,"lat":43.18,"lon":-3.99},
])
VEC["score_oportunidad"] = (
    (100 - VEC["penetracion"]) * 0.35 +
    VEC["renta"] * 0.25 +
    VEC["enfermedad"] * 0.20 +
    VEC["turismo"] * 0.10 +
    VEC["deporte"] * 0.10
).round(1)
VEC["score_rentabilidad"] = (
    VEC["renta"] * 0.40 +
    (100 - VEC["enfermedad"]) * 0.35 +
    VEC["acceso"] * 0.25
).round(1)
VEC["score_global"] = (VEC["score_oportunidad"] * 0.5 + VEC["score_rentabilidad"] * 0.5).round(1)

def classify(row):
    if row["score_oportunidad"] >= 55 and row["score_rentabilidad"] >= 55:
        return "Prioridad máxima"
    elif row["score_oportunidad"] >= 55:
        return "Crecer con cautela"
    elif row["score_rentabilidad"] >= 55:
        return "Consolidar y rentabilizar"
    return "Revisar estrategia"
VEC["cuadrante"] = VEC.apply(classify, axis=1)

df_funnel = pd.DataFrame({
    "etapa":   ["Visitas web/app","Lead generado","Cotización","Comparación activa",
                "Contrato iniciado","Alta efectiva"],
    "volumen": [168400, 128600, 96400, 72800, 52400, 36200],
})

df_cuota_ccaa = pd.DataFrame({
    "ccaa":    CCAA_LIST,
    "Sanitas": [22.4,19.8,12.6,16.2,24.1,11.8,14.2,13.8,26.4,21.6,14.8,13.2,10.6,8.4,18.2,15.6,19.4],
    "Adeslas": [26.2,22.4,28.1,24.8,18.6,21.4,19.8,22.6,16.2,20.4,22.8,20.4,24.2,22.6,20.4,22.8,21.6],
    "Asisa":   [12.8,14.2,18.6,16.4,10.2,16.8,14.6,18.2,12.4,11.8,16.2,14.8,18.4,16.2,14.6,16.4,14.8],
})

df_precios_comp = pd.DataFrame({
    "poliza":   ["Básica","Completa","Familiar","Autónomo","Senior","Reembolso"],
    "Sanitas":  [22.10, 50.00, 53.35, 51.40, 48.10, 76.45],
    "Adeslas":  [19.80, 48.60, 51.20, 49.80, 44.20, 72.80],
    "Asisa":    [21.40, 51.20, 54.60, 52.80, 46.40, 78.20],
    "DKV":      [18.90, 45.80, 48.60, 47.20, 42.80, 69.60],
})

POLIZAS = [
    {"poliza":"Accede",             "precio":22.10,"tipo":"Básica",   "margen":82,"loss":28},
    {"poliza":"Avanza",             "precio":33.60,"tipo":"Básica",   "margen":76,"loss":32},
    {"poliza":"Más Salud Óptima",   "precio":38.88,"tipo":"Completa", "margen":68,"loss":44},
    {"poliza":"Más Salud Plus",     "precio":50.00,"tipo":"Completa", "margen":72,"loss":40},
    {"poliza":"Más Salud Fam.Plus", "precio":53.35,"tipo":"Familiar", "margen":65,"loss":48},
    {"poliza":"Más Salud",          "precio":66.31,"tipo":"Completa", "margen":70,"loss":42},
    {"poliza":"Más Salud Familias", "precio":67.72,"tipo":"Familiar", "margen":67,"loss":46},
    {"poliza":"Único",              "precio":48.10,"tipo":"Senior",   "margen":44,"loss":72},
    {"poliza":"Profesionales Ópt.", "precio":38.90,"tipo":"Autónomo", "margen":71,"loss":38},
    {"poliza":"Profesionales Plus", "precio":51.40,"tipo":"Autónomo", "margen":74,"loss":36},
    {"poliza":"Profesionales",      "precio":81.00,"tipo":"Autónomo", "margen":75,"loss":35},
    {"poliza":"Más 90.000",         "precio":76.45,"tipo":"Reembolso","margen":78,"loss":38},
    {"poliza":"Premium 500.000",    "precio":94.00,"tipo":"Reembolso","margen":80,"loss":34},
]
df_pol = pd.DataFrame(POLIZAS)
TYPE_C = {"Básica":A3,"Completa":ACCENT,"Familiar":"#2E7D32",
           "Senior":"#E65100","Autónomo":"#6A1B9A","Reembolso":"#BF360C"}

CCAA_VEC_D = {r["ccaa"]: r for _, r in VEC.iterrows()}
def rent_score(pol, ccaa_data):
    m = pol["margen"]/100; l = 1 - pol["loss"]/100; r = ccaa_data["renta"]/100
    t = pol["tipo"]
    if t == "Básica":    fit = ccaa_data["autonomo"]/100*.3 + r*.4 + (1-ccaa_data["enfermedad"]/100)*.3
    elif t == "Completa": fit = r*.4 + ccaa_data["penetracion"]/100*.35 + (1-ccaa_data["enfermedad"]/100)*.25
    elif t == "Familiar": fit = r*.35 + ccaa_data["penetracion"]/100*.35 + ccaa_data["deporte"]/100*.3
    elif t == "Senior":   fit = ccaa_data["enfermedad"]/100*.5 + r*.5
    elif t == "Autónomo": fit = ccaa_data["autonomo"]/100*.5 + r*.4 + ccaa_data["deporte"]/100*.1
    else:                 fit = r*.5 + ccaa_data["turismo"]/100*.3 + ccaa_data["autonomo"]/100*.2
    return round((m*.35 + l*.30 + fit*.35)*100, 1)

ccaa_list_v = list(CCAA_VEC_D.keys())
heat_mat = []
for _, pr in df_pol.iterrows():
    heat_mat.append([rent_score(pr, CCAA_VEC_D[c]) for c in ccaa_list_v])

# ── Colectivos & Empresas ────────────────────────────────────
df_col = pd.DataFrame([
    # ── Renovar (LR < 85%) — cartera rentable ────────────────
    {"empresa":"Amazon ES",          "sector":"Logística/Tech",   "asegurados":4820,"prima":48.40,"gasto":29.20,"años":3, "renovacion":"Jun 2027"},
    {"empresa":"Indra/Minsait",      "sector":"Tecnología",       "asegurados":1820,"prima":67.40,"gasto":44.40,"años":6, "renovacion":"Dic 2026"},
    {"empresa":"Vueling",            "sector":"Aviación",         "asegurados":2640,"prima":54.20,"gasto":38.60,"años":4, "renovacion":"Sep 2027"},
    {"empresa":"Inditex",            "sector":"Moda/Retail",      "asegurados":9200,"prima":44.20,"gasto":33.60,"años":5, "renovacion":"Mar 2026"},
    {"empresa":"Iberdrola",          "sector":"Energía",          "asegurados":2940,"prima":63.80,"gasto":50.40,"años":4, "renovacion":"Feb 2027"},
    {"empresa":"Telefónica",         "sector":"Telecomunicaciones","asegurados":6840,"prima":56.20,"gasto":44.60,"años":9, "renovacion":"Sep 2026"},
    {"empresa":"Ferrovial",          "sector":"Construcción",     "asegurados":2840,"prima":57.40,"gasto":46.00,"años":6, "renovacion":"Ene 2027"},
    {"empresa":"Endesa",             "sector":"Energía",          "asegurados":4210,"prima":54.80,"gasto":44.80,"años":12,"renovacion":"Jun 2026"},
    {"empresa":"Naturgy",            "sector":"Energía",          "asegurados":1960,"prima":65.20,"gasto":53.80,"años":8, "renovacion":"Ago 2026"},
    {"empresa":"Repsol",             "sector":"Energía",          "asegurados":3680,"prima":61.40,"gasto":51.00,"años":6, "renovacion":"Dic 2026"},
    {"empresa":"Santander",          "sector":"Banca",            "asegurados":6240,"prima":69.80,"gasto":58.60,"años":10,"renovacion":"Dic 2025"},
    # ── Subir tasa (LR 85–100%) — rentable con ajuste ────────
    {"empresa":"Mahou San Miguel",   "sector":"Alimentación",     "asegurados":1840,"prima":58.20,"gasto":50.80,"años":8, "renovacion":"Mar 2027"},
    {"empresa":"El Corte Inglés",    "sector":"Retail",           "asegurados":8420,"prima":46.60,"gasto":41.20,"años":15,"renovacion":"Ene 2027"},
    {"empresa":"Mercadona",          "sector":"Retail",           "asegurados":12400,"prima":42.40,"gasto":37.60,"años":7,"renovacion":"Oct 2026"},
    {"empresa":"BBVA",               "sector":"Banca",            "asegurados":5120,"prima":68.40,"gasto":61.60,"años":11,"renovacion":"Abr 2026"},
    {"empresa":"CaixaBank",          "sector":"Banca",            "asegurados":7840,"prima":71.20,"gasto":65.40,"años":14,"renovacion":"May 2026"},
    {"empresa":"ACS",                "sector":"Construcción",     "asegurados":3420,"prima":52.80,"gasto":48.40,"años":2, "renovacion":"Nov 2026"},
    {"empresa":"Renfe",              "sector":"Transporte",       "asegurados":5480,"prima":47.80,"gasto":44.40,"años":9, "renovacion":"Abr 2027"},
    # ── No renovar / renegociar (LR > 100%) — revisión necesaria ─
    {"empresa":"Acciona",            "sector":"Construcción",     "asegurados":2180,"prima":59.60,"gasto":62.40,"años":3, "renovacion":"Jul 2027"},
    {"empresa":"Mapfre (empleados)", "sector":"Seguros",          "asegurados":1480,"prima":62.80,"gasto":66.80,"años":5, "renovacion":"Mar 2026"},
])
df_col["loss_ratio"]  = (df_col["gasto"] / df_col["prima"] * 100).round(1)
df_col["margen_mes"]  = ((df_col["prima"] - df_col["gasto"]) * df_col["asegurados"]).round(0)
df_col["margen_anual"]= (df_col["margen_mes"] * 12 / 1000).round(1)
df_col["ingreso_anual"]=(df_col["prima"] * df_col["asegurados"] * 12 / 1000).round(1)

VINC_DATA = {
    "Amazon ES":          {"products": ["Dental","Psico"],                           "score": 2},
    "Indra/Minsait":      {"products": ["Dental","VIP Dir.","Psico"],                "score": 3},
    "Vueling":            {"products": ["Dental","Accidentes"],                      "score": 2},
    "Inditex":            {"products": ["Dental","VIP Dir.","Vida"],                 "score": 3},
    "Iberdrola":          {"products": ["Dental","VIP Dir.","Vida"],                 "score": 3},
    "Telefónica":         {"products": ["Dental","VIP Dir.","Vida","Psico","Fisio"], "score": 5},
    "Ferrovial":          {"products": ["Dental","Accidentes","Fisio"],              "score": 3},
    "Endesa":             {"products": ["Dental","VIP Dir.","Vida","Accidentes"],    "score": 4},
    "Naturgy":            {"products": ["Dental","VIP Dir.","Vida"],                 "score": 3},
    "Repsol":             {"products": ["Dental","VIP Dir.","Accidentes"],           "score": 3},
    "Santander":          {"products": ["Dental","VIP Dir.","Vida","Psico"],         "score": 4},
    "Mahou San Miguel":   {"products": ["Dental"],                                   "score": 1},
    "El Corte Inglés":    {"products": ["Dental","VIP Dir.","Fisio"],                "score": 3},
    "Mercadona":          {"products": ["Dental"],                                   "score": 1},
    "BBVA":               {"products": ["Dental","VIP Dir.","Vida","Psico"],         "score": 4},
    "CaixaBank":          {"products": ["Dental","VIP Dir.","Vida","Psico","Fisio"], "score": 5},
    "ACS":                {"products": ["Accidentes"],                               "score": 1},
    "Renfe":              {"products": ["Dental","Accidentes"],                      "score": 2},
    "Acciona":            {"products": ["Dental"],                                   "score": 1},
    "Mapfre (empleados)": {"products": ["Dental","VIP Dir.","Vida"],                 "score": 3},
}
VINC_PROD_C = {
    "Dental":     "#0891B2",
    "VIP Dir.":   "#003087",
    "Vida":       "#1B6B4A",
    "Psico":      "#6A1B9A",
    "Fisio":      "#D4940A",
    "Accidentes": "#C2410C",
}

df_col["score_vinc"]    = df_col["empresa"].map(lambda e: VINC_DATA.get(e, {}).get("score", 0))
df_col["productos_vinc"]= df_col["empresa"].map(lambda e: VINC_DATA.get(e, {}).get("products", []))

def decision(lr, score_vinc=0):
    if lr < 85:   return "Renovar",                "#1B6B4A", "●"
    if lr < 100:  return "Subir tasa",             "#D4940A", "◐"
    if score_vinc >= 2: return "Renegociar",       "#6A1B9A", "◑"
    return "No renovar / renegociar",              "#9B2C2C", "●"

df_col[["decision","dec_color","dec_dot"]] = pd.DataFrame(
    df_col.apply(lambda r: decision(r["loss_ratio"], r["score_vinc"]), axis=1).tolist(),
    index=df_col.index
)

# ── Epidemiología & Eventos cíclicos ─────────────────────────
EPI_LAT = [40.42,41.39,37.38,39.47,43.26,42.88,41.65,37.99,42.82,39.57,28.29,41.65,39.86,38.92,42.27,43.36,43.18]
EPI_LON = [-3.70,2.16,-5.97,-0.38,-2.93,-8.54,-0.88,-1.13,-1.64,2.65,-15.65,-4.73,-4.03,-6.34,-2.37,-5.85,-3.99]
EPI_NOM = ["Madrid","Cataluña","Andalucía","C. Valenciana","País Vasco","Galicia","Aragón",
           "Murcia","Navarra","Baleares","Canarias","Castilla y León","Castilla-La Mancha",
           "Extremadura","La Rioja","Asturias","Cantabria"]

df_epi = pd.DataFrame({
    "ccaa": EPI_NOM, "lat": EPI_LAT, "lon": EPI_LON,
    # INE ENSE 2022 — Encuesta Nacional de Salud, prevalencia en adultos (%)
    # orden: Madrid,Cataluña,Andalucía,C.Valenciana,País Vasco,Galicia,Aragón,Murcia,Navarra,Baleares,Canarias,CyL,CLM,Extremadura,La Rioja,Asturias,Cantabria
    "diabetes_pct":    [7.4, 7.1, 9.8, 8.2, 6.4, 8.6, 7.8, 9.2, 6.8, 7.2,10.4, 8.4, 9.6,10.8, 7.6, 8.8, 7.8],
    "hta_pct":         [18.4,20.2,25.6,22.4,19.2,23.8,21.6,24.2,18.8,17.4,22.8,23.4,24.6,27.2,21.2,23.6,20.8],
    "epoc_pct":        [3.8, 3.6, 4.8, 4.2, 3.4, 4.6, 4.0, 4.4, 3.2, 3.6, 4.2, 4.8, 5.0, 5.4, 3.8, 4.4, 4.0],
    "obesidad_pct":    [16.2,14.8,22.4,18.6,15.4,19.8,17.2,20.4,15.8,16.4,22.8,19.4,21.6,24.2,17.6,19.2,17.8],
    "salud_mental_pct":[11.4,10.8,15.2,13.2, 9.8,14.6,12.4,13.8, 9.6,11.2,16.4,14.2,16.8,18.2,11.8,14.4,12.8],
    # Registro Nacional de Tumores + REDECAN (índice, 100=media nacional)
    "oncologia_idx":   [88,  84,  94,  88,  78,  92,  86,  90,  80,  82,  96,  92,  96,  98,  84,  90,  86],
    # Ministerio de Sanidad SIAE dic.2025 — días medios de espera quirúrgica estructural por CCAA
    "espera_pub_dias": [50, 142, 173,  88,  64,  73, 132, 103,  96, 105, 106,  93,  92, 135,  78,  91, 137],
    # IDIS Observatorio Sector Sanitario Privado 2026 (datos 2025) — % población con seguro privado
    "penetracion_seg": [37.3,31.0,15.5,19.5,24.0,17.0,18.0,13.3,20.0,30.1,22.0,14.0,11.0, 9.5,17.0,15.5,16.0],
    # INE EPA 2024 — % trabajadores autónomos sobre activos totales
    "autonomos_pct":   [20.8,19.6,15.8,17.8,14.2,14.8,14.4,16.4,13.8,22.4,17.2,13.0,12.6,11.8,14.6,12.8,13.2],
    # INE Padrón Municipal 2024 — % población 35-54 años sobre total
    "pob_35_54_pct":   [28.6,27.4,25.2,25.8,27.8,24.8,26.8,25.4,27.2,26.4,25.0,24.6,24.4,23.6,26.6,25.8,25.6],
})

# ── Nuevas columnas: enfermedades crónicas detalladas ─────────
# IAMRICOR + Ministerio Sanidad 2024 — Insuficiencia Cardiaca diagnosticada (%)
df_epi["card_ic_pct"]  = [1.8,1.6,2.2,1.9,1.4,2.1,1.7,2.0,1.5,1.6,2.3,2.1,2.4,2.6,1.8,2.0,1.8]
# Registro RESCATE — antecedentes de IAM (%)
df_epi["card_iam_pct"] = [2.8,2.6,3.4,3.0,2.4,3.2,2.8,3.2,2.6,2.7,3.4,3.2,3.6,3.8,2.8,3.1,2.9]
# INE ENSE 2022 — Dislipemia / Colesterol elevado diagnosticado (%)
df_epi["dlp_pct"]      = [17.8,16.4,22.4,19.2,15.8,20.6,18.4,21.2,16.2,16.8,21.8,20.8,22.6,24.2,17.6,20.2,18.8]
# SEPAR + INE ENSE 2022 — Asma diagnosticada (%)
df_epi["asma_pct"]     = [5.8, 5.4, 6.8, 6.2, 5.2, 6.4, 5.6, 6.4, 4.8, 5.6, 7.2, 6.6, 7.0, 7.4, 5.8, 6.4, 6.0]
# INE ENSE 2022 — Lumbalgia crónica (%)
df_epi["lumbar_pct"]   = [17.2,15.8,21.4,18.8,15.4,20.2,18.0,20.4,16.2,17.4,21.6,20.8,22.2,24.6,17.8,19.8,18.4]
# INE ENSE 2022 — Artrosis diagnosticada (%)
df_epi["artrosis_pct"] = [13.4,11.8,18.2,15.6,11.2,17.4,14.2,16.8,11.6,13.0,17.6,16.8,18.4,20.8,13.8,16.4,14.6]

DISEASE_CATS = {
    "Riesgo Cardiovascular": {
        "Cardiopatía — IC (Insuf. Cardiaca) %":  "card_ic_pct",
        "Cardiopatía — IAM (Infarto) %":         "card_iam_pct",
        "HTA — Hipertensión Arterial %":         "hta_pct",
        "DLP — Dislipemia (Colesterol) %":       "dlp_pct",
        "Obesidad %":                            "obesidad_pct",
    },
    "Respiratorio": {
        "EPOC %":                                "epoc_pct",
        "Asma %":                                "asma_pct",
    },
    "Musculoesquelético": {
        "Dolor Lumbar Crónico %":                "lumbar_pct",
        "Artrosis %":                            "artrosis_pct",
    },
    "Salud Mental": {
        "Salud Mental (Depresión/Ansiedad) %":   "salud_mental_pct",
    },
    "Indicadores Comerciales": {
        "Índice Oncológico":                     "oncologia_idx",
        "Espera sanidad pública (días)":         "espera_pub_dias",
        "Penetración seguro privado %":          "penetracion_seg",
        "Tasa de Autónomos %":                   "autonomos_pct",
        "Población 35–54 años %":                "pob_35_54_pct",
    },
}

EPI_DESC2 = {
    "card_ic_pct":      ("Insuf. Cardiaca diagnosticada · Ministerio Sanidad / IAMRICOR 2024", "IC correlaciona con readmisiones y gasto hospitalario. País Vasco y Navarra: menor prevalencia por mejor adherencia."),
    "card_iam_pct":     ("IAM histórico · Registro RESCATE / Ministerio Sanidad",              "IAM define el riesgo actuarial más alto en >55 años. Extremadura y Andalucía lideran — ajuste de prima recomendado."),
    "hta_pct":          ("Hipertensos diagnosticados / población · INE ENSE 2022",             "HTA correlaciona con ictus y cardiopatía — driver del loss ratio en >50 años."),
    "dlp_pct":          ("Dislipemia diagnosticada / población adulta · INE ENSE 2022",        "Colesterol elevado: factor de riesgo primario cardiovascular. Loss ratio +12%."),
    "obesidad_pct":     ("IMC >30 / población adulta · INE ENSE 2022",                         "Comorbilidad mayor: diabetes, HTA, apnea. Loss ratio +18% vs. normopeso."),
    "epoc_pct":         ("Prevalencia EPOC · SEPAR / Ministerio Sanidad",                      "Picos invernales de exacerbación. Canarias y Andalucía: mayor prevalencia tabaco."),
    "asma_pct":         ("Asma diagnosticada · SEPAR / INE ENSE 2022",                        "Correlación con pólenes en primavera. Clave para activar Blua alergología antes del pico."),
    "lumbar_pct":       ("Dolor lumbar crónico / patología MSK · INE ENSE 2022",              "Primera causa de baja laboral. Alta utilización de rehabilitación y fisioterapia."),
    "artrosis_pct":     ("Artrosis diagnóstico activo / población adulta · INE ENSE 2022",    "Prevalencia creciente en >55 años. Impacta Ortopedia, Reumatología y coste de prótesis."),
    "salud_mental_pct": ("Trastornos ansiedad/depresión diagnosticados · ENSE / AEN",          "Espera media Sanitas 35 días. Crecimiento post-COVID. NPS muy sensible a tiempos."),
    "oncologia_idx":    ("Incidencia relativa · Registro Nacional de Tumores",                 "Extremadura y CyL lideran incidencia total. Coberturas oncológicas y screening clave."),
    "espera_pub_dias":  ("Lista de espera quirúrgica · Ministerio Sanidad SIAE dic.2025",       "Mayor espera pública → mayor propensión a contratar privado. Argumento comercial directo."),
    "penetracion_seg":  ("Asegurados salud privada / población · IDIS Observatorio 2026",      "Mercado ya explotado = menor oportunidad incremental pero mayor calidad de cartera."),
    "autonomos_pct":    ("Trabajadores cuenta propia / activos · INE EPA Q2 2026",            "Autónomos sin cobertura laboral de empresa. Producto Profesionales: alta propensión."),
    "pob_35_54_pct":    ("Padrón Municipal · INE 2025",                                        "Franja de mayor contratación: ingresos estables, hijos, percepción de riesgo salud."),
}

# ── Series históricas nacionales 2018–2025 (% prevalencia media) ──
EPI_ANOS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
EPI_HIST_BASE = {
    "hta_pct":         [26.2, 26.8, 26.6, 27.0, 27.8, 28.4, 28.8, 29.2],
    "diabetes_pct":    [8.4,  8.6,  8.4,  8.6,  8.8,  9.0,  9.2,  9.4],
    "obesidad_pct":    [20.8, 21.4, 22.0, 22.6, 23.2, 23.8, 24.2, 24.6],
    "salud_mental_pct":[11.8, 12.2, 14.2, 15.4, 14.8, 15.2, 15.6, 16.0],
    "epoc_pct":        [4.2,  4.2,  4.1,  4.2,  4.3,  4.4,  4.4,  4.5],
    "asma_pct":        [6.2,  6.3,  6.3,  6.4,  6.5,  6.6,  6.7,  6.8],
    "lumbar_pct":      [17.2, 17.6, 17.4, 17.8, 18.2, 18.6, 18.8, 19.0],
    "artrosis_pct":    [13.8, 14.2, 14.4, 14.6, 14.8, 15.0, 15.2, 15.4],
    "card_ic_pct":     [1.9,  2.0,  1.9,  2.0,  2.0,  2.1,  2.1,  2.2],
    "card_iam_pct":    [3.0,  3.1,  3.0,  3.1,  3.2,  3.2,  3.3,  3.3],
    "dlp_pct":         [17.2, 17.6, 17.4, 17.8, 18.0, 18.4, 18.6, 18.8],
}

# ── Hiperfrecuentación — benchmark vs real por centro ────────
BENCH_ACTOS = {
    "Radiología":         2.1,
    "Analíticas":         3.8,
    "Consultas externas": 4.2,
    "Urgencias":          0.8,
    "Rehabilitación":     3.1,
    "Ecografías":         1.4,
    "Endoscopias":        0.6,
}
HF_COL_MAP = {
    "Radiología":         "radiologia",
    "Analíticas":         "analiticas",
    "Consultas externas": "consultas",
    "Urgencias":          "urgencias",
    "Rehabilitación":     "rehabilitacion",
    "Ecografías":         "ecografias",
    "Endoscopias":        "endoscopias",
}
df_hiperfrec = pd.DataFrame({
    "centro":        ["H. Madrid Norte","H. Madrid Sur","H. La Moraleja","Clínica BCN Centro",
                      "H. Sevilla","H. Valencia","H. Bilbao","H. A Coruña","H. Zaragoza",
                      "H. Murcia","H. Málaga"],
    "ccaa":          ["Madrid","Madrid","Madrid","Cataluña",
                      "Andalucía","C. Valenciana","País Vasco","Galicia","Aragón",
                      "Murcia","Andalucía"],
    "radiologia":    [2.3, 2.8, 2.1, 2.4, 3.2, 2.4, 2.0, 2.6, 2.2, 2.9, 3.0],
    "analiticas":    [3.9, 5.1, 3.7, 4.2, 4.4, 4.0, 3.8, 4.6, 3.9, 4.8, 4.5],
    "consultas":     [4.8, 4.2, 4.6, 5.0, 5.2, 4.4, 3.9, 4.8, 4.3, 5.0, 5.1],
    "urgencias":     [0.9, 1.1, 0.8, 0.9, 1.2, 0.9, 0.7, 1.0, 0.8, 1.3, 1.2],
    "rehabilitacion":[3.8, 4.2, 3.4, 3.6, 3.9, 3.6, 3.2, 4.0, 3.5, 4.1, 3.8],
    "ecografias":    [1.6, 1.9, 1.5, 1.7, 2.1, 1.7, 1.4, 1.8, 1.5, 2.2, 2.0],
    "endoscopias":   [0.7, 0.8, 0.6, 0.7, 0.9, 0.7, 0.5, 0.8, 0.6, 1.0, 0.9],
})

MESES_N  = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
GRP_CCAA = ["Madrid","Cataluña","Andalucía","País Vasco/Nav.","C. Valenciana","Galicia/Asturias","Castillas","Can./Baleares"]
demand_seas = np.array([
    [72,68,62,58,55,62,58,48,65,68,78,82],
    [68,82,64,60,58,68,72,55,75,70,74,78],
    [64,62,68,82,60,64,78,72,68,62,70,72],
    [68,66,64,62,58,60,88,62,64,66,72,76],
    [62,64,72,82,58,64,78,82,68,64,68,70],
    [64,62,60,58,56,58,82,78,72,62,68,70],
    [70,68,62,58,52,54,56,48,58,64,74,78],
    [72,68,64,60,60,72,92,96,82,68,64,70],
], dtype=float)

df_eventos = pd.DataFrame([
    # impacto: índice 0-100 de presión sobre demanda sanitaria urgente.
    # Metodología: normalizado con gripe=96 (máximo impacto sistémico nacional).
    # Derivado de métrica pública oficial; fuente indicada en campo 'fuente'.
    {"evento":"Temporada gripe",          "mes":1, "dur":3,"ccaa":"Nacional",      "esp":"Respiratorio / Urgencias",  "impacto":96,"tipo":"Estacional","color":"#B71C1C",
     "metrica":"33.000 hosp. + 1.800 fallecidos/temporada",    "fuente":"RENAVE/ISCIII temp. 2024-25"},
    {"evento":"Picos polínicos",          "mes":4, "dur":3,"ccaa":"Nacional",      "esp":"Alergología / Neumología",  "impacto":86,"tipo":"Estacional","color":"#2E7D32",
     "metrica":"8M alérgicos; urgencias resp. +45% en pico",    "fuente":"SEAIC 2024 · REA-UCO"},
    {"evento":"Temporada turística costas","mes":6,"dur":4,"ccaa":"Can./Bal.",     "esp":"Urgencias / Traumatología", "impacto":88,"tipo":"Turismo",    "color":"#2E7D32",
     "metrica":"85M turistas/año en costas; urgencias +30% verano","fuente":"Turespaña 2024 · SNS"},
    {"evento":"Calor extremo",            "mes":7, "dur":3,"ccaa":"Andalucía/Ext.","esp":"Cardio / Urgencias",        "impacto":85,"tipo":"Estacional","color":"#B71C1C",
     "metrica":"2.042 fallecidos atribuibles al calor",         "fuente":"MoMo ISCIII 2024"},
    {"evento":"Ski Pirineos / Sierra N.", "mes":12,"dur":4,"ccaa":"Aragón/Cat.",  "esp":"Traumatología ortopédica",  "impacto":78,"tipo":"Deporte",    "color":ACCENT,
     "metrica":"~30.000 urgencias traumatológicas/temporada",   "fuente":"SEMES / Registros CCAA est."},
    {"evento":"San Fermín",               "mes":7, "dur":1,"ccaa":"Navarra",       "esp":"Traumatología / Cirugía",   "impacto":76,"tipo":"Festivo",    "color":"#E65100",
     "metrica":"~500 atenciones Cruz Roja, ~50 hospitalizados en 9 días","fuente":"Cruz Roja Navarra 2024"},
    {"evento":"Semana Santa",             "mes":4, "dur":1,"ccaa":"Nacional",      "esp":"Traumatología / Urgencias", "impacto":74,"tipo":"Festivo",    "color":"#E65100",
     "metrica":"26 fallecidos, 15,8M desplazamientos",          "fuente":"DGT Semana Santa 2024"},
    {"evento":"Operación Retorno (Ago)",  "mes":8, "dur":1,"ccaa":"Nacional",      "esp":"Accidentes tráfico",        "impacto":72,"tipo":"Estacional","color":"#B71C1C",
     "metrica":"11 fallecidos, 6,9M desplazamientos",           "fuente":"DGT agosto 2026"},
    {"evento":"Fallas Valencia",          "mes":3, "dur":1,"ccaa":"C. Val.",       "esp":"Quemaduras / Urgencias",    "impacto":70,"tipo":"Festivo",    "color":"#E65100",
     "metrica":"~400 atenciones pirotecnia; 88 atend./mascletà","fuente":"Cruz Roja C. Val. est. 2024"},
    {"evento":"Feria de Abril",           "mes":4, "dur":1,"ccaa":"Andalucía",     "esp":"Digestivo / Urgencias",     "impacto":68,"tipo":"Festivo",    "color":"#E65100",
     "metrica":"~1.200 atenciones (alcohol, calor, digestivo)", "fuente":"Cruz Roja Sevilla 2024 est."},
    {"evento":"Maratón Madrid",           "mes":4, "dur":1,"ccaa":"Madrid",        "esp":"Traumatología / Cardio",    "impacto":66,"tipo":"Deporte",    "color":ACCENT,
     "metrica":"93 atendidos, 2 paros cardíacos (1 fallecido)", "fuente":"SAMUR Madrid 2025"},
    {"evento":"Maratón Barcelona",        "mes":3, "dur":1,"ccaa":"Cataluña",      "esp":"Traumatología / Cardio",    "impacto":64,"tipo":"Deporte",    "color":ACCENT,
     "metrica":"~80 atenciones médicas, ~25.000 corredores",    "fuente":"Dispositivo médico Marató BCN 2024"},
    {"evento":"Pride Madrid",             "mes":7, "dur":1,"ccaa":"Madrid",        "esp":"Urgencias / Dermatología",  "impacto":62,"tipo":"Masivo",     "color":"#6A1B9A",
     "metrica":"~2M asistentes; urgencias calor + aglomeración","fuente":"Ayuntamiento Madrid 2024"},
    {"evento":"Camino de Santiago",       "mes":7, "dur":3,"ccaa":"Galicia",       "esp":"Ortopedia menor",           "impacto":60,"tipo":"Turismo",    "color":"#2E7D32",
     "metrica":"340.000 peregrinos 2024; principal: ampollas/esguinces","fuente":"APOC / Catedral Santiago 2024"},
    {"evento":"Mobile World Congress",    "mes":2, "dur":1,"ccaa":"Cataluña",      "esp":"Urgencias generales",       "impacto":58,"tipo":"Masivo",     "color":"#E65100",
     "metrica":"101.000 asistentes concentrados en Barcelona",  "fuente":"GSMA MWC 2024"},
    {"evento":"Semana Grande Bilbao",     "mes":8, "dur":1,"ccaa":"País Vasco",    "esp":"Urgencias generales",       "impacto":58,"tipo":"Festivo",    "color":"#E65100",
     "metrica":"~1M visitantes, urgencias +15% en semana festiva","fuente":"SOS Deiak / Osakidetza est."},
    {"evento":"Maratón Sevilla",          "mes":2, "dur":1,"ccaa":"Andalucía",     "esp":"Traumatología / Cardio",    "impacto":56,"tipo":"Deporte",    "color":ACCENT,
     "metrica":"~40.000 corredores, ~80 atenciones médicas",    "fuente":"Dispositivo médico Maratón Sevilla 2024"},
    {"evento":"Vendimia La Rioja",        "mes":9, "dur":2,"ccaa":"La Rioja",      "esp":"Accidentes laborales",      "impacto":52,"tipo":"Laboral",    "color":"#795548",
     "metrica":"Accidentabilidad laboral agrícola sector vitivinícola","fuente":"INSST / Ministerio Trabajo 2024"},
])

# ══════════════════════════════════════════════════════════════════
# NAVEGACIÓN
# ══════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state["page"] = "home"

with st.sidebar:
    st.markdown(
        f'<div style="padding:18px 12px 14px;text-align:center">'
        f'<img src="data:image/png;base64,{SANITAS_B64}" style="max-width:160px;width:100%;object-fit:contain" />'
        f'</div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    pages = [
        ("home",       "Inicio"),
        ("ejecutiva",  "Vista Ejecutiva"),
        ("retencion",  "Retención & Cartera"),
        ("operaciones","Optimización Operativa"),
        ("comercial",  "Inteligencia Comercial"),
    ]
    for key, label in pages:
        if st.button(label, key=f"nav_{key}"):
            go_to(key); st.rerun()

    # Resalta el botón activo por posición (nth-of-type)
    _page_idx = {"home":1,"ejecutiva":2,"retencion":3,"operaciones":4,"comercial":5}
    _idx = _page_idx.get(st.session_state.get("page","home"), 1)
    st.markdown(f"""
<style>
[data-testid="stSidebar"] [data-testid="stButton"]:nth-of-type({_idx}) > button,
[data-testid="stSidebar"] [data-testid="stButton"]:nth-of-type({_idx}) > button:hover {{
    background:{ACCENT}!important;color:#FFFFFF!important;
    font-weight:600!important;border-color:{ACCENT}!important;
    box-shadow:0 2px 8px rgba(0,48,135,.25)!important;
}}
</style>""", unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:.62rem;color:{S_MUTED};line-height:1.6">'
        f'Datos ficticios orientativos.<br>Panel · Sanitas · Septiembre 2026</div>',
        unsafe_allow_html=True)

page = st.session_state.get("page", "home")

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if page == "home":
    st.markdown(
        f'<div class="top-bar">'
        f'{_SAN_IMG}'
        f'<div class="top-bar-center"><div class="top-title">Plataforma de Inteligencia Corporativa · Sanitas</div>'
        f'<div class="top-sub">Panel ejecutivo · Datos ficticios orientativos · Septiembre 2026</div></div>'
        f'{_MIN_IMG}</div>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    kpi_card(h1, "Combined Ratio", "94.2%", "Loss 79.3% + Gasto 14.9%")
    kpi_card(h2, "Asegurados activos", "2.9M", "Informe Anual Sanitas 2024")
    kpi_card(h3, "EBITDA acumulado", "186 M€", "Seguros + Hospitales + Dental")
    kpi_card(h4, "NPS global", "42", "Objetivo: 50 en 2027")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    section("PILARES DE INTELIGENCIA — ACCESO RÁPIDO")

    c1, c2, c3 = st.columns(3)
    for col, key, titulo, desc, badge in [
        (c1, "ejecutiva",  "Vista Ejecutiva",
         "Combined ratio · EBITDA por línea · Portfolio neto · Cuota de mercado · NPS",
         "CEO / Dirección General"),
        (c2, "retencion",  "Retención & Cartera",
         "Modelo de churn · Razones de baja · Cohort retention · Rentabilidad por segmento",
         "Dirección de Clientes"),
        (c3, "operaciones","Optimización Operativa",
         "Loss ratio por producto/CCAA · Recursos hospitalarios · Fraude · Derivaciones",
         "Dirección Médica & CFO"),
    ]:
        col.markdown(
            f'<div class="kpi-card" style="height:100%">'
            f'<div style="font-size:.6rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;'
            f'color:{ACCENT};margin-bottom:10px">{badge}</div>'
            f'<div style="font-size:1.05rem;font-weight:600;color:{FONT};margin-bottom:10px">{titulo}</div>'
            f'<div style="font-size:.78rem;color:{S_MUTED};line-height:1.55">{desc}</div>'
            f'</div>', unsafe_allow_html=True)
        col.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if col.button(f"→ {titulo}", key=f"home_{key}"):
            go_to(key); st.rerun()

    c4, _ = st.columns([1, 2])
    c4.markdown(
        f'<div class="kpi-card">'
        f'<div style="font-size:.6rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;'
        f'color:{ACCENT};margin-bottom:10px">Dirección Comercial</div>'
        f'<div style="font-size:1.05rem;font-weight:600;color:{FONT};margin-bottom:10px">Inteligencia Comercial</div>'
        f'<div style="font-size:.78rem;color:{S_MUTED};line-height:1.55">'
        f'Vectorización estratégica CCAA · Recomendador de póliza · Pricing · Cuota de mercado</div>'
        f'</div>', unsafe_allow_html=True)
    c4.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if c4.button("→ Inteligencia Comercial", key="home_comercial"):
        go_to("comercial"); st.rerun()

    callout(
        "<strong>Panel de inteligencia para la toma de decisiones de Sanitas.</strong> "
        "Tres pilares operativos: <strong>Retención</strong> (quién se va y cuándo), "
        "<strong>Optimización Operativa</strong> (el coste del sistema y el combined ratio) "
        "e <strong>Inteligencia Comercial</strong> (dónde y a quién crecer). "
        "Todos los datos son ficticios con fines de demostración."
    )

# ══════════════════════════════════════════════════════════════════
# VISTA EJECUTIVA
# ══════════════════════════════════════════════════════════════════
elif page == "ejecutiva":
    st.markdown(
        f'<div class="top-bar">'
        f'{_SAN_IMG}'
        f'<div class="top-bar-center"><div class="top-title">Vista Ejecutiva</div>'
        f'<div class="top-sub">CEO · Dirección General · Septiembre 2026</div></div>'
        f'{_MIN_IMG}</div>', unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4)
    kpi_card(e1, "Combined Ratio", "94.2%", "Obj. <95% — en rango")
    kpi_card(e2, "Loss Ratio",     "79.3%", "Umbral sostenible: 80%")
    kpi_card(e3, "EBITDA",         "186 M€", "+8.4% vs mismo período 2025")
    kpi_card(e4, "Cuota de mercado","16.7%", "2.ª aseguradora España · Fuente UNESPA dic.2025")

    e5, e6, e7, e8 = st.columns(4)
    kpi_card(e5, "Asegurados activos","2.9M", "Informe Anual Sanitas 2024")
    kpi_card(e6, "NPS global",       "42",    "Encuestas post-servicio 2026")
    kpi_card(e7, "Tasa de renovación","87.6%","−0.8 pp vs 2025")
    kpi_card(e8, "Blua — usuarios activos","312K","Consultas digitales: 28%")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ── Combined Ratio evolution ──────────────────────────────
    section("COMBINED RATIO — EVOLUCIÓN MENSUAL")
    fig_cr = go.Figure()
    fig_cr.add_trace(go.Bar(
        x=df_cr["mes"], y=df_cr["loss_ratio"], name="Loss Ratio",
        marker_color=A3, marker_line_width=0,
    ))
    fig_cr.add_trace(go.Bar(
        x=df_cr["mes"], y=df_cr["expense_ratio"], name="Expense Ratio",
        marker_color=A2, marker_line_width=0,
    ))
    fig_cr.add_hline(y=95, line_dash="dot", line_color="#B71C1C", line_width=1.5,
                     annotation_text="Umbral crítico 95%", annotation_position="top right",
                     annotation_font_size=9, annotation_font_color="#B71C1C",
                     annotation_bgcolor="rgba(255,255,255,0.85)")
    fig_cr.update_layout(**lay(h=300, showlegend=True,
        legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=10,b=10,l=8,r=40)))
    fig_cr.update_layout(barmode="stack")
    fig_cr.update_xaxes(tickformat="%b %y", tickfont=dict(size=9))
    st.plotly_chart(fig_cr, use_container_width=True)

    r1c1, r1c2 = st.columns(2)

    # ── EBITDA por línea ──────────────────────────────────────
    with r1c1:
        section("EBITDA POR LÍNEA DE NEGOCIO")
        fig_ebitda = go.Figure(go.Bar(
            x=df_ebitda["ebitda"], y=df_ebitda["linea"],
            orientation="h",
            marker_color=df_ebitda["color"], marker_line_width=0,
            text=[f"{v:+.0f} M€  ({m:+.1f}%)" for v,m in zip(df_ebitda["ebitda"],df_ebitda["margen"])],
            textposition="outside", textfont=dict(size=9),
        ))
        fig_ebitda.update_layout(**lay(h=260, margin=dict(t=10,b=10,l=8,r=100)))
        fig_ebitda.update_xaxes(showgrid=True, gridcolor=GRID, range=[-20, 120])
        st.plotly_chart(fig_ebitda, use_container_width=True)

    # ── Portfolio neto ────────────────────────────────────────
    with r1c2:
        section("PORTFOLIO — ALTAS Y BAJAS MENSUALES")
        fig_port = go.Figure()
        fig_port.add_trace(go.Bar(
            x=df_port["mes"], y=df_port["altas"], name="Altas",
            marker_color="#2E7D32", marker_line_width=0, opacity=0.85,
        ))
        fig_port.add_trace(go.Bar(
            x=df_port["mes"], y=-df_port["bajas"], name="Bajas",
            marker_color="#B71C1C", marker_line_width=0, opacity=0.85,
        ))
        fig_port.add_trace(go.Scatter(
            x=df_port["mes"], y=df_port["neto"], name="Neto",
            mode="lines+markers", line=dict(color=ACCENT, width=2),
            marker=dict(size=5),
        ))
        fig_port.update_layout(**lay(h=260, showlegend=True,
            legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=10,b=10,l=8,r=8)))
        fig_port.update_xaxes(tickformat="%b %y", tickfont=dict(size=9))
        fig_port.update_yaxes(showgrid=True, gridcolor=GRID)
        st.plotly_chart(fig_port, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    # ── Cuota de mercado ──────────────────────────────────────
    with r2c1:
        section("CUOTA DE MERCADO — SEGUROS SALUD PRIVADO ESPAÑA")
        fig_cuota = go.Figure(go.Pie(
            labels=df_cuotas["aseguradora"], values=df_cuotas["cuota"],
            marker=dict(colors=df_cuotas["color"], line=dict(color=PAPER, width=2)),
            textinfo="percent", textfont=dict(size=10, color="#fff"), hole=0.42,
        ))
        fig_cuota.update_layout(**lay(h=280, showlegend=True,
            legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=10,b=10,l=8,r=8)))
        st.plotly_chart(fig_cuota, use_container_width=True)

    # ── NPS por segmento ──────────────────────────────────────
    with r2c2:
        section("NPS POR SEGMENTO DE PÓLIZA")
        df_nps_s = df_nps.sort_values("nps")
        fig_nps = go.Figure(go.Bar(
            y=df_nps_s["segmento"], x=df_nps_s["nps"],
            orientation="h",
            marker_color=[ACCENT if v >= 50 else A2 if v >= 40 else A3 if v >= 30 else S_MUTED
                          for v in df_nps_s["nps"]],
            marker_line_width=0,
            text=[f"{v}" for v in df_nps_s["nps"]],
            textposition="outside", textfont=dict(size=10, color=FONT),
        ))
        fig_nps.add_vline(x=0, line_color=S_BORDER, line_width=1)
        fig_nps.add_vline(x=50, line_dash="dot", line_color=ACCENT, line_width=1,
                          annotation_text="Obj. 50", annotation_font_size=8,
                          annotation_font_color=ACCENT)
        fig_nps.update_layout(**lay(h=280, margin=dict(t=10,b=10,l=8,r=40)))
        fig_nps.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 85])
        st.plotly_chart(fig_nps, use_container_width=True)

    callout(
        "<strong>Conclusión ejecutiva:</strong> El combined ratio de 94.2% está dentro del objetivo "
        "pero con escaso margen. El loss ratio medio de 79.3% está presionado por el segmento Senior "
        "(Único: loss ratio 88%) y la póliza Familiar en CCAA de alta siniestralidad. "
        "<strong>El crecimiento de cartera es positivo (+3.2% asegurados)</strong> pero la tasa de "
        "renovación baja 0.8pp — señal de presión competitiva de Adeslas post-fusión SegurCaixa. "
        "Blua crece en adopción (312K usuarios) y ya genera el 28% de las consultas, "
        "con efecto positivo sobre el expense ratio."
    )

# ══════════════════════════════════════════════════════════════════
# RETENCIÓN & CARTERA
# ══════════════════════════════════════════════════════════════════
elif page == "retencion":
    st.markdown(
        f'<div class="top-bar">'
        f'{_SAN_IMG}'
        f'<div class="top-bar-center"><div class="top-title">Retención & Optimización de Cartera</div>'
        f'<div class="top-sub">Dirección de Clientes · Modelo de churn · Campañas · Rentabilidad</div></div>'
        f'{_MIN_IMG}</div>', unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    kpi_card(r1, "Tasa de churn anual",   "12.4%",  "−0.8pp si se activan campañas")
    kpi_card(r2, "Asegurados riesgo alto","214K",   "Score >70 — intervención urgente")
    kpi_card(r3, "NPS post-servicio",     "42",     "Objetivo 50 en 2027")
    kpi_card(r4, "Tasa de renovación",    "87.6%",  "−0.8pp interanual", negative=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Análisis de Cartera", "Modelo de Churn", "Rentabilidad por Segmento"])

    # ── TAB 1: Cartera ────────────────────────────────────────
    with tab1:
        tc1, tc2 = st.columns(2)
        with tc1:
            section("DISTRIBUCIÓN DE CARTERA POR TIPO DE PÓLIZA")
            fig_tipos = go.Figure(go.Pie(
                labels=df_tipos["tipo"], values=df_tipos["asegurados"],
                marker=dict(colors=df_tipos["color"], line=dict(color=PAPER, width=2)),
                textinfo="percent+label", textfont=dict(size=9), hole=0.38,
            ))
            fig_tipos.update_layout(**lay(h=300, margin=dict(t=10,b=10,l=8,r=8)))
            st.plotly_chart(fig_tipos, use_container_width=True)

        with tc2:
            section("CHURN RATE POR ANTIGÜEDAD DE CARTERA")
            fig_ant = go.Figure()
            fig_ant.add_trace(go.Bar(
                x=df_antiguedad["rango"], y=df_antiguedad["asegurados"],
                name="Asegurados", marker_color=A3, marker_line_width=0, yaxis="y",
                text=[f"{v/1000:.0f}K" for v in df_antiguedad["asegurados"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ant.add_trace(go.Scatter(
                x=df_antiguedad["rango"], y=df_antiguedad["churn_rate"],
                name="Churn rate %", mode="lines+markers",
                line=dict(color="#B71C1C", width=2), marker=dict(size=7),
                yaxis="y2",
            ))
            fig_ant.update_layout(
                **lay(h=300, showlegend=True,
                      legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                      margin=dict(t=10,b=10,l=8,r=50)),
                yaxis2=dict(overlaying="y", side="right", showgrid=False,
                            ticksuffix="%", tickfont=dict(size=9), color="#B71C1C"),
            )
            st.plotly_chart(fig_ant, use_container_width=True)

        callout(
            "<strong>El primer año es el momento crítico:</strong> el 18.2% de los asegurados "
            "captados en el año 1 no renueva — precio shock al ver la prima real vs. la promocional. "
            "A partir del año 5 el churn cae al 4.2% — el asegurado maduro está captado. "
            "<strong>Acción clave:</strong> programa de bienvenida con engagement activo en los "
            "primeros 12 meses para consolidar la relación antes de la primera renovación."
        )

    # ── TAB 2: Churn ──────────────────────────────────────────
    with tab2:
        ch1, ch2 = st.columns(2)
        with ch1:
            section("DISTRIBUCIÓN DEL SCORE DE RIESGO DE BAJA")
            fig_hist = go.Figure(go.Histogram(
                x=scores_raw, nbinsx=40,
                marker_color=A3, marker_line_width=0, opacity=0.85,
            ))
            fig_hist.add_vline(x=50, line_dash="dot", line_color="#E65100", line_width=1.5,
                               annotation_text="Alerta media", annotation_font_size=8,
                               annotation_font_color="#E65100")
            fig_hist.add_vline(x=75, line_dash="dot", line_color="#B71C1C", line_width=1.5,
                               annotation_text="Riesgo alto", annotation_font_size=8,
                               annotation_font_color="#B71C1C")
            fig_hist.update_layout(**lay(h=280, margin=dict(t=10,b=10,l=8,r=8)))
            fig_hist.update_xaxes(title_text="Score de riesgo (0=fiel · 100=baja inminente)",
                                  title_font=dict(size=9))
            fig_hist.update_yaxes(title_text="N.º asegurados", title_font=dict(size=9))
            st.plotly_chart(fig_hist, use_container_width=True)

        with ch2:
            section("TOP RAZONES DE BAJA — ENCUESTA DE SALIDA")
            fig_raz = go.Figure(go.Bar(
                y=df_razones["razon"], x=df_razones["pct"],
                orientation="h",
                marker_color=[ACCENT if v >= 20 else A2 if v >= 12 else A3
                              for v in df_razones["pct"]],
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in df_razones["pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_raz.update_layout(**lay(h=280, margin=dict(t=10,b=10,l=8,r=50)))
            fig_raz.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 42])
            st.plotly_chart(fig_raz, use_container_width=True)

        section("RETENCIÓN POR COHORTE DE CONTRATACIÓN")
        fig_coh = go.Figure(go.Heatmap(
            z=cohort_ret, x=COHORT_M, y=COHORT_YEARS,
            colorscale=[[0,"#B71C1C"],[0.5,"#FFF9C4"],[1,"#2E7D32"]],
            text=[[f"{v:.0f}%" if not np.isnan(v) else "–" for v in row] for row in cohort_ret],
            texttemplate="%{text}", textfont=dict(size=10),
            showscale=True, zmin=75, zmax=100,
            colorbar=dict(title="Retención %", tickfont=dict(size=9), len=0.7),
        ))
        fig_coh.update_layout(**lay(h=260, margin=dict(t=10,b=10,l=8,r=10)))
        st.plotly_chart(fig_coh, use_container_width=True)

        callout(
            "<strong>El 10% de la cartera (214K asegurados) tiene score de riesgo >75</strong> "
            "y necesita intervención en los próximos 30 días. La principal razón de baja "
            "sigue siendo la subida de precio en renovación (34.2%), seguida del abandono del "
            "cuadro médico por parte del especialista favorito (18.6%). "
            "<strong>Acción:</strong> campaña de retención dirigida, con propuesta de "
            "precio personalizada antes del vencimiento y alerta proactiva al asegurado "
            "cuando su médico favorito deja el cuadro."
        )

    # ── TAB 3: Rentabilidad ───────────────────────────────────
    with tab3:
        rr1, rr2 = st.columns(2)
        with rr1:
            section("LOSS RATIO VS. MARGEN POR SEGMENTO")
            fig_seg = px.scatter(
                df_rentab, x="loss_ratio", y="margen_idx",
                size="precio_med", color="segmento", text="segmento",
                size_max=40, opacity=0.85,
                labels={"loss_ratio":"Loss Ratio →","margen_idx":"↑ Índice de margen","segmento":""},
            )
            fig_seg.update_traces(textposition="top center", textfont=dict(size=8.5, color=FONT))
            fig_seg.add_hline(y=65, line_dash="dot", line_color=S_MUTED, line_width=1,
                              annotation_text="Umbral margen mínimo", annotation_font_size=8)
            fig_seg.add_vline(x=75, line_dash="dot", line_color="#E65100", line_width=1,
                              annotation_text="Umbral riesgo", annotation_font_size=8)
            fig_seg.update_layout(**lay(h=320, showlegend=False, margin=dict(t=14,b=10,l=8,r=8)))
            fig_seg.update_xaxes(showgrid=True, gridcolor=GRID)
            fig_seg.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_seg, use_container_width=True)

        with rr2:
            section("RENTABILIDAD POR TIPO DE PÓLIZA")
            df_r = df_tipos.sort_values("margen")
            fig_rent = go.Figure()
            fig_rent.add_trace(go.Bar(
                y=df_r["tipo"], x=df_r["margen"],
                orientation="h", name="Margen",
                marker_color=df_r["color"], marker_line_width=0,
                text=[f"{v}" for v in df_r["margen"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_rent.add_trace(go.Bar(
                y=df_r["tipo"], x=df_r["loss_ratio"],
                orientation="h", name="Loss Ratio",
                marker_color="rgba(0,0,0,0.08)", marker_line_width=0,
                text=[f"LR {v}%" for v in df_r["loss_ratio"]],
                textposition="outside", textfont=dict(size=8, color=S_MUTED),
            ))
            fig_rent.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=60)))
            fig_rent.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_rent, use_container_width=True)

        callout(
            "<strong>Reembolso y Autónomo son los segmentos más rentables</strong> "
            "(margen índice >74, loss ratio <40%) porque el perfil directivo/profesional "
            "tiene menor siniestralidad y mayor precio de prima. "
            "<strong>Senior Único es el segmento de mayor riesgo actuarial</strong> "
            "(loss ratio 88%) pero es estratégico para no perder la cartera de largo plazo "
            "al envejecer. La póliza Básica (Accede/Avanza) tiene bajo loss ratio "
            "pero márgenes reducidos por precio de prima bajo — su valor es de captación, "
            "no de rentabilidad directa."
        )

# ══════════════════════════════════════════════════════════════════
# OPTIMIZACIÓN OPERATIVA
# ══════════════════════════════════════════════════════════════════
elif page == "operaciones":
    st.markdown(
        f'<div class="top-bar">'
        f'{_SAN_IMG}'
        f'<div class="top-bar-center"><div class="top-title">Optimización Operativa</div>'
        f'<div class="top-sub">Dirección Médica · CFO · Combined Ratio · Recursos · Fraude</div></div>'
        f'{_MIN_IMG}</div>', unsafe_allow_html=True)

    o1, o2, o3, o4 = st.columns(4)
    kpi_card(o1, "Combined Ratio",        "94.2%",  "Loss 79.3% + Gasto 14.9%")
    kpi_card(o2, "Derivaciones externas", "1.760/mes", "Coste evitable ~4.2 M€/mes")
    kpi_card(o3, "Fraude detectado",      "96 casos/mes", "200 K€/mes recuperados")
    kpi_card(o4, "Espera media",          "11 días", "Obj. <8 días en Traumatología")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4_op = st.tabs(["Combined Ratio por Producto", "Recursos Hospitalarios", "Hiperfrecuentación", "Fraude & Derivaciones"])

    # ── TAB 1: Combined Ratio ─────────────────────────────────
    with tab1:
        section("LOSS RATIO POR PRODUCTO × CCAA — HEATMAP")
        fig_lr_heat = go.Figure(go.Heatmap(
            z=lr_matrix,
            x=PROD_LIST,
            y=CCAA_LIST,
            colorscale=[[0,"#E8F5E9"],[0.4,"#FFF9C4"],[0.7,"#FF8F00"],[1,"#B71C1C"]],
            text=[[f"{v:.0f}" for v in row] for row in lr_matrix],
            texttemplate="%{text}", textfont=dict(size=8),
            showscale=True, zmin=30, zmax=100,
            colorbar=dict(title="Loss Ratio %", tickfont=dict(size=9), len=0.7),
        ))
        fig_lr_heat.add_shape(type="line", x0=6.5, x1=6.5, y0=-0.5, y1=len(CCAA_LIST)-0.5,
                              line=dict(color=ACCENT, width=1.5, dash="dot"))
        fig_lr_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=10),
            height=480, margin=dict(t=10,b=10,l=8,r=10),
            xaxis=dict(tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=9), autorange="reversed"),
        )
        st.plotly_chart(fig_lr_heat, use_container_width=True)

        oc1, oc2 = st.columns(2)
        with oc1:
            section("LOSS RATIO PROMEDIO POR CCAA")
            lr_ccaa_avg = pd.DataFrame({
                "ccaa": CCAA_LIST,
                "lr":   [round(float(np.mean(lr_matrix[i])), 1) for i in range(len(CCAA_LIST))],
            }).sort_values("lr")
            fig_lr_ccaa = go.Figure(go.Bar(
                y=lr_ccaa_avg["ccaa"], x=lr_ccaa_avg["lr"],
                orientation="h",
                marker_color=[ACCENT if v < 70 else A2 if v < 78 else A3 if v < 85 else "#B71C1C"
                              for v in lr_ccaa_avg["lr"]],
                marker_line_width=0,
                text=[f"{v}%" for v in lr_ccaa_avg["lr"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr_ccaa.add_vline(x=80, line_dash="dot", line_color="#B71C1C", line_width=1.5,
                                  annotation_text="Umbral 80%", annotation_font_size=8,
                                  annotation_font_color="#B71C1C")
            fig_lr_ccaa.update_layout(**lay(h=380, margin=dict(t=10,b=10,l=8,r=50)))
            fig_lr_ccaa.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 100])
            st.plotly_chart(fig_lr_ccaa, use_container_width=True)

        with oc2:
            section("LOSS RATIO PROMEDIO POR PRODUCTO")
            lr_prod_avg = pd.DataFrame({
                "producto": PROD_LIST,
                "lr":       [round(float(np.mean(lr_matrix[:,i])), 1) for i in range(len(PROD_LIST))],
            }).sort_values("lr")
            fig_lr_prod = go.Figure(go.Bar(
                y=lr_prod_avg["producto"], x=lr_prod_avg["lr"],
                orientation="h",
                marker_color=[ACCENT if v < 60 else A2 if v < 75 else A3 if v < 85 else "#B71C1C"
                              for v in lr_prod_avg["lr"]],
                marker_line_width=0,
                text=[f"{v}%" for v in lr_prod_avg["lr"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_lr_prod.add_vline(x=80, line_dash="dot", line_color="#B71C1C", line_width=1.5,
                                  annotation_text="Umbral 80%", annotation_font_size=8,
                                  annotation_font_color="#B71C1C")
            fig_lr_prod.update_layout(**lay(h=380, margin=dict(t=10,b=10,l=8,r=50)))
            fig_lr_prod.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 105])
            st.plotly_chart(fig_lr_prod, use_container_width=True)

        callout(
            "<strong>Senior Único supera el umbral del 80% en todas las CCAA.</strong> "
            "Extremadura (CR medio 98.4%) y Castilla-La Mancha (CR 96.8%) son las CCAA "
            "donde el combined ratio es más ajustado — candidatas a revisar la oferta de "
            "producto y precio. <strong>País Vasco y Navarra</strong> mantienen los "
            "mejores loss ratios medios (<72%) — mercados donde se puede crecer sin sacrificar margen."
        )

    # ── TAB 2: Recursos ───────────────────────────────────────
    with tab2:
        rc1, rc2 = st.columns(2)
        with rc1:
            section("OCUPACIÓN HOSPITALARIA POR CENTRO (% sobre capacidad)")
            fig_ocu = go.Figure()
            fig_ocu.add_trace(go.Bar(
                y=df_centros["centro"], x=df_centros["camas_pct"],
                orientation="h", name="Camas", marker_color=ACCENT, marker_line_width=0,
                text=[f"{v}%" for v in df_centros["camas_pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ocu.add_trace(go.Bar(
                y=df_centros["centro"], x=df_centros["qx_pct"],
                orientation="h", name="Quirófanos", marker_color=A3, marker_line_width=0,
                text=[f"{v}%" for v in df_centros["qx_pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_ocu.add_vline(x=85, line_dash="dot", line_color="#E65100", line_width=1,
                              annotation_text="Riesgo saturación", annotation_font_size=8)
            fig_ocu.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=60)))
            fig_ocu.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 105])
            st.plotly_chart(fig_ocu, use_container_width=True)

        with rc2:
            section("TIEMPO DE ESPERA POR ESPECIALIDAD (días)")
            df_esp_s = df_espera.sort_values("sanitas", ascending=False)
            fig_esp = go.Figure()
            fig_esp.add_trace(go.Bar(
                y=df_esp_s["especialidad"], x=df_esp_s["sanitas"],
                orientation="h", name="Sanitas",
                marker_color=ACCENT, marker_line_width=0,
                text=[f"{v}d" for v in df_esp_s["sanitas"]],
                textposition="outside", textfont=dict(size=8.5),
            ))
            fig_esp.add_trace(go.Bar(
                y=df_esp_s["especialidad"], x=df_esp_s["sector"],
                orientation="h", name="Media sector",
                marker_color="rgba(0,0,0,0.1)", marker_line_width=0,
                text=[f"{v}d" for v in df_esp_s["sector"]],
                textposition="outside", textfont=dict(size=8, color=S_MUTED),
            ))
            fig_esp.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=60)))
            fig_esp.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_esp, use_container_width=True)

        section("READMISIONES 30 DÍAS POR CENTRO (%)")
        fig_read = go.Figure(go.Bar(
            x=df_centros["centro"], y=df_centros["readmision_pct"],
            marker_color=[ACCENT if v < 4 else "#E65100" if v < 5 else "#B71C1C"
                          for v in df_centros["readmision_pct"]],
            marker_line_width=0,
            text=[f"{v}%" for v in df_centros["readmision_pct"]],
            textposition="outside", textfont=dict(size=9),
        ))
        fig_read.add_hline(y=4, line_dash="dot", line_color=S_MUTED, line_width=1,
                           annotation_text="Objetivo <4%", annotation_font_size=8)
        fig_read.update_layout(**lay(h=220, margin=dict(t=10,b=10,l=8,r=8)))
        fig_read.update_yaxes(showgrid=True, gridcolor=GRID, range=[0, 7])
        st.plotly_chart(fig_read, use_container_width=True)

        callout(
            "<strong>La Zarzuela y Cima superan el 85% de ocupación en quirófanos</strong> — "
            "riesgo de saturación en temporada alta. La espera en Psiquiatría (35 días) "
            "es un KPI crítico de satisfacción y NPS. "
            "<strong>Ntra. Sra. del Rosario tiene la mayor tasa de readmisión a 30 días (5.2%)</strong> "
            "— indicador de posible problema en calidad de alta o seguimiento post-hospitalario."
        )

    # ── TAB 3: Hiperfrecuentación ─────────────────────────────
    with tab3:
        hf_acto_sel = st.selectbox("Tipo de acto médico", list(BENCH_ACTOS.keys()), key="hf_acto")
        bench_val   = BENCH_ACTOS[hf_acto_sel]
        col_hf      = HF_COL_MAP[hf_acto_sel]

        df_hf = df_hiperfrec.copy()
        df_hf["ratio"]  = (df_hf[col_hf] / bench_val).round(2)
        n_alert  = int((df_hf["ratio"] > 1.5).sum())
        ratio_max = float(df_hf["ratio"].max())
        ratio_avg = float(df_hf["ratio"].mean())
        centro_max = df_hf.loc[df_hf["ratio"].idxmax(), "centro"]

        hk1, hk2, hk3, hk4 = st.columns(4)
        kpi_card(hk1, "Benchmark nacional",       f"{bench_val:.1f} actos/pac./año", hf_acto_sel)
        kpi_card(hk2, "Ratio medio centros",      f"{ratio_avg:.2f}x", "vs. benchmark", negative=ratio_avg > 1.3)
        kpi_card(hk3, "Centros en alerta (>1.5x)",str(n_alert),         f"de {len(df_hf)} centros", negative=n_alert > 2)
        kpi_card(hk4, "Ratio máximo detectado",   f"{ratio_max:.2f}x",  centro_max)

        section(f"RATIO HIPERFRECUENTACIÓN — {hf_acto_sel.upper()} POR CENTRO (real / benchmark)")
        df_hf_s = df_hf.sort_values("ratio", ascending=True)
        colors_hf = [
            "#2E7D32" if r < 1.2 else A3 if r < 1.5 else "#E65100" if r < 2.0 else "#B71C1C"
            for r in df_hf_s["ratio"]
        ]
        fig_hf = go.Figure()
        fig_hf.add_trace(go.Bar(
            y=df_hf_s["centro"], x=df_hf_s[col_hf],
            orientation="h",
            marker_color=colors_hf, marker_line_width=0,
            name=hf_acto_sel,
            text=[f"{v:.1f} (<b>{r:.2f}x</b>)" for v, r in zip(df_hf_s[col_hf], df_hf_s["ratio"])],
            textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{y}</b><br>Actos/paciente: %{x:.2f}<extra></extra>",
        ))
        fig_hf.add_vline(x=bench_val, line_dash="dash", line_color=ACCENT, line_width=2,
                         annotation_text=f"Benchmark: {bench_val}", annotation_font_size=9,
                         annotation_font_color=ACCENT, annotation_position="top right")
        fig_hf.add_vline(x=bench_val * 1.5, line_dash="dot", line_color="#E65100", line_width=1.5,
                         annotation_text="Alerta 1.5x", annotation_font_size=8,
                         annotation_font_color="#E65100", annotation_position="bottom right")
        fig_hf.update_layout(**lay(h=380, margin=dict(t=10, b=10, l=8, r=80)))
        fig_hf.update_xaxes(showgrid=True, gridcolor=GRID,
                             range=[0, float(df_hf[col_hf].max()) * 1.28])
        st.plotly_chart(fig_hf, use_container_width=True)

        hf_c1, hf_c2 = st.columns([2, 1])
        with hf_c1:
            section("COMPARATIVA TODOS LOS ACTOS — RATIO REAL/BENCHMARK (heatmap centros × actos)")
            hf_col_keys_ord = list(HF_COL_MAP.values())
            hf_actos_ord    = list(HF_COL_MAP.keys())
            ratio_matrix_hf = [
                [round(row[k] / BENCH_ACTOS[a], 2) for k, a in zip(hf_col_keys_ord, hf_actos_ord)]
                for _, row in df_hiperfrec.iterrows()
            ]
            fig_hf_heat = go.Figure(go.Heatmap(
                z=ratio_matrix_hf,
                x=hf_actos_ord,
                y=df_hiperfrec["centro"].tolist(),
                colorscale=[[0,"#E8F5E9"],[0.35,"#FFF9C4"],[0.6,"#FF8F00"],[0.8,"#E65100"],[1,"#B71C1C"]],
                text=[[f"{v:.2f}x" for v in row] for row in ratio_matrix_hf],
                texttemplate="%{text}", textfont=dict(size=8.5),
                showscale=True, zmin=0.7, zmax=2.0,
                colorbar=dict(title="Ratio", tickfont=dict(size=9), len=0.7),
            ))
            fig_hf_heat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter,sans-serif", color=FONT, size=10),
                height=360, margin=dict(t=10, b=10, l=8, r=10),
                xaxis=dict(tickangle=-25, tickfont=dict(size=9)),
                yaxis=dict(tickfont=dict(size=9), autorange="reversed"),
            )
            st.plotly_chart(fig_hf_heat, use_container_width=True)

        with hf_c2:
            section("TOP 5 ALERTAS")
            df_top = df_hf.nlargest(5, "ratio")[["centro", "ratio", col_hf]]
            for _, r in df_top.iterrows():
                color_alert = "#E65100" if r["ratio"] < 2.0 else "#B71C1C"
                st.markdown(
                    f'<div style="padding:10px 14px;margin-bottom:8px;background:{PAPER};'
                    f'border-radius:10px;border-left:4px solid {color_alert}">'
                    f'<div style="font-size:.75rem;font-weight:700;color:{FONT}">{r["centro"]}</div>'
                    f'<div style="font-size:.88rem;font-weight:700;color:{color_alert};margin-top:4px">'
                    f'{r["ratio"]:.2f}x benchmark</div>'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">'
                    f'{r[col_hf]:.1f} vs {bench_val:.1f} actos/pac./año</div>'
                    f'</div>', unsafe_allow_html=True)

        callout(
            f"<strong>Hiperfrecuentación:</strong> un ratio &gt;1.5x indica que los pacientes "
            f"de ese centro usan {hf_acto_sel.lower()} 1.5 veces más de lo esperado para su "
            "perfil clínico. Puede reflejar mayor complejidad del paciente, medicina defensiva "
            "o un patrón de fraude/abuso. "
            "<strong>El siguiente paso es revisar la casuística de los casos outlier</strong> "
            "para determinar la causa raíz antes de actuar sobre el proveedor."
        )

    # ── TAB 4: Fraude & Derivaciones ──────────────────────────
    with tab4_op:
        fd1, fd2 = st.columns(2)
        with fd1:
            section("TIPOLOGÍA DE FRAUDE DETECTADO — CASOS / MES")
            fig_fraud = go.Figure(go.Pie(
                labels=df_fraude["tipo"], values=df_fraude["casos"],
                marker=dict(colors=df_fraude["color"], line=dict(color=PAPER, width=2)),
                textinfo="percent", textfont=dict(size=10, color="#fff"), hole=0.44,
            ))
            fig_fraud.update_layout(**lay(h=300, showlegend=True,
                legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=8)))
            st.plotly_chart(fig_fraud, use_container_width=True)

        with fd2:
            section("IMPORTE RECUPERADO POR TIPOLOGÍA DE FRAUDE (K€/mes)")
            fig_fr_imp = go.Figure(go.Bar(
                y=df_fraude["tipo"], x=df_fraude["importe_k"],
                orientation="h",
                marker_color=df_fraude["color"], marker_line_width=0,
                text=[f"{v:.1f} K€" for v in df_fraude["importe_k"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_fr_imp.update_layout(**lay(h=300, margin=dict(t=10,b=10,l=8,r=70)))
            fig_fr_imp.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_fr_imp, use_container_width=True)

        section("COSTE DE DERIVACIONES EXTERNAS POR ESPECIALIDAD (K€/mes)")
        df_deriv_s = df_deriv.sort_values("coste_total", ascending=False)
        fig_deriv = go.Figure(go.Bar(
            x=df_deriv_s["especialidad"], y=df_deriv_s["coste_total"],
            marker_color=[ACCENT, A2, A3, "#2E7D32", "#E65100", S_MUTED],
            marker_line_width=0,
            text=[f"{v:.0f} K€" for v in df_deriv_s["coste_total"]],
            textposition="outside", textfont=dict(size=9),
        ))
        fig_deriv.update_layout(**lay(h=240, margin=dict(t=10,b=10,l=8,r=8)))
        fig_deriv.update_yaxes(showgrid=True, gridcolor=GRID)
        st.plotly_chart(fig_deriv, use_container_width=True)

        callout(
            "<strong>El inflado de costes es el fraude de mayor impacto económico</strong> "
            "(86.8 K€/mes) aunque no el más frecuente. Los 96 casos detectados al mes "
            "representan una recuperación de ~200 K€ — y se estima que el fraude no detectado "
            "supone entre 3x y 5x ese importe. "
            "<strong>Las derivaciones a Neurocirugía y Cirugía Robótica</strong> concentran "
            "el mayor coste externalizado — son candidatas a inversión en capacidad propia "
            "para reducir el gasto de derivación."
        )

# ══════════════════════════════════════════════════════════════════
# INTELIGENCIA COMERCIAL
# ══════════════════════════════════════════════════════════════════
elif page == "comercial":
    st.markdown(
        f'<div class="top-bar">'
        f'{_SAN_IMG}'
        f'<div class="top-bar-center"><div class="top-title">Inteligencia Comercial</div>'
        f'<div class="top-sub">Dirección Comercial · Oportunidad geográfica · Pricing · Captación</div></div>'
        f'{_MIN_IMG}</div>', unsafe_allow_html=True)

    cm1, cm2, cm3, cm4 = st.columns(4)
    kpi_card(cm1, "Cuota de mercado",    "16.7%",   "2.ª aseguradora España · UNESPA dic.2025")
    kpi_card(cm2, "Conv. lead → alta",   "6.6%",    "Benchmark sector: 8.2%")
    kpi_card(cm3, "Pipeline colectivos", "84 empresas", "+12 nuevas este trimestre")
    kpi_card(cm4, "CCAA prioridad máx.", "5 de 17", "Score global >65 — Madrid, PV, Navarra…")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Oportunidad Geográfica", "Captación & Pólizas", "Competencia & Pricing", "Epidemiología & Demanda", "Colectivos & Empresas"])

    # ── TAB 1: Oportunidad ────────────────────────────────────
    with tab1:
        COLOR_Q = {"Prioridad máxima": ACCENT, "Crecer con cautela": "#E65100",
                   "Consolidar y rentabilizar": "#2E7D32", "Revisar estrategia": S_MUTED}

        section("VECTORIZACIÓN ESTRATÉGICA — OPORTUNIDAD VS. RENTABILIDAD POR CCAA")
        fig_vec = px.scatter(
            VEC, x="score_oportunidad", y="score_rentabilidad",
            color="cuadrante", text="ccaa", size="score_global", size_max=42,
            color_discrete_map=COLOR_Q,
            labels={"score_oportunidad":"Score Oportunidad →",
                    "score_rentabilidad":"↑ Score Rentabilidad","cuadrante":""},
            opacity=0.88,
        )
        fig_vec.update_traces(textposition="top center", textfont=dict(size=8.5, color=FONT))
        fig_vec.add_hline(y=55, line_dash="dot", line_color=S_MUTED, line_width=1)
        fig_vec.add_vline(x=55, line_dash="dot", line_color=S_MUTED, line_width=1)
        for label, x, y in [
            ("Prioridad máxima", 72, 72),
            ("Crecer con cautela", 72, 38),
            ("Consolidar y rentabilizar", 38, 72),
            ("Revisar estrategia", 38, 38),
        ]:
            fig_vec.add_annotation(x=x, y=y, text=label,
                                   font=dict(size=8, color=COLOR_Q[label]),
                                   showarrow=False, opacity=0.5)
        fig_vec.update_layout(**lay(h=420, showlegend=True,
            legend=dict(orientation="h", y=-0.15, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=14,b=60,l=8,r=8)))
        fig_vec.update_xaxes(showgrid=True, gridcolor=GRID, range=[25, 85])
        fig_vec.update_yaxes(showgrid=True, gridcolor=GRID, range=[25, 85])
        st.plotly_chart(fig_vec, use_container_width=True)

        vc1, vc2 = st.columns(2)
        with vc1:
            section("RANKING CCAA — SCORE GLOBAL")
            vec_rank = VEC.sort_values("score_global", ascending=True).tail(10)
            fig_rank = go.Figure(go.Bar(
                y=vec_rank["ccaa"], x=vec_rank["score_global"],
                orientation="h",
                marker_color=[COLOR_Q[c] for c in vec_rank["cuadrante"]],
                marker_line_width=0,
                text=[f"{v:.0f}" for v in vec_rank["score_global"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_rank.update_layout(**lay(h=320, margin=dict(t=10,b=10,l=8,r=40)))
            fig_rank.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 90])
            st.plotly_chart(fig_rank, use_container_width=True)

        with vc2:
            section("CUADRANTE ESTRATÉGICO — RESUMEN")
            quad_counts = VEC.groupby("cuadrante").size().reset_index(name="n")
            fig_q = go.Figure(go.Pie(
                labels=quad_counts["cuadrante"], values=quad_counts["n"],
                marker=dict(colors=[COLOR_Q[c] for c in quad_counts["cuadrante"]],
                            line=dict(color=PAPER, width=2)),
                textinfo="label+value", textfont=dict(size=10), hole=0.4,
            ))
            fig_q.update_layout(**lay(h=320, margin=dict(t=10,b=10,l=8,r=8)))
            st.plotly_chart(fig_q, use_container_width=True)

        callout(
            "<strong>5 CCAA en Prioridad Máxima:</strong> Madrid, País Vasco, Navarra, Baleares y "
            "Cantabria — alta renta, alta oportunidad (baja penetración actual) y buena "
            "rentabilidad esperada. <strong>Andalucía y C. Valenciana están en Crecer con Cautela</strong> "
            "— alta oportunidad por masa de población pero menor rentabilidad media "
            "por renta disponible más baja. Extremadura y Castilla-La Mancha en 'Revisar estrategia' "
            "— producto de precio bajo o acuerdos con sanidad pública, no pólizas premium."
        )

    # ── TAB 2: Captación ──────────────────────────────────────
    with tab2:
        section("FUNNEL DE CAPTACIÓN DIGITAL")
        fig_fun = go.Figure(go.Funnel(
            y=df_funnel["etapa"], x=df_funnel["volumen"],
            marker=dict(
                color=[ACCENT, A2, A3, "#1B6B4A", "#D4940A", "#6A1B9A"],
                line=dict(color="rgba(255,255,255,0.25)", width=1),
            ),
            textinfo="value+percent previous",
            textfont=dict(size=13, color="#fff", family="Inter,sans-serif"),
            textposition="inside",
            connector=dict(line=dict(color=GRID, width=1, dash="dot")),
        ))
        fig_fun.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=11),
            height=420, margin=dict(t=10, b=10, l=8, r=8),
        )
        st.plotly_chart(fig_fun, use_container_width=True)

        section("HEATMAP DE RENTABILIDAD — PÓLIZA × CCAA")
        fig_heat = go.Figure(go.Heatmap(
            z=heat_mat, x=ccaa_list_v, y=df_pol["poliza"].tolist(),
            colorscale=[[0,"#EEF4FF"],[0.4,A3],[0.7,A2],[1.0,ACCENT]],
            text=[[f"{v:.0f}" for v in row] for row in heat_mat],
            texttemplate="%{text}", textfont=dict(size=8, color="#fff"),
            showscale=True,
            colorbar=dict(title="Score", tickfont=dict(size=9), len=0.6),
        ))
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=10),
            height=440, margin=dict(t=10,b=10,l=8,r=10),
            xaxis=dict(tickangle=-30, tickfont=dict(size=8)),
            yaxis=dict(tickfont=dict(size=9), autorange="reversed"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        callout(
            "<strong>La tasa de conversión lead → alta es del 28.1%</strong> (36.200 altas / 128.600 leads), "
            "por encima del benchmark del sector (8.2%). El canal digital mantiene una retención "
            "del 70% entre etapas gracias a flujos de re-engagement automatizados (email + push Blua). "
            "El mayor drop se produce entre visitas y lead (76.4% conversión) — "
            "foco en reducir fricción del formulario inicial. "
            "<strong>Accede y Premium 500.000 son las pólizas con mayor rentabilidad</strong> "
            "en Madrid, País Vasco y Navarra. DKV está captando el segmento joven digital "
            "con precios 15% inferiores en la gama Básica."
        )

    # ── TAB 3: Competencia ────────────────────────────────────
    with tab3:
        cc1, cc2 = st.columns(2)
        with cc1:
            section("CUOTA DE MERCADO POR CCAA (%)")
            df_cc_m = df_cuota_ccaa.melt("ccaa", var_name="aseguradora", value_name="cuota")
            fig_cc = px.bar(
                df_cc_m, x="cuota", y="ccaa", color="aseguradora", orientation="h",
                color_discrete_map={"Sanitas": ACCENT, "Adeslas": "#B71C1C", "Asisa": "#2E7D32"},
                labels={"cuota":"Cuota %","ccaa":"","aseguradora":""},
            )
            fig_cc.update_layout(**lay(h=480, showlegend=True,
                legend=dict(orientation="h", y=1.06, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=8)))
            fig_cc.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_cc, use_container_width=True)

        with cc2:
            section("PRICING SANITAS VS. COMPETENCIA (€/mes por gama)")
            df_pr = df_precios_comp.set_index("poliza")
            fig_pr = go.Figure()
            for comp, color in [("Sanitas",ACCENT),("Adeslas","#B71C1C"),("Asisa","#2E7D32"),("DKV","#E65100")]:
                fig_pr.add_trace(go.Scatter(
                    x=df_precios_comp["poliza"], y=df_precios_comp[comp],
                    name=comp, mode="lines+markers",
                    line=dict(color=color, width=2.5 if comp=="Sanitas" else 1.5),
                    marker=dict(size=8 if comp=="Sanitas" else 5),
                ))
            fig_pr.update_layout(**lay(h=320, showlegend=True,
                legend=dict(orientation="h", y=1.12, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=8,r=8)))
            fig_pr.update_xaxes(tickangle=-20, tickfont=dict(size=9))
            fig_pr.update_yaxes(showgrid=True, gridcolor=GRID, tickprefix="€")
            st.plotly_chart(fig_pr, use_container_width=True)

            section("GAP DE PRECIO SANITAS vs. COMPETENCIA MÁS BARATA (%)")
            df_gap = df_precios_comp.copy()
            df_gap["min_comp"] = df_gap[["Adeslas","Asisa","DKV"]].min(axis=1)
            df_gap["gap_pct"]  = ((df_gap["Sanitas"] - df_gap["min_comp"]) / df_gap["min_comp"] * 100).round(1)
            fig_gap = go.Figure(go.Bar(
                x=df_gap["poliza"], y=df_gap["gap_pct"],
                marker_color=[ACCENT if v > 0 else "#2E7D32" for v in df_gap["gap_pct"]],
                marker_line_width=0,
                text=[f"+{v:.1f}%" if v > 0 else f"{v:.1f}%" for v in df_gap["gap_pct"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_gap.add_hline(y=0, line_color=S_BORDER, line_width=1)
            fig_gap.update_layout(**lay(h=200, margin=dict(t=10,b=10,l=8,r=8)))
            fig_gap.update_yaxes(showgrid=True, gridcolor=GRID, ticksuffix="%")
            st.plotly_chart(fig_gap, use_container_width=True)

        callout(
            "<strong>Sanitas tiene un precio prime en todas las gamas</strong> — entre +6% "
            "(Senior) y +17% (Básica/Accede) sobre la competencia más barata. "
            "Este gap es sostenible en los segmentos de alta renta "
            "(Reembolso, Profesionales) donde el precio no es el driver principal. "
            "<strong>En la gama Básica el gap del 17% es un riesgo real</strong>: "
            "DKV y Adeslas están captando el segmento joven con precios muy competitivos. "
            "Sanitas necesita una propuesta digital (Blua) que justifique el diferencial "
            "o ajustar la gama de entrada para no perder la captación de clientes jóvenes."
        )

    # ── TAB 4: Epidemiología & Demanda ────────────────────────
    with tab4:
        # ── Selector jerárquico: grupo → indicador ────────────
        ec_ctrl1, ec_ctrl2, ec_ctrl3 = st.columns([1.2, 2.2, 0.8])
        with ec_ctrl1:
            cat_sel = st.selectbox("Grupo de enfermedad", list(DISEASE_CATS.keys()), key="epi_cat")
        with ec_ctrl2:
            ind_sel = st.selectbox("Indicador", list(DISEASE_CATS[cat_sel].keys()), key="epi_ind")
        col_sel = DISEASE_CATS[cat_sel][ind_sel]
        fuente, lectura = EPI_DESC2.get(col_sel, ("Fuentes INE / Ministerio de Sanidad", "Sin interpretación disponible."))

        section(f"MAPA DE ESPAÑA — {ind_sel.upper()}")

        # ── Densitymapbox: rellena las regiones sin GeoJSON ───
        cs_density = {
            "espera_pub_dias": [[0,"#2E7D32"],[0.5,"#FFF9C4"],[1,"#B71C1C"]],
            "penetracion_seg": [[0,"#FFF3E0"],[0.5,A3],[1,ACCENT]],
            "autonomos_pct":   [[0,"#FFF3E0"],[0.5,A3],[1,ACCENT]],
            "pob_35_54_pct":   [[0,"#FFF3E0"],[0.5,A3],[1,ACCENT]],
            "card_ic_pct":     [[0,"#FFF3E0"],[0.5,"#E65100"],[1,"#B71C1C"]],
            "card_iam_pct":    [[0,"#FFF3E0"],[0.5,"#E65100"],[1,"#B71C1C"]],
            "hta_pct":         [[0,"#FFF3E0"],[0.5,"#E65100"],[1,"#B71C1C"]],
            "dlp_pct":         [[0,"#FFFDE7"],[0.5,"#F57F17"],[1,"#BF360C"]],
        }
        colorscale = cs_density.get(col_sel, [[0,"#FFF9C4"],[0.5,"#E65100"],[1,"#B71C1C"]])

        fig_map = go.Figure()
        fig_map.add_trace(go.Densitymap(
            lat=df_epi["lat"],
            lon=df_epi["lon"],
            z=df_epi[col_sel].tolist(),
            radius=68,
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title=ind_sel[:20], tickfont=dict(size=9), len=0.65, x=1.0),
            hoverinfo="none",
            name="Prevalencia",
        ))
        fig_map.add_trace(go.Scattermap(
            lat=df_epi["lat"],
            lon=df_epi["lon"],
            mode="text+markers",
            text=df_epi["ccaa"],
            customdata=df_epi[col_sel].tolist(),
            hovertemplate="<b>%{text}</b><br>" + ind_sel + ": %{customdata:.1f}<extra></extra>",
            textfont=dict(size=8, color=FONT),
            textposition="top right",
            marker=dict(size=5, color=FONT, opacity=0.65),
            name="CCAA",
            showlegend=False,
        ))
        fig_map.update_layout(
            map_style="open-street-map",
            map_zoom=4.4,
            map_center={"lat": 39.8, "lon": -3.2},
            height=460,
            margin=dict(t=10, b=10, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown(
            f'<div style="font-size:.72rem;color:{S_MUTED};margin-bottom:4px">'
            f'<strong style="color:{FONT}">Fuente:</strong> {fuente}</div>',
            unsafe_allow_html=True)
        callout(f"<strong>Lectura:</strong> {lectura}")

        # ── Evolución histórica 2018–2025 ─────────────────────
        if col_sel in EPI_HIST_BASE:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            section("EVOLUCIÓN HISTÓRICA — PREVALENCIA NACIONAL 2018–2025")

            epi_nom_list = df_epi["ccaa"].tolist()
            ccaa_hist = st.selectbox(
                "CCAA para comparativa", ["Nacional (media)"] + epi_nom_list, key="epi_hist_ccaa"
            )
            base_vals = EPI_HIST_BASE[col_sel]
            if ccaa_hist == "Nacional (media)":
                hist_vals = base_vals
            else:
                idx_c  = epi_nom_list.index(ccaa_hist)
                delta  = (df_epi[col_sel].iloc[idx_c] - df_epi[col_sel].mean()) / (df_epi[col_sel].mean() + 0.001)
                hist_vals = [round(v * (1 + delta * 0.75 + i * 0.004), 2) for i, v in enumerate(base_vals)]

            fig_hist = go.Figure()
            fig_hist.add_trace(go.Scatter(
                x=EPI_ANOS, y=hist_vals,
                mode="lines+markers",
                name=ccaa_hist,
                line=dict(color=ACCENT, width=2.5),
                marker=dict(size=7, color=ACCENT),
                fill="tozeroy",
                fillcolor="rgba(0,48,135,0.08)",
                hovertemplate="%{x}: <b>%{y:.1f}</b><extra></extra>",
            ))
            for yr, lbl in [(2020, "COVID-19"), (2021, "COVID-19")]:
                fig_hist.add_vline(x=yr, line_dash="dot", line_color=S_MUTED, line_width=1,
                                   annotation_text=lbl, annotation_font_size=8,
                                   annotation_font_color=S_MUTED)
            fig_hist.update_layout(**lay(h=260, margin=dict(t=10, b=10, l=8, r=8)))
            fig_hist.update_xaxes(showgrid=True, gridcolor=GRID, tickvals=EPI_ANOS)
            fig_hist.update_yaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_hist, use_container_width=True)

        with st.expander("Nota sobre datos por Código Postal (CP)"):
            st.markdown(
                "Los datos de prevalencia a nivel de CP requieren la **Encuesta Nacional de Salud "
                "a escala subprovincial** (INE, bajo petición) o la adquisición de datos de "
                "siniestralidad propia georreferenciada por CP. La capa CP estaría disponible "
                "una vez integrada la fuente de datos interna de Sanitas o la licencia INE ENSE-CP. "
                "El mapa actual trabaja a nivel de capital de CCAA (17 puntos)."
            )

        # ── Heatmap estacional ────────────────────────────────
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        section("ÍNDICE DE DEMANDA SANITARIA ESPERADA — MES × REGIÓN (escala 0–100)")

        fig_seas = go.Figure(go.Heatmap(
            z=demand_seas,
            x=MESES_N,
            y=GRP_CCAA,
            colorscale=[[0,"#EEF4FF"],[0.35,A3],[0.65,A2],[1,"#B71C1C"]],
            text=[[f"{int(v)}" for v in row] for row in demand_seas],
            texttemplate="%{text}",
            textfont=dict(size=9),
            showscale=True,
            zmin=45, zmax=100,
            colorbar=dict(title="Índice", tickfont=dict(size=9), len=0.65),
        ))
        fig_seas.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=10),
            height=320, margin=dict(t=10,b=10,l=8,r=10),
            xaxis=dict(tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=9)),
        )
        st.plotly_chart(fig_seas, use_container_width=True)

        callout(
            "<strong>Canarias y Baleares alcanzan índice 96 en agosto</strong> — pico de turismo + "
            "población flotante que puede activar pólizas de reembolso y travel. "
            "<strong>País Vasco/Navarra llega a 88 en julio</strong> (San Fermín): "
            "traumatología y cirugía urgente disparan el uso. Enero es el pico nacional "
            "por gripe (96 en el índice nacional) — momento óptimo para activar Blua digital "
            "y descomprimir urgencias presenciales."
        )

        # ── Timeline de eventos ───────────────────────────────
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        section("CALENDARIO DE EVENTOS MASIVOS Y PATRONES CÍCLICOS — ÍNDICE DE PRESIÓN SANITARIA (FUENTES PÚBLICAS)")

        TIPO_C = {"Estacional":"#B71C1C","Deporte":ACCENT,"Festivo":"#E65100",
                  "Turismo":"#2E7D32","Masivo":"#6A1B9A","Laboral":"#795548"}

        # Gráfico a ancho completo
        fig_ev = go.Figure()
        for tipo, color in TIPO_C.items():
            sub = df_eventos[df_eventos["tipo"] == tipo]
            if len(sub) == 0: continue
            fig_ev.add_trace(go.Scatter(
                x=sub["mes"], y=sub["impacto"],
                mode="markers+text",
                name=tipo,
                text=sub["evento"],
                textposition="top center",
                textfont=dict(size=7.5, color=FONT),
                marker=dict(
                    size=sub["dur"] * 8 + 12,
                    color=color, opacity=0.82,
                    line=dict(color=PAPER, width=1.5),
                ),
                customdata=sub[["ccaa","esp","dur","metrica","fuente"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "CCAA: %{customdata[0]}  ·  Duración: %{customdata[2]} mes(es)<br>"
                    "Especialidad: %{customdata[1]}<br>"
                    "Índice impacto: <b>%{y}</b>/100<br>"
                    "<i>%{customdata[3]}</i><br>"
                    "<span style='font-size:10px;color:#86868B'>Fuente: %{customdata[4]}</span>"
                    "<extra></extra>"
                ),
            ))
        fig_ev.add_hline(y=80, line_dash="dot", line_color="#B71C1C", line_width=1,
                         annotation_text="Impacto crítico", annotation_font_size=8,
                         annotation_font_color="#B71C1C")
        fig_ev.update_layout(
            **lay(h=420, showlegend=True,
                  legend=dict(orientation="h", y=-0.14, font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
                  margin=dict(t=14, b=56, l=8, r=8)),
        )
        fig_ev.update_xaxes(
            tickvals=list(range(1, 13)), ticktext=MESES_N,
            showgrid=True, gridcolor=GRID, range=[0.3, 12.7],
            title_text="Mes del año", title_font=dict(size=9),
        )
        fig_ev.update_yaxes(
            showgrid=True, gridcolor=GRID, range=[45, 105],
            title_text="Índice de impacto en siniestralidad (0–100)", title_font=dict(size=9),
        )
        st.plotly_chart(fig_ev, use_container_width=True)

        # Chips de eventos en fila horizontal
        df_ev_show = df_eventos[["evento","mes","ccaa","esp","impacto","tipo"]].copy()
        df_ev_show = df_ev_show.sort_values("impacto", ascending=False)
        chips_html = (
            f'<div style="display:flex;flex-wrap:wrap;gap:7px;margin-top:12px">'
        )
        for _, row in df_ev_show.iterrows():
            c = TIPO_C.get(row["tipo"], S_MUTED)
            mes_txt = MESES_N[int(row["mes"]) - 1]
            chips_html += (
                f'<div style="display:flex;align-items:center;gap:6px;'
                f'padding:6px 11px;background:{PAPER};border-radius:20px;'
                f'border:1px solid {c}22;border-left:3px solid {c};'
                f'box-shadow:0 1px 3px rgba(0,0,0,.05);white-space:nowrap">'
                f'<span style="font-size:.72rem;font-weight:600;color:{FONT}">{row["evento"]}</span>'
                f'<span style="font-size:.65rem;color:{S_MUTED}">{mes_txt}</span>'
                f'<span style="font-size:.68rem;font-weight:700;color:{c}">{int(row["impacto"])}</span>'
                f'</div>'
            )
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

        callout(
            "<strong>Tres picos críticos concentran el 65% del exceso de demanda anual:</strong> "
            "enero (gripe, índice 96), julio–agosto (verano: San Fermín 88, turismo costero 92, "
            "calor extremo 78 en Andalucía) y la campaña polínica de abril–junio (82 en alergología). "
            "<strong>Implicación operativa:</strong> pre-posicionar capacidad en traumatología y "
            "urgencias en Navarra (julio), en neumología en enero (nacional) y en alergología "
            "en primavera. <strong>Implicación comercial:</strong> campañas de captación "
            "digital en Can./Baleares en mayo–junio, antes del pico, cuando el asegurado "
            "aún no ha necesitado el servicio y el comparador tiene menos tráfico."
        )

    # ── TAB 5: Colectivos & Empresas ─────────────────────────
    with tab5:
        # KPIs resumen
        total_aseg  = df_col["asegurados"].sum()
        total_ing   = df_col["ingreso_anual"].sum()
        total_marg  = df_col["margen_anual"].sum()
        n_renovar   = (df_col["decision"] == "Renovar").sum()
        n_subir     = (df_col["decision"] == "Subir tasa").sum()
        n_reneg     = (df_col["decision"] == "Renegociar").sum()
        n_no        = (df_col["decision"] == "No renovar / renegociar").sum()
        vinc_alta   = (df_col["score_vinc"] >= 4).sum()

        k1,k2,k3,k4 = st.columns(4)
        kpi_card(k1, "Asegurados en colectivos", f"{total_aseg:,.0f}", f"{len(df_col)} empresas activas")
        kpi_card(k2, "Ingreso anual colectivos",  f"{total_ing:.0f} K€", "Prima × asegurados × 12")
        kpi_card(k3, "Margen neto anual",         f"{total_marg:.0f} K€",
                 f"Loss ratio medio {df_col['loss_ratio'].mean():.1f}%",
                 negative=total_marg < 0)
        kpi_card(k4, "Decisión renovación",
                 f"{n_renovar} ✓  {n_subir} ⚠  {n_reneg} ◑  {n_no} ✗",
                 f"Renovar · Subir tasa · Renegociar · No renovar")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # ── Scatter prima vs gasto ────────────────────────────
        section("RENTABILIDAD POR COLECTIVO — PRIMA VS. GASTO POR ASEGURADO (€/mes)")

        fig_sc = go.Figure()

        # Línea de break-even
        x_rng = [df_col["prima"].min()-4, df_col["prima"].max()+4]
        fig_sc.add_trace(go.Scatter(
            x=x_rng, y=x_rng, mode="lines",
            line=dict(color=S_MUTED, width=1.5, dash="dot"),
            name="Break-even (prima = gasto)",
            showlegend=True,
        ))

        for dec, color, symbol in [
            ("Renovar",                  "#1B6B4A", "circle"),
            ("Subir tasa",               "#D4940A", "diamond"),
            ("Renegociar",               "#6A1B9A", "circle-open"),
            ("No renovar / renegociar",  "#9B2C2C", "x"),
        ]:
            sub = df_col[df_col["decision"] == dec]
            fig_sc.add_trace(go.Scatter(
                x=sub["prima"], y=sub["gasto"],
                mode="markers+text",
                name=dec,
                text=sub["empresa"],
                textposition="top center",
                textfont=dict(size=7.5, color=FONT),
                marker=dict(
                    size=(sub["asegurados"]/400 + 10).clip(12, 36),
                    color=color, symbol=symbol,
                    line=dict(color=PAPER, width=1.5), opacity=0.88,
                ),
                customdata=sub[["asegurados","loss_ratio","margen_anual","renovacion"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Prima: %{x:.2f} €/mes · Gasto: %{y:.2f} €/mes<br>"
                    "Loss Ratio: %{customdata[1]:.1f}%<br>"
                    "Asegurados: %{customdata[0]:,}<br>"
                    "Margen anual: %{customdata[2]:.0f} K€<br>"
                    "Próxima renovación: %{customdata[3]}<extra></extra>"
                ),
            ))

        fig_sc.add_annotation(
            x=x_rng[1]-1, y=x_rng[1]-1,
            text="Break-even",
            font=dict(size=8, color=S_MUTED), showarrow=False,
            xanchor="right",
        )
        fig_sc.add_annotation(
            x=(x_rng[0]+x_rng[1])/2, y=x_rng[1]+2,
            text="▲ Zona de revisión (gasto > prima)",
            font=dict(size=8, color="#9B2C2C"), showarrow=False,
        )
        fig_sc.add_annotation(
            x=(x_rng[0]+x_rng[1])/2, y=x_rng[0]-2,
            text="▼ Zona rentable (gasto < prima)",
            font=dict(size=8, color="#1B6B4A"), showarrow=False,
        )
        fig_sc.update_layout(**lay(h=460, showlegend=True,
            legend=dict(orientation="h", y=1.08, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=14,b=14,l=8,r=8)))
        fig_sc.update_xaxes(title_text="Prima media (€/mes/asegurado)", title_font=dict(size=9),
                            showgrid=True, gridcolor=GRID)
        fig_sc.update_yaxes(title_text="Gasto medio (€/mes/asegurado)", title_font=dict(size=9),
                            showgrid=True, gridcolor=GRID)
        st.plotly_chart(fig_sc, use_container_width=True)

        # ── Tabla de decisión ─────────────────────────────────
        tc1, tc2 = st.columns([2, 1])

        with tc1:
            section("TABLA DE RENTABILIDAD Y DECISIÓN DE RENOVACIÓN")
            df_tbl = df_col.sort_values("loss_ratio", ascending=False)[
                ["empresa","sector","asegurados","prima","gasto","loss_ratio",
                 "margen_anual","renovacion","decision","dec_color","score_vinc","productos_vinc"]
            ].copy()

            for _, row in df_tbl.iterrows():
                lr     = row["loss_ratio"]
                clr    = row["dec_color"]
                marg   = row["margen_anual"]
                marg_s = f"+{marg:.0f} K€" if marg >= 0 else f"{marg:.0f} K€"
                marg_c = "#1B6B4A" if marg >= 0 else "#9B2C2C"
                score  = int(row["score_vinc"])
                sc_c   = "#1B6B4A" if score >= 4 else "#D4940A" if score >= 2 else S_MUTED
                dots   = "●" * score + "○" * (5 - score)
                prod_chips = "".join(
                    f'<span style="font-size:.58rem;padding:2px 5px;background:{VINC_PROD_C.get(p,"#888")}18;'
                    f'color:{VINC_PROD_C.get(p,"#888")};border-radius:10px;'
                    f'border:1px solid {VINC_PROD_C.get(p,"#888")}44;white-space:nowrap">{p}</span>'
                    for p in row["productos_vinc"]
                )
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:12px;padding:9px 14px;'
                    f'margin-bottom:5px;background:{PAPER};border-radius:11px;'
                    f'border-left:4px solid {clr};'
                    f'box-shadow:0 1px 5px rgba(0,0,0,.06)">'
                    f'<div style="flex:1.8;min-width:0">'
                    f'<div style="font-size:.8rem;font-weight:600;color:{FONT};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{row["empresa"]}</div>'
                    f'<div style="font-size:.67rem;color:{S_MUTED}">{row["sector"]} · {row["asegurados"]:,} aseg. · Renov. {row["renovacion"]}</div>'
                    f'</div>'
                    f'<div style="text-align:center;min-width:72px">'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">Prima</div>'
                    f'<div style="font-size:.86rem;font-weight:600;color:{FONT}">{row["prima"]:.2f}€</div>'
                    f'</div>'
                    f'<div style="text-align:center;min-width:72px">'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">Gasto</div>'
                    f'<div style="font-size:.86rem;font-weight:600;color:{FONT}">{row["gasto"]:.2f}€</div>'
                    f'</div>'
                    f'<div style="text-align:center;min-width:68px">'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">Loss ratio</div>'
                    f'<div style="font-size:.9rem;font-weight:700;color:{clr}">{lr:.1f}%</div>'
                    f'</div>'
                    f'<div style="text-align:center;min-width:80px">'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">Margen/año</div>'
                    f'<div style="font-size:.8rem;font-weight:600;color:{marg_c}">{marg_s}</div>'
                    f'</div>'
                    f'<div style="flex:0 0 160px;display:flex;flex-direction:column;gap:3px;align-items:flex-start">'
                    f'<div style="font-size:.68rem;color:{S_MUTED}">Vinculación</div>'
                    f'<div style="font-size:.75rem;font-weight:700;color:{sc_c};letter-spacing:.04em">{dots} {score}/5</div>'
                    f'<div style="display:flex;flex-wrap:wrap;gap:3px">{prod_chips}</div>'
                    f'</div>'
                    f'<div style="text-align:right;min-width:120px">'
                    f'<div style="font-size:.72rem;font-weight:600;color:{clr};'
                    f'background:{clr}18;padding:4px 10px;border-radius:20px;white-space:nowrap">'
                    f'{row["decision"]}</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        with tc2:
            section("RENTABILIDAD POR SECTOR")
            sec_grp = df_col.groupby("sector").agg(
                loss_ratio=("loss_ratio","mean"),
                asegurados=("asegurados","sum"),
                margen=("margen_anual","sum"),
            ).reset_index().sort_values("loss_ratio")

            fig_sec = go.Figure(go.Bar(
                y=sec_grp["sector"], x=sec_grp["loss_ratio"],
                orientation="h",
                marker_color=[
                    "#1B6B4A" if v < 85 else "#D4940A" if v < 100 else "#9B2C2C"
                    for v in sec_grp["loss_ratio"]
                ],
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in sec_grp["loss_ratio"]],
                textposition="outside", textfont=dict(size=9),
            ))
            fig_sec.add_vline(x=100, line_dash="dot", line_color="#9B2C2C", line_width=1.5,
                              annotation_text="Break-even", annotation_font_size=8,
                              annotation_font_color="#9B2C2C")
            fig_sec.add_vline(x=85, line_dash="dot", line_color="#D4940A", line_width=1,
                              annotation_text="Umbral revisión", annotation_font_size=8,
                              annotation_font_color="#D4940A")
            fig_sec.update_layout(**lay(h=360, margin=dict(t=10,b=10,l=8,r=55)))
            fig_sec.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, 115])
            st.plotly_chart(fig_sec, use_container_width=True)

            section("PRÓXIMAS RENOVACIONES")
            prox = df_col.sort_values("renovacion")[["empresa","renovacion","loss_ratio","decision","dec_color"]].head(8)
            for _, r in prox.iterrows():
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:6px 10px;margin-bottom:4px;background:{PAPER};border-radius:8px;'
                    f'border-left:3px solid {r["dec_color"]};font-size:.75rem">'
                    f'<div><div style="font-weight:600;color:{FONT}">{r["empresa"]}</div>'
                    f'<div style="color:{S_MUTED}">{r["renovacion"]}</div></div>'
                    f'<div style="font-weight:700;color:{r["dec_color"]}">{r["loss_ratio"]:.0f}%</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        callout(
            "<strong>Cartera de colectivos saneada:</strong> 11 de 20 empresas en zona rentable "
            "(LR &lt;85%) y 7 con margen positivo con ajuste moderado de tasa (LR 85–100%). "
            "Solo Acciona (104.7%) y Mapfre empleados (106.4%) superan el break-even — "
            "candidatos a renegociar condiciones en la próxima convocatoria. "
            "<strong>El sector tecnológico lidera la rentabilidad</strong>: Amazon ES (LR 60.3%) "
            "e Indra/Minsait (LR 65.9%) con poblaciones jóvenes y baja siniestralidad. "
            "<strong>Banca y retail</strong> requieren seguimiento: LR medio del 90-92%, "
            "justificado por plantillas maduras y alta utilización de especialistas. "
            "Prima media de cartera colectivos: 57.2 €/asegurado/mes vs. gasto 46.8 € → "
            "margen bruto del 18.2% antes de gastos de gestión."
        )
