"""
pages/control_tower.py
Panel de Control CX — alertas en tiempo real, gestión de detractores y casos activos.
"""

import streamlit as st
import datetime
import random
from data.clientes_demo import CLIENTES_DEMO, get_fp_by_id
from data.base_conocimiento import BASE_CONOCIMIENTO
from modules.nlp_categorizer import detectar_error_probable
from modules.chatbot import activar_chatbot
from modules.report_generator import generar_informe_tecnico, registrar_accion_log
from modules.notificaciones import render_correos_simulados


def _generar_casos_demo():
    """Genera casos demo para el Control Tower."""
    casos = [
        {
            "id": "CASO-001",
            "cliente": CLIENTES_DEMO[0],
            "nps": 4,
            "categoria": "Solicité un retiro",
            "comentario": "No pude completar mi retiro, el sistema dice que mi cuenta bancaria está activa en otro contrato",
            "error_id": "ERR001",
            "estado": "Abierto",
            "hora": "09:15",
            "prioridad": "ALTA"
        },
        {
            "id": "CASO-002",
            "cliente": CLIENTES_DEMO[1],
            "nps": 2,
            "categoria": "Registros de cuentas bancarias",
            "comentario": "Intenté inscribir mi cuenta pero aparece un bloqueo SARLAFT, muy frustrante",
            "error_id": "ERR009",
            "estado": "En gestión",
            "hora": "09:42",
            "prioridad": "CRÍTICA"
        },
        {
            "id": "CASO-003",
            "cliente": CLIENTES_DEMO[2],
            "nps": 5,
            "categoria": "Gestioné mi portafolio",
            "comentario": "No puedo cambiar mi perfil de inversión, hay una firma electrónica pendiente que no puedo completar",
            "error_id": "ERR011",
            "estado": "Abierto",
            "hora": "10:05",
            "prioridad": "MEDIA"
        },
        {
            "id": "CASO-004",
            "cliente": CLIENTES_DEMO[3],
            "nps": 3,
            "categoria": "Consulté documentos/certificados",
            "comentario": "El certificado de aportes no carga, llevo 30 minutos intentando",
            "error_id": "ERR005",
            "estado": "Abierto",
            "hora": "10:28",
            "prioridad": "BAJA"
        },
        {
            "id": "CASO-005",
            "cliente": CLIENTES_DEMO[4],
            "nps": 1,
            "categoria": "Solicité un retiro",
            "comentario": "Mi retiro fue rechazado por fondos insuficientes pero tengo saldo suficiente",
            "error_id": "ERR002",
            "estado": "Escalado",
            "hora": "10:45",
            "prioridad": "ALTA"
        },
    ]
    return casos


def render_control_tower():
    """Renderiza el panel de control CX completo."""
    st.markdown("## 🎯 Control Tower CX — Gestión en tiempo real")

    if not st.session_state.get("casos_cx"):
        st.session_state["casos_cx"] = _generar_casos_demo()

    casos = st.session_state["casos_cx"]

    # Métricas en tiempo real
    abiertos = sum(1 for c in casos if c["estado"] == "Abierto")
    en_gestion = sum(1 for c in casos if c["estado"] == "En gestión")
    escalados = sum(1 for c in casos if c["estado"] == "Escalado")
    resueltos = sum(1 for c in casos if c["estado"] == "Resuelto")

    # Alerta global si hay detractores sin gestionar
    if abiertos > 0:
        st.markdown(f"""
        <div class='sk-alert-critical blink-alert'>
            🔴 <strong>ALERTA:</strong> Hay <strong>{abiertos}</strong> caso(s) de detractores sin atender.
            Tiempo máximo de primera respuesta: <strong>30 minutos</strong>
        </div>
        """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("🔴 Abiertos", abiertos)
    with m2:
        st.metric("🟡 En gestión", en_gestion)
    with m3:
        st.metric("🟠 Escalados", escalados)
    with m4:
        st.metric("✅ Resueltos hoy", resueltos)
    with m5:
        st.metric("⏱️ T. prom. 1ª resp.", "12 min")

    st.markdown("---")

    # Tabs por estado
    tab1, tab2, tab3 = st.tabs(["🔴 Casos activos", "🔄 En gestión / Escalados", "✅ Resueltos"])

    with tab1:
        casos_activos = [c for c in casos if c["estado"] == "Abierto"]
        if not casos_activos:
            st.success("✅ No hay casos abiertos en este momento.")
        for caso in casos_activos:
            _render_card_caso(caso, casos)

    with tab2:
        casos_proceso = [c for c in casos if c["estado"] in ["En gestión", "Escalado"]]
        if not casos_proceso:
            st.info("No hay casos en proceso.")
        for caso in casos_proceso:
            _render_card_caso(caso, casos, modo_proceso=True)

    with tab3:
        casos_resueltos = [c for c in casos if c["estado"] == "Resuelto"]
        if not casos_resueltos:
            st.info("No hay casos resueltos hoy.")
        for caso in casos_resueltos:
            _render_card_caso_resuelto(caso)


def _render_card_caso(caso, todos_casos, modo_proceso=False):
    """Renderiza la tarjeta de un caso activo."""
    cliente = caso.get("cliente", {})
    error_id = caso.get("error_id", "ERR001")
    error = BASE_CONOCIMIENTO.get(error_id, {})
    fp = get_fp_by_id(cliente.get("fp_asignado", "FP001"))
    prioridad = caso.get("prioridad", "MEDIA")

    color_prior = {"CRÍTICA": "#D32F2F", "ALTA": "#F57C00", "MEDIA": "#FF8F00", "BAJA": "#00D261"}.get(prioridad, "#6B6560")
    color_estado = {"Abierto": "#D32F2F", "En gestión": "#F57C00", "Escalado": "#003087"}.get(caso["estado"], "#6B6560")

    with st.container():
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:16px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:12px;
                    border-left:4px solid {color_prior};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <span style="font-weight:700;font-size:15px;">
                        <span style="background:#FFEBEE;color:{color_prior};padding:2px 8px;
                                     border-radius:10px;font-size:12px;margin-right:8px;">
                            NPS {caso['nps']} | {prioridad}
                        </span>
                        {cliente.get('nombre','')}
                    </span>
                    <span style="color:#6B6560;font-size:12px;margin-left:12px;">
                        📋 {cliente.get('contrato','')} | {caso['hora']}
                    </span>
                </div>
                <span style="background:{color_estado};color:white;padding:2px 10px;
                             border-radius:10px;font-size:12px;font-weight:600;">
                    {caso['estado']}
                </span>
            </div>
            <div style="margin-top:8px;font-size:13px;">
                <span style="color:#003087;">📌 {caso['categoria']}</span> &nbsp;|&nbsp;
                <span style="color:#F57C00;">🔧 {error_id}: {error.get('titulo','')}</span>
            </div>
            <div style="font-size:13px;color:#4a4a4a;margin-top:4px;font-style:italic;">
                "{caso['comentario'][:120]}..."
            </div>
            <div style="font-size:12px;color:#6B6560;margin-top:4px;">
                👤 FP: {fp.get('nombre','')} | 📧 {cliente.get('email','')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("💬 Chat en línea", key=f"chat_cx_{caso['id']}", type="primary", use_container_width=True):
                st.session_state["cliente_activo"] = cliente
                activar_chatbot(error_id, "Control Tower CX")
                st.session_state["tecnico_conectado"] = True
                _cambiar_estado_caso(todos_casos, caso["id"], "En gestión")
                log = registrar_accion_log(f"Chat iniciado con {cliente.get('nombre','')} — Caso {caso['id']}")
                st.session_state.setdefault("chatbot_log", []).append(log)
                st.success(f"💬 Chat iniciado con **{cliente.get('nombre','')}**. El agente fue notificado con el historial completo.")
                st.rerun()

        with col2:
            if st.button("📞 Recibir llamada", key=f"call_cx_{caso['id']}", use_container_width=True):
                _cambiar_estado_caso(todos_casos, caso["id"], "En gestión")
                st.success(f"📞 Llamada programada para los próximos 10 minutos con **{cliente.get('nombre','')}**.")
                st.rerun()

        with col3:
            if st.button("👨‍💻 Ver en Técnico", key=f"tec_cx_{caso['id']}", use_container_width=True):
                st.session_state["cliente_activo"] = cliente
                st.session_state["error_actual"] = error
                st.session_state["error_id_actual"] = error_id
                st.session_state["tecnico_conectado"] = True
                st.session_state["current_page"] = "tecnico"
                st.rerun()

        with col4:
            if st.button("✅ Resolver", key=f"resolve_cx_{caso['id']}", use_container_width=True):
                _resolver_caso_cx(todos_casos, caso, cliente, fp, error, error_id)

        st.markdown("")


def _render_card_caso_resuelto(caso):
    """Tarjeta de caso resuelto."""
    cliente = caso.get("cliente", {})
    st.markdown(f"""
    <div style="background:#f8f9fa;border-radius:8px;padding:12px;margin-bottom:8px;
                border-left:3px solid #00D261;opacity:0.8;">
        ✅ <strong>{cliente.get('nombre','')}</strong> —
        {caso['categoria']} | NPS {caso['nps']} |
        <span style="color:#6B6560;font-size:12px;">Resuelto hoy</span>
    </div>
    """, unsafe_allow_html=True)


def _cambiar_estado_caso(casos, caso_id, nuevo_estado):
    """Cambia el estado de un caso en la lista."""
    for c in casos:
        if c["id"] == caso_id:
            c["estado"] = nuevo_estado
            break
    st.session_state["casos_cx"] = casos


def _resolver_caso_cx(todos_casos, caso, cliente, fp, error, error_id):
    """Resuelve un caso desde el Control Tower y envía notificaciones."""
    from modules.notificaciones import generar_correos_resolucion, render_correos_simulados
    from data.clientes_demo import AGENTES_DEMO

    agente = AGENTES_DEMO[2] if len(AGENTES_DEMO) > 2 else AGENTES_DEMO[0]
    solucion = f"Caso resuelto por el equipo CX. Error {error_id} solucionado satisfactoriamente."

    _cambiar_estado_caso(todos_casos, caso["id"], "Resuelto")

    correos = generar_correos_resolucion(cliente, fp, agente, {}, solucion)
    st.session_state["notificaciones_enviadas"] = correos

    st.success(f"✅ Caso **{caso['id']}** marcado como resuelto. Notificaciones enviadas.")
    render_correos_simulados(correos, "Ver notificaciones de cierre")
    st.rerun()
