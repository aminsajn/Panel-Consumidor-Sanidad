#!/usr/bin/env python3
"""
Sanitas — Plataforma de Inteligencia Corporativa
Vista Ejecutiva · Retención & Cartera · Optimización Operativa · Inteligencia Comercial
python -m streamlit run panel_sanitas.py
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
[data-testid="stSidebar"] *{{color:#1D1D1F!important;font-family:'Inter',sans-serif!important}}
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
.top-bar{{background:transparent;padding:20px 0 0;display:flex;align-items:baseline;
  justify-content:space-between;border-bottom:1px solid rgba(0,0,0,.06);margin-bottom:2.4rem}}
.top-title{{font-size:.95rem;font-weight:600;color:#1D1D1F;letter-spacing:-.01em}}
.top-sub{{font-size:.72rem;color:#86868B;letter-spacing:.02em}}
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
    "aseguradora": ["Adeslas","Sanitas","Asisa","DKV","Mapfre Salud","AXA Salud","Otros"],
    "cuota":       [24.8, 18.7, 14.2, 8.6, 7.4, 5.9, 20.4],
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
    {"ccaa":"Madrid",        "renta":88,"penetracion":62,"enfermedad":58,"acceso":82,"turismo":82,"deporte":68,"autonomo":32,"lat":40.42,"lon":-3.70},
    {"ccaa":"Cataluña",      "renta":85,"penetracion":54,"enfermedad":61,"acceso":78,"turismo":98,"deporte":72,"autonomo":28,"lat":41.39,"lon":2.16},
    {"ccaa":"País Vasco",    "renta":92,"penetracion":58,"enfermedad":54,"acceso":84,"turismo":48,"deporte":74,"autonomo":30,"lat":43.26,"lon":-2.93},
    {"ccaa":"Navarra",       "renta":90,"penetracion":52,"enfermedad":52,"acceso":80,"turismo":36,"deporte":76,"autonomo":26,"lat":42.82,"lon":-1.64},
    {"ccaa":"Baleares",      "renta":82,"penetracion":48,"enfermedad":50,"acceso":74,"turismo":94,"deporte":70,"autonomo":34,"lat":39.57,"lon":2.65},
    {"ccaa":"Aragón",        "renta":78,"penetracion":38,"enfermedad":56,"acceso":62,"turismo":30,"deporte":62,"autonomo":20,"lat":41.65,"lon":-0.88},
    {"ccaa":"C. Valenciana", "renta":70,"penetracion":44,"enfermedad":60,"acceso":72,"turismo":86,"deporte":61,"autonomo":26,"lat":39.47,"lon":-0.38},
    {"ccaa":"Andalucía",     "renta":58,"penetracion":32,"enfermedad":64,"acceso":60,"turismo":72,"deporte":55,"autonomo":22,"lat":37.38,"lon":-5.97},
    {"ccaa":"Murcia",        "renta":62,"penetracion":34,"enfermedad":62,"acceso":64,"turismo":52,"deporte":57,"autonomo":22,"lat":37.99,"lon":-1.13},
    {"ccaa":"Canarias",      "renta":60,"penetracion":30,"enfermedad":58,"acceso":58,"turismo":96,"deporte":58,"autonomo":24,"lat":28.29,"lon":-15.65},
    {"ccaa":"Galicia",       "renta":64,"penetracion":36,"enfermedad":68,"acceso":60,"turismo":42,"deporte":54,"autonomo":18,"lat":42.88,"lon":-8.54},
    {"ccaa":"Castilla y León","renta":68,"penetracion":34,"enfermedad":70,"acceso":54,"turismo":28,"deporte":52,"autonomo":16,"lat":41.65,"lon":-4.73},
    {"ccaa":"Castilla-La Mancha","renta":56,"penetracion":28,"enfermedad":66,"acceso":50,"turismo":18,"deporte":48,"autonomo":14,"lat":39.86,"lon":-4.03},
    {"ccaa":"Extremadura",   "renta":44,"penetracion":22,"enfermedad":62,"acceso":44,"turismo":14,"deporte":44,"autonomo":12,"lat":38.92,"lon":-6.34},
    {"ccaa":"La Rioja",      "renta":76,"penetracion":40,"enfermedad":54,"acceso":70,"turismo":22,"deporte":64,"autonomo":20,"lat":42.27,"lon":-2.37},
    {"ccaa":"Asturias",      "renta":66,"penetracion":38,"enfermedad":72,"acceso":64,"turismo":30,"deporte":60,"autonomo":16,"lat":43.36,"lon":-5.85},
    {"ccaa":"Cantabria",     "renta":72,"penetracion":42,"enfermedad":60,"acceso":68,"turismo":32,"deporte":63,"autonomo":18,"lat":43.18,"lon":-3.99},
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
    "volumen": [285000, 42800, 18600, 9200, 4100, 2840],
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

# ══════════════════════════════════════════════════════════════════
# NAVEGACIÓN
# ══════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state["page"] = "home"

with st.sidebar:
    st.markdown(
        f'<div style="padding:20px 0 6px">'
        f'<div style="font-size:1.02rem;font-weight:700;color:{ACCENT};letter-spacing:-.01em">Sanitas</div>'
        f'<div style="font-size:.68rem;color:{S_MUTED};margin-top:2px;letter-spacing:.04em">INTELIGENCIA CORPORATIVA</div>'
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
        active = st.session_state["page"] == key
        bg  = ACCENT if active else "transparent"
        col = "#fff" if active else FONT
        brd = f"1px solid {ACCENT}" if active else "1px solid transparent"
        if st.button(label, key=f"nav_{key}"):
            go_to(key); st.rerun()
        if active:
            st.markdown(
                f'<style>.stButton:last-of-type>button{{background:{bg}!important;'
                f'color:{col}!important;border:{brd}!important}}</style>',
                unsafe_allow_html=True)

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
        f'<div><div class="top-title">Plataforma de Inteligencia Corporativa · Sanitas</div>'
        f'<div class="top-sub">Panel ejecutivo · Datos ficticios orientativos · Septiembre 2026</div></div>'
        f'</div>', unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    kpi_card(h1, "Combined Ratio", "94.2%", "Loss 79.3% + Gasto 14.9%")
    kpi_card(h2, "Asegurados activos", "2.14M", "+3.2% interanual")
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
        f'<div><div class="top-title">Vista Ejecutiva</div>'
        f'<div class="top-sub">CEO · Dirección General · Septiembre 2026</div></div>'
        f'</div>', unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4)
    kpi_card(e1, "Combined Ratio", "94.2%", "Obj. <95% — en rango")
    kpi_card(e2, "Loss Ratio",     "79.3%", "Umbral sostenible: 80%")
    kpi_card(e3, "EBITDA",         "186 M€", "+8.4% vs mismo período 2025")
    kpi_card(e4, "Cuota de mercado","18.7%", "2.ª aseguradora de España")

    e5, e6, e7, e8 = st.columns(4)
    kpi_card(e5, "Asegurados activos","2.14M", "+3.2% interanual")
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
        f'<div><div class="top-title">Retención & Optimización de Cartera</div>'
        f'<div class="top-sub">Dirección de Clientes · Modelo de churn · Campañas · Rentabilidad</div></div>'
        f'</div>', unsafe_allow_html=True)

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
        f'<div><div class="top-title">Optimización Operativa</div>'
        f'<div class="top-sub">Dirección Médica · CFO · Combined Ratio · Recursos · Fraude</div></div>'
        f'</div>', unsafe_allow_html=True)

    o1, o2, o3, o4 = st.columns(4)
    kpi_card(o1, "Combined Ratio",        "94.2%",  "Loss 79.3% + Gasto 14.9%")
    kpi_card(o2, "Derivaciones externas", "1.760/mes", "Coste evitable ~4.2 M€/mes")
    kpi_card(o3, "Fraude detectado",      "96 casos/mes", "200 K€/mes recuperados")
    kpi_card(o4, "Espera media",          "11 días", "Obj. <8 días en Traumatología")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Combined Ratio por Producto", "Recursos Hospitalarios", "Fraude & Derivaciones"])

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

    # ── TAB 3: Fraude & Derivaciones ──────────────────────────
    with tab3:
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
        f'<div><div class="top-title">Inteligencia Comercial</div>'
        f'<div class="top-sub">Dirección Comercial · Oportunidad geográfica · Pricing · Captación</div></div>'
        f'</div>', unsafe_allow_html=True)

    cm1, cm2, cm3, cm4 = st.columns(4)
    kpi_card(cm1, "Cuota de mercado",    "18.7%",   "2.ª aseguradora España")
    kpi_card(cm2, "Conv. lead → alta",   "6.6%",    "Benchmark sector: 8.2%")
    kpi_card(cm3, "Pipeline colectivos", "84 empresas", "+12 nuevas este trimestre")
    kpi_card(cm4, "CCAA prioridad máx.", "5 de 17", "Score global >65 — Madrid, PV, Navarra…")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Oportunidad Geográfica", "Captación & Pólizas", "Competencia & Pricing"])

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
            marker=dict(color=[ACCENT, A2, A3, "#2E7D32", "#E65100", "#6A1B9A"]),
            textinfo="value+percent initial",
            textfont=dict(size=9, color="#fff"),
        ))
        fig_fun.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter,sans-serif", color=FONT, size=10),
            height=300, margin=dict(t=10,b=10,l=8,r=8),
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
            "<strong>La tasa de conversión lead → alta es del 6.6%</strong>, por debajo del "
            "benchmark del sector (8.2%). El mayor drop se produce entre cotización y comparación "
            "activa — momento donde el comparador de precios entra en juego. "
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
