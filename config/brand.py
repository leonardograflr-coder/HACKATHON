"""
config/brand.py
Identidad visual Skandia Colombia — logo SVG, colores y CSS global moderno.
"""

COLOR_VERDE       = "#00D261"
COLOR_VERDE_DARK  = "#00A84F"
COLOR_VERDE_LIGHT = "#E8F5E9"
COLOR_FONDO       = "#F0EEE9"
COLOR_TEXTO       = "#2D2926"
COLOR_AZUL        = "#003087"
COLOR_ROJO        = "#D32F2F"
COLOR_ROJO_LIGHT  = "#FFEBEE"
COLOR_GRIS        = "#6B6560"

# ── Logo SVG Skandia Colombia ────────────────────────────────────────────────
SKANDIA_LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="22" cy="22" r="22" fill="#00D261"/>
  <!-- Hoja principal -->
  <path d="M22 8 C22 8 10 14 10 24 C10 31 15.5 36 22 36 C28.5 36 34 31 34 24 C34 14 22 8 22 8 Z"
        fill="white" opacity="0.95"/>
  <!-- Nervadura central -->
  <path d="M22 12 C22 12 16 17 16 24 C16 28.5 18.5 32 22 34"
        stroke="#00D261" stroke-width="2" stroke-linecap="round" fill="none"/>
  <!-- Nervaduras secundarias -->
  <path d="M18 22 C20 20 24 19 27 18" stroke="#00D261" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M17 26 C19 24 23 23 26 22" stroke="#00D261" stroke-width="1.2" stroke-linecap="round"/>
</svg>
"""

def _make_logo_html(height: int = 40) -> str:
    """Carga el logo PNG real de Skandia en base64; si no existe, usa el SVG de respaldo."""
    import base64, os
    for path in [r"C:\Users\wreyes\Desktop\HACKATHON\skandia.png", "skandia.png"]:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return (
                    '<div style="display:inline-flex;align-items:center;gap:10px;">'
                    f'<img src="data:image/png;base64,{b64}" '
                    f'style="height:{height}px;width:auto;object-fit:contain;" alt="Skandia">'
                    "</div>"
                )
            except Exception:
                pass
    # SVG fallback — escala proporcional
    sw = int(height * 1.0)
    fs_brand = int(height * 0.50)
    fs_sub   = int(height * 0.25)
    return f"""<div style="display:inline-flex;align-items:center;gap:10px;">
  <svg width="{sw}" height="{sw}" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="22" cy="22" r="22" fill="#00D261"/>
    <path d="M22 8 C22 8 10 14 10 24 C10 31 15.5 36 22 36 C28.5 36 34 31 34 24 C34 14 22 8 22 8 Z"
          fill="white" opacity="0.95"/>
    <path d="M22 12 C22 12 16 17 16 24 C16 28.5 18.5 32 22 34"
          stroke="#00D261" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M18 22 C20 20 24 19 27 18" stroke="#00D261" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M17 26 C19 24 23 23 26 22" stroke="#00D261" stroke-width="1.2" stroke-linecap="round"/>
  </svg>
  <div style="line-height:1.15;">
    <div style="font-size:{fs_brand}px;font-weight:800;color:#2D2926;letter-spacing:-0.03em;">skandia</div>
    <div style="font-size:{fs_sub}px;font-weight:600;color:#6B6560;letter-spacing:0.12em;text-transform:uppercase;">colombia</div>
  </div>
</div>"""


SKANDIA_LOGO_HTML       = _make_logo_html(40)
SKANDIA_LOGO_HTML_LARGE = _make_logo_html(80)

# ── CSS Global ───────────────────────────────────────────────────────────────
SKANDIA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

.stApp { background-color: #F4F2EE; }

/* ── Ocultar chrome Streamlit ── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #EBEBEB;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Métricas ── */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    border: 1px solid #F0F0F0;
}
[data-testid="metric-container"] label { color: #6B6560 !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 22px !important; font-weight: 700 !important; color: #2D2926 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 8px !important;
    border: 1.5px solid #E8E8E8 !important;
    font-size: 14px !important;
    height: 44px !important;
    padding: 0 12px !important;
    background: #FAFAFA !important;
    transition: border 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00D261 !important;
    box-shadow: 0 0 0 3px rgba(0,210,97,0.12) !important;
    background: white !important;
}
.stTextArea textarea {
    border-radius: 8px !important; border: 1.5px solid #E8E8E8 !important;
    background: #FAFAFA !important;
}
.stTextArea textarea:focus {
    border-color: #00D261 !important; box-shadow: 0 0 0 3px rgba(0,210,97,0.12) !important;
}
.stSelectbox > div > div {
    border-radius: 8px !important; border: 1.5px solid #E8E8E8 !important;
    background: #FAFAFA !important;
}

/* ══════════════════════════════════════════
   BOTONES — altura y estilo 100% uniformes
   ══════════════════════════════════════════ */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 0 18px !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.16s cubic-bezier(.4,0,.2,1) !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    white-space: nowrap !important;
    line-height: 1 !important;
}

/* Primario */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #00D261 !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 2px 10px rgba(0,210,97,0.28) !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #00B554 !important;
    box-shadow: 0 4px 16px rgba(0,210,97,0.38) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 4px rgba(0,210,97,0.2) !important;
}

/* Secundario */
.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]),
.stFormSubmitButton > button:not([kind="primary"]),
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #00D261 !important;
    border: 1.5px solid #00D261 !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover,
.stFormSubmitButton > button:not([kind="primary"]):hover {
    background: #E8F5E9 !important;
    transform: translateY(-1px) !important;
}

/* Deshabilitado */
.stButton > button:disabled {
    background: #F0F0F0 !important; color: #BDBDBD !important;
    border: 1.5px solid #E8E8E8 !important; box-shadow: none !important;
    cursor: not-allowed !important; transform: none !important;
}

/* ── Alertas ── */
.sk-alert-critical {
    background: #FFF0F0;
    border-left: 4px solid #D32F2F;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 12px 0;
    font-size: 14px;
}

/* ── Warning banner ── */
.sk-warning-banner {
    background: #FFFBEB;
    border: 1px solid #F59E0B;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    margin-bottom: 14px;
}

/* ── Blink detractores ── */
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:.35; }
}
.blink-alert { animation: blink 1.5s ease-in-out infinite; }

/* ── Panel decorativo izquierdo ── */
.sk-left-panel {
    background: linear-gradient(155deg, #E8F5E9 0%, #D4F0DC 100%);
    border-radius: 14px;
    padding: 36px 20px;
    min-height: 440px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { font-weight: 600 !important; font-size: 14px !important; }
.stTabs [aria-selected="true"] { color: #00D261 !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #00D261 !important; }

/* ── Expander ── */
.streamlit-expanderHeader { font-weight: 600 !important; font-size: 13px !important; }

/* ── Slider ── */
[data-baseweb="slider"] [data-testid="stThumbValue"] { color: #00D261 !important; }
.stSlider [role="slider"] { background: #00D261 !important; }

/* ── Radio ── */
.stRadio > div { gap: 8px !important; }

/* ── HR ── */
hr { border: none !important; border-top: 1px solid #EBEBEB !important; margin: 14px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F4F2EE; }
::-webkit-scrollbar-thumb { background: #C8C8C8; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #A0A0A0; }

/* ── Chat panel column ── */
.chat-col-active {
    background: white !important;
    border-radius: 16px 16px 0 0 !important;
    box-shadow: -2px 0 20px rgba(0,0,0,0.08) !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    /* Stack columns */
    [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }
    /* Reduce metric font sizes */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 16px !important;
    }
    /* Touch-friendly buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        height: auto !important;
        min-height: 48px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        white-space: normal !important;
        line-height: 1.3 !important;
    }
    /* Full-width inputs on mobile */
    .stTextInput, .stSelectbox, .stNumberInput {
        width: 100% !important;
    }
    /* Reduce header nav padding */
    [data-testid="stAppViewContainer"] > section > div > div > div {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
    /* Card paddings */
    div[style*="border-radius:16px"][style*="padding:40px"] {
        padding: 20px 16px !important;
    }
}

@media (max-width: 480px) {
    /* Smaller headings on phones */
    h3 { font-size: 18px !important; }
    h4 { font-size: 15px !important; }
    p, span, div { font-size: 13px; }
    /* Metric value even smaller */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 14px !important;
    }
}
</style>
"""


def apply_styles():
    import streamlit as st
    st.markdown(SKANDIA_CSS, unsafe_allow_html=True)
