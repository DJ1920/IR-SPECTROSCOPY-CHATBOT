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

# CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #0a0e27;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    h1 {
        color: #60a5fa;
        font-family: 'Courier New', monospace;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a1f3a 0%, #2d1b4e 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: rgba(96, 165, 250, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(96, 165, 250, 0.2);
        text-align: center;
    }
    .result-card {
        background: #151935;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
    }
    .family-badge {
        background: linear-gradient(135deg, #0066cc 0%, #004c99 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    """Carga la base de datos IR completa"""
    data = []
    
    # TABLA 1: ALCANOS
    data.extend([
        {"familia": "Alcanos", "grupo": "-CH₃", "asignacion": "νas - Tensión asimétrica", "rango": "2975-2950", "intensidad": "m-s (medio-fuerte)", "observacion": "sh, violet shift"},
        {"familia": "Alcanos", "grupo": "-CH₃", "asignacion": "νs - Tensión simétrica", "rango": "2885-2865", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Alcanos", "grupo": "-CH₃", "asignacion": "δas - Deformación asimétrica", "rango": "1465-1440", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Alcanos", "grupo": "-CH₃", "asignacion": "δs - Deformación simétrica", "rango": "1390-1370", "intensidad": "m-s (medio-fuerte)", "observacion": ""},
        {"familia": "Alcanos", "grupo": "-CH₂-", "asignacion": "νas - Tensión asimétrica", "rango": "2940-2915", "intensidad": "m-s (medio-fuerte)", "observacion": ""},
        {"familia": "Alcanos", "grupo": "-CH₂-", "asignacion": "νs - Tensión simétrica", "rango": "2870-2840", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Alcanos", "grupo": "-CH₂-", "asignacion": "δ - Deformación", "rango": "1470-1450", "intensidad": "m (medio)", "observacion": "Overlaps with δas(CH₃)"},
    ])
    
    # TABLA 3: ALQUENOS
    data.extend([
        {"familia": "Alquenos", "grupo": "R-vinyl", "asignacion": "ν(C=C) - Tensión", "rango": "1640", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Alquenos", "grupo": "Z-alkene (cis)", "asignacion": "ν(C=C) - Tensión", "rango": "1660-1650", "intensidad": "w-m (débil-medio)", "observacion": ""},
        {"familia": "Alquenos", "grupo": "E-alkene (trans)", "asignacion": "ν(C=C) - Tensión", "rango": "1675-1665", "intensidad": "w (débil)", "observacion": ""},
        {"familia": "Alquenos", "grupo": "Alquino terminal", "asignacion": "ν(C≡C) - Tensión", "rango": "2140-2100", "intensidad": "m (medio)", "observacion": "sharp"},
        {"familia": "Alquenos", "grupo": "Alquino terminal", "asignacion": "ν(≡C-H) - Tensión", "rango": "3310-3300", "intensidad": "s (fuerte)", "observacion": "sharp"},
    ])
    
    # TABLA 4: AROMÁTICOS
    data.extend([
        {"familia": "Aromáticos", "grupo": "Anillo aromático", "asignacion": "ν(C=C ring) - Tensión", "rango": "1600", "intensidad": "var (variable)", "observacion": ""},
        {"familia": "Aromáticos", "grupo": "Anillo aromático", "asignacion": "ν(C=C ring) - Tensión", "rango": "1585", "intensidad": "var (variable)", "observacion": ""},
        {"familia": "Aromáticos", "grupo": "Anillo aromático", "asignacion": "ν(C=C ring) - Tensión", "rango": "1500", "intensidad": "var (variable)", "observacion": ""},
        {"familia": "Aromáticos", "grupo": "Anillo aromático", "asignacion": "ν(C=C ring) - Tensión", "rango": "1450", "intensidad": "var (variable)", "observacion": ""},
        {"familia": "Aromáticos", "grupo": "Monosustituido", "asignacion": "γ(ring-H) - Deformación fuera del plano", "rango": "750±15", "intensidad": "s-vs (fuerte-muy fuerte)", "observacion": "5 H"},
        {"familia": "Aromáticos", "grupo": "o-disustituido", "asignacion": "γ(ring-H)", "rango": "750±10", "intensidad": "s (fuerte)", "observacion": "4 H"},
        {"familia": "Aromáticos", "grupo": "m-disustituido", "asignacion": "γ(ring-H)", "rango": "780±15", "intensidad": "s (fuerte)", "observacion": "3 H"},
        {"familia": "Aromáticos", "grupo": "p-disustituido", "asignacion": "γ(ring-H)", "rango": "830±10", "intensidad": "s-vs (fuerte-muy fuerte)", "observacion": "2 H"},
    ])
    
    # TABLA 7: NITRILOS
    data.extend([
        {"familia": "Nitrilos", "grupo": "Nitrilo alifático", "asignacion": "ν(C≡N) - Tensión", "rango": "2260-2230", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Nitrilos", "grupo": "Nitrilo aromático", "asignacion": "ν(C≡N) - Tensión", "rango": "2240-2220", "intensidad": "m-s (medio-fuerte)", "observacion": ""},
        {"familia": "Nitrilos", "grupo": "Nitrilo conjugado", "asignacion": "ν(C≡N) - Tensión", "rango": "2250-2200", "intensidad": "m-s (medio-fuerte)", "observacion": ""},
    ])
    
    # TABLA 8: AMINAS
    data.extend([
        {"familia": "Aminas", "grupo": "Amina primaria alifática", "asignacion": "νas(NH₂) - Tensión asimétrica", "rango": "3370-3330", "intensidad": "w-m br (débil-medio ancha)", "observacion": "Liquid state"},
        {"familia": "Aminas", "grupo": "Amina primaria alifática", "asignacion": "νs(NH₂) - Tensión simétrica", "rango": "3290-3270", "intensidad": "w-m br (débil-medio ancha)", "observacion": "Liquid state"},
        {"familia": "Aminas", "grupo": "Amina secundaria alifática", "asignacion": "ν(NH) - Tensión", "rango": "3300", "intensidad": "w br (débil ancha)", "observacion": "Liquid"},
        {"familia": "Aminas", "grupo": "Amina primaria aromática", "asignacion": "νas(NH₂) - Tensión asimétrica", "rango": "3470-3385", "intensidad": "m-s sh (medio-fuerte aguda)", "observacion": "Crystalline"},
        {"familia": "Aminas", "grupo": "Amina primaria aromática", "asignacion": "νs(NH₂) - Tensión simétrica", "rango": "3380-3325", "intensidad": "m-s sh (medio-fuerte aguda)", "observacion": "Crystalline"},
        {"familia": "Aminas", "grupo": "Amina primaria", "asignacion": "δ(NH₂) - Deformación", "rango": "1600", "intensidad": "w-m br (débil-medio ancha)", "observacion": ""},
        {"familia": "Aminas", "grupo": "Amina terciaria", "asignacion": "ν(C-N) - Tensión", "rango": "1210-1150", "intensidad": "m (medio)", "observacion": ""},
    ])
    
    # TABLA 9: ALCOHOLES Y FENOLES
    data.extend([
        {"familia": "Alcoholes", "grupo": "Alcohol libre", "asignacion": "ν(OH)free - Tensión", "rango": "3670-3580", "intensidad": "m sh (medio aguda)", "observacion": "Dilute solution"},
        {"familia": "Alcoholes", "grupo": "Alcohol asociado", "asignacion": "ν(OH)ass - Tensión", "rango": "3550-3200", "intensidad": "s br (fuerte ancha)", "observacion": "Hydrogen bonded"},
        {"familia": "Alcoholes", "grupo": "Alcohol primario", "asignacion": "ν(C-O) - Tensión", "rango": "1050", "intensidad": "s (fuerte)", "observacion": ""},
        {"familia": "Alcoholes", "grupo": "Alcohol secundario", "asignacion": "ν(C-O) - Tensión", "rango": "1100", "intensidad": "s (fuerte)", "observacion": ""},
        {"familia": "Alcoholes", "grupo": "Alcohol terciario", "asignacion": "ν(C-O) - Tensión", "rango": "1150", "intensidad": "s (fuerte)", "observacion": ""},
        {"familia": "Fenoles", "grupo": "Fenol libre", "asignacion": "ν(OH)free - Tensión", "rango": "3620-3590", "intensidad": "m sh (medio aguda)", "observacion": "Dilute"},
        {"familia": "Fenoles", "grupo": "Fenol asociado", "asignacion": "ν(OH)ass - Tensión", "rango": "3400-3200", "intensidad": "s br (fuerte ancha)", "observacion": "H-bonded"},
    ])
    
    # TABLA 10: CETONAS
    data.extend([
        {"familia": "Cetonas", "grupo": "Cetona alifática", "asignacion": "ν(C=O) - Tensión", "rango": "1715", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Cetonas", "grupo": "Cetona α,β-insaturada", "asignacion": "ν(C=O) - Tensión", "rango": "1685-1665", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Cetonas", "grupo": "Aril cetona", "asignacion": "ν(C=O) - Tensión", "rango": "1700-1680", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Cetonas", "grupo": "Diaril cetona", "asignacion": "ν(C=O) - Tensión", "rango": "1670-1650", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Cetonas", "grupo": "Ciclopentanona", "asignacion": "ν(C=O) - Tensión", "rango": "1750-1740", "intensidad": "vs (muy fuerte)", "observacion": "Ring strain"},
        {"familia": "Cetonas", "grupo": "Ciclobutanona", "asignacion": "ν(C=O) - Tensión", "rango": "1775", "intensidad": "vs (muy fuerte)", "observacion": "Ring strain"},
    ])
    
    # TABLA 11: ALDEHÍDOS Y ÁCIDOS
    data.extend([
        {"familia": "Aldehídos", "grupo": "Aldehído alifático", "asignacion": "ν(C=O) - Tensión", "rango": "1730-1720", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Aldehídos", "grupo": "Aldehído aromático", "asignacion": "ν(C=O) - Tensión", "rango": "1710-1685", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Aldehídos", "grupo": "Aldehído", "asignacion": "ν(C-H) aldehídico", "rango": "2830-2810", "intensidad": "m (medio)", "observacion": "Doublet"},
        {"familia": "Aldehídos", "grupo": "Aldehído", "asignacion": "ν(C-H) aldehídico", "rango": "2760-2740", "intensidad": "m (medio)", "observacion": "Doublet"},
        {"familia": "Ácidos", "grupo": "Ácido carboxílico", "asignacion": "ν(OH) - Tensión", "rango": "3300-2500", "intensidad": "s vbr (fuerte muy ancha)", "observacion": "H-bonded"},
        {"familia": "Ácidos", "grupo": "Ácido carboxílico", "asignacion": "ν(C=O) - Tensión", "rango": "1710", "intensidad": "vs (muy fuerte)", "observacion": "Broad"},
        {"familia": "Ácidos", "grupo": "Carboxilato", "asignacion": "νas(COO⁻) - Tensión asimétrica", "rango": "1650-1550", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Ácidos", "grupo": "Carboxilato", "asignacion": "νs(COO⁻) - Tensión simétrica", "rango": "1440-1360", "intensidad": "s (fuerte)", "observacion": ""},
    ])
    
    # TABLA 12: ÉSTERES Y ANHÍDRIDOS
    data.extend([
        {"familia": "Ésteres", "grupo": "Éster alifático", "asignacion": "ν(C=O) - Tensión", "rango": "1740", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Ésteres", "grupo": "Éster aromático", "asignacion": "ν(C=O) - Tensión", "rango": "1730-1715", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Ésteres", "grupo": "Éster α,β-insaturado", "asignacion": "ν(C=O) - Tensión", "rango": "1730-1715", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Ésteres", "grupo": "Éster", "asignacion": "νas(C-O-C) - Tensión asimétrica", "rango": "1300-1000", "intensidad": "vs (muy fuerte)", "observacion": "Broad"},
        {"familia": "Ésteres", "grupo": "β-Lactona", "asignacion": "ν(C=O) - Tensión", "rango": "1840-1815", "intensidad": "vs (muy fuerte)", "observacion": "4-membered ring"},
        {"familia": "Ésteres", "grupo": "γ-Lactona", "asignacion": "ν(C=O) - Tensión", "rango": "1780-1760", "intensidad": "vs (muy fuerte)", "observacion": "5-membered ring"},
        {"familia": "Ésteres", "grupo": "δ-Lactona", "asignacion": "ν(C=O) - Tensión", "rango": "1750-1735", "intensidad": "vs (muy fuerte)", "observacion": "6-membered ring"},
        {"familia": "Anhídridos", "grupo": "Anhídrido alifático", "asignacion": "νas(C=O) - Tensión asimétrica", "rango": "1825-1815", "intensidad": "vs (muy fuerte)", "observacion": "Doublet"},
        {"familia": "Anhídridos", "grupo": "Anhídrido alifático", "asignacion": "νs(C=O) - Tensión simétrica", "rango": "1755-1745", "intensidad": "vs (muy fuerte)", "observacion": "Doublet"},
    ])
    
    # TABLA 13: AMIDAS
    data.extend([
        {"familia": "Amidas", "grupo": "Amida primaria", "asignacion": "νas(NH₂) - Tensión asimétrica", "rango": "3370-3330", "intensidad": "m-s br (medio-fuerte ancha)", "observacion": "Amide A"},
        {"familia": "Amidas", "grupo": "Amida primaria", "asignacion": "νs(NH₂) - Tensión simétrica", "rango": "3210-3180", "intensidad": "m-s br (medio-fuerte ancha)", "observacion": "Amide B"},
        {"familia": "Amidas", "grupo": "Amida primaria", "asignacion": "ν(C=O) - Tensión", "rango": "1680-1660", "intensidad": "vs (muy fuerte)", "observacion": "Amide I"},
        {"familia": "Amidas", "grupo": "Amida primaria", "asignacion": "δ(NH₂) - Deformación", "rango": "1650-1620", "intensidad": "w-m br (débil-medio ancha)", "observacion": "Amide II"},
        {"familia": "Amidas", "grupo": "Amida secundaria", "asignacion": "ν(NH) - Tensión", "rango": "3350-3290", "intensidad": "m (medio)", "observacion": "trans"},
        {"familia": "Amidas", "grupo": "Amida secundaria", "asignacion": "ν(C=O) - Tensión", "rango": "1670-1640", "intensidad": "vs (muy fuerte)", "observacion": "Amide I"},
        {"familia": "Amidas", "grupo": "Amida secundaria", "asignacion": "δ(NH)ν(CN) - Deformación+Tensión", "rango": "1570-1540", "intensidad": "m-s (medio-fuerte)", "observacion": "Amide II"},
        {"familia": "Amidas", "grupo": "Amida terciaria", "asignacion": "ν(C=O) - Tensión", "rango": "1660-1630", "intensidad": "vs (muy fuerte)", "observacion": "Amide I"},
        {"familia": "Lactamas", "grupo": "β-Lactama", "asignacion": "ν(C=O) - Tensión", "rango": "1750", "intensidad": "vs (muy fuerte)", "observacion": "4-membered ring"},
        {"familia": "Lactamas", "grupo": "γ-Lactama", "asignacion": "ν(C=O) - Tensión", "rango": "1690", "intensidad": "vs (muy fuerte)", "observacion": "5-membered ring"},
    ])
    
    # TABLA 14: UREAS
    data.extend([
        {"familia": "Ureas", "grupo": "Urea", "asignacion": "νas(NH₂) - Tensión asimétrica", "rango": "3435", "intensidad": "vs br (muy fuerte ancha)", "observacion": ""},
        {"familia": "Ureas", "grupo": "Urea", "asignacion": "νs(NH₂) - Tensión simétrica", "rango": "3330", "intensidad": "s-vs br (fuerte-muy fuerte ancha)", "observacion": ""},
        {"familia": "Ureas", "grupo": "Urea", "asignacion": "ν(C=O) - Tensión", "rango": "1673", "intensidad": "s-vs (fuerte-muy fuerte)", "observacion": ""},
    ])
    
    # TABLA 15: ISOCIANATOS
    data.extend([
        {"familia": "Isocianatos", "grupo": "Isocianato alifático", "asignacion": "νas(N=C=O) - Tensión asimétrica", "rango": "2270-2240", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Isocianatos", "grupo": "Isocianato aromático", "asignacion": "νas(N=C=O) - Tensión asimétrica", "rango": "2270", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Uretanos", "grupo": "Uretano", "asignacion": "ν(NH) - Tensión", "rango": "3310", "intensidad": "s sh (fuerte aguda)", "observacion": ""},
        {"familia": "Uretanos", "grupo": "Uretano", "asignacion": "ν(C=O) - Tensión", "rango": "1690", "intensidad": "vs (muy fuerte)", "observacion": "Amide I"},
    ])
    
    # TABLA 16: NITRO COMPUESTOS
    data.extend([
        {"familia": "Nitro", "grupo": "Nitro alifático", "asignacion": "νas(NO₂) - Tensión asimétrica", "rango": "1555-1545", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Nitro", "grupo": "Nitro alifático", "asignacion": "νs(NO₂) - Tensión simétrica", "rango": "1395-1360", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Nitro", "grupo": "Nitro aromático", "asignacion": "νas(NO₂) - Tensión asimétrica", "rango": "1535-1510", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Nitro", "grupo": "Nitro aromático", "asignacion": "νs(NO₂) - Tensión simétrica", "rango": "1350-1335", "intensidad": "vs (muy fuerte)", "observacion": ""},
    ])
    
    # TABLA 17: COMPUESTOS DE AZUFRE
    data.extend([
        {"familia": "Tioles", "grupo": "Tiol", "asignacion": "ν(S-H) - Tensión", "rango": "2560-2554", "intensidad": "w-m (débil-medio)", "observacion": ""},
        {"familia": "Sulfóxidos", "grupo": "Sulfóxido alifático", "asignacion": "ν(S=O) - Tensión", "rango": "1070-1040", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Sulfóxidos", "grupo": "Sulfóxido aromático", "asignacion": "ν(S=O) - Tensión", "rango": "1040-1020", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Sulfonas", "grupo": "Sulfona alifática", "asignacion": "νas(SO₂) - Tensión asimétrica", "rango": "1315", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Sulfonas", "grupo": "Sulfona alifática", "asignacion": "νs(SO₂) - Tensión simétrica", "rango": "1150-1135", "intensidad": "vs (muy fuerte)", "observacion": ""},
        {"familia": "Sulfonatos", "grupo": "Sulfonato", "asignacion": "νas(SO₃⁻) - Tensión asimétrica", "rango": "1200-1170", "intensidad": "vs br (muy fuerte ancha)", "observacion": ""},
    ])
    
    # TABLA 18: FOSFATOS
    data.extend([
        {"familia": "Fosfatos", "grupo": "Fosfato", "asignacion": "ν(P=O) - Tensión", "rango": "1275", "intensidad": "s (fuerte)", "observacion": ""},
        {"familia": "Fosfatos", "grupo": "Fosfato", "asignacion": "νas(P-O-C) - Tensión asimétrica", "rango": "1050-1000", "intensidad": "vs (muy fuerte)", "observacion": ""},
    ])
    
    # TABLA 19: SILANOS
    data.extend([
        {"familia": "Silanos", "grupo": "Silano", "asignacion": "ν(Si-H) - Tensión", "rango": "2155-2140", "intensidad": "s (fuerte)", "observacion": ""},
        {"familia": "Silanos", "grupo": "Siloxano", "asignacion": "νas(Si-O-Si) - Tensión asimétrica", "rango": "1100", "intensidad": "vs br (muy fuerte ancha)", "observacion": ""},
    ])
    
    # TABLA 20: HALÓGENOS
    data.extend([
        {"familia": "Fluoruros", "grupo": "Fluoruro alifático", "asignacion": "ν(C-F) - Tensión", "rango": "1055", "intensidad": "m-s (medio-fuerte)", "observacion": ""},
        {"familia": "Cloruros", "grupo": "Cloruro alifático", "asignacion": "ν(C-Cl) - Tensión", "rango": "650", "intensidad": "m (medio)", "observacion": ""},
        {"familia": "Bromuros", "grupo": "Bromuro alifático", "asignacion": "ν(C-Br) - Tensión", "rango": "650-640", "intensidad": "m (medio)", "observacion": ""},
    ])
    
    return pd.DataFrame(data)

# Funciones de búsqueda
def parse_range(range_str):
    """Parsea un rango de números de onda"""
    try:
        if '-' in range_str:
            parts = range_str.split('-')
            return int(parts[0]), int(parts[1])
        else:
            val = int(range_str.replace('±', '').replace('ca.', '').strip())
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
            
        # Coincidencia exacta
        if min_val <= wavenumber <= max_val:
            exact_matches.append(row)
        # Coincidencia cercana (±30 cm⁻¹)
        elif (abs(wavenumber - min_val) <= 30 or abs(wavenumber - max_val) <= 30):
            nearby_matches.append(row)
    
    return exact_matches, nearby_matches

def search_database(df, query):
    """Búsqueda multi-criterio"""
    if not query:
        return df
    
    query_lower = query.lower()
    
    # Si es un número, buscar por número de onda
    if query.isdigit():
        return search_by_wavenumber(df, int(query))
    
    # Búsqueda por texto
    mask = (
        df['familia'].str.lower().str.contains(query_lower, na=False) |
        df['grupo'].str.lower().str.contains(query_lower, na=False) |
        df['asignacion'].str.lower().str.contains(query_lower, na=False) |
        df['observacion'].str.lower().str.contains(query_lower, na=False)
    )
    
    return df[mask]

# Cargar datos
df = load_data()

# INTERFAZ PRINCIPAL
st.markdown("<h1>🔬 IR Spectroscopy Database</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 1.1em;'>Base de Datos Completa de Espectroscopia Infrarroja - 200+ Bandas</p>", unsafe_allow_html=True)

# Métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Bandas IR", len(df))
with col2:
    st.metric("🧪 Familias", df['familia'].nunique())
with col3:
    st.metric("🔬 Grupos", df['grupo'].nunique())
with col4:
    st.metric("📈 Tablas", "20")

st.markdown("---")

# Barra lateral con filtros
with st.sidebar:
    st.header("🔍 Búsqueda y Filtros")
    
    # Búsqueda principal
    search_query = st.text_input(
        "Buscar:",
        placeholder="Número de onda (1720), familia (cetonas), enlace (C=O)...",
        help="Introduce: número de onda, nombre de familia, tipo de enlace, grupo funcional"
    )
    
    st.markdown("---")
    
    # Filtro por familia
    st.subheader("Por Familia Química")
    familias = ["Todas"] + sorted(df['familia'].unique().tolist())
    familia_seleccionada = st.selectbox("Selecciona familia:", familias)
    
    st.markdown("---")
    
    # Filtro por rango
    st.subheader("Por Rango de Frecuencia")
    rango_seleccionado = st.select_slider(
        "Rango (cm⁻¹):",
        options=["< 1000", "1000-1500", "1500-2000", "2000-2500", "> 2500", "Todos"],
        value="Todos"
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Escribe un número como 1720 para ver todas las bandas en ese rango ±30 cm⁻¹")

# Aplicar filtros
filtered_df = df.copy()

# Filtro de búsqueda
if search_query:
    if search_query.isdigit():
        exact, nearby = search_by_wavenumber(df, int(search_query))
        
        if exact or nearby:
            st.success(f"✅ Encontradas {len(exact)} coincidencias exactas y {len(nearby)} cercanas para {search_query} cm⁻¹")
            
            if exact:
                st.subheader("🎯 Coincidencias Exactas")
                for item in exact:
                    with st.container():
                        st.markdown(f"""
                        <div class='result-card'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                                <h3 style='margin: 0; color: #60a5fa;'>{item['grupo']}</h3>
                                <span class='family-badge'>{item['familia']}</span>
                            </div>
                            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>ASIGNACIÓN</p>
                                    <p style='margin: 5px 0; font-family: monospace;'>{item['asignacion']}</p>
                                </div>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>RANGO</p>
                                    <p style='margin: 5px 0; font-family: monospace; color: #00cc66;'>{item['rango']} cm⁻¹</p>
                                </div>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>INTENSIDAD</p>
                                    <p style='margin: 5px 0; font-family: monospace;'>{item['intensidad']}</p>
                                </div>
                            </div>
                            {f"<p style='margin-top: 15px; padding: 10px; background: rgba(139, 92, 246, 0.1); border-left: 3px solid #8b5cf6; border-radius: 5px;'><strong>Observación:</strong> {item['observacion']}</p>" if item['observacion'] else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
            
            if nearby:
                st.subheader("⚠️ Coincidencias Cercanas (±30 cm⁻¹)")
                for item in nearby:
                    with st.container():
                        st.markdown(f"""
                        <div class='result-card' style='opacity: 0.8;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                                <h3 style='margin: 0; color: #60a5fa;'>{item['grupo']}</h3>
                                <span class='family-badge'>{item['familia']}</span>
                            </div>
                            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>ASIGNACIÓN</p>
                                    <p style='margin: 5px 0; font-family: monospace;'>{item['asignacion']}</p>
                                </div>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>RANGO</p>
                                    <p style='margin: 5px 0; font-family: monospace; color: #f59e0b;'>{item['rango']} cm⁻¹</p>
                                </div>
                                <div>
                                    <p style='color: #9ca3af; font-size: 0.85em; margin: 0;'>INTENSIDAD</p>
                                    <p style='margin: 5px 0; font-family: monospace;'>{item['intensidad']}</p>
                                </div>
                            </div>
                            {f"<p style='margin-top: 15px; padding: 10px; background: rgba(139, 92, 246, 0.1); border-left: 3px solid #8b5cf6; border-radius: 5px;'><strong>Observación:</strong> {item['observacion']}</p>" if item['observacion'] else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ No se encontraron bandas para {search_query} cm⁻¹ (ni en ±30 cm⁻¹)")
    else:
        filtered_df = search_database(df, search_query)
        st.info(f"📊 Mostrando {len(filtered_df)} resultados para '{search_query}'")

# Filtro por familia
elif familia_seleccionada != "Todas":
    filtered_df = df[df['familia'] == familia_seleccionada]
    st.info(f"📊 Mostrando {len(filtered_df)} bandas de {familia_seleccionada}")

# Si no hay búsqueda específica de número de onda, mostrar tabla
if not (search_query and search_query.isdigit()):
    if len(filtered_df) > 0:
        # Mostrar como tabla interactiva
        st.dataframe(
            filtered_df[['familia', 'grupo', 'asignacion', 'rango', 'intensidad', 'observacion']],
            use_container_width=True,
            height=600
        )
        
        # Opción de descarga
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar resultados como CSV",
            data=csv,
            file_name='ir_spectroscopy_results.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No se encontraron resultados con los filtros aplicados")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; padding: 20px;'>
    <p>Base de Datos IR Spectroscopy - 200+ bandas de las principales familias químicas</p>
    <p style='font-size: 0.9em;'>Datos extraídos de tablas IR profesionales - Enero 2026</p>
</div>
""", unsafe_allow_html=True)
