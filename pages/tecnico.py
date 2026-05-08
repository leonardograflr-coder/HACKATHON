"""
pages/tecnico.py
Interfaz del técnico en tiempo real: vista del cliente, checklist, chat y generación de informe.
"""

import streamlit as st
import datetime
from data.base_conocimiento import BASE_CONOCIMIENTO
from data.clientes_demo import get_fp_by_id, AGENTES_DEMO
from modules.report_generator import generar_informe_tecnico, generar_ticket_escalamiento, generar_texto_ticket, registrar_accion_log
from modules.notificaciones import generar_correos_escalamiento, generar_correos_resolucion, render_correos_simulados


@st.dialog("🎫 Caso escalado exitosamente")
def _popup_escalamiento(numero: str, ans: str, prioridad: str, fp_nombre: str):
    """Modal de confirmación del ticket de escalamiento."""
    color_prior = {"CRÍTICA": "#D32F2F", "ALTA": "#F57C00", "MEDIA": "#003087", "BAJA": "#00D261"}.get(prioridad, "#6B6560")
    st.markdown(f"""
    <div style="text-align:center;padding:8px 0 12px;">
        <div style="font-size:48px;margin-bottom:8px;">🎫</div>
        <h4 style="color:#2D2926;margin:0 0 4px;">Caso escalado exitosamente</h4>
    </div>
    <div style="background:#F0F7FF;border-radius:10px;padding:14px;margin-bottom:14px;">
        <div style="font-size:14px;margin:6px 0;">🎫 <strong>Ticket:</strong> <span style="font-weight:700;color:#003087;">{numero}</span></div>
        <div style="font-size:14px;margin:6px 0;">⚡ <strong>Prioridad:</strong>
            <span style="background:{color_prior};color:white;padding:2px 10px;border-radius:10px;font-size:12px;">{prioridad}</span>
        </div>
        <div style="font-size:14px;margin:6px 0;">⏱️ <strong>ANS respuesta:</strong> {ans}</div>
        <div style="font-size:14px;margin:6px 0;">👤 <strong>FP notificado:</strong> {fp_nombre}</div>
    </div>
    <p style="color:#6B6560;font-size:13px;text-align:center;margin:0;">
        Tu caso ha sido escalado con el número <strong>{numero}</strong>.<br>
        Recibirás respuesta en un máximo de <strong>{ans}</strong>.<br>
        Tu Financial Planner <strong>{fp_nombre}</strong> también fue notificado.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Aceptar", type="primary", use_container_width=True, key="popup_escal_aceptar"):
        st.session_state["caso_escalado"] = False
        st.session_state["ticket_actual"] = None
        st.session_state["chatbot_activo"] = False
        st.session_state["current_page"] = "portal"
        st.rerun()


def render_tecnico():
    """Renderiza la interfaz del técnico en tiempo real."""
    cliente = st.session_state.get("cliente_activo", {})
    error = st.session_state.get("error_actual", {})
    error_id = st.session_state.get("error_id_actual", "ERR001")
    pasos_completados = st.session_state.get("chatbot_pasos_completados", [])
    log_acciones = st.session_state.get("chatbot_log", [])
    modulo = st.session_state.get("modulo_origen", "Portal")

    if not cliente:
        st.warning("No hay cliente activo. Selecciona un cliente en el sidebar.")
        return

    fp = get_fp_by_id(cliente.get("fp_asignado", "FP001"))

    # Mostrar popup de escalamiento si el caso fue escalado
    if st.session_state.get("caso_escalado") and st.session_state.get("ticket_actual"):
        ticket = st.session_state["ticket_actual"]
        _popup_escalamiento(
            ticket.get("numero", "TICK-2026-001"),
            ticket.get("ans_horas", "4 a 12 horas hábiles"),
            ticket.get("prioridad", "MEDIA"),
            fp.get("nombre", ""),
        )

    agente = AGENTES_DEMO[2] if len(AGENTES_DEMO) > 2 else AGENTES_DEMO[0]

    st.markdown("## 👨‍💻 Interfaz del Técnico — Caso en tiempo real")

    # Banner de caso activo
    es_critico = error.get("es_critico", False) or error.get("severidad") == "critica"
    color_banner = "#FFEBEE" if es_critico else "#E8F5E9"
    color_border = "#D32F2F" if es_critico else "#00D261"

    st.markdown(f"""
    <div style="background:{color_banner};border-left:4px solid {color_border};border-radius:8px;
                padding:14px 18px;margin-bottom:16px;">
        <strong>{'🚨 CASO CRÍTICO' if es_critico else '🔴 CASO ACTIVO'}</strong> —
        {error.get('icono','🔧')} {error_id}: {error.get('titulo','Error detectado')} &nbsp;|&nbsp;
        Cliente: {cliente.get('nombre','')} &nbsp;|&nbsp;
        Módulo: {modulo} &nbsp;|&nbsp;
        Hora: {datetime.datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

    # Generar informe automático
    informe = generar_informe_tecnico(
        cliente=cliente,
        error=error,
        error_id=error_id,
        pasos_completados=pasos_completados,
        log_acciones=log_acciones,
        fp=fp,
        modulo_origen=modulo
    )
    st.session_state["informe_tecnico_actual"] = informe

    col_cliente, col_tecnico = st.columns([1, 1])

    # ─── PANEL IZQUIERDO: Vista del cliente ───
    with col_cliente:
        st.markdown("### 📱 Vista del cliente")

        st.markdown(f"""
        <div style="background:#f8f9fa;border-radius:12px;padding:16px;
                    border:1px solid #E0E0E0;margin-bottom:12px;">
            <div style="font-size:12px;color:#6B6560;margin-bottom:8px;">CLIENTE EN PANTALLA</div>
            <div style="background:#FFEBEE;border-radius:8px;padding:12px;
                        border-left:3px solid #D32F2F;font-size:13px;">
                ❌ <strong>{error.get('titulo','Error detectado')}</strong><br>
                <span style="color:#6B6560;">{error.get('descripcion','')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Checklist de pasos del cliente
        st.markdown("**Pasos realizados con el asistente IA:**")
        pasos = error.get("solucion_ia", [])
        for i, paso in enumerate(pasos):
            completado = i in pasos_completados
            icon = "✅" if completado else "⬜"
            color = "#00A84F" if completado else "#6B6560"
            st.markdown(
                f'<div style="font-size:13px;color:{color};padding:4px 0;">'
                f'{icon} Paso {i+1}: {paso}</div>',
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("**Chat con el cliente:**")

        if "tecnico_chat" not in st.session_state:
            st.session_state["tecnico_chat"] = []

        # Mostrar mensajes del chat
        for msg in st.session_state["tecnico_chat"][-6:]:
            rol = msg.get("rol", "cliente")
            texto = msg.get("texto", "")
            ts = msg.get("ts", "")
            bg = "#E8F5E9" if rol == "tecnico" else "#f0f0f0"
            align = "right" if rol == "tecnico" else "left"
            st.markdown(f"""
            <div style="background:{bg};border-radius:8px;padding:8px 12px;
                        margin:4px 0;text-align:{align};font-size:13px;">
                <strong>{'🎧 Técnico' if rol=='tecnico' else '👤 Cliente'}:</strong> {texto}
                <div style="font-size:10px;color:#9E9E9E;margin-top:2px;">{ts}</div>
            </div>
            """, unsafe_allow_html=True)

        with st.form("chat_cliente_form"):
            msg_cliente = st.text_input("Mensaje del cliente:", placeholder="Escribe el mensaje del cliente...")
            if st.form_submit_button("📤 Enviar como cliente", use_container_width=True):
                if msg_cliente:
                    st.session_state["tecnico_chat"].append({
                        "rol": "cliente",
                        "texto": msg_cliente,
                        "ts": datetime.datetime.now().strftime("%H:%M")
                    })
                    log = registrar_accion_log(f"Mensaje del cliente: {msg_cliente[:50]}")
                    st.session_state.setdefault("chatbot_log", []).append(log)
                    st.rerun()

    # ─── PANEL DERECHO: Vista del técnico ───
    with col_tecnico:
        st.markdown("### 🎧 Panel del técnico")

        # Info del caso
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:16px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:12px;">
            <div style="font-size:12px;color:#6B6560;margin-bottom:8px;font-weight:600;">INFORMACIÓN DEL CASO</div>
            <table style="width:100%;font-size:13px;">
                <tr><td style="color:#6B6560;padding:3px 0;">Cliente:</td><td><strong>{cliente.get('nombre','')}</strong></td></tr>
                <tr><td style="color:#6B6560;padding:3px 0;">Contrato:</td><td>{cliente.get('contrato','')}</td></tr>
                <tr><td style="color:#6B6560;padding:3px 0;">Error:</td><td>{error_id} — {error.get('titulo','')}</td></tr>
                <tr><td style="color:#6B6560;padding:3px 0;">Módulo:</td><td>{modulo}</td></tr>
                <tr><td style="color:#6B6560;padding:3px 0;">FP Asignado:</td><td>{fp.get('nombre','')}</td></tr>
                <tr><td style="color:#6B6560;padding:3px 0;">Severidad:</td><td>
                    <span style="background:{'#D32F2F' if es_critico else '#F57C00'};color:white;
                                 padding:2px 8px;border-radius:10px;font-size:11px;">
                        {error.get('severidad','media').upper()}
                    </span>
                </td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Log de acciones del cliente
        st.markdown("**📋 Log de acciones del cliente:**")
        if log_acciones:
            log_texto = ""
            for entry in log_acciones[-8:]:
                log_texto += f"[{entry.get('timestamp','')}] {entry.get('descripcion','')}\n"
            st.code(log_texto, language="text")
        else:
            st.markdown("<span style='color:#9E9E9E;font-size:13px;'>Sin acciones registradas aún.</span>", unsafe_allow_html=True)

        # Chat del técnico
        st.markdown("**Respuesta del técnico:**")
        with st.form("chat_tecnico_form"):
            msg_tecnico = st.text_input("Escribe tu respuesta:", placeholder="Respuesta al cliente...")
            if st.form_submit_button("📤 Enviar respuesta", type="primary", use_container_width=True):
                if msg_tecnico:
                    st.session_state["tecnico_chat"].append({
                        "rol": "tecnico",
                        "texto": msg_tecnico,
                        "ts": datetime.datetime.now().strftime("%H:%M")
                    })
                    log = registrar_accion_log(f"Técnico respondió: {msg_tecnico[:50]}")
                    st.session_state.setdefault("chatbot_log", []).append(log)
                    st.rerun()

        st.markdown("---")

        # Botones de acción
        st.markdown("**Acciones del técnico:**")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Marcar como resuelto", type="primary", use_container_width=True, key="resolver_tecnico"):
                _resolver_caso(cliente, fp, agente, error, error_id)
        with col_b:
            if st.button("🚨 Escalar a mesa de ayuda", use_container_width=True, key="escalar_tecnico"):
                _escalar_caso(cliente, fp, error, error_id, informe)

        # Informe técnico descargable
        st.markdown("---")
        with st.expander("📄 Ver informe técnico generado"):
            st.code(informe, language="text")
            st.download_button(
                "⬇ Descargar informe",
                data=informe,
                file_name=f"informe_{error_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )


def _resolver_caso(cliente, fp, agente, error, error_id):
    """Cierra el caso y redirige al cliente al módulo correspondiente de inmediato."""
    destino_map = {
        "ERR009": "cuentas",
        "ERR001": "cuentas",
        "ERR011": "portafolio",
    }
    destino = destino_map.get(error_id, "portal")

    log = registrar_accion_log(f"Técnico marcó caso como RESUELTO — {error_id}")
    st.session_state.setdefault("chatbot_log", []).append(log)

    st.session_state["tecnico_conectado"] = False
    st.session_state["chatbot_activo"]    = False
    st.session_state["chatbot_resuelto"]  = True
    st.session_state["current_page"]      = destino

    if error_id == "ERR009":
        st.session_state["sarlaft_resuelto"] = True
        st.session_state["cuentas_paso"]     = "formulario"

    st.rerun()


def _escalar_caso(cliente, fp, error, error_id, informe):
    """Genera ticket de escalamiento y muestra popup de confirmación."""
    from modules.notificaciones import generar_correos_escalamiento

    if st.session_state.get("caso_escalado"):
        return  # popup ya mostrado desde render_tecnico

    ticket = generar_ticket_escalamiento(
        cliente=cliente,
        error=error,
        error_id=error_id,
        informe_tecnico=informe,
        acciones_tecnico=st.session_state.get("tecnico_chat", []),
        fp=fp,
    )
    st.session_state["caso_escalado"] = True
    st.session_state["ticket_actual"] = ticket

    log = registrar_accion_log(f"Caso escalado a mesa de ayuda — Ticket: {ticket['numero']}")
    st.session_state.setdefault("chatbot_log", []).append(log)

    correos = generar_correos_escalamiento(cliente, fp, ticket)
    st.session_state["notificaciones_enviadas"] = correos
    st.rerun()  # Popup se mostrará en el siguiente render desde render_tecnico


def _render_confirmacion_escalamiento(cliente, fp, ticket):
    """Pantalla de confirmación del escalamiento para el cliente."""
    numero = ticket.get("numero", "TICK-2026-001")
    ans = ticket.get("ans_horas", "4 a 12 horas hábiles")
    prioridad = ticket.get("prioridad", "MEDIA")

    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:24px;
                box-shadow:0 2px 8px rgba(0,0,0,0.10);text-align:center;margin:16px 0;">
        <div style="font-size:56px;margin-bottom:12px;">🎫</div>
        <h3 style="color:#2D2926;">Caso escalado exitosamente</h3>
        <div style="background:#E8F5E9;border-radius:8px;padding:16px;margin:12px 0;text-align:left;">
            <div style="font-size:13px;margin:4px 0;"><strong>🎫 Ticket:</strong> {numero}</div>
            <div style="font-size:13px;margin:4px 0;"><strong>⚡ Prioridad:</strong> {prioridad}</div>
            <div style="font-size:13px;margin:4px 0;"><strong>⏱️ ANS respuesta:</strong> {ans}</div>
            <div style="font-size:13px;margin:4px 0;"><strong>👤 FP notificado:</strong> {fp.get('nombre','')}</div>
        </div>
        <p style="color:#6B6560;font-size:14px;">
            Tu caso ha sido escalado con el número <strong>{numero}</strong>.<br>
            Recibirás respuesta en un máximo de <strong>{ans}</strong>.<br>
            Tu Financial Planner <strong>{fp.get('nombre','')}</strong> también fue notificado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    texto_ticket = generar_texto_ticket(ticket)
    st.download_button(
        "⬇ Descargar ticket completo",
        data=texto_ticket,
        file_name=f"{numero}.txt",
        mime="text/plain"
    )

    if st.button("← Volver al portal", key="back_portal_escalado", type="primary"):
        st.session_state["current_page"] = "portal"
        st.rerun()
