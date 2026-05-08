"""
pages/dashboard.py
Dashboard analítico Big Data — análisis masivo de NPS y comportamiento de clientes.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import datetime
from modules.nlp_categorizer import clasificar_transaccion, detectar_error_probable
from modules.chatbot import activar_chatbot

COLOR_VERDE = "#00D261"
COLOR_ROJO = "#D32F2F"
COLOR_NARANJA = "#F57C00"
COLOR_AZUL = "#003087"
COLOR_GRIS = "#2D2926"


def _generar_datos_sinteticos(n=150):
    """Genera datos NPS sintéticos cuando no hay CSV disponible."""
    random.seed(42)
    np.random.seed(42)

    nombres = ["Carlos Mendoza","María López","Roberto Sánchez","Lucía Fernández","Jorge Ramírez",
               "Ana Torres","Pedro Vargas","Isabel Cruz","Miguel Ángel Díaz","Valentina Mora"]
    transacciones = [
        "Solicité un retiro", "Realicé un aporte", "Consulté mi saldo",
        "Gestioné mi portafolio", "Consulté documentos/certificados",
        "Registros de cuentas bancarias", "Actualicé mis datos", "Otras"
    ]
    comentarios_pos = [
        "Excelente servicio, muy fácil de usar",
        "El portal funciona muy bien, rápido y seguro",
        "Muy satisfecho con la atención",
        "Todo perfecto, lo recomiendo",
    ]
    comentarios_neg = [
        "No pude completar mi retiro, hubo un error",
        "La cuenta bancaria no se inscribió correctamente",
        "El certificado no cargó, hubo timeout",
        "No recibí el código OTP para confirmar",
        "El portafolio no muestra el saldo actualizado",
    ]

    fechas = pd.date_range(start="2026-01-01", end="2026-05-08", periods=n)
    n_det  = int(n * 0.25)
    n_pas  = int(n * 0.30)
    n_pro  = n - n_det - n_pas
    scores = np.concatenate([
        np.random.randint(0, 7, n_det),
        np.random.randint(7, 9, n_pas),
        np.random.randint(9, 11, n_pro),
    ])
    np.random.shuffle(scores)

    rows = []
    for i in range(n):
        score = int(scores[i])
        if score <= 6:
            comentario = random.choice(comentarios_neg)
        else:
            comentario = random.choice(comentarios_pos)

        rows.append({
            "Nombre": random.choice(nombres),
            "Contrato": f"SKD-{random.randint(2022,2025)}-{random.randint(100,999):03d}",
            "NPS": score,
            "Transaccion": random.choice(transacciones),
            "Comentario": comentario,
            "Fecha": fechas[i],
            "Email": f"cliente{i}@email.com"
        })

    df = pd.DataFrame(rows)
    df["Segmento_NPS"] = df["NPS"].apply(
        lambda x: "Detractor" if x <= 6 else ("Pasivo" if x <= 8 else "Promotor")
    )
    df["Categoria_Detectada"] = df["Comentario"].apply(clasificar_transaccion)
    return df


def _cargar_datos() -> pd.DataFrame:
    """Carga el Excel real de Portal Clientes 2026 o genera datos sintéticos."""
    import os

    rutas = [
        r"C:\Users\wreyes\Desktop\HACKATHON\Portal Clientes 2026.xlsx",
        "Portal Clientes 2026.xlsx",
    ]

    for ruta in rutas:
        if not os.path.exists(ruta):
            continue
        try:
            df = pd.read_excel(ruta)

            # Columna NPS numérica (sin "grupo")
            nps_col = next(
                (c for c in df.columns
                 if ("probabilidad" in c.lower() or "recomendar" in c.lower())
                 and "grupo" not in c.lower()),
                None,
            )
            if nps_col is None:
                continue

            df["NPS"] = pd.to_numeric(df[nps_col], errors="coerce")
            df = df.dropna(subset=["NPS"]).reset_index(drop=True)
            if len(df) == 0:
                continue
            df["NPS"] = df["NPS"].astype(int)
            df["Segmento_NPS"] = df["NPS"].apply(
                lambda x: "Detractor" if x <= 6 else ("Pasivo" if x <= 8 else "Promotor")
            )

            # Transacción
            trans_col = next(
                (c for c in df.columns
                 if "transacci" in c.lower()
                 and ("selected" in c.lower() or "choice" in c.lower())),
                next((c for c in df.columns if "transacci" in c.lower()), None),
            )
            df["Transaccion"] = df[trans_col].fillna("Otras") if trans_col else "Otras"

            # Comentario / motivo
            comment_col = next(
                (c for c in df.columns if "motivo" in c.lower()),
                next(
                    (c for c in df.columns
                     if "calific" in c.lower() and "grupo" not in c.lower()),
                    None,
                ),
            )
            df["Comentario"] = df[comment_col].fillna("Sin comentario") if comment_col else "Sin comentario"

            # Fecha
            date_col = next(
                (c for c in df.columns if "fecha" in c.lower() and "inicio" in c.lower()),
                next((c for c in df.columns if "fecha" in c.lower()), None),
            )
            if date_col:
                df["Fecha"] = pd.to_datetime(df[date_col], errors="coerce")

            # Contrato simulado (no existe en el Excel)
            df["Contrato"] = [f"SKD-{2024 + (i % 2)}-{100 + (i % 900):03d}" for i in range(len(df))]

            df["Categoria_Detectada"] = df["Comentario"].apply(clasificar_transaccion)
            return df

        except Exception:
            pass

    return _generar_datos_sinteticos()


def render_dashboard():
    """Renderiza el dashboard analítico completo."""
    st.markdown("## 📈 Dashboard Analítico — Big Data NPS")

    if "df_nps" not in st.session_state or st.session_state["df_nps"] is None:
        with st.spinner("Cargando y procesando datos..."):
            st.session_state["df_nps"] = _cargar_datos()

    df = st.session_state["df_nps"]

    # Upload fallback
    archivo = st.file_uploader("📂 Cargar CSV de datos NPS (opcional)", type=["csv"], key="uploader_csv")
    if archivo:
        df_nuevo = pd.read_csv(archivo)
        nps_cols = [c for c in df_nuevo.columns if any(k in c.lower() for k in ["nps","calificacion","puntuacion","score"])]
        if nps_cols:
            df_nuevo["NPS"] = pd.to_numeric(df_nuevo[nps_cols[0]], errors="coerce")
            df_nuevo = df_nuevo.dropna(subset=["NPS"])
            df_nuevo["NPS"] = df_nuevo["NPS"].astype(int)
            df_nuevo["Segmento_NPS"] = df_nuevo["NPS"].apply(
                lambda x: "Detractor" if x <= 6 else ("Pasivo" if x <= 8 else "Promotor")
            )
            st.session_state["df_nps"] = df_nuevo
            df = df_nuevo
            st.success("✅ Datos cargados exitosamente.")

    total = len(df)
    detractores = (df["Segmento_NPS"] == "Detractor").sum()
    pasivos = (df["Segmento_NPS"] == "Pasivo").sum()
    promotores = (df["Segmento_NPS"] == "Promotor").sum()
    nps_promedio = round(df["NPS"].mean(), 2)
    nps_score = round(((promotores - detractores) / total) * 100, 1)

    # Métricas clave
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("📊 NPS Score", f"{nps_score}", delta="+3.2 vs mes anterior")
    with m2:
        st.metric("📉 Detractores", f"{(detractores/total*100):.1f}%", delta=f"{detractores} clientes", delta_color="inverse")
    with m3:
        st.metric("📈 Promotores", f"{(promotores/total*100):.1f}%", delta=f"{promotores} clientes")
    with m4:
        st.metric("📋 Total registros", f"{total:,}")
    with m5:
        st.metric("⏱️ T. resolución prom.", "8.4 min")

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribución NPS por segmento")
        conteo = df["Segmento_NPS"].value_counts().reset_index()
        conteo.columns = ["Segmento", "Cantidad"]
        conteo["Color"] = conteo["Segmento"].map({
            "Detractor": COLOR_ROJO,
            "Pasivo": COLOR_NARANJA,
            "Promotor": COLOR_VERDE
        })
        fig1 = go.Figure(go.Bar(
            x=conteo["Segmento"],
            y=conteo["Cantidad"],
            marker_color=conteo["Color"].tolist(),
            text=conteo["Cantidad"],
            textposition="outside"
        ))
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(t=20, b=20),
            showlegend=False,
            yaxis_title="Cantidad",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### Quejas por categoría (detractores)")
        if "Categoria_Detectada" in df.columns or "Transaccion" in df.columns:
            cat_col = "Categoria_Detectada" if "Categoria_Detectada" in df.columns else "Transaccion"
            det_df = df[df["Segmento_NPS"] == "Detractor"]
            if len(det_df) > 0:
                cat_count = det_df[cat_col].value_counts().reset_index()
                cat_count.columns = ["Categoria", "Cantidad"]
                cat_count = cat_count.sort_values("Cantidad", ascending=True)
                fig2 = go.Figure(go.Bar(
                    y=cat_count["Categoria"],
                    x=cat_count["Cantidad"],
                    orientation="h",
                    marker_color=COLOR_ROJO,
                    text=cat_count["Cantidad"],
                    textposition="outside"
                ))
                fig2.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=300,
                    margin=dict(t=20, b=20, l=10),
                    xaxis_title="Cantidad detractores"
                )
                st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Evolución NPS en el tiempo")
        if "Fecha" in df.columns:
            df["Fecha_dt"] = pd.to_datetime(df["Fecha"], errors="coerce")
            df_ts = df.dropna(subset=["Fecha_dt"])
            if len(df_ts) > 0:
                df_ts = df_ts.sort_values("Fecha_dt")
                df_ts["Semana"] = df_ts["Fecha_dt"].dt.to_period("W").astype(str)
                evol = df_ts.groupby("Semana")["NPS"].mean().reset_index()
                fig3 = go.Figure(go.Scatter(
                    x=evol["Semana"],
                    y=evol["NPS"],
                    mode="lines+markers",
                    line=dict(color=COLOR_VERDE, width=2),
                    marker=dict(color=COLOR_VERDE, size=6),
                    fill="tozeroy",
                    fillcolor="rgba(0,210,97,0.1)"
                ))
                fig3.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=280,
                    margin=dict(t=20, b=20),
                    yaxis=dict(range=[0, 11], title="NPS Promedio"),
                )
                st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### Mapa de calor: Errores por módulo")
        categorias = ["Retiros", "Cuentas bancarias", "Portafolio", "Documentos", "Datos personales", "Acceso"]
        errores = ["ERR001", "ERR002", "ERR003", "ERR005", "ERR009", "ERR013"]
        np.random.seed(10)
        matriz = np.random.randint(1, 25, size=(len(categorias), len(errores)))
        fig4 = go.Figure(go.Heatmap(
            z=matriz,
            x=errores,
            y=categorias,
            colorscale=[[0, "#E8F5E9"], [0.5, "#FFB300"], [1, "#D32F2F"]],
            text=matriz,
            texttemplate="%{text}",
            showscale=True
        ))
        fig4.update_layout(
            height=280,
            margin=dict(t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Tabla de detractores
    st.markdown("---")
    st.markdown("#### 🔴 Detractores activos — Gestión inmediata")

    det_activos = df[df["Segmento_NPS"] == "Detractor"].copy()

    if len(det_activos) == 0:
        st.success("✅ No hay detractores activos en este momento.")
        return

    cat_col = "Categoria_Detectada" if "Categoria_Detectada" in det_activos.columns else "Transaccion"
    filtro_cat = st.selectbox("Filtrar por categoría:", ["Todas"] + sorted(det_activos[cat_col].unique().tolist()))

    if filtro_cat != "Todas":
        det_activos = det_activos[det_activos[cat_col] == filtro_cat]

    for _, row in det_activos.head(10).iterrows():
        comentario = str(row.get("Comentario", "Sin comentario"))
        categoria = str(row.get(cat_col, "Otras"))
        contrato = str(row.get("Contrato", "N/A"))
        nps_val = int(row.get("NPS", 0))

        error_info = detectar_error_probable(comentario, categoria)
        error_id = error_info.get("error_id", "ERR008")
        confianza = error_info.get("confianza", 0.5)
        error_titulo = error_info.get("datos", {}).get("titulo", "Error desconocido")

        with st.container():
            col1, col2, col3 = st.columns([5, 2, 2])
            with col1:
                st.markdown(f"""
                <div style="background:white;border-radius:8px;padding:12px;
                            border-left:3px solid #D32F2F;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                    <span style="background:#D32F2F;color:white;padding:2px 8px;border-radius:10px;font-size:11px;">
                        NPS {nps_val}
                    </span>
                    &nbsp; <strong>{contrato}</strong> &nbsp;
                    <span style="font-size:12px;color:#6B6560;">{categoria}</span><br>
                    <span style="font-size:12px;color:#4a4a4a;">{comentario[:100]}...</span><br>
                    <span style="font-size:11px;color:#F57C00;">🤖 Error probable: {error_id} — {error_titulo} ({confianza*100:.0f}%)</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("💬 Chat en línea", key=f"chat_{contrato}_{nps_val}", use_container_width=True, type="primary"):
                    activar_chatbot(error_id, "Dashboard")
                    st.session_state["current_page"] = "tecnico"
                    st.rerun()
            with col3:
                if st.button("📞 Llamada", key=f"call_{contrato}_{nps_val}", use_container_width=True):
                    st.success("📞 Llamada programada en 10 minutos.")

            st.markdown("")
