"""
modules/chatbot.py
Agente IA conversacional flotante con auto-avance de pasos y acompañamiento continuo.
Sin API externa — respuestas 100% desde la base de conocimiento local.
"""

import streamlit as st
import datetime
from data.base_conocimiento import BASE_CONOCIMIENTO
from modules.report_generator import registrar_accion_log


# ── Condiciones de auto-completado por error y paso ─────────────────────────
def _trigger_page(page: str):
    return lambda: st.session_state.get("current_page") == page

def _trigger_cuentas_avanzado():
    return st.session_state.get("cuentas_paso") in ["formulario","biometria","exito"]

def _trigger_cuenta_registrada():
    return st.session_state.get("cuentas_paso") == "exito" or \
           len(st.session_state.get("cliente_activo",{}).get("cuentas_bancarias",[])) > 0

def _trigger_retiro_iniciado():
    return st.session_state.get("current_page") == "retiros" and \
           st.session_state.get("retiro_paso",1) >= 2

def _trigger_retiro_exitoso():
    return st.session_state.get("retiro_exitoso", False)

def _trigger_portafolio():
    return st.session_state.get("current_page") == "portafolio"

def _trigger_tecnico():
    return st.session_state.get("tecnico_conectado", False)

STEP_TRIGGERS: dict = {
    "ERR001": {
        0: _trigger_page("cuentas"),
        1: _trigger_cuentas_avanzado,
        2: _trigger_cuenta_registrada,
        3: _trigger_retiro_iniciado,
    },
    "ERR002": {
        0: _trigger_portafolio,
    },
    "ERR003": {
        0: _trigger_portafolio,
    },
    "ERR009": {
        # Todo manual — requiere validación de compliance
    },
    "ERR011": {
        0: lambda: st.session_state.get("err011_vio_solicitudes", False),
        1: lambda: st.session_state.get("err011_acepto_tc", False),
        2: lambda: st.session_state.get("err011_otp_verificado", False),
    },
    "ERR013": {
        0: lambda: st.session_state.get("login_intentos",0) >= 3,
    },
}


def init_chatbot_state():
    defaults = {
        "chatbot_activo": False,
        "chatbot_minimizado": False,
        "error_actual": None,
        "error_id_actual": None,
        "chatbot_pasos_completados": [],
        "chatbot_log": [],
        "modulo_origen": "",
        "timestamp_inicio": None,
        "chatbot_resuelto": None,
        "chatbot_mensaje_inicial": True,
        "tecnico_conectado": False,
        "tecnico_chat": [],
        "caso_escalado": False,
        "ticket_actual": None,
        "notificaciones_enviadas": [],
        "retiro_exitoso": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def activar_chatbot(error_id: str, modulo: str, cliente_nombre: str = ""):
    error = BASE_CONOCIMIENTO.get(error_id, {})
    st.session_state.update({
        "chatbot_activo": True,
        "chatbot_minimizado": False,
        "error_actual": error,
        "error_id_actual": error_id,
        "chatbot_pasos_completados": [],
        "modulo_origen": modulo,
        "timestamp_inicio": datetime.datetime.now(),
        "chatbot_resuelto": None,
        "chatbot_mensaje_inicial": True,
    })
    st.session_state.setdefault("chatbot_log", []).append(
        registrar_accion_log(f"Chatbot activado — {error_id}: {error.get('titulo','')}")
    )


def check_auto_advance():
    """
    Se ejecuta en cada render. Detecta automáticamente si el usuario completó
    un paso según las condiciones definidas en STEP_TRIGGERS.
    Retorna True si hubo algún avance (para forzar rerun).
    """
    if not st.session_state.get("chatbot_activo"):
        return False
    if st.session_state.get("chatbot_resuelto") is not None:
        return False

    error_id = st.session_state.get("error_id_actual", "")
    error = st.session_state.get("error_actual", {})
    pasos_completados = list(st.session_state.get("chatbot_pasos_completados", []))
    total_pasos = len(error.get("solucion_ia", []))
    triggers = STEP_TRIGGERS.get(error_id, {})

    advanced = False
    for step_idx, trigger_fn in triggers.items():
        if step_idx not in pasos_completados:
            try:
                if trigger_fn():
                    pasos_completados.append(step_idx)
                    st.session_state["chatbot_pasos_completados"] = pasos_completados
                    solucion = error.get("solucion_ia", [])
                    desc = solucion[step_idx][:60] if step_idx < len(solucion) else ""
                    st.session_state["chatbot_log"].append(
                        registrar_accion_log(f"Auto-completado Paso {step_idx+1}: {desc}…")
                    )
                    advanced = True
            except Exception:
                pass

    # Si se completaron todos los pasos automáticos disponibles y quedan pasos manuales,
    # no hacer nada — el usuario debe marcarlos
    return advanced


# ── Render principal ─────────────────────────────────────────────────────────

def render_chatbot_flotante():
    """
    Botón flotante (HTML/CSS) que se muestra cuando el chatbot está inactivo o minimizado.
    Los elementos interactivos se renderizan dentro del panel de columna en app.py.
    """
    init_chatbot_state()

    if not st.session_state.get("chatbot_activo", False):
        _render_fab_inactive()
        return

    if st.session_state.get("chatbot_minimizado", False):
        _render_fab_minimized()
        return


def render_chatbot_panel():
    """
    Panel completo del chatbot. Se renderiza en la columna derecha cuando el chatbot está activo.
    """
    init_chatbot_state()

    cliente = st.session_state.get("cliente_activo", {})
    nombre = cliente.get("nombre", "Cliente") if cliente else "Cliente"
    error = st.session_state.get("error_actual", {})
    error_id = st.session_state.get("error_id_actual", "")
    pasos = error.get("solucion_ia", [])
    pasos_completados = st.session_state.get("chatbot_pasos_completados", [])
    es_critico = error.get("es_critico", False) or error.get("severidad") == "critica"
    icono = error.get("icono", "🤖")
    modulo_origen = st.session_state.get("modulo_origen", "")

    color_header = "#D32F2F" if es_critico else "#00D261"

    # ── Header del panel ──
    st.markdown(f"""
    <div style="background:{color_header};border-radius:14px 14px 0 0;
                padding:14px 18px;display:flex;align-items:center;justify-content:space-between;
                margin-bottom:0;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;background:rgba(255,255,255,0.2);border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:18px;">
                {icono}
            </div>
            <div>
                <div style="color:white;font-weight:700;font-size:14px;">Asistente IA Skandia</div>
                <div style="color:rgba(255,255,255,0.8);font-size:11px;">
                    {'🚨 ALERTA CRÍTICA' if es_critico else '● En línea · Acompañándote'}
                </div>
            </div>
        </div>
    </div>
    <div style="background:white;border-radius:0 0 14px 14px;
                box-shadow:0 8px 32px rgba(0,0,0,0.12);padding:16px;
                border:1px solid #F0F0F0;border-top:none;">
    """, unsafe_allow_html=True)

    # ── Alerta crítica ──
    if es_critico:
        st.error(f"🚨 **ALERTA CRÍTICA:** {error.get('titulo','')}")

    # ── Mensaje inicial ──
    if st.session_state.get("chatbot_mensaje_inicial", True):
        categoria = error.get("categoria", "")
        titulo = error.get("titulo", "")
        st.markdown(f"""
        <div style="background:#F0FFF6;border-radius:10px;padding:12px 14px;margin-bottom:12px;
                    border-left:3px solid #00D261;font-size:13px;">
            <strong>👋 Hola {nombre},</strong><br>
            Detecté un inconveniente en <strong>{categoria}</strong>.<br>
            <span style="color:#6B6560;">Probable causa: <strong>{titulo}</strong></span><br>
            <span style="color:#00D261;font-size:12px;">Te acompaño paso a paso para resolverlo.</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Progreso general ──
    total = len(pasos)
    completados = len(pasos_completados)
    pct = int((completados / total) * 100) if total > 0 else 0

    st.markdown(f"""
    <div style="margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;font-size:11px;
                    color:#6B6560;margin-bottom:4px;">
            <span>Progreso</span><span>{completados}/{total} pasos</span>
        </div>
        <div style="background:#F0F0F0;border-radius:4px;height:5px;">
            <div style="background:#00D261;width:{pct}%;height:5px;border-radius:4px;
                        transition:width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Checklist de pasos ──
    st.markdown("**📋 Pasos para resolver:**")

    for i, paso in enumerate(pasos):
        completado = i in pasos_completados
        es_actual  = (not completado) and all(j in pasos_completados for j in range(i))
        if completado:
            bg, color, icn = "#F0FFF6", "#00A84F", "✅"
        elif es_actual:
            bg, color, icn = "#FFFBEB", "#F59E0B", "▶"
        else:
            bg, color, icn = "#FAFAFA", "#9E9E9E", "⬜"

        st.markdown(f"""
        <div style="background:{bg};border-radius:8px;padding:8px 12px;margin:4px 0;
                    font-size:12px;color:{color};border:1px solid {'#C8F0D8' if completado else '#F0F0F0'};">
            <span style="font-weight:700;margin-right:6px;">{icn} Paso {i+1}</span>
            <span style="{'text-decoration:line-through;opacity:0.7;' if completado else ''}">{paso}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Botón de navegación al módulo destino ──
    modulo_destino = error.get("modulo_destino", "")
    _render_nav_button(modulo_destino, modulo_origen)

    st.markdown("")

    # ── Acción del paso actual ──
    if st.session_state.get("chatbot_resuelto") is None:
        siguiente = next((i for i in range(len(pasos)) if i not in pasos_completados), None)

        if siguiente is not None:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✓ Completar Paso {siguiente+1}",
                             key=f"completar_paso_{siguiente}_{error_id}",
                             type="primary", use_container_width=True):
                    st.session_state["chatbot_pasos_completados"].append(siguiente)
                    st.session_state["chatbot_mensaje_inicial"] = False
                    st.session_state["chatbot_log"].append(
                        registrar_accion_log(f"Paso {siguiente+1} marcado manualmente")
                    )
                    st.rerun()
            with col2:
                if st.button("¿Necesitas ayuda?", key=f"ayuda_{siguiente}_{error_id}",
                             use_container_width=True):
                    st.info(f"💡 **Consejo:** {pasos[siguiente]}")

        else:
            # Todos los pasos vistos — preguntar resolución
            st.success("✅ ¡Has completado todos los pasos!")
            st.markdown("**¿Lograste resolver el inconveniente?**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sí, resuelto", key=f"resuelto_si_{error_id}",
                             type="primary", use_container_width=True):
                    st.session_state["chatbot_resuelto"] = True
                    st.session_state["chatbot_log"].append(
                        registrar_accion_log("Cliente confirmó resolución exitosa")
                    )
                    st.rerun()
            with col2:
                if st.button("❌ No resuelto", key=f"resuelto_no_{error_id}",
                             use_container_width=True):
                    st.session_state["chatbot_resuelto"] = False
                    st.session_state["chatbot_log"].append(
                        registrar_accion_log("Cliente reportó que el problema persiste")
                    )
                    st.rerun()

    elif st.session_state.get("chatbot_resuelto") is True:
        _render_exito(nombre, modulo_origen)

    elif st.session_state.get("chatbot_resuelto") is False:
        _render_escalar(nombre)

    # ── Controles del panel ──
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➖ Minimizar", key=f"min_chat_{error_id}", use_container_width=True):
            st.session_state["chatbot_minimizado"] = True
            st.rerun()
    with col2:
        if st.button("✖ Cerrar", key=f"close_chat_{error_id}", use_container_width=True):
            st.session_state["chatbot_activo"] = False
            st.session_state["error_actual"] = None
            st.rerun()


def _render_nav_button(modulo_destino: str, modulo_origen: str):
    """Botón de navegación contextual dentro del chatbot."""
    MAPA = {
        "Cuentas Bancarias":    "cuentas",
        "Mi Portafolio":        "portafolio",
        "Documentos":           "documentos",
        "Mis Datos":            "datos",
        "Retiros":              "retiros",
        "Login":                "login",
        "Validación de seguridad": "login",
        "Aportes":              "retiros",
        "Portafolio":           "portafolio",
    }
    page_key = MAPA.get(modulo_destino, "")
    current  = st.session_state.get("current_page", "")

    if page_key and page_key != current:
        st.markdown(f"""
        <div style="background:#F0FFF6;border-radius:8px;padding:8px 12px;margin:8px 0;
                    border-left:3px solid #00D261;font-size:12px;color:#2D2926;">
            💡 Para el siguiente paso ve a: <strong>{modulo_destino}</strong>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"➡ Ir a {modulo_destino}", key=f"nav_{modulo_destino}_{page_key}",
                     type="primary", use_container_width=True):
            st.session_state["current_page"] = page_key
            st.session_state["chatbot_minimizado"] = False
            st.session_state["chatbot_log"].append(
                registrar_accion_log(f"Navegó a: {modulo_destino}")
            )
            st.rerun()


def _render_exito(nombre: str, modulo_origen: str):
    """Panel de resolución exitosa — retorna al módulo de origen."""
    MAPA_MODULO = {
        "Retiros": "retiros", "Cuentas Bancarias": "cuentas",
        "Mi Portafolio": "portafolio", "Documentos": "documentos",
        "Mis Datos": "datos", "Mi Portal": "portal",
        "Control Tower CX": "control_tower",
    }
    page_retorno = MAPA_MODULO.get(modulo_origen, "portal")

    st.markdown(f"""
    <div style="background:#F0FFF6;border-radius:10px;padding:14px;border-left:3px solid #00D261;
                margin:8px 0;font-size:13px;">
        <div style="font-weight:700;color:#2D2926;margin-bottom:4px;">
            🎉 ¡Excelente, {nombre}!
        </div>
        <div style="color:#4a4a4a;">
            Tu inconveniente fue resuelto. Puedes continuar donde lo dejaste.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        label_retorno = {
            "retiros":"↩ Volver a Retiros", "cuentas":"↩ Volver a Cuentas",
            "portafolio":"↩ Volver a Portafolio", "portal":"↩ Ir a Mi Portal",
        }.get(page_retorno, "↩ Continuar")
        if st.button(label_retorno, key="volver_origen", type="primary", use_container_width=True):
            st.session_state["chatbot_activo"] = False
            st.session_state["current_page"]   = page_retorno
            st.rerun()
    with col2:
        if st.button("⭐ Calificar y salir", key="calificar_cerrar", use_container_width=True):
            st.session_state["chatbot_activo"] = False
            _ir_nps()


def _render_escalar(nombre: str):
    """Panel para escalar al técnico."""
    st.warning("**El problema persiste.** Podemos conectarte con un Agente Técnico especializado.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💻 Hablar con Técnico", key="escalar_tecnico_chat",
                     type="primary", use_container_width=True):
            st.session_state["tecnico_conectado"] = True
            st.session_state["chatbot_log"].append(
                registrar_accion_log("Cliente solicitó técnico especializado")
            )
            st.session_state["current_page"] = "tecnico"
            st.rerun()
    with col2:
        if st.button("📞 Solicitar llamada", key="llamada_escalar", use_container_width=True):
            st.success("📞 Llamada programada en los próximos 10 minutos.")


def _render_fab_inactive():
    """Botón flotante cuando el chatbot está inactivo (solo visual HTML)."""
    st.markdown("""
    <div style="position:fixed;bottom:28px;right:28px;z-index:9998;pointer-events:none;">
        <div style="background:#00D261;color:white;border-radius:50px;padding:12px 18px;
                    box-shadow:0 4px 20px rgba(0,210,97,0.35);font-size:13px;font-weight:600;
                    display:flex;align-items:center;gap:8px;opacity:0.7;">
            🤖 Asistente IA
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_fab_minimized():
    """Botón flotante cuando el chatbot está minimizado — con animación si hay error."""
    tiene_error = st.session_state.get("error_actual") is not None
    color = "#D32F2F" if tiene_error else "#00D261"
    anim  = "animation:blink 1.4s infinite;" if tiene_error else ""

    st.markdown(f"""
    <div style="position:fixed;bottom:28px;right:28px;z-index:9998;">
        <div style="background:{color};color:white;border-radius:50px;padding:13px 20px;
                    box-shadow:0 4px 20px rgba(0,0,0,0.25);font-size:13px;font-weight:700;
                    display:flex;align-items:center;gap:8px;{anim}cursor:pointer;">
            {'🚨' if tiene_error else '🤖'} {'Error detectado' if tiene_error else 'Asistente IA'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💬 Abrir asistente", key="abrir_chat_min", type="primary"):
        st.session_state["chatbot_minimizado"] = False
        st.rerun()


def _ir_nps():
    """Navega a la encuesta NPS post-sesión."""
    import datetime as dt
    cliente  = st.session_state.get("cliente_activo", {})
    escenario= st.session_state.get("escenario_demo", "libre")
    pagina   = st.session_state.get("current_page", "portal")
    st.session_state["nps_contexto"] = {
        "cliente": cliente, "escenario": escenario,
        "pagina_origen": pagina,
        "timestamp": dt.datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state["autenticado"]  = False
    st.session_state["current_page"] = "nps_post"
    st.rerun()
