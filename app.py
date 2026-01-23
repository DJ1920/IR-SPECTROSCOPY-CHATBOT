import streamlit as st
import pandas as pd
import re

# Configuración de la página
st.set_page_config(
    page_title="IR Spectroscopy Database",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - TEMA CLARO
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
    }
    h1 {
        color: #1e40af;
        font-family: 'Courier New', monospace;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
        border-radius: 10px;
        margin-bottom: 30px;
        border: 2px solid #6366f1;
    }
    .result-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .family-badge {
        background: linear-gradient(135deg, #0066cc 0%, #004c99 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
    }
    .stMarkdown {
        color: #1f2937;
    }
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    .stTextInput input {
        background-color: white;
        color: #1f2937;
        border: 2px solid #d1d5db;
    }
    h2, h3 {
        color: #1e40af;
    }
    .filter-indicator {
        background: #dbeafe;
        color: #1e40af;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-size: 0.9em;
        border-left: 3px solid #3b82f6;
    }
    .clear-filters-btn {
        background: #ef4444;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    """Carga la base de datos IR completa - 860 bandas"""
    data =     data = [
        {
                "familia": "Alcanos",
                "grupo": "-CH₃",
                "asignacion": "νas",
                "rango": "2975-2950 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "sh, violet shift by adjacent aromat, N or O"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃",
                "asignacion": "νs",
                "rango": "2885-2865 cm⁻¹",
                "intensidad": "m",
                "observacion": "Same"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃",
                "asignacion": "δas",
                "rango": "1465-1440 cm⁻¹",
                "intensidad": "m",
                "observacion": "Same"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃",
                "asignacion": "δs",
                "rango": "1390-1370 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Same"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₂- open",
                "asignacion": "νas",
                "rango": "2940-2915 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Same"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₂- open",
                "asignacion": "νs",
                "rango": "2870-2840 cm⁻¹",
                "intensidad": "m",
                "observacion": "Same"
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₃ cyclic",
                "asignacion": "νas",
                "rango": "3100-3070 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₃ cyclic",
                "asignacion": "νs",
                "rango": "3040-2995 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₄ cyclic",
                "asignacion": "νas",
                "rango": "3000-2975 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₄ cyclic",
                "asignacion": "νs",
                "rango": "2925-2875 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₅ cyclic",
                "asignacion": "νas",
                "rango": "2960-2950 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₅ cyclic",
                "asignacion": "νs",
                "rango": "2870-2850 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH<",
                "asignacion": "ν",
                "rango": "2890-2880 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH<",
                "asignacion": "Sin asignación específica",
                "rango": "2830±2770 cm⁻¹",
                "intensidad": "m",
                "observacion": "In aldehydes, Fermi resonance"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃ (deformaciones)",
                "asignacion": "δas",
                "rango": "1475-1465 cm⁻¹",
                "intensidad": "m",
                "observacion": "High-frequency side of δ(CH₂)"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃ (deformaciones)",
                "asignacion": "δs",
                "rango": "1390-1380 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "sh"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₃ (deformaciones)",
                "asignacion": "δs",
                "rango": "1385, 1370 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Doublet by coupling, almost equal intensity"
        },
        {
                "familia": "Alcanos",
                "grupo": "-C(CH₃)₃",
                "asignacion": "δs",
                "rango": "1395, 1365 cm⁻¹",
                "intensidad": "m, m-s",
                "observacion": "Doublet by coupling, sh"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₂-",
                "asignacion": "δ",
                "rango": "1470-1450 cm⁻¹",
                "intensidad": "m",
                "observacion": "Overlaps with δas(CH₃)"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH<",
                "asignacion": "δ",
                "rango": "ca. 1340 cm⁻¹",
                "intensidad": "w",
                "observacion": "Rarely identifiable"
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₃ cyclic",
                "asignacion": "δ(CH₂)",
                "rango": "1420-1400 cm⁻¹",
                "intensidad": "s",
                "observacion": "Varies with substitution"
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₃ cyclic",
                "asignacion": "νas(ring)",
                "rango": "1365-1295 cm⁻¹",
                "intensidad": "s",
                "observacion": "Varies with substitution"
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₄ cyclic",
                "asignacion": "δ(CH₂)",
                "rango": "1450-1440 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "(CH₂)₄ cyclic",
                "asignacion": "νas(ring)",
                "rango": "1245-1220 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Varies with substitution"
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH(CH₃)₂",
                "asignacion": "ν(C-C)",
                "rango": "1175-1165 cm⁻¹",
                "intensidad": "m",
                "observacion": "No H on central C: 1190"
        },
        {
                "familia": "Alcanos",
                "grupo": "-C(CH₃)₃-",
                "asignacion": "ρ(CH₃)",
                "rango": "1150-1130 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-C(CH₃)₃-",
                "asignacion": "ω(CH₃)₂?",
                "rango": "840-790 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-C(CH₃)₃-",
                "asignacion": "Sin asignación específica",
                "rango": "495-490 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "C-CH₃",
                "asignacion": "ρ(CH₃)",
                "rango": "ca. 970 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "C-CH₂-CH₃",
                "asignacion": "ρ(CH₃)",
                "rango": "ca. 925 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-C(CH₃)₂-",
                "asignacion": "δ(CCC)",
                "rango": "510-505 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-(CH₂)n-, n >3",
                "asignacion": "ρ(CH₂)",
                "rango": "725-720 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Splits in crystalline chains"
        },
        {
                "familia": "Alcanos",
                "grupo": "-(CH₂)₄-",
                "asignacion": "Sin asignación específica",
                "rango": "735-725 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-(CH₂)₃-",
                "asignacion": "Sin asignación específica",
                "rango": "745-735 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alcanos",
                "grupo": "-CH₂-",
                "asignacion": "Sin asignación específica",
                "rango": "785-770 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "νas(CH₃)",
                "rango": "2995-2955 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "νs(CH₃)",
                "rango": "2900-2865 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "Sin asignación específica",
                "rango": "2835-2815 cm⁻¹",
                "intensidad": "s",
                "observacion": "Fermi resonance"
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "δas(CH₃)",
                "rango": "1470-1430 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "δs",
                "rango": "1445-1430 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-O-CH₃",
                "asignacion": "νas(C-O-C)",
                "rango": "1120-1100 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "Ar-O-CH₃",
                "asignacion": "νas(CH₃)",
                "rango": "2840-2820 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "Ar-O-CH₃",
                "asignacion": "νas(Ar-O-C)",
                "rango": "1260-1245 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "R-N-CH₃",
                "asignacion": "νa(CH₃)",
                "rango": "2805-2780 cm⁻¹",
                "intensidad": "s",
                "observacion": "Fermi resonance?"
        },
        {
                "familia": "Éteres",
                "grupo": "R-N-CH₃",
                "asignacion": "δ(CH₃)",
                "rango": "ca. 1460 cm⁻¹",
                "intensidad": "m",
                "observacion": "Merges with δ(CH₂)"
        },
        {
                "familia": "Éteres",
                "grupo": "R-N(CH₃)₂",
                "asignacion": "ν(CH₃)",
                "rango": "2825-2810 cm⁻¹",
                "intensidad": "s",
                "observacion": "Fermi resonance?"
        },
        {
                "familia": "Éteres",
                "grupo": "R-N(CH₃)₂",
                "asignacion": "ν(CH₃)",
                "rango": "2775-2765 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "Ar-N-CH₃",
                "asignacion": "ν(CH₃)",
                "rango": "2820-2810 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "Ar-N(CH₃)₂",
                "asignacion": "ν(CH₃)",
                "rango": "2800 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "P-CH₃",
                "asignacion": "δs(CH₃)",
                "rango": "1320-1280 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "P-CH₃",
                "asignacion": "ρ(CH₃)",
                "rango": "960-830 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "S-CH₃",
                "asignacion": "δs(CH₃)",
                "rango": "1325-1300 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "S-CH₃",
                "asignacion": "ρ(CH₃)",
                "rango": "1030-950 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Éteres",
                "grupo": "O-Si-CH₃",
                "asignacion": "νas(CH₃)",
                "rango": "ca. 2960 cm⁻¹",
                "intensidad": "s",
                "observacion": "In polysiloxanes"
        },
        {
                "familia": "Éteres",
                "grupo": "O-Si-CH₃",
                "asignacion": "νs(CH₃)",
                "rango": "ca. 2910 cm⁻¹",
                "intensidad": "w",
                "observacion": "Same"
        },
        {
                "familia": "Éteres",
                "grupo": "O-Si-CH₃",
                "asignacion": "δs(CH₃)",
                "rango": "1260 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Same"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles, furans, thiophenes (general)",
                "asignacion": "ν(ring)",
                "rango": "ca. 1580 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles, furans, thiophenes (general)",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1490 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles, furans, thiophenes (general)",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1400 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "ν(NH)",
                "rango": "3500-3400 cm⁻¹",
                "intensidad": "var sh",
                "observacion": "In dilute solution"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "Sin asignación específica",
                "rango": "3400-3000 cm⁻¹",
                "intensidad": "s br",
                "observacion": "In condensed state"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "ν(ring-H)",
                "rango": "3100-3010 cm⁻¹",
                "intensidad": "m",
                "observacion": "Several peaks"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "ν(ring)",
                "rango": "1580-1545 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "N substituted: 2 bands"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1470 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "Sin asignación específica",
                "rango": "1430-1390 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyrroles",
                "asignacion": "γ(ring)",
                "rango": "ca. 480 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Not greatly influenced by substit."
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "ν(ring-H)",
                "rango": "3090-3000 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Several bands"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "ν(ring)",
                "rango": "1615-1575 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Intensity depends on substitution"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "Sin asignación específica",
                "rango": "1575-1555 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "Sin asignación específica",
                "rango": "1500-1465 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "Sin asignación específica",
                "rango": "1430-1410 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "δ(ring-H)",
                "rango": "1055-990 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "δ(ring)",
                "rango": "635-600 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Not with p-substitution"
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines",
                "asignacion": "ν(ring)",
                "rango": "1300-1270 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines - 2-substituted",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1150 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines - 2-substituted",
                "asignacion": "δ(ring-H)",
                "rango": "1055-1040 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Heterociclos",
                "grupo": "Pyridines - 2-substituted",
                "asignacion": "γ(ring-H)",
                "rango": "770-740 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Four adjacent H"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Nitriles alkyl- -CH₂-CN",
                "asignacion": "ν(CN)",
                "rango": "2260-2230 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Nitriles alkyl- -CH₂-CN",
                "asignacion": "δ(CH₂CN)",
                "rango": "580-555 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "CN trans to C"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Nitriles alkyl- -CH₂-CN",
                "asignacion": "Sin asignación específica",
                "rango": "560-525 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "CN trans to H"
        },
        {
                "familia": "Nitrilos",
                "grupo": ">CH-CN",
                "asignacion": "Sin asignación específica",
                "rango": "580-550 cm⁻¹",
                "intensidad": "var",
                "observacion": "Depends on conformation"
        },
        {
                "familia": "Nitrilos",
                "grupo": ">CH-CN",
                "asignacion": "Sin asignación específica",
                "rango": "545-530 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": ">CR-CN",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 595 cm⁻¹",
                "intensidad": "m",
                "observacion": "Depends on conformation"
        },
        {
                "familia": "Nitrilos",
                "grupo": ">CR-CN",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 575 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "conjugated with C=C aryl-",
                "asignacion": "ν(CN)",
                "rango": "2250-2200 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "conjugated with C=C aryl-",
                "asignacion": "ν(CN)",
                "rango": "2240-2220 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "conjugated with C=C aryl-",
                "asignacion": "δ(Ar-CN)γ(ring)",
                "rango": "580-540 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "conjugated with C=C aryl-",
                "asignacion": "δ(Ar-CN)",
                "rango": "430-380 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Imines",
                "asignacion": "ν(NH)free",
                "rango": "3400-3300 cm⁻¹",
                "intensidad": "var sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Imines",
                "asignacion": "ν(NH)ass",
                "rango": "3400-3100 cm⁻¹",
                "intensidad": "s br",
                "observacion": "Condensed state"
        },
        {
                "familia": "Nitrilos",
                "grupo": "R₂C=NH, ArCR=NH, R₂C=NR, ArCH=NAr",
                "asignacion": "ν(C=N)",
                "rango": "1650-1640 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "R₂C=NH, ArCR=NH, R₂C=NR, ArCH=NAr",
                "asignacion": "Sin asignación específica",
                "rango": "1635-1620 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "R₂C=NH, ArCR=NH, R₂C=NR, ArCH=NAr",
                "asignacion": "Sin asignación específica",
                "rango": "1665-1645 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "R₂C=NH, ArCR=NH, R₂C=NR, ArCH=NAr",
                "asignacion": "Sin asignación específica",
                "rango": "1645-1605 cm⁻¹",
                "intensidad": "var",
                "observacion": "Often 2 bands"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Oximes",
                "asignacion": "ν(OH)free",
                "rango": "3650-3500 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Oximes",
                "asignacion": "ν(OH)ass",
                "rango": "3450-3100 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Cond. state, several bands"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Oximes",
                "asignacion": "ν(C=N)",
                "rango": "1680-1660 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds conj.-olefin. and aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "1650-1620 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds conj.-olefin. and aromatic",
                "asignacion": "δ(OH)",
                "rango": "1500-1400 cm⁻¹",
                "intensidad": "m",
                "observacion": "br, 2 bands?"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds conj.-olefin. and aromatic",
                "asignacion": "ν(N-O)",
                "rango": "960-930 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds conj.-olefin. and aromatic",
                "asignacion": "ν(N=N)",
                "rango": "1575-1500 cm⁻¹",
                "intensidad": "var",
                "observacion": "Inactive or weak"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds alkyl, Z-aryl, E-aryl, Azoimidides,aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "1575-1555 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds alkyl, Z-aryl, E-aryl, Azoimidides,aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1510 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Azo compounds alkyl, Z-aryl, E-aryl, Azoimidides,aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "1440-1410 cm⁻¹",
                "intensidad": "w",
                "observacion": "Mixed vibration"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Isocyanates aliphatic, aromatic",
                "asignacion": "νas(N=C=N)",
                "rango": "ca. 2170 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Broader than ring vibrations"
        },
        {
                "familia": "Nitrilos",
                "grupo": "Isocyanates aliphatic, aromatic",
                "asignacion": "νas(N=C=O)",
                "rango": "ca. 2275 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Isocyanates aliphatic, aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 2265 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitrilos",
                "grupo": "Isocyanates aliphatic, aromatic",
                "asignacion": "νs(N=C=O)",
                "rango": "1460-1340 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "νas(NH₂)",
                "rango": "ca. 3330 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Crystalline"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 3250 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Noncryst. phase"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "νs(NH₂)",
                "rango": "ca. 3170 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Noncryst. phase"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "νas(NH₂)",
                "rango": "3370-3330 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Liquid"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "νs(NH₂)",
                "rango": "3290-3270 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "State"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "δ(NH₂)",
                "rango": "ca. 1600 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Condensed state"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "ν(C-N)",
                "rango": "1140-1080 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Depends on substitution"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "Sin asignación específica",
                "rango": "1090-1020 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "γ(NH₂)",
                "rango": "940-800 cm⁻¹",
                "intensidad": "m-s vbr",
                "observacion": "Max. ca. 850"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. primary",
                "asignacion": "Sin asignación específica",
                "rango": "950-870 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Cryst. phase, multiply split"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. secondary",
                "asignacion": "ν(NH)",
                "rango": "ca. 3300 cm⁻¹",
                "intensidad": "w br",
                "observacion": "Liquid"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. secondary",
                "asignacion": "δ(NH)",
                "rango": "ca. 1650 cm⁻¹",
                "intensidad": "vw",
                "observacion": "Liquid"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. secondary",
                "asignacion": "ν(C-N)",
                "rango": "1145-1130 cm⁻¹",
                "intensidad": "m",
                "observacion": "-CH₂-NH-CH₂-"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. secondary",
                "asignacion": "Sin asignación específica",
                "rango": "1190-1170 cm⁻¹",
                "intensidad": "m",
                "observacion": "-CH₂-NH-CH<"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. secondary",
                "asignacion": "γ(NH)",
                "rango": "750-710 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. tertiary",
                "asignacion": "ν(C-N)",
                "rango": "1210-1150 cm⁻¹",
                "intensidad": "m",
                "observacion": "N(-CH₂-)₃"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. tertiary",
                "asignacion": "Sin asignación específica",
                "rango": "1100-1030 cm⁻¹",
                "intensidad": "m",
                "observacion": "Same"
        },
        {
                "familia": "Aminas",
                "grupo": "Amines, aliph. tertiary",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1040 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "-CH₂-N(CH₃)₂"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "νas(NH₂)",
                "rango": "3470-3385 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Crystalline phase"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "νs(NH₂)",
                "rango": "3380-3325 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "νas(NH₂)",
                "rango": "3300-3280 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Non-crystalline phase"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "Sin asignación específica",
                "rango": "3210-3180 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "νas(NH₂)",
                "rango": "ca. 3430 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "νs(NH₂)",
                "rango": "ca. 3350 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 3200 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "δ(NH₂)",
                "rango": "ca. 1630 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "ν(Ar-N)?",
                "rango": "ca. 1280 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Possibly ω(NH₂)"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic primary",
                "asignacion": "γ(NH₂)",
                "rango": "800-600 cm⁻¹",
                "intensidad": "m, vvbr",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-R",
                "asignacion": "ν(NH)",
                "rango": "ca. 3400 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Liquid"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-R",
                "asignacion": "δ(NH)?",
                "rango": "1330-1320 cm⁻¹",
                "intensidad": "s",
                "observacion": "Liquid"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-R",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1260 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-Ar",
                "asignacion": "ν(NH)",
                "rango": "ca. 3400 (doublet) cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Solid, crystal splitting"
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-Ar",
                "asignacion": "δ(NH)?",
                "rango": "ca. 1310 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic secondary Ar-NH-Ar",
                "asignacion": "γ(NH)",
                "rango": "430-400 cm⁻¹",
                "intensidad": "vbr",
                "observacion": ""
        },
        {
                "familia": "Aminas",
                "grupo": "Aromatic tertiary Ar-NR₂",
                "asignacion": "ν(Ar-N)?",
                "rango": "ca. 1300 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols",
                "asignacion": "ν(OH)free",
                "rango": "3670-3580 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols",
                "asignacion": "ν(OH)ass.",
                "rango": "ca. 3300 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Solid state"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 3330 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Liquid"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols",
                "asignacion": "γ(OH)ass.",
                "rango": "ca. 650 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Liquid"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols primary",
                "asignacion": "ν(C-O)",
                "rango": "1080-1050 cm⁻¹",
                "intensidad": "s",
                "observacion": "Several bands, strongest 1070"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols secondary",
                "asignacion": "Sin asignación específica",
                "rango": "1160-1100 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Several bands"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Alcohols tertiary",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1200 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "ν(OH)free",
                "rango": "3620-3590 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 3650 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Sterically hindered"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "ν(OH)ass.",
                "rango": "3400-3300 cm⁻¹",
                "intensidad": "vbr",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "δ(OH)",
                "rango": "ca. 1350 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "ν(Ar-O)",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "s br",
                "observacion": "Assoc. OH"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Phenols",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1240 cm⁻¹",
                "intensidad": "s sh",
                "observacion": "Free OH"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Ethers, aliph. R-O-CH₃",
                "asignacion": "νas(CH₃)",
                "rango": "3000-2970 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Ethers, aliph. R-O-CH₃",
                "asignacion": "δs(CH₃)",
                "rango": "ca. 1450 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Together w. δ(CH₂)"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Ethers, aliph. R-O-CH₃",
                "asignacion": "ν(CH)",
                "rango": "ca. 2780 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "Ethers, aliph. R-O-CH₃",
                "asignacion": "νas(C-O-C)",
                "rango": "ca. 1110 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "Splits in cryst. ethers"
        },
        {
                "familia": "Alcoholes",
                "grupo": "Ethers -O-CH₂-O-, R-O-R",
                "asignacion": "Sin asignación específica",
                "rango": "1225-1200 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "vinyl ethers",
                "asignacion": "ν(ring)",
                "rango": "1260-1230 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "epoxides monosubst. trisubst.",
                "asignacion": "δ(ring)",
                "rango": "ca. 850 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "epoxides monosubst. trisubst.",
                "asignacion": "Sin asignación específica",
                "rango": "770-750 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "oxolane and oxane deriv.",
                "asignacion": "νas(ring)",
                "rango": "1090-1070 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Tetrahydrofurane, Tetrahydropyrane"
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides",
                "asignacion": "ν(C-O)",
                "rango": "1150-1030 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides",
                "asignacion": "ν(O-O)",
                "rango": "900-830 cm⁻¹",
                "intensidad": "vw",
                "observacion": "May be inactive"
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides aliphatic-aromatic",
                "asignacion": "νas(ring-O-C)",
                "rango": "1270-1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Donors shift red"
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides aliphatic-aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides aromatic",
                "asignacion": "νas(ring-O-ring)",
                "rango": "ca. 1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Alcoholes",
                "grupo": "peroxides aromatic",
                "asignacion": "ν(C-O)",
                "rango": "ca. 1000 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones, aliph. sat., open",
                "asignacion": "2x ν(C=O)",
                "rango": "ca. 3410 cm⁻¹",
                "intensidad": "vw",
                "observacion": "First overtone"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones, aliph. sat., open",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1715 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones, aliph. sat., open",
                "asignacion": "ν(CH₂CO)",
                "rango": "ca. 1415 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones, aliph. sat., open",
                "asignacion": "δs(CH₃CO)",
                "rango": "ca. 1360 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Acetyl band"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones, aliph. sat., open",
                "asignacion": "δ(C-CO)",
                "rango": "530-510 cm⁻¹",
                "intensidad": "w",
                "observacion": "Also with aldehydes"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones cyclic cyclobutanone, cyclopentanone, cyclohexanone, conj. unsatur.",
                "asignacion": "ν(C=O)",
                "rango": "1790-1765 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Derivatives"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones cyclic cyclobutanone, cyclopentanone, cyclohexanone, conj. unsatur.",
                "asignacion": "Sin asignación específica",
                "rango": "1750-1740 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Derivatives"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones cyclic cyclobutanone, cyclopentanone, cyclohexanone, conj. unsatur.",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1715 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Derivatives"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones cyclic cyclobutanone, cyclopentanone, cyclohexanone, conj. unsatur.",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1690 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones Z-config., E-config.",
                "asignacion": "ν(C=C)",
                "rango": "ca. 1620 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones Z-config., E-config.",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1675 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ketones Z-config., E-config.",
                "asignacion": "ν(C=C)",
                "rango": "ca. 1635 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Aliph.-aromatic Ar-CO-CH₃",
                "asignacion": "νas(CH₃)",
                "rango": "ca. 3000 cm⁻¹",
                "intensidad": "vw-w",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Aliph.-aromatic Ar-CO-CH₃",
                "asignacion": "ν(C=O)",
                "rango": "1700-1680 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Aliph.-aromatic Ar-CO-CH₃",
                "asignacion": "δs(CH₃)",
                "rango": "ca. 1360 cm⁻¹",
                "intensidad": "s",
                "observacion": "Acetyl band"
        },
        {
                "familia": "Cetonas",
                "grupo": "Aliph.-aromatic Ar-CO-CH₃",
                "asignacion": "δ(ring-CO-C)",
                "rango": "600-580 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Aliph.-aromatic Ar-CO-CH₃",
                "asignacion": "ν(ring-C)",
                "rango": "1275-1250 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ar-CO-CH₂-R",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1690 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ar-CO-Ar",
                "asignacion": "2x ν(C=O)",
                "rango": "ca. 3280 cm⁻¹",
                "intensidad": "vw",
                "observacion": "First overtone"
        },
        {
                "familia": "Cetonas",
                "grupo": "Ar-CO-Ar",
                "asignacion": "ν(C=O)",
                "rango": "1670-1650 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ar-CO-Ar",
                "asignacion": "ν(ring-C)",
                "rango": "ca. 1275 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "Ar-CO-Ar",
                "asignacion": "δ(C-CO-C)",
                "rango": "ca. 640 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "νas(C=O)",
                "rango": "1680-1655 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Sometimes split"
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "γ(CH)",
                "rango": "915-900 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "Sin asignación específica",
                "rango": "865-825 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "Sin asignación específica",
                "rango": "860-800 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "Sin asignación específica",
                "rango": "920-895 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "νas(C=O)",
                "rango": "1680-1650 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "νas(NH₂)",
                "rango": "ca. 3410 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "νs(NH₂)",
                "rango": "ca. 3300 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "p-Quinones (p-benzoquinones monosubst., 2,3-disubst., 2,5/2,6-disub., anthraquinones (no OH or NH), anthraquin.-NH₂)",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1600 cm⁻¹",
                "intensidad": "s",
                "observacion": "Multiply split"
        },
        {
                "familia": "Cetonas",
                "grupo": "anthraquin.-OH",
                "asignacion": "ν(OH)",
                "rango": "ca. 3450 cm⁻¹",
                "intensidad": "vw vbr",
                "observacion": ""
        },
        {
                "familia": "Cetonas",
                "grupo": "anthraquin.-OH",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1630 cm⁻¹",
                "intensidad": "s",
                "observacion": "Split"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO saturated",
                "asignacion": "2x ν(C=O)",
                "rango": "ca. 3430 cm⁻¹",
                "intensidad": "vw sh",
                "observacion": "First overtone"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO saturated",
                "asignacion": "ν(C-H)",
                "rango": "2845-2820 cm⁻¹",
                "intensidad": "m",
                "observacion": "Fermi resonance"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO saturated",
                "asignacion": "Sin asignación específica",
                "rango": "2735-2720 cm⁻¹",
                "intensidad": "m",
                "observacion": "Broader than ν(CH₂)"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO saturated",
                "asignacion": "ν(C=O)",
                "rango": "1730-1720 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO saturated",
                "asignacion": "δ(CH₂-CO)",
                "rango": "ca. 1410 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "2x ν(C=O)",
                "rango": "3370-3320 cm⁻¹",
                "intensidad": "vw sh",
                "observacion": "First overtone"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "ν(C-H)",
                "rango": "2845-2780 cm⁻¹",
                "intensidad": "w",
                "observacion": "Fermi resonance"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "Sin asignación específica",
                "rango": "2755-2700 cm⁻¹",
                "intensidad": "vw-w",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "ν(C=O)",
                "rango": "1695-1680 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "ν(C=C)",
                "rango": "1640-1615 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-CHO conjug.-unsat.",
                "asignacion": "ν(C-H)",
                "rango": "2865-2820 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-CHO",
                "asignacion": "ν(C=O)",
                "rango": "1705-1695 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Additl. weak bands in this range"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-CHO",
                "asignacion": "ν(ring-C)",
                "rango": "2760-2720 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-CHO",
                "asignacion": "ν(C-H)",
                "rango": "ca. 1200 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Not always present"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "Sin asignación específica",
                "rango": "All bands of the 8-memb. ring of dimers are broad",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "ν(OH)free",
                "rango": "3580-3500 cm⁻¹",
                "intensidad": "m",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "ν(OH)ass.",
                "rango": "3400-2500 cm⁻¹",
                "intensidad": "s vbr",
                "observacion": "Overlappg. of several H-bond species"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "Sin asignación específica",
                "rango": "2700-2500 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Two bds.of defin.associates"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1710 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Medium broad"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "ν(CO)δ(OH)",
                "rango": "ca. 1410 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Combination band"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH saturated",
                "asignacion": "γ(O-H...O)",
                "rango": "ca. 950 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH conj.unsatur.",
                "asignacion": "ν(C=O)",
                "rango": "1705-1690 cm⁻¹",
                "intensidad": "vs",
                "observacion": "E-configuration"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aliphatic-COOH conj.unsatur.",
                "asignacion": "ν(C=C)",
                "rango": "1650-1635 cm⁻¹",
                "intensidad": "s",
                "observacion": "Intensif. by conj."
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "ν(OH)ass.",
                "rango": "3150-2500 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Mult. overlapping bands"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 2650 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Defined"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "Sin asignación específica",
                "rango": "2550-2520 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Associates"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "ν(C=O)",
                "rango": "1690-1680 cm⁻¹",
                "intensidad": "vst",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "ν(CO)δ(OH)",
                "rango": "1420-1400 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Combination band"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Aromatic-COOH",
                "asignacion": "γ(O-H...O)",
                "rango": "940-905 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Carboxylates aliphatic -CO₂⁻",
                "asignacion": "νas(CO₂)",
                "rango": "1560-1520 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Sometimes split"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Carboxylates aliphatic -CO₂⁻",
                "asignacion": "νs(CO₂)",
                "rango": "ca. 1425 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Sometimes split"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Carboxylates aliphatic -CO₂⁻",
                "asignacion": "δ(CO₂)",
                "rango": "ca. 700 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Red flank of ρ(CH₂)n"
        },
        {
                "familia": "Aldehídos",
                "grupo": "Carboxylates aromatic -CO₂⁻",
                "asignacion": "νas(CO₂)",
                "rango": "1565-1530 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Aldehídos",
                "grupo": "Carboxylates aromatic -CO₂⁻",
                "asignacion": "νs(CO₂)",
                "rango": "1390-1360 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "ν(H-C=O)",
                "rango": "ca. 2880 cm⁻¹",
                "intensidad": "w",
                "observacion": "Formates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1740 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "δ(CH₂-C=O)",
                "rango": "ca. 1420 cm⁻¹",
                "intensidad": "vw-w",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "δs(CH₃-C=O)",
                "rango": "ca. 1375 cm⁻¹",
                "intensidad": "s",
                "observacion": "Acetyl band"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "νas(C-O-CO)",
                "rango": "ca. 1245 cm⁻¹",
                "intensidad": "s",
                "observacion": "Acetates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1200 cm⁻¹",
                "intensidad": "s",
                "observacion": "Butyrates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1190 cm⁻¹",
                "intensidad": "s",
                "observacion": "Formates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1190 cm⁻¹",
                "intensidad": "s",
                "observacion": "Propionates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1175 cm⁻¹",
                "intensidad": "s",
                "observacion": "Stearates, adipates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1170 cm⁻¹",
                "intensidad": "s",
                "observacion": "Sebacates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1165 cm⁻¹",
                "intensidad": "s",
                "observacion": "Fatty glycerates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "δ(C-O-CO)",
                "rango": "ca. 635 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Acetates"
        },
        {
                "familia": "Ésteres",
                "grupo": "Aliphatic esters saturated",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 605 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Acetates"
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates aliphatic",
                "asignacion": "ν(C=O)",
                "rango": "1755-1745 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates aliphatic",
                "asignacion": "νas(O-CO-O)",
                "rango": "1280-1260 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Higher carbonates: 1260"
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates aliphatic",
                "asignacion": "δ(O-CO-O)",
                "rango": "800-790 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates R-O-CO-O-Ar, Ar-O-CO-O-Ar",
                "asignacion": "ν(C=O)",
                "rango": "1790-1755 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates R-O-CO-O-Ar, Ar-O-CO-O-Ar",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1775 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates R-O-CO-O-Ar, Ar-O-CO-O-Ar",
                "asignacion": "νas(O-CO-O)",
                "rango": "ca. 1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Multiply split"
        },
        {
                "familia": "Ésteres",
                "grupo": "carbonates R-O-CO-O-Ar, Ar-O-CO-O-Ar",
                "asignacion": "Sin asignación específica",
                "rango": "1180-1160 cm⁻¹",
                "intensidad": "s",
                "observacion": "Split"
        },
        {
                "familia": "Ésteres",
                "grupo": "lactones, aliph.",
                "asignacion": "δ(O-CO-O)",
                "rango": "ca. 790 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "lactones, aliph.",
                "asignacion": "ν(C=O)",
                "rango": "1840-1815 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Four-membered ring"
        },
        {
                "familia": "Ésteres",
                "grupo": "lactones, aliph.",
                "asignacion": "Sin asignación específica",
                "rango": "1780-1765 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Five-membered ring"
        },
        {
                "familia": "Ésteres",
                "grupo": "lactones, aliph.",
                "asignacion": "νas(ring)",
                "rango": "1175-1170 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "lactones, aliph.",
                "asignacion": "Sin asignación específica",
                "rango": "1060-1020 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Unsaturated aliphatic esters conjug. to C=O",
                "asignacion": "ν(C=O)",
                "rango": "1730-1720 cm⁻¹",
                "intensidad": "vst",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Unsaturated aliphatic esters conjug. to C=O",
                "asignacion": "ν(C=C)",
                "rango": "1660-1630 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Intensif. by conjugation"
        },
        {
                "familia": "Ésteres",
                "grupo": "Z-vinylene fatty esters",
                "asignacion": "ν(=C-H)",
                "rango": "ca. 3010 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Isolated"
        },
        {
                "familia": "Ésteres",
                "grupo": "Z-vinylene fatty esters",
                "asignacion": "ν(C=C)",
                "rango": "ca. 1655 cm⁻¹",
                "intensidad": "w br",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Z-vinylene fatty esters",
                "asignacion": "γ(HC=CH)",
                "rango": "ca. 730 cm⁻¹",
                "intensidad": "m br",
                "observacion": "below ρ(CH₂) of long chains"
        },
        {
                "familia": "Ésteres",
                "grupo": "E-vinylene fatty esters",
                "asignacion": "ν(=C-H)",
                "rango": "ca. 3010 cm⁻¹",
                "intensidad": "w",
                "observacion": "Shoulder"
        },
        {
                "familia": "Ésteres",
                "grupo": "E-vinylene fatty esters",
                "asignacion": "ν(C=C)",
                "rango": "1660-1650 cm⁻¹",
                "intensidad": "vw",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "E-vinylene fatty esters",
                "asignacion": "γ(HC=CH)",
                "rango": "ca. 970 cm⁻¹",
                "intensidad": "m",
                "observacion": "Isolated"
        },
        {
                "familia": "Ésteres",
                "grupo": "E-vinylene fatty esters",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 985 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "-CH=CH-CH=CH-"
        },
        {
                "familia": "Ésteres",
                "grupo": "E-vinylene fatty esters",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 995 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Three conjugated -CH=CH-"
        },
        {
                "familia": "Ésteres",
                "grupo": "Esters of aromatic carboxylic acids with alcohols - benzoates",
                "asignacion": "ν(C=O)",
                "rango": "1720 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "Esters of aromatic carboxylic acids with alcohols - benzoates",
                "asignacion": "ν(ring)",
                "rango": "1600/1580 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Double band"
        },
        {
                "familia": "Ésteres",
                "grupo": "Esters of aromatic carboxylic acids with alcohols - benzoates",
                "asignacion": "νas(C-O-CO)",
                "rango": "1280-1260 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Broader than neighbour"
        },
        {
                "familia": "Ésteres",
                "grupo": "Esters of aromatic carboxylic acids with alcohols - benzoates",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1110 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "ring vibrations"
        },
        {
                "familia": "Ésteres",
                "grupo": "o-phthalates",
                "asignacion": "ν(C=O)",
                "rango": "1728 cm⁻¹",
                "intensidad": "vs",
                "observacion": "All bands are rather constant and"
        },
        {
                "familia": "Ésteres",
                "grupo": "o-phthalates",
                "asignacion": "ν(ring)",
                "rango": "1600/1580 cm⁻¹",
                "intensidad": "w",
                "observacion": "broader than neighb. ring vibr."
        },
        {
                "familia": "Ésteres",
                "grupo": "o-phthalates",
                "asignacion": "νas(C-O-CO)",
                "rango": "1287 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "o-phthalates",
                "asignacion": "Sin asignación específica",
                "rango": "1123 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "o-phthalates",
                "asignacion": "Sin asignación específica",
                "rango": "1074 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "isophthalates",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1733 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "isophthalates",
                "asignacion": "ν(ring)",
                "rango": "1610 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "isophthalates",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1300 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Fused with 1260"
        },
        {
                "familia": "Ésteres",
                "grupo": "isophthalates",
                "asignacion": "νas(C-O-CO)",
                "rango": "1235-1230 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "isophthalates",
                "asignacion": "Sin asignación específica",
                "rango": "1095-1075 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Frequently double band"
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "γ(ring-H)",
                "rango": "730 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "ν(C=O)",
                "rango": "1720 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "ν(ring)",
                "rango": "ca. 1575 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1410 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "νas(C-O-CO)",
                "rango": "1265/1245 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Fused double band"
        },
        {
                "familia": "Ésteres",
                "grupo": "terephthalates",
                "asignacion": "Sin asignación específica",
                "rango": "1120/1100 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Fused double band"
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "γ(ring-H)",
                "rango": "725 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "γ(ring)",
                "rango": "505 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "ν(C=O)",
                "rango": "1730 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "ν(ring)",
                "rango": "1600/1570 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Twin bands"
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "νas(C-O-CO)",
                "rango": "1280 cm⁻¹",
                "intensidad": "s",
                "observacion": "Fused with 1240"
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "Sin asignación específica",
                "rango": "1240 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ésteres",
                "grupo": "trimellitates",
                "asignacion": "Sin asignación específica",
                "rango": "1115 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "νas(NH₂)free",
                "rango": "3540-3480 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "νs(NH₂)free",
                "rango": "3420-3380 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "νas(NH₂)ass.",
                "rango": "3370-3330 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Solid state"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "νs(NH₂)ass.",
                "rango": "3210-3180 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Amide band I"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "ν(C=O)ass.",
                "rango": "1680-1660 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Amide band I"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "Sin asignación específica",
                "rango": "1650-1620 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Fused with ν(CO)"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "ν(C-N)",
                "rango": "1420-1400 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Amide band III"
        },
        {
                "familia": "Amidas",
                "grupo": "Aliphatic amides R-CO-NX-R primary -CO-NH₂",
                "asignacion": "γ(NH₂)ass.",
                "rango": "700-600 cm⁻¹",
                "intensidad": "m vbr",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "ν(NH)free",
                "rango": "3460-3420 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Dilute solution"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "ν(NH)ass.",
                "rango": "3350-3290 cm⁻¹",
                "intensidad": "m",
                "observacion": "trans conformation"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "Sin asignación específica",
                "rango": "3100-3070 cm⁻¹",
                "intensidad": "w",
                "observacion": "2×amide II"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "ν(C=O)ass.",
                "rango": "1670-1640 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Amide band I"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "δ(NH)ν(CO)",
                "rango": "1570-1540 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Combin., amide II"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "ν(C-N)",
                "rango": "1300-1240 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "trans, amide III"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "Sin asignación específica",
                "rango": "1350-1310 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "cis, amide III"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "δ(NH...OC)",
                "rango": "750-660 cm⁻¹",
                "intensidad": "m vbr",
                "observacion": "Amide V"
        },
        {
                "familia": "Amidas",
                "grupo": "secondary -CO-NH-",
                "asignacion": "Sin asignación específica",
                "rango": "630-600 cm⁻¹",
                "intensidad": "w",
                "observacion": "Amide IV"
        },
        {
                "familia": "Amidas",
                "grupo": "tertiary -CO-N<",
                "asignacion": "ν(C=O)",
                "rango": "1660-1630 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Amide I"
        },
        {
                "familia": "Amidas",
                "grupo": "tertiary -CO-N<",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1675 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Dialkylformamides"
        },
        {
                "familia": "Amidas",
                "grupo": "tertiary -CO-N<",
                "asignacion": "Sin asignación específica",
                "rango": "1650-1640 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Dialkylamides"
        },
        {
                "familia": "Amidas",
                "grupo": "tertiary -CO-N<",
                "asignacion": "δs(CH₃-CO)",
                "rango": "1355-1350 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Acetyl band"
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 3-propane-",
                "asignacion": "ν(NH)ass.",
                "rango": "ca. 3260 cm⁻¹",
                "intensidad": "m",
                "observacion": "cis conformation"
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 3-propane-",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1750 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 4-butane-",
                "asignacion": "ν(NH)ass.",
                "rango": "ca. 3250 cm⁻¹",
                "intensidad": "m br",
                "observacion": "cis conformation"
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 4-butane-",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1690 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 4-butane-",
                "asignacion": "ν(C-N)",
                "rango": "1300-1285 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 4-butane-",
                "asignacion": "δ(ring)",
                "rango": "ca. 1000 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 4-butane-",
                "asignacion": "δ(NH...OC)",
                "rango": "850-600 cm⁻¹",
                "intensidad": "m vbr",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "ν(NH)ass.",
                "rango": "3225 cm⁻¹",
                "intensidad": "m br",
                "observacion": "cis conformation"
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "ν(C=O)",
                "rango": "1670 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "ν(C-N)",
                "rango": "ca. 1310 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "Sin asignación específica",
                "rango": "1120 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "δ(ring)",
                "rango": "990 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "lactams 5-pentane-",
                "asignacion": "δ(NH...OC)",
                "rango": "900-700 cm⁻¹",
                "intensidad": "m vbr",
                "observacion": ""
        },
        {
                "familia": "Amidas",
                "grupo": "ε-capro-",
                "asignacion": "ν(NH)ass.",
                "rango": "3215 cm⁻¹",
                "intensidad": "m br",
                "observacion": "cis conformation"
        },
        {
                "familia": "Amidas",
                "grupo": "ε-capro-",
                "asignacion": "ν(CO)+δ(NH)",
                "rango": "3090 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Combination vibration"
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "νas(NH₂)ass.",
                "rango": "3435 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "νs(NH₂)ass.",
                "rango": "3330 cm⁻¹",
                "intensidad": "s-vs br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "ν(C=O)",
                "rango": "1673 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "Sin asignación específica",
                "rango": "1630-1590 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Merged doublet"
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "δ(NH₂)ν(C-N)",
                "rango": "1458 cm⁻¹",
                "intensidad": "s",
                "observacion": "Coupled vibration"
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "ν(C-N)",
                "rango": "1147 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "Urea and defined urea derivatives - urea",
                "asignacion": "δ(NH...OC)",
                "rango": "700-300 cm⁻¹",
                "intensidad": "m-s vbr",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "νas(NH₂)ass.",
                "rango": "3425 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "νs(NH₂)ass.",
                "rango": "3355 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "ν(NH)ass.",
                "rango": "3215 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "ν(C=O)",
                "rango": "1661 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Amide I"
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "Sin asignación específica",
                "rango": "1598 cm⁻¹",
                "intensidad": "vs sh",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "δ(NH)ν(C-N)",
                "rango": "1565 cm⁻¹",
                "intensidad": "s br",
                "observacion": "Amide II"
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "ν(C-N)",
                "rango": "1160 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "ethyl-",
                "asignacion": "δ(NH...OC)",
                "rango": "605 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "ν(NH)ass.",
                "rango": "3345 cm⁻¹",
                "intensidad": "s-vs br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "ν(CO)+δ(NH)",
                "rango": "3175 cm⁻¹",
                "intensidad": "m",
                "observacion": "Combination vibration"
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "ν(C=O)",
                "rango": "1630 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "δ(NH)ν(C-N)",
                "rango": "1585 cm⁻¹",
                "intensidad": "s",
                "observacion": "Amide II, merged w. amide I"
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "ν(C-N)",
                "rango": "1270 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "Sin asignación específica",
                "rango": "1175 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-dimethyl-",
                "asignacion": "δ(NH...OC)",
                "rango": "675 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "ν(NH)ass.",
                "rango": "3340 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "ν(CO)+δ(NH)",
                "rango": "3140 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": "Combination vibration"
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "ν(C=O)",
                "rango": "1627 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Amide I"
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "δ(NH)ν(C-N)",
                "rango": "1585 cm⁻¹",
                "intensidad": "s",
                "observacion": "Amide II, merged w. amide I"
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "ν(C-N)",
                "rango": "1260 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "Sin asignación específica",
                "rango": "1158 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diethyl-",
                "asignacion": "δ(NH...OC)",
                "rango": "660 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Ureas",
                "grupo": "1,3-diaryl-",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1640 cm⁻¹",
                "intensidad": "s",
                "observacion": "Amide I"
        },
        {
                "familia": "Isocianatos",
                "grupo": "-N=C=O aliphatic",
                "asignacion": "Sin asignación específica",
                "rango": "3680-3630 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Combination vibration"
        },
        {
                "familia": "Isocianatos",
                "grupo": "-N=C=O aliphatic",
                "asignacion": "νas(NCO)",
                "rango": "2270-2240 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "-N=C=O aliphatic",
                "asignacion": "νs(NCO)",
                "rango": "1375-1350 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "-N=C=O aliphatic",
                "asignacion": "δ(NCO)",
                "rango": "ca. 585 (peak) cm⁻¹",
                "intensidad": "m-s br",
                "observacion": "Fused band on the violet side"
        },
        {
                "familia": "Isocianatos",
                "grupo": "aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "3690 cm⁻¹",
                "intensidad": "w",
                "observacion": "Combination vibration"
        },
        {
                "familia": "Isocianatos",
                "grupo": "aromatic",
                "asignacion": "νas(NCO)",
                "rango": "ca. 2270 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "aromatic",
                "asignacion": "ν(ring)",
                "rango": "ca. 1525 cm⁻¹",
                "intensidad": "s",
                "observacion": "Intensified by coupling with NCO"
        },
        {
                "familia": "Isocianatos",
                "grupo": "aromatic",
                "asignacion": "δ(NCO)",
                "rango": "570-560 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Neighbouring ring vibrations"
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "ν(CO)δ(NH₂)",
                "rango": "1630-1620 cm⁻¹",
                "intensidad": "vs",
                "observacion": "\"Amide\" I"
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "ν(NH)",
                "rango": "ca. 3310 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1690 cm⁻¹",
                "intensidad": "vs",
                "observacion": "\"Amide\" I"
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "ν(C-N)δ(NH)",
                "rango": "ca. 1535 cm⁻¹",
                "intensidad": "s",
                "observacion": "\"Amide\" II"
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "νas(C-O-CO)",
                "rango": "ca. 1260 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "H₂N-CO-O- -NH-CO-O- aliphatic",
                "asignacion": "δ(NH...OC)",
                "rango": "ca. 655 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Ar-NH-CO-O-R",
                "asignacion": "ν(NH)",
                "rango": "ca. 3300 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "Broad shoulder on the violet side"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Ar-NH-CO-O-R",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1695 cm⁻¹",
                "intensidad": "vs",
                "observacion": "\"Amide\" I"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Ar-NH-CO-O-R",
                "asignacion": "ν(C-N)δ(NH)",
                "rango": "ca. 1540 cm⁻¹",
                "intensidad": "s",
                "observacion": "\"Amide\" II"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Ar-NH-CO-O-R",
                "asignacion": "νas(C-O-CO)",
                "rango": "ca. 1240 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Ar-NH-CO-O-R",
                "asignacion": "νs(C-O-CO)",
                "rango": "ca. 1070 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "ν(C=O)",
                "rango": "1690-1680 cm⁻¹",
                "intensidad": "vs",
                "observacion": "\"Amide\" I"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "ν(NH)",
                "rango": "3280-3200 cm⁻¹",
                "intensidad": "m",
                "observacion": "trans-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Sin asignación específica",
                "rango": "3245-3190 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "cis-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1735 cm⁻¹",
                "intensidad": "vs",
                "observacion": "trans-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1700 cm⁻¹",
                "intensidad": "vs",
                "observacion": "cis-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Unknown",
                "rango": "ca. 1650 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1630 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Sin asignación específica",
                "rango": "1510-1500 cm⁻¹",
                "intensidad": "s",
                "observacion": "trans-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": ">N-CO-O- R-CO-NH-CO-R",
                "asignacion": "Sin asignación específica",
                "rango": "1235-1165 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "δ(NH...OC)",
                "rango": "835-815 cm⁻¹",
                "intensidad": "m",
                "observacion": "cis-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "δ(NH...OC)",
                "rango": "740-730 cm⁻¹",
                "intensidad": "m br",
                "observacion": "trans-trans"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "ν(NH)",
                "rango": "ca. 3150 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "νs(C=O)",
                "rango": "ca. 1775 cm⁻¹",
                "intensidad": "m",
                "observacion": "s and as relate to"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1700 cm⁻¹",
                "intensidad": "vs",
                "observacion": "coupled C=O vibration"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Succinimides",
                "asignacion": "ν(ring)",
                "rango": "ca. 1190 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Aspartimides",
                "asignacion": "νs(C=O)",
                "rango": "ca. 1780 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Aspartimides",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1705 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "ν(NH)",
                "rango": "ca. 3200 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "νs(C=O)",
                "rango": "ca. 1775 cm⁻¹",
                "intensidad": "m",
                "observacion": "Weak in maleimide"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1700 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "ν(C=C)",
                "rango": "1650-1630 cm⁻¹",
                "intensidad": "m",
                "observacion": "Not in maleimide"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "ν(ring)",
                "rango": "1365-1340 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "δ(ring-H)",
                "rango": "1080-1040 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Maleimides",
                "asignacion": "δ(NH...OC)",
                "rango": "850 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Maleimide"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Phthalimides",
                "asignacion": "ν(NH)",
                "rango": "ca. 3200 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Phthalimides",
                "asignacion": "νs(C=O)",
                "rango": "1790-1735 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "ca. 1770"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Phthalimides",
                "asignacion": "νas(C=O)",
                "rango": "1745-1670 cm⁻¹",
                "intensidad": "vs",
                "observacion": "ca. 1750, several merged bands"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "2 x ν(C=O)",
                "rango": "3480 cm⁻¹",
                "intensidad": "w sh",
                "observacion": "Overtone"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "ν(NH)",
                "rango": "ca. 3360 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Asymmetric"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "νs(C=O)",
                "rango": "ca. 1780 cm⁻¹",
                "intensidad": "m sh",
                "observacion": "Imide ring"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1720 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Imide ring"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1665 cm⁻¹",
                "intensidad": "s",
                "observacion": "Aromatic amide I"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "δ(NH)ν(C-N)",
                "rango": "ca. 1530 cm⁻¹",
                "intensidad": "m",
                "observacion": "Aromatic amide II merged w."
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "Sin asignación específica",
                "rango": "",
                "intensidad": "",
                "observacion": "ν(ring)"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Trimellitic amide-imides, aromatic, N,N'-substituted",
                "asignacion": "ν(C-N)",
                "rango": "ca. 1225 cm⁻¹",
                "intensidad": "s",
                "observacion": "Aromatic amide III"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Pyromellitic imides, aromatic, N,N'-substituted",
                "asignacion": "2×ν(C=O)",
                "rango": "ca. 3480 cm⁻¹",
                "intensidad": "w sh",
                "observacion": "Overtone"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Pyromellitic imides, aromatic, N,N'-substituted",
                "asignacion": "νs(C=O)",
                "rango": "ca. 1775 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Pyromellitic imides, aromatic, N,N'-substituted",
                "asignacion": "νas(C=O)",
                "rango": "ca. 1720 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Isocianatos",
                "grupo": "Pyromellitic imides, aromatic, N,N'-substituted",
                "asignacion": "ν(ring)",
                "rango": "ca. 1570 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Imide ring"
        },
        {
                "familia": "Isocianatos",
                "grupo": "Pyromellitic imides, aromatic, N,N'-substituted",
                "asignacion": "ν(C-N)",
                "rango": "ca. 1240 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "Amine oxides aliphatic",
                "asignacion": "ν(N→O)",
                "rango": "970-950 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "Amine oxides aliphatic",
                "asignacion": "δ(N→O)",
                "rango": "ca. 775 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "pyridine→O",
                "asignacion": "Sin asignación específica",
                "rango": "1320-1230 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Depends on ring substitution;"
        },
        {
                "familia": "Nitro",
                "grupo": "pyridine→O",
                "asignacion": "",
                "rango": "",
                "intensidad": "",
                "observacion": "pyridine→O: 1250 s"
        },
        {
                "familia": "Nitro",
                "grupo": "pyridine→O",
                "asignacion": "",
                "rango": "",
                "intensidad": "",
                "observacion": "Pyridine→O: 1172"
        },
        {
                "familia": "Nitro",
                "grupo": "pyridine→O",
                "asignacion": "δ(N→O)",
                "rango": "1190-1150 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "pyridine→O",
                "asignacion": "Sin asignación específica",
                "rango": "895-840 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "Monomer -N=O aliphatic",
                "asignacion": "ν(N=O)",
                "rango": "1590-1540 cm⁻¹",
                "intensidad": "s",
                "observacion": "Usually at 1550"
        },
        {
                "familia": "Nitro",
                "grupo": "aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "1515-1480 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "Dimer (-N=O)₂ aliphatic",
                "asignacion": "ν(N-O)",
                "rango": "1425-1330 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Z configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "Dimer (-N=O)₂ aliphatic",
                "asignacion": "Sin asignación específica",
                "rango": "1290-1175 cm⁻¹",
                "intensidad": "s",
                "observacion": "E configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1390 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Z configuration, three fused bands"
        },
        {
                "familia": "Nitro",
                "grupo": "aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "1300-1250 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "E configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-NO₂ aliphatic tertiary",
                "asignacion": "νas(O=N=O)",
                "rango": "1555-1545 cm⁻¹",
                "intensidad": "vs",
                "observacion": "CH₃NO₂: 1563"
        },
        {
                "familia": "Nitro",
                "grupo": "-NO₂ aliphatic tertiary",
                "asignacion": "Sin asignación específica",
                "rango": "1550-1530 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "CH₃-NO₂",
                "asignacion": "νs(O=N=O)",
                "rango": "1395-1360ª cm⁻¹",
                "intensidad": "m",
                "observacion": "CH₃NO₂: 1404"
        },
        {
                "familia": "Nitro",
                "grupo": "CH₃-NO₂",
                "asignacion": "δ(O=N=O)",
                "rango": "620-600 cm⁻¹",
                "intensidad": "m br",
                "observacion": "CH₃NO₂: 657"
        },
        {
                "familia": "Nitro",
                "grupo": ">CH-NO₂ aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "630-610 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": ">CH-NO₂ aromatic",
                "asignacion": "νas(O=N=O)",
                "rango": "1535-1510 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": ">CH-NO₂ aromatic",
                "asignacion": "νs(O=N=O)",
                "rango": "1350-1335 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": ">CH-NO₂ aromatic",
                "asignacion": "δ(O=N=O)",
                "rango": "680-655 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "-O-N=O",
                "asignacion": "ν(N=O)",
                "rango": "1680-1650 cm⁻¹",
                "intensidad": "vs",
                "observacion": "E configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-N=O",
                "asignacion": "Sin asignación específica",
                "rango": "1625-1610 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Z configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-N=O",
                "asignacion": "ν(N-O)",
                "rango": "850-810 cm⁻¹",
                "intensidad": "s",
                "observacion": "Z configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-N=O",
                "asignacion": "Sin asignación específica",
                "rango": "815-750 cm⁻¹",
                "intensidad": "vs",
                "observacion": "E configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "δ(O-N=O)",
                "rango": "690-615 cm⁻¹",
                "intensidad": "s",
                "observacion": "Z configuration, C₂H₅NO₂: 690"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "Sin asignación específica",
                "rango": "625-565 cm⁻¹",
                "intensidad": "s",
                "observacion": "E configuration"
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "νas(NO₂)",
                "rango": "1660-1625 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "νs(NO₂)",
                "rango": "1285-1270 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "ν(N-O)",
                "rango": "870-855 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "δ(NO₂)",
                "rango": "760-755 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Nitro",
                "grupo": "-O-NO₂ aliphatic",
                "asignacion": "γ(NO₂)",
                "rango": "710-695 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SH thiols aliphatic",
                "asignacion": "ν(S-H)",
                "rango": "2560-2554 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SH thiols aliphatic",
                "asignacion": "δ(CH₂-S)",
                "rango": "ca. 1430 cm⁻¹",
                "intensidad": "w",
                "observacion": "Merges with δ(CH₂-C)"
        },
        {
                "familia": "Azufre",
                "grupo": "-SH thiols aliphatic",
                "asignacion": "ω(CH₂-S)",
                "rango": "1278-1247 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SH thiols aliphatic",
                "asignacion": "ν(CH₂-S)",
                "rango": "655-650 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SH thiols aliphatic",
                "asignacion": "ν(>CH-S)",
                "rango": "620-610 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "ν(S-H)",
                "rango": "2560 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "δ(SH)",
                "rango": "1099-1082 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "ν(ring-S)",
                "rango": "630-620 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "ν(SH)",
                "rango": "482-477 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-S-R",
                "asignacion": "δas(CH₂-S)",
                "rango": "1435-1430 cm⁻¹",
                "intensidad": "m",
                "observacion": "H₂C-S-CH₂: 1433s"
        },
        {
                "familia": "Azufre",
                "grupo": "R-S-R",
                "asignacion": "δ(CH₂-S)",
                "rango": "1425-1420 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Merges with δ(CH₂-C)"
        },
        {
                "familia": "Azufre",
                "grupo": "R-S-R",
                "asignacion": "δs(CH₃-S)",
                "rango": "ca. 1310 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-S-R",
                "asignacion": "ω(CH₃-S)",
                "rango": "1270-1255 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-S-R",
                "asignacion": "νas(C-S-C)",
                "rango": "ca. 690 cm⁻¹",
                "intensidad": "w-m",
                "observacion": "Not in S(CH₂)₂"
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-CH₃",
                "asignacion": "δas(CH₃-S)",
                "rango": "ca. 1440 cm⁻¹",
                "intensidad": "m",
                "observacion": "Merged with ν(ring)?"
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-CH₃",
                "asignacion": "δs(CH₃-S)",
                "rango": "ca. 1315 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-CH₃",
                "asignacion": "νas(C-S-C)",
                "rango": "615 cm⁻¹",
                "intensidad": "vw",
                "observacion": "δ(ring) ?"
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-Ar",
                "asignacion": "νas(C-S-C)",
                "rango": "475 cm⁻¹",
                "intensidad": "m",
                "observacion": "γ(ring) ?"
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-Ar",
                "asignacion": "νas(C-S-C)",
                "rango": "617 cm⁻¹",
                "intensidad": "vw",
                "observacion": "Diphenylsulfide"
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-S-Ar",
                "asignacion": "νs(C-S-C)",
                "rango": "463 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "νas(CH₂-S=O)",
                "rango": "2995 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "δs(CH₂-S=O)",
                "rango": "ca. 1310 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "ν(S=O)",
                "rango": "1070-1040 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "Sin asignación específica",
                "rango": "1055-1010 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Hydrogen-bonded"
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "ν(C-S)",
                "rango": "ca. 700 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": ">S=O sulfoxides aliphatic",
                "asignacion": "δ(C-S=O)",
                "rango": "395-360 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic >SO₂ sulfones aliphatic",
                "asignacion": "ν(S=O)",
                "rango": "1040-1020 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Split"
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic >SO₂ sulfones aliphatic",
                "asignacion": "νas(CH₂-SO₂)",
                "rango": "ca. 3025 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic >SO₂ sulfones aliphatic",
                "asignacion": "νas(SO₂)",
                "rango": "ca. 1315 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Split"
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic >SO₂ sulfones aliphatic",
                "asignacion": "νs(SO₂)",
                "rango": "1150-1135 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "alkylaryl-",
                "asignacion": "νas(SO₂)",
                "rango": "1335-1325 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "alkylaryl-",
                "asignacion": "νs(SO₂)",
                "rango": "1160-1150 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "diaryl-",
                "asignacion": "νas(SO₂)",
                "rango": "ca. 1310 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Split"
        },
        {
                "familia": "Azufre",
                "grupo": "diaryl-",
                "asignacion": "νs(SO₂)",
                "rango": "ca. 1160 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "ν(OH)",
                "rango": "ca. 2900 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 2400 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "νas(SO₂)",
                "rango": "1350-1340 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "νs(SO₂)",
                "rango": "1200-1100 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "ν(S-O)",
                "rango": "1165-1150 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₂-OH sulfonic acids aliphatic anhydrous",
                "asignacion": "δ(OH...OS)",
                "rango": "910-890 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "hydrated",
                "asignacion": "ν(OH)",
                "rango": "3500-2600 cm⁻¹",
                "intensidad": "s vbr",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "hydrated",
                "asignacion": "Sin asignación específica",
                "rango": "2440-2400 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "hydrated",
                "asignacion": "νas(SO₂)",
                "rango": "1350-1340 cm⁻¹",
                "intensidad": "s-vs br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "hydrated",
                "asignacion": "νs(SO₂)",
                "rango": "1165-1155 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "hydrated",
                "asignacion": "Sin asignación específica",
                "rango": "910-900 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "ν(OH)",
                "rango": "3300-2600 cm⁻¹",
                "intensidad": "m-s vbr",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "Sin asignación específica",
                "rango": "2460-2400 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "νas(SO₂)",
                "rango": "ca. 1350 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "νs(SO₂)",
                "rango": "ca. 1175 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Complex of usually three bands"
        },
        {
                "familia": "Azufre",
                "grupo": "aromatic",
                "asignacion": "δ(OH...OS)",
                "rango": "ca. 910 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₃⁻ aliphatic",
                "asignacion": "νas(-SO₃⁻)",
                "rango": "1200-1170 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₃⁻ aliphatic",
                "asignacion": "νs(-SO₃⁻)",
                "rango": "ca. 1050 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₃⁻ aliphatic",
                "asignacion": "δ(-SO₃⁻)",
                "rango": "ca. 620 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "-SO₃⁻ aliphatic",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 550 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "νas(CH₂-SO₂)",
                "rango": "3025 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "νas(SO₂)",
                "rango": "ca. 1350 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "νs(SO₂)",
                "rango": "ca. 1175 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "νas(C-O-S)",
                "rango": "1010-1000 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "νs(C-O-S)",
                "rango": "ca. 815 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-R",
                "asignacion": "δ(O=S=O)",
                "rango": "ca. 530 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-Ar",
                "asignacion": "νas(SO₂)",
                "rango": "ca. 1360 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-Ar",
                "asignacion": "ν(Ar-O)",
                "rango": "ca. 1200 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-Ar",
                "asignacion": "νs(SO₂)",
                "rango": "ca. 1150 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-SO₂-O-Ar",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 870 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-OR",
                "asignacion": "νas(O=S=O)",
                "rango": "1365-1335 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-OR",
                "asignacion": "νs(O=S=O)",
                "rango": "1200-1185 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "ν(OSO₂O)",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "s",
                "observacion": "Linear alkyl"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1220 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Linear alkyl"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Merged double band"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "Sin asignación específica",
                "rango": "1085-1080 cm⁻¹",
                "intensidad": "s sh",
                "observacion": "Linear alkyl"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "Sin asignación específica",
                "rango": "1070 cm⁻¹",
                "intensidad": "s sh",
                "observacion": "Branched alkyl"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "ν(C-O-S)",
                "rango": "ca. 835 cm⁻¹",
                "intensidad": "m",
                "observacion": "Fused band on red side"
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-Na⁺",
                "asignacion": "δ(OSO₂O)",
                "rango": "ca. 690 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-R",
                "asignacion": "νas(O=S=O)",
                "rango": "ca. 1390 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "R-O-SO₂-O-R",
                "asignacion": "νs(O=S=O)",
                "rango": "1200-1190 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "νas(NH₂)",
                "rango": "3350-3325 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "νs(NH₂)",
                "rango": "3270-3240 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "δ(NH₂)",
                "rango": "1570-1550 cm⁻¹",
                "intensidad": "w-m br",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "νas(O=S=O)",
                "rango": "1335-1325 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "νs(O=S=O)",
                "rango": "1160-1150 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH₂",
                "asignacion": "δ(O=S=O)",
                "rango": "540-530 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH-R",
                "asignacion": "ν(NH)",
                "rango": "ca. 3290 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "Ar-SO₂-NH-R",
                "asignacion": "νas(O=S=O)",
                "rango": "ca. 1325 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "νs(O=S=O)",
                "rango": "ca. 1160 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "δ(O=S=O)",
                "rango": "590-570 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "Fused with δ (ring)?"
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "ν(CN)",
                "rango": "2155 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "ν(S-C)",
                "rango": "ca. 685 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "ν(Cₙ-S)",
                "rango": "680-580 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "same",
                "rango": "625-590 cm⁻¹",
                "intensidad": "m",
                "observacion": "Aliphatic substituent"
        },
        {
                "familia": "Azufre",
                "grupo": "(R,Ar)-SCN",
                "asignacion": "δ(SCN)",
                "rango": "ca. 410 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₃P=O",
                "asignacion": "ν(P=O)",
                "rango": "ca. 1275 cm⁻¹",
                "intensidad": "s",
                "observacion": "Two components"
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₃P=O",
                "asignacion": "νas(P-O-C)",
                "rango": "1050-1000 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Max. 1050, 3 components"
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₃P=O",
                "asignacion": "ν(P=O)",
                "rango": "ca. 1300 cm⁻¹",
                "intensidad": "s",
                "observacion": "Two components"
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₃P=O",
                "asignacion": "ν(Ar-O)",
                "rango": "1170-1150 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₃P=O",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 970 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Broader than ring vibrations"
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "δ(PO₃)",
                "rango": "530-510 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "ν(P=O)",
                "rango": "1295 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "ν(Ar-O)",
                "rango": "1200 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "νas(P-O-C)",
                "rango": "ca. 1025 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Two components"
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "ν(O-P-O)",
                "rango": "950 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ΦO)₂ROP=O",
                "asignacion": "δ(PO₃)",
                "rango": "530-510 cm⁻¹",
                "intensidad": "m",
                "observacion": "Two components"
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂(HO)P=O",
                "asignacion": "ν(P=O)",
                "rango": "1250-1210 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂(HO)P=O",
                "asignacion": "γ(OH...O=P)",
                "rango": "590-460 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂(HO)P=O",
                "asignacion": "Sin asignación específica",
                "rango": "400-380 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "ν(P=O)",
                "rango": "ca. 1275 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "δ(PO₃)",
                "rango": "600-580 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "Sin asignación específica",
                "rango": "565-535 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "Sin asignación específica",
                "rango": "515-500 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "Sin asignación específica",
                "rango": "490-470 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂(HO)P=O",
                "asignacion": "Sin asignación específica",
                "rango": "400-380 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "ν(OH)",
                "rango": "ca. 3220 cm⁻¹",
                "intensidad": "s vr",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 2400 cm⁻¹",
                "intensidad": "m vbr",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "δ(OH)",
                "rango": "1670 cm⁻¹",
                "intensidad": "w-m vbr",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "ν(P=O)",
                "rango": "1233 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "Sin asignación específica",
                "rango": "1192 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "ν(P-O-C)",
                "rango": "1115+1090 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Merged"
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "Sin asignación específica",
                "rango": "980 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "Sin asignación específica",
                "rango": "900 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)(HO)P(O)O⁻ surfactant",
                "asignacion": "Sin asignación específica",
                "rango": "533 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂RP=O",
                "asignacion": "ν(P=O)",
                "rango": "1265-1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂RP=O",
                "asignacion": "Sin asignación específica",
                "rango": "800-750 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂RP=O",
                "asignacion": "Sin asignación específica",
                "rango": "570-500 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂RP=O",
                "asignacion": "Sin asignación específica",
                "rango": "490-410 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂RP=O",
                "asignacion": "Sin asignación específica",
                "rango": "440-400 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂ArP=O",
                "asignacion": "ν(P=O)",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1050 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂ArP=O",
                "asignacion": "ν(P-O-C)",
                "rango": "970 cm⁻¹",
                "intensidad": "s br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(RO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "920 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OR)₃",
                "asignacion": "νas(PO₃)",
                "rango": "ca. 1000 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "Several components"
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OR)₃",
                "asignacion": "δ(PO₃)",
                "rango": "ca. 750 cm⁻¹",
                "intensidad": "s br",
                "observacion": "Three components"
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OAr)₃",
                "asignacion": "νas(P-O-Ar)",
                "rango": "1220-1210 cm⁻¹",
                "intensidad": "vs",
                "observacion": "Double band"
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OAr)₃",
                "asignacion": "Sin asignación específica",
                "rango": "1200-1175 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OAr)₃",
                "asignacion": "Sin asignación específica",
                "rango": "875-850 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OΦ)₃",
                "asignacion": "νas(P-O-Φ)",
                "rango": "1200 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OΦ)₃",
                "asignacion": "Sin asignación específica",
                "rango": "1165 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OΦ)₃",
                "asignacion": "δ(P-O-Φ)",
                "rango": "875 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OΦ)₃",
                "asignacion": "Sin asignación específica",
                "rango": "765 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "P(OΦ)₃",
                "asignacion": "Sin asignación específica",
                "rango": "725 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "R-P-H",
                "asignacion": "ν(P-H)",
                "rango": "2285-2265 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "R-P-H",
                "asignacion": "δ(H-P-H)",
                "rango": "1100-1085 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "R-P-H",
                "asignacion": "δ(P-H)",
                "rango": "1065-1040 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "R-P-H",
                "asignacion": "ω(H-P-H)",
                "rango": "940-910 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "Ar-P-H",
                "asignacion": "ν(P-H)",
                "rango": "2285-2270 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "Ar-P-H",
                "asignacion": "δ(P-H)",
                "rango": "1100-1085 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "ν(P-C)",
                "rango": "830+800 cm⁻¹",
                "intensidad": "s+m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "585-565 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "530-520 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "ν(P=O)",
                "rango": "1265-1230 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "620-600 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Fósforo",
                "grupo": "(ArO)₂ArP=O",
                "asignacion": "Sin asignación específica",
                "rango": "535-515 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "SiH derivatives RSiH₃",
                "asignacion": "ν(SiH)",
                "rango": "2155-2140 cm⁻¹",
                "intensidad": "s",
                "observacion": "Reduced coupling"
        },
        {
                "familia": "Silicio",
                "grupo": "SiH derivatives RSiH₃",
                "asignacion": "δas(SiH₃)",
                "rango": "945-930 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "No splitting"
        },
        {
                "familia": "Silicio",
                "grupo": "SiH derivatives RSiH₃",
                "asignacion": "δs(SiH₃)",
                "rango": "930-910 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "in asymmetric and sym. modes"
        },
        {
                "familia": "Silicio",
                "grupo": "SiH derivatives RSiH₃",
                "asignacion": "σ(SiH₃)",
                "rango": "680-540 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "R₂SiH₂",
                "asignacion": "ν(SiH)",
                "rango": "2140-2115 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "R₂SiH₂",
                "asignacion": "δ(SiH₂)",
                "rango": "950-930 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "R₂SiH₂",
                "asignacion": "ω(SiH₂)",
                "rango": "895-885 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "R₃SiH",
                "asignacion": "ν(SiH)",
                "rango": "2100-2090 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "R₃SiH",
                "asignacion": "ω(SiH)",
                "rango": "845-800 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "ArSiH₃",
                "asignacion": "ν(SiH)",
                "rango": "2160-2150 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "ArSiH₃",
                "asignacion": "δas(SiH₃)",
                "rango": "945-930 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "ArSiH₃",
                "asignacion": "δs(SiH₃)",
                "rango": "930-910 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar₂SiH₂",
                "asignacion": "ν(SiH)",
                "rango": "2150-2130 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar₂SiH₂",
                "asignacion": "δ(SiH)",
                "rango": "950-925 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar₂SiH₂",
                "asignacion": "ω(SiH)",
                "rango": "870-840 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar₃SiH",
                "asignacion": "ν(SiH)",
                "rango": "2135-2110 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar₃SiH",
                "asignacion": "ω(SiH)",
                "rango": "845-800 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-Si(CH₃)H",
                "asignacion": "ν(SiH)",
                "rango": "ca. 2230 cm⁻¹",
                "intensidad": "",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "SiC derivatives C-Si(CH₃)₃₋₃",
                "asignacion": "νas(CH₃)",
                "rango": "2980 cm⁻¹",
                "intensidad": "s-vs sh",
                "observacion": "May be merged with νas(CH₂-C)"
        },
        {
                "familia": "Silicio",
                "grupo": "SiC derivatives C-Si(CH₃)₃₋₃",
                "asignacion": "δs(CH₃)",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "O-Si(CH₃)₃₋₃",
                "asignacion": "νas(CH₃)",
                "rango": "2980 cm⁻¹",
                "intensidad": "s-vs sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "O-Si(CH₃)₃₋₃",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 1265 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(C,C)>Si(CH₃)₂",
                "asignacion": "ν(Si-C)",
                "rango": "ca. 830 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(C,C)>Si(CH₃)₂",
                "asignacion": "Sin asignación específica",
                "rango": "815-800 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(C,C)>Si(CH₃)₂",
                "asignacion": "Sin asignación específica",
                "rango": "770-750 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(O,O)>Si(CH₃)₂",
                "asignacion": "ν(Si-C)",
                "rango": "ca. 800 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(O,O)>Si(CH₃)₂",
                "asignacion": "Sin asignación específica",
                "rango": "770-750 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-Si(CH₃)₃",
                "asignacion": "ν(Si-C)",
                "rango": "ca. 860 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "O-Si(CH₃)₃",
                "asignacion": "ν(Si-C)",
                "rango": "ca. 850 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "O-Si(CH₃)₃",
                "asignacion": "Sin asignación específica",
                "rango": "770-750 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "ν(ring-H)",
                "rango": "3080±3070 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "ν(ring)",
                "rango": "1430 cm⁻¹",
                "intensidad": "s sh",
                "observacion": "All bands due to ring vibrations are"
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "Sin asignación específica",
                "rango": "",
                "intensidad": "",
                "observacion": "sharp"
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "ν(Si-ring)",
                "rango": "1110 cm⁻¹",
                "intensidad": "s-vs sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 820 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "γ(ring-H)",
                "rango": "700 cm⁻¹",
                "intensidad": "vs sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "δ(ring)",
                "rango": "540 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "C-SiΦ₂-C",
                "asignacion": "γ(C-Si-Φ)",
                "rango": "465 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "ν(ring-H)",
                "rango": "3085±3075 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "ν(ring)",
                "rango": "1430 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "Sin asignación específica",
                "rango": "1400 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "ν(Si-ring)",
                "rango": "1110 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "δ(ring-H)",
                "rango": "1015 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "ν(Si-ring)",
                "rango": "830 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "γ(ring-H)",
                "rango": "700 cm⁻¹",
                "intensidad": "vs sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Ar-SiΦ₂-Ar",
                "asignacion": "δ(ring)",
                "rango": "530-515 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": ">SiΦ-O-",
                "asignacion": "ν(ring-H)",
                "rango": "3080 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": ">SiΦ-O-",
                "asignacion": "ν(ring-H)",
                "rango": "3070 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": ">SiΦ-O-",
                "asignacion": "ν(Si-ring)",
                "rango": "1130 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": ">SiΦ-O-",
                "asignacion": "γ(ring-H)",
                "rango": "ca. 735 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": ">SiΦ-O-",
                "asignacion": "Sin asignación específica",
                "rango": "700 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "δ(Φ-Si-O)",
                "rango": "ca. 480 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "ν(ring-H)",
                "rango": "3080±3070 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "δ(ring-H)",
                "rango": "995 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "Sin asignación específica",
                "rango": "740 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "Sin asignación específica",
                "rango": "720 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "γ(ring-H)",
                "rango": "700 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "δ(Si-O-Φ)",
                "rango": "ca. 520 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-O-SiΦ₂-",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 490 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Si-OH and Si-O derivatives Si-OH",
                "asignacion": "ν(OH)",
                "rango": "3800-3600 cm⁻¹",
                "intensidad": "m br",
                "observacion": "Silanols"
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(CH₃)₂-O- siloxanes",
                "asignacion": "νas(Si-O-Si)",
                "rango": "1100 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "Fused double band"
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(CH₃)₂-O- siloxanes",
                "asignacion": "Sin asignación específica",
                "rango": "1025 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-R silylethers",
                "asignacion": "δ(Si-O-Si)",
                "rango": "400 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-R silylethers",
                "asignacion": "νas(Si-O-C)",
                "rango": "1110-1000 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "Frequently around 1050"
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-R silylethers",
                "asignacion": "δ(Si-O-C)",
                "rango": "ca. 500 cm⁻¹",
                "intensidad": "m br",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-Ar",
                "asignacion": "νas(Si-O-Ar)",
                "rango": "1250-1180 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "Broader than ring vibr."
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-Ar",
                "asignacion": "Sin asignación específica",
                "rango": "1000-900 cm⁻¹",
                "intensidad": "s br",
                "observacion": "2–3 components"
        },
        {
                "familia": "Silicio",
                "grupo": "Si-O-Ar",
                "asignacion": "δ(Si-O-Ar)",
                "rango": "520-500 cm⁻¹",
                "intensidad": "m-s br",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "Si(OR)₁₋₃ silyl esters >Si(OCH₃)₂",
                "asignacion": "γ(Si-O-C)",
                "rango": "390-360 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OCH₃)₃",
                "asignacion": "νas(CH₃)",
                "rango": "ca. 2850 cm⁻¹",
                "intensidad": "s-vs sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OCH₃)₃",
                "asignacion": "Sin asignación específica",
                "rango": "1410-1400 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OCH₃)₃",
                "asignacion": "νas(Si-O-C)",
                "rango": "1190 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OCH₃)₃",
                "asignacion": "νas(OSiO)",
                "rango": "ca. 1090 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OCH₃)₃",
                "asignacion": "δ(Si-O-C)",
                "rango": "645-620 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OC₂H₅)₃",
                "asignacion": "overtone",
                "rango": "2770 cm⁻¹",
                "intensidad": "w sh",
                "observacion": "Important for identification"
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OC₂H₅)₃",
                "asignacion": "overtone",
                "rango": "2740 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OC₂H₅)₃",
                "asignacion": "νas(Si-O-C)",
                "rango": "1170 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OC₂H₅)₃",
                "asignacion": "νas(O-Si-O)",
                "rango": "1110+1080 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "Merged twin band"
        },
        {
                "familia": "Silicio",
                "grupo": "-Si(OC₂H₅)₃",
                "asignacion": "Sin asignación específica",
                "rango": "645-635 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(RO)ₙSi-CH=CH₂",
                "asignacion": "ν(HC=CH₂)",
                "rango": "3060 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(RO)ₙSi-CH=CH₂",
                "asignacion": "ν(C=C)",
                "rango": "1600 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(RO)ₙSi-CH=CH₂",
                "asignacion": "δ(HC=CH₂)",
                "rango": "1010 cm⁻¹",
                "intensidad": "s sh",
                "observacion": ""
        },
        {
                "familia": "Silicio",
                "grupo": "(RO)ₙSi-CH=CH₂",
                "asignacion": "Sin asignación específica",
                "rango": "550-540 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "C-F aliphatic R-CH₂-F",
                "asignacion": "δ(CH₂F)",
                "rango": "ca. 1430 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "C-F aliphatic R-CH₂-F",
                "asignacion": "ν(CF/CC)",
                "rango": "ca. 1055 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "coupled vibration"
        },
        {
                "familia": "Halógenos",
                "grupo": "C-F aliphatic R-CH₂-F",
                "asignacion": "ν(CF/CC)",
                "rango": "ca. 1015 cm⁻¹",
                "intensidad": "s",
                "observacion": "coupled vibration"
        },
        {
                "familia": "Halógenos",
                "grupo": "C-F aliphatic R-CH₂-F",
                "asignacion": "ν(CCF/CF)",
                "rango": "ca. 915 cm⁻¹",
                "intensidad": "m",
                "observacion": "coupled vibration"
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CHF-CH₂-",
                "asignacion": "δ(CH₂F)",
                "rango": "ca. 1420 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CHF-CH₂-",
                "asignacion": "ν(CF/CC)",
                "rango": "ca. 1090 cm⁻¹",
                "intensidad": "vs br",
                "observacion": "coupled vibration"
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CHF-CH₂-",
                "asignacion": "ν(CCF/CF)",
                "rango": "ca. 1030 cm⁻¹",
                "intensidad": "s-vs br",
                "observacion": "coupled vibration"
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CHF-CH₂-",
                "asignacion": "ν(CCF)δ(CHF)",
                "rango": "ca. 830 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CF₂-CH₂-",
                "asignacion": "νas(CF₂)",
                "rango": "3020 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CF₂-CH₂-",
                "asignacion": "νs(CF₂)",
                "rango": "2980 cm⁻¹",
                "intensidad": "w sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CF₂-CH₂-",
                "asignacion": "δ(CH₂-CF₂)",
                "rango": "1400 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CF₂-CH₂-",
                "asignacion": "νas(CF₂)",
                "rango": "ca. 1180 cm⁻¹",
                "intensidad": "vs br",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "-CH₂-CF₂-CH₂-",
                "asignacion": "ν(CCF)δ(CF₂)",
                "rango": "880 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CH₂-",
                "asignacion": "δ(CH₂)",
                "rango": "ca. 1415 cm⁻¹",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CH₂-",
                "asignacion": "νas(CF₃)",
                "rango": "ca. 1280 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CH₂-",
                "asignacion": "νs(CF₃)",
                "rango": "1165+1145 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CH₂-",
                "asignacion": "δ(CF₃)",
                "rango": "ca. 665 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CO-",
                "asignacion": "ν(C=O)",
                "rango": "ca. 1785 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CO-",
                "asignacion": "νas(CF₃)",
                "rango": "ca. 1230 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CO-",
                "asignacion": "νs(CF₃)",
                "rango": "ca. 1170 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-CO-",
                "asignacion": "δ(CF₃)",
                "rango": "ca. 690 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-Ar",
                "asignacion": "νas(CF₃)",
                "rango": "1335-1320 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-Ar",
                "asignacion": "νs(CF₃)",
                "rango": "1140-1130 cm⁻¹",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "CF₃-Ar",
                "asignacion": "δ(CF₃)",
                "rango": "700-600 cm⁻¹",
                "intensidad": "m-s sh",
                "observacion": "dependent on substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-F",
                "asignacion": "ν(Ar-F)",
                "rango": "1265-1200 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "dependent on substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-F",
                "asignacion": "Sin asignación específica",
                "rango": "550-500 cm⁻¹",
                "intensidad": "var",
                "observacion": "dependent on substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-F",
                "asignacion": "Sin asignación específica",
                "rango": "455-440 cm⁻¹",
                "intensidad": "w-m sh",
                "observacion": "ΦF: 405m"
        },
        {
                "familia": "Halógenos",
                "grupo": "CCl³ aliphatic R-CH₂-Cl",
                "asignacion": "ωCH₂ClνCCCl",
                "rango": "1300-1240 cm⁻¹",
                "intensidad": "var sh",
                "observacion": "i-alkyl: vs"
        },
        {
                "familia": "Halógenos",
                "grupo": "CCl³ aliphatic R-CH₂-Cl",
                "asignacion": "ν(C-Cl)",
                "rango": "ca. 650 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "β-branched",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 730 cm⁻¹",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "β-branched",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 690 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "(CH₂)₄>CH-Cl",
                "asignacion": "νCCClωCH₂Cl",
                "rango": "ca. 1250 cm⁻¹",
                "intensidad": "s-vs br",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "(CH₂)₄>CH-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 960 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "(CH₂)₄>CH-Cl",
                "asignacion": "ν(C-Cl)",
                "rango": "760-740 cm⁻¹",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "(CH₂)₄>CH-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "690-660 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 640 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "ca. 610 cm⁻¹",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "ν(C-CCl)",
                "rango": "1240-1225 cm⁻¹",
                "intensidad": "m sh",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "1160-1145 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "ν(C-Cl)",
                "rango": "ca. 620 cm⁻¹",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "R₃C-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "570-560 cm⁻¹",
                "intensidad": "m-s",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Cl",
                "asignacion": "δ(ring-H)/",
                "rango": "1100-1090 cm⁻¹",
                "intensidad": "s",
                "observacion": "p-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Cl",
                "asignacion": "ν(ring-Cl)",
                "rango": "1080-1070 cm⁻¹",
                "intensidad": "m",
                "observacion": "m-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "1060-1030 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "o-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Cl",
                "asignacion": "ν(ring-Cl)",
                "rango": "ca. 680 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "o- and m-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Cl",
                "asignacion": "Sin asignación específica",
                "rango": "640-630 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "p-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "C-Br aliphatic R-CH₂-Br",
                "asignacion": "νCCBroνCH₂Br",
                "rango": "1255-1225 cm⁻¹",
                "intensidad": "s-vs",
                "observacion": "numerous acti-"
        },
        {
                "familia": "Halógenos",
                "grupo": "C-Br aliphatic R-CH₂-Br",
                "asignacion": "ν(C-Br)",
                "rango": "650-640 cm⁻¹",
                "intensidad": "m",
                "observacion": "vated skeleton"
        },
        {
                "familia": "Halógenos",
                "grupo": "C-Br aliphatic R-CH₂-Br",
                "asignacion": "Sin asignación específica",
                "rango": "570-555 cm⁻¹",
                "intensidad": "m",
                "observacion": "vibrations"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Br",
                "asignacion": "δ(ring-H)/",
                "rango": "1085-1070 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "m- and p-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Br",
                "asignacion": "ν(ring-Br)",
                "rango": "1030-1020 cm⁻¹",
                "intensidad": "m-vst",
                "observacion": "o-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Br",
                "asignacion": "Sin asignación específica",
                "rango": "680-655 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "o- and m-substitution"
        },
        {
                "familia": "Halógenos",
                "grupo": "Ar-Br",
                "asignacion": "Sin asignación específica",
                "rango": "605-595 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "p-substituted"
        },
        {
                "familia": "Halógenos",
                "grupo": "R-I aliphatic n-alkyl",
                "asignacion": "ν(C-CI)",
                "rango": "1250-1185 cm⁻¹",
                "intensidad": "m-vs",
                "observacion": "dependent on chain length"
        },
        {
                "familia": "Halógenos",
                "grupo": "R-I aliphatic n-alkyl",
                "asignacion": "Sin asignación específica",
                "rango": "1190-1170 cm⁻¹",
                "intensidad": "m-s",
                "observacion": "not always present"
        },
        {
                "familia": "Halógenos",
                "grupo": "R-I aliphatic n-alkyl",
                "asignacion": "ν(C-I)ᵈ",
                "rango": "600-590 cm⁻¹",
                "intensidad": "vw-m",
                "observacion": "C₃H₇I: 500"
        },
        {
                "familia": "Halógenos",
                "grupo": "R-I aliphatic n-alkyl",
                "asignacion": "Sin asignación específica",
                "rango": "505-500 cm⁻¹",
                "intensidad": "w-vw",
                "observacion": ""
        },
        {
                "familia": "Halógenos",
                "grupo": "i-alkyl numerous activated skeleton vibrations",
                "asignacion": "Ar-I",
                "rango": "ν(Ar-I)",
                "intensidad": "655-640 cm⁻¹",
                "observacion": "m-vs sh"
        },
        {
                "familia": "Halógenos",
                "grupo": "i-alkyl numerous activated skeleton vibrations",
                "asignacion": "Sin asignación específica",
                "rango": "465-430 cm⁻¹",
                "intensidad": "w-s sh",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Primary amines",
                "asignacion": "ν(-NH)",
                "rango": "3400-3380",
                "intensidad": "3400-3380",
                "observacion": "s/m"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Secondary amines",
                "asignacion": "ν(-NH)",
                "rango": "3350-3320",
                "intensidad": "3350-3320",
                "observacion": "s/m"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Alkyldimethylamines and dialkylamethylamines",
                "asignacion": "ν(C-H)",
                "rango": "2810-2760",
                "intensidad": "2810-2760",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Protonated primary amines",
                "asignacion": "νas(NH₃⁺)",
                "rango": "3000",
                "intensidad": "3000",
                "observacion": "s"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Protonated secondary amines",
                "asignacion": "νas(N⁺H₂)",
                "rango": "2800-2950",
                "intensidad": "2800-2950",
                "observacion": "s"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Protonated tertiary amines",
                "asignacion": "ν(N⁺H)",
                "rango": "2700",
                "intensidad": "2700",
                "observacion": "s"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Alkyltrimethylammonium salts",
                "asignacion": "ν(N⁺R₄)",
                "rango": "960",
                "intensidad": "960",
                "observacion": "s"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Dialkyldimethylammonium salts",
                "asignacion": "ν(N⁺R₄)",
                "rango": "≈ 1000",
                "intensidad": "≈ 1000",
                "observacion": "w"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Benzalkonium salts",
                "asignacion": "δ(ring)",
                "rango": "700",
                "intensidad": "700",
                "observacion": "m"
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Esterquats",
                "asignacion": "ν(ester group)",
                "rango": "1700-1750",
                "intensidad": "1700-1750",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Cuaternarios",
                "grupo": "Sulfate anion",
                "asignacion": "S=O doublet bands",
                "rango": "1248 and 1217",
                "intensidad": "1248 and 1217",
                "observacion": "s"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Alkylbenzene sulfonate",
                "asignacion": "6.7",
                "rango": "1493",
                "intensidad": "1493",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Fatty alcohol sulfate",
                "asignacion": "8.0",
                "rango": "1250",
                "intensidad": "1250",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Sulfonated amide (taurate)",
                "asignacion": "6.1",
                "rango": "1639",
                "intensidad": "1639",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Sulfonated ester (isethionate)",
                "asignacion": "5.8",
                "rango": "1724",
                "intensidad": "1724",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Sulfated monoglyceride",
                "asignacion": "3.0",
                "rango": "3333",
                "intensidad": "3333",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Sulfated phenoxy ether",
                "asignacion": "6.2",
                "rango": "1613",
                "intensidad": "1613",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Ethoxylated fatty acid",
                "asignacion": "2.9",
                "rango": "3448",
                "intensidad": "3448",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Ethoxylated fatty alcohol",
                "asignacion": "2.9",
                "rango": "3448",
                "intensidad": "3448",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Ethoxylated alkyl phenol",
                "asignacion": "3.0",
                "rango": "3448",
                "intensidad": "3448",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Glyceryl monostearate",
                "asignacion": "3.0",
                "rango": "3333",
                "intensidad": "3333",
                "observacion": "broad"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Mono-alkylol amide",
                "asignacion": "3.0",
                "rango": "3333",
                "intensidad": "3333",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Soap",
                "asignacion": "6.4",
                "rango": "1563",
                "intensidad": "1563",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Aliphatic quaternary ammonium chloride",
                "asignacion": "2.9",
                "rango": "3448",
                "intensidad": "3448",
                "observacion": "sharp"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Alcohol polyether sulfate",
                "asignacion": "7.4",
                "rango": "1351",
                "intensidad": "1351",
                "observacion": "broad"
        },
        {
                "familia": "Tensoactivos Comerciales",
                "grupo": "Alpha olefin sulfonate",
                "asignacion": "2.9",
                "rango": "3448",
                "intensidad": "3448",
                "observacion": "broad"
        },
        {
                "familia": "Alquenos",
                "grupo": "-C≡CH",
                "asignacion": "ν(≡C-H) - Tensión",
                "rango": "3340-3300",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "-C≡CH",
                "asignacion": "ν(C≡C) - Tensión",
                "rango": "2130-2110",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "-C≡C-",
                "asignacion": "Sin asignación específica",
                "rango": "2210-2190",
                "intensidad": "var",
                "observacion": "Inactive with equal substituents"
        },
        {
                "familia": "Alquenos",
                "grupo": "R-C≡CH",
                "asignacion": "δ(CC-H)",
                "rango": "640-625",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-C≡CH",
                "asignacion": "δ(HCC-C)",
                "rango": "355-335",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "νas(=CH₂) - Tensión asimétrica",
                "rango": "3080",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ν(=C-H) - Tensión",
                "rango": "3000",
                "intensidad": "vw",
                "observacion": "Merges with νas(CH₃)"
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "overtone",
                "rango": "1820",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ν(C=C) - Tensión",
                "rango": "1640",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "δs(=CH₂)",
                "rango": "1415",
                "intensidad": "vw",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ρ(C=CH₂)",
                "rango": "1300",
                "intensidad": "vw",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ωE(HC=CH)",
                "rango": "990",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ω(=CH₂)",
                "rango": "910",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R-vinyl",
                "asignacion": "ωZ(HC=CH)",
                "rango": "630",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "Z R-CH=CH-R' (cis)",
                "asignacion": "νas(HC=CH)",
                "rango": "3020-3000",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "Z R-CH=CH-R' (cis)",
                "asignacion": "ν(C=C)",
                "rango": "1660-1650",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "Z R-CH=CH-R' (cis)",
                "asignacion": "γs(HC=CH)",
                "rango": "690-750",
                "intensidad": "m, br",
                "observacion": "Frequency depends on substitution"
        },
        {
                "familia": "Alquenos",
                "grupo": "E R-CH=CH-R' (trans)",
                "asignacion": "νas(HC=CH)",
                "rango": "3015",
                "intensidad": "w",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "E R-CH=CH-R' (trans)",
                "asignacion": "ν(C=C)",
                "rango": "1660",
                "intensidad": "var",
                "observacion": "Inactive with equal substituents"
        },
        {
                "familia": "Alquenos",
                "grupo": "E R-CH=CH-R' (trans)",
                "asignacion": "γs(HC=CH)",
                "rango": "970",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "RR'>C=CH₂",
                "asignacion": "νs(=CH₂)",
                "rango": "3080",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "RR'>C=CH₂",
                "asignacion": "overtone",
                "rango": "1785",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "RR'>C=CH₂",
                "asignacion": "ν(C=C)",
                "rango": "1650",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "RR'>C=CH₂",
                "asignacion": "γ(C=CH₂)",
                "rango": "895-885",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R₂C=CHR'",
                "asignacion": "ν(C=C)",
                "rango": "1670-1665",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R₂C=CHR'",
                "asignacion": "γ(HC=C)",
                "rango": "840-790",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Alquenos",
                "grupo": "R₂C=CR'₂",
                "asignacion": "ν(C=C)",
                "rango": "1680-1665",
                "intensidad": "vw-w",
                "observacion": "Often inactive"
        },
        {
                "familia": "Alquenos",
                "grupo": "C=C-C=C conjugated",
                "asignacion": "ν(C=C)",
                "rango": "1650, 1600",
                "intensidad": "m-s",
                "observacion": "Two bands"
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "ν(C-H) - Tensión",
                "rango": "3100-3000",
                "intensidad": "w-m",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "ν(C=C ring)",
                "rango": "1600",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "ν(C=C ring)",
                "rango": "1585",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "ν(C=C ring)",
                "rango": "1500",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "ν(C=C ring)",
                "rango": "1450",
                "intensidad": "var",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Anillo aromático",
                "asignacion": "δ(C-H) in-plane",
                "rango": "1300-1000",
                "intensidad": "w-m",
                "observacion": "Complex region"
        },
        {
                "familia": "Aromáticos",
                "grupo": "Monosustituido",
                "asignacion": "γ(ring-H) - Fuera del plano",
                "rango": "750",
                "intensidad": "s-vs",
                "observacion": "5 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "Monosustituido",
                "asignacion": "γ(ring-H)",
                "rango": "700-685",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "o-disustituido",
                "asignacion": "γ(ring-H)",
                "rango": "750",
                "intensidad": "s",
                "observacion": "4 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "m-disustituido",
                "asignacion": "γ(ring-H)",
                "rango": "900-860",
                "intensidad": "w",
                "observacion": "1 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "m-disustituido",
                "asignacion": "γ(ring-H)",
                "rango": "810-750",
                "intensidad": "s",
                "observacion": "2 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "m-disustituido",
                "asignacion": "γ(ring-H)",
                "rango": "725-680",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "p-disustituido",
                "asignacion": "γ(ring-H)",
                "rango": "860-800",
                "intensidad": "s-vs",
                "observacion": "2 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,3-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "800-770",
                "intensidad": "s",
                "observacion": "2 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,3-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "745-705",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,4-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "900-860",
                "intensidad": "m",
                "observacion": "1 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,4-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "860-800",
                "intensidad": "s",
                "observacion": "2 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,3,5-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "900-860",
                "intensidad": "vs",
                "observacion": "3 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,3,5-trisustituido",
                "asignacion": "γ(ring-H)",
                "rango": "730-675",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,3,4-tetrasustituido",
                "asignacion": "γ(ring-H)",
                "rango": "825-810",
                "intensidad": "s",
                "observacion": "2 H adjacent"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,3,5-tetrasustituido",
                "asignacion": "γ(ring-H)",
                "rango": "900-860",
                "intensidad": "m",
                "observacion": "2 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "1,2,4,5-tetrasustituido",
                "asignacion": "γ(ring-H)",
                "rango": "870-855",
                "intensidad": "s",
                "observacion": "2 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "Pentasustituido",
                "asignacion": "γ(ring-H)",
                "rango": "900-860",
                "intensidad": "m",
                "observacion": "1 H isolated"
        },
        {
                "familia": "Aromáticos",
                "grupo": "Naftaleno",
                "asignacion": "ν(C=C)",
                "rango": "1600, 1580, 1510",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Naftaleno",
                "asignacion": "γ(C-H)",
                "rango": "800-750",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Antraceno",
                "asignacion": "ν(C=C)",
                "rango": "1625, 1435",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Aromáticos",
                "grupo": "Antraceno",
                "asignacion": "γ(C-H)",
                "rango": "890-740",
                "intensidad": "s",
                "observacion": "Multiple bands"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "O-H valence",
                "asignacion": "O-H",
                "rango": "3600-3200",
                "intensidad": "s",
                "observacion": "Alcohols"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "N-H valence",
                "asignacion": "N-H",
                "rango": "3430-3160",
                "intensidad": "s",
                "observacion": "Amides"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C-H valence",
                "asignacion": "C-H",
                "rango": "3125-3000",
                "intensidad": "m",
                "observacion": "Olefins and aromatics"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C-H methyl",
                "asignacion": "C-H",
                "rango": "2960-2870",
                "intensidad": "s",
                "observacion": "All surfactants"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C-H methylene",
                "asignacion": "C-H",
                "rango": "2930-2850",
                "intensidad": "s",
                "observacion": "All surfactants"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C=O esters",
                "asignacion": "C=O",
                "rango": "1750-1715",
                "intensidad": "vs",
                "observacion": "Esters"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C=O amides",
                "asignacion": "C=O",
                "rango": "1680-1630",
                "intensidad": "vs",
                "observacion": "Amides"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C=C olefins",
                "asignacion": "C=C",
                "rango": "1680-1620",
                "intensidad": "w",
                "observacion": "Olefins"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "C=C aromatics",
                "asignacion": "C=C",
                "rango": "1600-1585",
                "intensidad": "m",
                "observacion": "Aromatics"
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Carboxylates",
                "asignacion": "C=O",
                "rango": "1650-1550",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Sulfates",
                "asignacion": "S=O",
                "rango": "1350-1220",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Sulfonates",
                "asignacion": "S=O",
                "rango": "1250-1140",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Sulfates S-O",
                "asignacion": "S-O",
                "rango": "1140-1050",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Ethers aromatic",
                "asignacion": "C-O-C",
                "rango": "1250",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos Aniónicos",
                "grupo": "Ethers aliphatic",
                "asignacion": "C-O-C",
                "rango": "1120-1100",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated alcohols",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated alcohols",
                "asignacion": "C-O",
                "rango": "1150-1100",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated alkylphenols",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated alkylphenols",
                "asignacion": "C=C",
                "rango": "1600-1580",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated alkylphenols",
                "asignacion": "C-O",
                "rango": "1150-1100",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated acids",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated acids",
                "asignacion": "C=O",
                "rango": "1740-1730",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Ethoxylated acids",
                "asignacion": "C-O",
                "rango": "1150-1100",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Fatty acid alkanolamides",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Fatty acid alkanolamides",
                "asignacion": "C=O",
                "rango": "1640",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Fatty acid alkanolamides",
                "asignacion": "N-H",
                "rango": "1550",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Esters of polyhydroxy",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "s",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "Esters of polyhydroxy",
                "asignacion": "C=O",
                "rango": "1740-1730",
                "intensidad": "vs",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "EO/PO copolymers",
                "asignacion": "OH",
                "rango": "3300",
                "intensidad": "m",
                "observacion": ""
        },
        {
                "familia": "Tensoactivos No Iónicos",
                "grupo": "EO/PO copolymers",
                "asignacion": "C-O",
                "rango": "1150-1100",
                "intensidad": "vs",
                "observacion": ""
        }
]
    
    return pd.DataFrame(data)

# Funciones de búsqueda
def parse_range(range_str):
    """Parsea un rango de números de onda"""
    try:
        range_str = str(range_str).replace('ca.', '').replace('±', '').strip()
        
        if '-' in range_str:
            parts = range_str.split('-')
            return int(re.sub(r'[^0-9]', '', parts[0])), int(re.sub(r'[^0-9]', '', parts[1]))
        else:
            val = int(re.sub(r'[^0-9]', '', range_str))
            return val - 10, val + 10
    except:
        return None, None

def search_by_wavenumber(df, wavenumber):
    """Busca por número de onda con tolerancia de ±30 cm⁻¹"""
    exact_matches = []
    nearby_matches = []
    
    for idx, row in df.iterrows():
        min_val, max_val = parse_range(row['rango'])
        if min_val is None:
            continue
            
        if min_val <= wavenumber <= max_val:
            exact_matches.append(row)
        elif (abs(wavenumber - min_val) <= 30 or abs(wavenumber - max_val) <= 30):
            nearby_matches.append(row)
    
    return exact_matches, nearby_matches

def search_contains(df, query):
    """Búsqueda por 'Contiene' - busca el término en todos los campos"""
    if not query:
        return df
    
    query_lower = query.lower()
    
    mask = (
        df['familia'].str.lower().str.contains(query_lower, na=False, regex=False) |
        df['grupo'].str.lower().str.contains(query_lower, na=False, regex=False) |
        df['asignacion'].str.lower().str.contains(query_lower, na=False, regex=False) |
        df['observacion'].str.lower().str.contains(query_lower, na=False, regex=False)
    )
    
    return df[mask]

def filter_by_bond_type(df, bond_type):
    """Filtrar por tipo de enlace"""
    if bond_type == "Todos":
        return df
    
    bond_mapping = {
        "C-C": ["c-c"],
        "C-H": ["c-h", "ch₃", "ch₂", "ch"],
        "C-O": ["c-o", "alcohol", "éter"],
        "C=O": ["c=o", "carbonilo", "cetona", "aldehído", "ácido", "éster", "amida"],
        "C=C": ["c=c", "alqueno", "vinyl"],
        "C≡C": ["c≡c", "alquino"],
        "N-H": ["n-h", "nh₂", "nh", "amina", "amida"],
        "C-N": ["c-n"],
        "C=N": ["c=n", "imina"],
        "C≡N": ["c≡n", "nitrilo"],
        "O-H": ["o-h", "oh", "alcohol", "fenol", "ácido"],
        "S-H": ["s-h", "sh", "tiol"],
        "C-S": ["c-s", "sulfuro"],
        "S=O": ["s=o", "sulfóxido", "sulfona"],
        "S-O": ["s-o", "sulfonato"],
        "C-P": ["c-p"],
        "P=O": ["p=o", "fosfato"],
        "P-O": ["p-o"],
        "C-F": ["c-f", "fluor"],
        "C-Cl": ["c-cl", "cloro"],
        "C-Br": ["c-br", "bromo"],
        "C-I": ["c-i", "iodo"],
        "N=O": ["n=o", "nitroso"],
        "NO₂": ["no₂", "nitro"]
    }
    
    terms = bond_mapping.get(bond_type, [bond_type.lower()])
    
    mask = False
    for term in terms:
        mask = mask | (
            df['grupo'].str.lower().str.contains(term, na=False, regex=False) |
            df['asignacion'].str.lower().str.contains(term, na=False, regex=False) |
            df['familia'].str.lower().str.contains(term, na=False, regex=False)
        )
    
    return df[mask]

def filter_by_frequency_range(df, min_freq, max_freq):
    """Filtrar por rango de frecuencia personalizado"""
    results = []
    
    for idx, row in df.iterrows():
        range_min, range_max = parse_range(row['rango'])
        if range_min is None:
            continue
        
        if (range_min <= max_freq and range_max >= min_freq):
            results.append(row)
    
    if results:
        return pd.DataFrame(results)
    return pd.DataFrame()

def apply_combined_filters(df, filters):
    """Aplica todos los filtros seleccionados de forma acumulativa"""
    filtered = df.copy()
    
    # Filtro por búsqueda de texto
    if filters.get('search_query'):
        filtered = search_contains(filtered, filters['search_query'])
    
    # Filtro por familia
    if filters.get('familia') and filters['familia'] != "Todas":
        filtered = filtered[filtered['familia'] == filters['familia']]
    
    # Filtro por tipo de enlace
    if filters.get('enlace') and filters['enlace'] != "Todos":
        filtered = filter_by_bond_type(filtered, filters['enlace'])
    
    # Filtro por rango de frecuencia
    if filters.get('rango_min') is not None and filters.get('rango_max') is not None:
        # Solo aplicar si se modificó del valor por defecto
        if filters['rango_min'] != 1000 or filters['rango_max'] != 2000:
            filtered = filter_by_frequency_range(filtered, filters['rango_min'], filters['rango_max'])
    
    return filtered

def get_active_filters_description(filters):
    """Genera descripción de filtros activos"""
    active = []
    
    if filters.get('search_query'):
        active.append(f"Texto: '{filters['search_query']}'")
    
    if filters.get('familia') and filters['familia'] != "Todas":
        active.append(f"Familia: {filters['familia']}")
    
    if filters.get('enlace') and filters['enlace'] != "Todos":
        active.append(f"Enlace: {filters['enlace']}")
    
    if filters.get('rango_min') is not None and filters.get('rango_max') is not None:
        if filters['rango_min'] != 1000 or filters['rango_max'] != 2000:
            active.append(f"Rango: {filters['rango_min']}-{filters['rango_max']} cm⁻¹")
    
    return active

# Cargar datos
df = load_data()

# INTERFAZ PRINCIPAL
st.markdown("<h1>🔬 IR Spectroscopy Database</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.1em;'>Base de Datos Completa - 860 Bandas IR - Filtros Combinados</p>", unsafe_allow_html=True)

# Métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Bandas IR", len(df))
with col2:
    st.metric("🧪 Familias", df['familia'].nunique())
with col3:
    st.metric("🔬 Grupos", df['grupo'].nunique())
with col4:
    st.metric("📈 Tablas", "24")

st.markdown("---")

# Barra lateral con filtros
with st.sidebar:
    st.header("🔍 Filtros de Búsqueda")
    
    st.info("💡 **Filtros combinados:** Todos los filtros se aplican simultáneamente. Combínalos para búsquedas precisas.")
    
    st.markdown("---")
    
    # Modo de búsqueda
    search_mode = st.radio(
        "Modo de búsqueda:",
        ["Búsqueda normal", "Búsqueda por 'Contiene'"],
        help="Normal: número de onda exacto. Contiene: busca texto en todos los campos"
    )
    
    # Búsqueda principal
    search_query = st.text_input(
        "🔎 Buscar texto:",
        placeholder="Número de onda, nombre, grupo funcional...",
        help="Busca en familia, grupo, asignación y observaciones",
        key="search_input"
    )
    
    st.markdown("---")
    
    # Filtro por familia
    st.subheader("🧪 Familia Química")
    familias = ["Todas"] + sorted(df['familia'].unique().tolist())
    familia_seleccionada = st.selectbox(
        "Selecciona:",
        familias,
        key="familia_select"
    )
    
    st.markdown("---")
    
    # Filtro por tipo de enlace
    st.subheader("🔗 Tipo de Enlace")
    tipos_enlace = [
        "Todos",
        "C-C", "C-H", "C-O", "C=O", "C=C", "C≡C",
        "N-H", "C-N", "C=N", "C≡N",
        "O-H", "S-H",
        "C-S", "S=O", "S-O",
        "C-P", "P=O", "P-O",
        "C-F", "C-Cl", "C-Br", "C-I",
        "N=O", "NO₂"
    ]
    enlace_seleccionado = st.selectbox(
        "Selecciona:",
        tipos_enlace,
        key="enlace_select"
    )
    
    st.markdown("---")
    
    # Filtro por rango
    st.subheader("📊 Rango de Frecuencia")
    
    rango_valores = st.slider(
        "Selecciona rango (cm⁻¹):",
        min_value=400,
        max_value=4000,
        value=(1000, 2000),
        step=50,
        help="Arrastra para ajustar el rango",
        key="rango_slider"
    )
    
    rango_min, rango_max = rango_valores
    
    st.markdown("---")
    
    # Botón para limpiar filtros
    if st.button("🗑️ Limpiar todos los filtros", use_container_width=True):
        st.session_state.search_input = ""
        st.session_state.familia_select = "Todas"
        st.session_state.enlace_select = "Todos"
        st.session_state.rango_slider = (1000, 2000)
        st.rerun()

# Preparar filtros
filters = {
    'search_query': search_query if search_mode == "Búsqueda por 'Contiene'" or not search_query.isdigit() else None,
    'familia': familia_seleccionada,
    'enlace': enlace_seleccionado,
    'rango_min': rango_min,
    'rango_max': rango_max
}

# Mostrar filtros activos
active_filters = get_active_filters_description(filters)
if active_filters:
    st.markdown("### 🎯 Filtros Activos")
    for filter_desc in active_filters:
        st.markdown(f"<div class='filter-indicator'>✓ {filter_desc}</div>", unsafe_allow_html=True)
    st.markdown("---")

# Aplicar filtros
mostrar_tabla = True

# Caso especial: búsqueda por número de onda exacto
if search_query and search_query.isdigit() and search_mode == "Búsqueda normal":
    mostrar_tabla = False
    
    # Aplicar otros filtros primero
    temp_filters = filters.copy()
    temp_filters['search_query'] = None
    pre_filtered = apply_combined_filters(df, temp_filters)
    
    # Luego buscar por número de onda en el conjunto filtrado
    exact, nearby = search_by_wavenumber(pre_filtered, int(search_query))
    
    total_results = len(exact) + len(nearby)
    
    if active_filters:
        st.success(f"✅ {len(exact)} exactas y {len(nearby)} cercanas para {search_query} cm⁻¹ (con {len(active_filters)} filtro(s) aplicado(s))")
    else:
        st.success(f"✅ {len(exact)} exactas y {len(nearby)} cercanas para {search_query} cm⁻¹")
    
    if exact:
        st.subheader("🎯 Coincidencias Exactas")
        for item in exact:
            with st.container():
                st.markdown(f"""
                <div class='result-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <h3 style='margin: 0; color: #1e40af;'>{item['grupo']}</h3>
                        <span class='family-badge'>{item['familia']}</span>
                    </div>
                    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>ASIGNACIÓN</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #1f2937;'>{item['asignacion']}</p>
                        </div>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>RANGO</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #059669; font-weight: bold;'>{item['rango']} cm⁻¹</p>
                        </div>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>INTENSIDAD</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #1f2937;'>{item['intensidad']}</p>
                        </div>
                    </div>
                    {f"<p style='margin-top: 15px; padding: 10px; background: rgba(99, 102, 241, 0.1); border-left: 3px solid #6366f1; border-radius: 5px; color: #1f2937;'><strong>Observación:</strong> {item['observacion']}</p>" if item['observacion'] else ""}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
    if nearby:
        st.subheader("⚠️ Cercanas (±30 cm⁻¹)")
        for item in nearby:
            with st.container():
                st.markdown(f"""
                <div class='result-card' style='opacity: 0.85;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <h3 style='margin: 0; color: #1e40af;'>{item['grupo']}</h3>
                        <span class='family-badge'>{item['familia']}</span>
                    </div>
                    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>ASIGNACIÓN</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #1f2937;'>{item['asignacion']}</p>
                        </div>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>RANGO</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #f59e0b; font-weight: bold;'>{item['rango']} cm⁻¹</p>
                        </div>
                        <div>
                            <p style='color: #6b7280; font-size: 0.85em; margin: 0;'>INTENSIDAD</p>
                            <p style='margin: 5px 0; font-family: monospace; color: #1f2937;'>{item['intensidad']}</p>
                        </div>
                    </div>
                    {f"<p style='margin-top: 15px; padding: 10px; background: rgba(99, 102, 241, 0.1); border-left: 3px solid #6366f1; border-radius: 5px; color: #1f2937;'><strong>Observación:</strong> {item['observacion']}</p>" if item['observacion'] else ""}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
    if not exact and not nearby:
        st.warning(f"⚠️ No se encontraron bandas para {search_query} cm⁻¹ con los filtros aplicados")

else:
    # Aplicar filtros combinados
    filtered_df = apply_combined_filters(df, filters)
    
    # Mostrar información de resultados
    if len(active_filters) > 0:
        st.info(f"📊 **{len(filtered_df)} bandas** encontradas con **{len(active_filters)} filtro(s)** combinado(s)")
    else:
        st.info(f"📊 Mostrando todas las **{len(filtered_df)} bandas** de la base de datos")

# Mostrar tabla
if mostrar_tabla:
    if len(filtered_df) > 0:
        st.dataframe(
            filtered_df[['familia', 'grupo', 'asignacion', 'rango', 'intensidad', 'observacion']],
            use_container_width=True,
            height=600
        )
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar resultados CSV",
            data=csv,
            file_name='ir_spectroscopy_results.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No se encontraron resultados con los filtros aplicados")
        st.info("💡 Intenta ajustar o eliminar algunos filtros para obtener más resultados")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p><strong>IR Spectroscopy Database</strong> - 860 bandas completas con filtros combinados</p>
    <p style='font-size: 0.9em;'>Base de datos IR profesional - Enero 2026</p>
</div>
""", unsafe_allow_html=True)
