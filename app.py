"""
app.py — Skandia Portal Clientes 2026 — Hackathon Demo
Router principal con layout adaptativo (2 columnas cuando el chatbot está activo).
"""

import streamlit as st
import datetime
import importlib

st.set_page_config(
    page_title="Skandia Portal Clientes 2026",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config.brand import apply_styles, SKANDIA_LOGO_HTML
from data.clientes_demo import CLIENTES_DEMO, get_fp_by_id

# Escenario → cliente + error + página de inicio
ESCENARIOS_CONFIG = {
    "A": {"cliente_idx": 0, "error_id": "ERR001", "pagina": "portal"},
    "B": {"cliente_idx": 1, "error_id": "ERR009", "pagina": "portal"},
    "C": {"cliente_idx": 2, "error_id": "ERR011", "pagina": "portal"},
}

ROUTE_MAP = {
    "portal":        ("pages.portal_cliente", "render_portal"),
    "retiros":       ("pages.portal_cliente", "render_retiros"),
    "cuentas":       ("pages.portal_cliente", "render_cuentas"),
    "portafolio":    ("pages.portal_cliente", "render_portafolio"),
    "documentos":    ("pages.portal_cliente", "render_documentos"),
    "datos":         ("pages.portal_cliente", "render_datos"),
    "nps":           ("pages.portal_cliente", "render_nps"),
    "dashboard":     ("pages.dashboard",      "render_dashboard"),
    "control_tower": ("pages.control_tower",  "render_control_tower"),
    "tecnico":       ("pages.tecnico",        "render_tecnico"),
}


# ── Session state ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "autenticado": False, "current_page": "login",
        "login_step": "credenciales", "login_intentos": 0,
        "cliente_activo": CLIENTES_DEMO[0],
        "escenario_demo": "libre", "escenario_anterior": None,
        "chatbot_activo": False, "chatbot_minimizado": False,
        "chatbot_pasos_completados": [], "chatbot_log": [],
        "error_actual": None, "error_id_actual": None,
        "chatbot_resuelto": None, "chatbot_mensaje_inicial": True,
        "tecnico_conectado": False, "tecnico_chat": [],
        "caso_escalado": False, "ticket_actual": None,
        "ticket_counter": 1, "modulo_origen": "",
        "notificaciones_enviadas": [], "df_nps": None,
        "retiro_paso": 1, "retiro_exitoso": False,
        "retiro_otp_modal": False, "retiro_tipo": "especifico",
        "retiro_monto": 500000, "retiro_vivienda": False,
        "cuentas_paso": "lista", "nueva_cuenta": None,
        "simular_fraude": False, "casos_cx": None,
        "nps_contexto": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_demo():
    preserve = {"df_nps", "ticket_counter"}
    for k in list(st.session_state.keys()):
        if k not in preserve:
            del st.session_state[k]
    st.session_state.update({"current_page": "login", "autenticado": False})


def cerrar_sesion_a_nps():
    st.session_state["nps_contexto"] = {
        "cliente":      st.session_state.get("cliente_activo", {}),
        "escenario":    st.session_state.get("escenario_demo", "libre"),
        "pagina_origen":st.session_state.get("current_page", "portal"),
        "timestamp":    datetime.datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state["autenticado"]  = False
    st.session_state["current_page"] = "nps_post"
    st.rerun()


def _aplicar_escenario(escenario: str):
    if escenario == "libre":
        return
    cfg = ESCENARIOS_CONFIG.get(escenario)
    if not cfg:
        return
    st.session_state.update({
        "cliente_activo": CLIENTES_DEMO[cfg["cliente_idx"]],
        "current_page": cfg.get("pagina", "portal"),
        "retiro_paso": 1, "retiro_exitoso": False,
        "cuentas_paso": "lista", "chatbot_activo": False,
        "chatbot_pasos_completados": [], "chatbot_log": [],
        "caso_escalado": False, "ticket_actual": None,
        "tecnico_conectado": False, "tecnico_chat": [],
        "chatbot_resuelto": None, "error_actual": None,
        "nueva_cuenta": None,
        "sarlaft_resuelto": False,
        "err011_vio_solicitudes": False,
        "err011_acepto_tc": False,
        "err011_otp_verificado": False,
    })


# ── Sidebar ──────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo Skandia Colombia
        st.markdown(f"""
        <div style="padding:18px 12px 14px;border-bottom:1px solid #EBEBEB;margin-bottom:14px;">
            {SKANDIA_LOGO_HTML}
        </div>
        """, unsafe_allow_html=True)

        autenticado = st.session_state.get("autenticado", False)

        if not autenticado:
            if st.button("🔐 Acceder al portal", use_container_width=True,
                         type="primary", key="nav_login"):
                st.session_state["current_page"] = "login"; st.rerun()
        else:
            # ── Selector de escenario ──
            st.markdown('<div style="font-size:11px;font-weight:700;color:#9E9E9E;'
                        'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">'
                        'MODO DEMO</div>', unsafe_allow_html=True)

            esc_actual = st.session_state.get("escenario_demo", "libre")
            escenario = st.selectbox(
                "Escenario:",
                ["libre","A","B","C"],
                format_func=lambda x: {
                    "libre":"🔓 Libre",
                    "A":    "A · Carlos / ERR001",
                    "B":    "B · María / ERR009",
                    "C":    "C · Roberto / ERR011",
                }.get(x, x),
                index=["libre","A","B","C"].index(esc_actual),
                key="sel_escenario",
                label_visibility="collapsed"
            )
            if escenario != st.session_state.get("escenario_anterior"):
                st.session_state.update({
                    "escenario_demo": escenario,
                    "escenario_anterior": escenario
                })
                _aplicar_escenario(escenario)
                st.rerun()

            if escenario != "libre":
                _render_guion_sidebar(escenario)

            st.markdown("---")

            # ── Cliente (modo libre) ──
            if escenario == "libre":
                st.markdown('<div style="font-size:11px;font-weight:700;color:#9E9E9E;'
                            'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">'
                            'CLIENTE</div>', unsafe_allow_html=True)
                cliente_actual = st.session_state.get("cliente_activo", CLIENTES_DEMO[0])
                idx = next((i for i,c in enumerate(CLIENTES_DEMO) if c["id"]==cliente_actual.get("id")), 0)
                sel = st.selectbox("Cliente:", range(len(CLIENTES_DEMO)),
                                   format_func=lambda i: CLIENTES_DEMO[i]["nombre"],
                                   index=idx, key="sel_cliente", label_visibility="collapsed")
                if CLIENTES_DEMO[sel]["id"] != cliente_actual.get("id"):
                    st.session_state["cliente_activo"] = CLIENTES_DEMO[sel]; st.rerun()
                st.markdown("---")
            else:
                cfg = ESCENARIOS_CONFIG.get(escenario, {})
                c = CLIENTES_DEMO[cfg.get("cliente_idx", 0)]
                st.markdown(f"""
                <div style="background:#F0FFF6;border-radius:8px;padding:10px 12px;
                            margin-bottom:12px;font-size:13px;">
                    👤 <strong>{c['nombre']}</strong><br>
                    <span style="font-size:11px;color:#6B6560;">{c['contrato']}</span>
                </div>
                """, unsafe_allow_html=True)

            # ── Navegación portal ──
            st.markdown('<div style="font-size:11px;font-weight:700;color:#9E9E9E;'
                        'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">'
                        'PORTAL</div>', unsafe_allow_html=True)
            current = st.session_state.get("current_page","portal")
            for label, page in [
                ("🏠 Mi Portal","portal"), ("💰 Retiros","retiros"),
                ("🏦 Cuentas Bancarias","cuentas"), ("📊 Mi Portafolio","portafolio"),
                ("📄 Documentos","documentos"), ("⚙️ Mis Datos","datos"),
            ]:
                t = "primary" if current==page else "secondary"
                if st.button(label, use_container_width=True, key=f"nav_{page}", type=t):
                    st.session_state["current_page"] = page; st.rerun()

            st.markdown("---")
            st.markdown('<div style="font-size:11px;font-weight:700;color:#9E9E9E;'
                        'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">'
                        'ANÁLISIS</div>', unsafe_allow_html=True)
            for label, page in [
                ("📈 Dashboard Analítico","dashboard"),
                ("🎯 Control Tower CX","control_tower"),
                ("👨‍💻 Interfaz Técnico","tecnico"),
            ]:
                t = "primary" if current==page else "secondary"
                if st.button(label, use_container_width=True, key=f"nav_{page}", type=t):
                    st.session_state["current_page"] = page; st.rerun()

            st.markdown("---")

            # Simular fraude
            st.session_state["simular_fraude"] = st.toggle(
                "🚨 Simular fraude en login",
                value=st.session_state.get("simular_fraude", False),
                key="toggle_fraude"
            )

            st.markdown("---")
            if st.button("🚪 Cerrar sesión → NPS", use_container_width=True,
                         key="btn_logout", type="secondary"):
                cerrar_sesion_a_nps()

        if st.button("🔄 Reset Demo", use_container_width=True,
                     key="btn_reset", type="secondary"):
            reset_demo(); st.rerun()

        # Indicador de chatbot activo
        if st.session_state.get("chatbot_activo") and st.session_state.get("error_actual"):
            err = st.session_state["error_actual"]
            st.markdown(f"""
            <div style="background:#FFF0F0;border-radius:8px;padding:10px 12px;
                        margin-top:10px;font-size:12px;border-left:3px solid #D32F2F;">
                🤖 <strong>IA activa</strong><br>
                {err.get('icono','🔧')} {err.get('titulo','')}
            </div>
            """, unsafe_allow_html=True)


def _render_guion_sidebar(escenario: str):
    guiones = {
        "A":{"color":"#F0FFF6","border":"#00D261","nombre":"Carlos Mendoza",
             "error":"ERR001","desc":"Cuenta bancaria activa",
             "pasos":["Retiros","IA detecta ERR001","Ir a Cuentas","Inscribir cuenta","Retiro exitoso","→ NPS"]},
        "B":{"color":"#FFFBEB","border":"#F59E0B","nombre":"María López",
             "error":"ERR009","desc":"Restricción SARLAFT",
             "pasos":["Inscribir cuenta","IA detecta ERR009","IA no resuelve","Técnico interviene","→ NPS"]},
        "C":{"color":"#EFF6FF","border":"#3B82F6","nombre":"Roberto Sánchez",
             "error":"ERR011","desc":"Firma electrónica pendiente",
             "pasos":["Cambiar perfil","IA detecta ERR011","Técnico no resuelve","Mesa de ayuda","→ NPS"]},
    }
    g = guiones[escenario]
    pasos_html = "".join([f"<div style='font-size:11px;color:#4a4a4a;padding:2px 0;'>{'✅' if i<1 else '○'} {p}</div>"
                          for i,p in enumerate(g["pasos"])])
    st.markdown(f"""
    <div style="background:{g['color']};border-radius:8px;padding:10px 12px;margin-bottom:4px;
                border-left:3px solid {g['border']};">
        <div style="font-size:11px;font-weight:700;color:#2D2926;">Escenario {escenario}</div>
        <div style="font-size:11px;color:#6B6560;margin-bottom:6px;">
            {g['error']} · {g['desc']}
        </div>
        {pasos_html}
    </div>
    """, unsafe_allow_html=True)


# ── Header del portal ─────────────────────────────────────────────────────────
def render_portal_header():
    current = st.session_state.get("current_page","portal")
    cliente = st.session_state.get("cliente_activo",{})
    nombre_corto = cliente.get("nombre","").split()[0] if cliente else ""

    st.markdown("<div style='border-top:4px solid #003087;'></div>", unsafe_allow_html=True)

    col_logo, col_nav, col_right = st.columns([3, 5, 3])

    with col_logo:
        st.markdown(f"""
        <div style="padding:10px 0;display:flex;align-items:center;">
            {SKANDIA_LOGO_HTML}
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        tabs = [
            ("🏠 MIS PRODUCTOS", "portal"),
            ("💸 RETIROS",       "retiros"),
            ("📊 PORTAFOLIO",    "portafolio"),
        ]
        cols = st.columns(len(tabs))
        for col, (label, page) in zip(cols, tabs):
            with col:
                active = current == page
                t = "primary" if active else "secondary"
                if st.button(label, key=f"nav_tab_{page}", type=t, use_container_width=True):
                    st.session_state["current_page"] = page
                    st.rerun()

    with col_right:
        cols = st.columns([1,1,1,1.5])
        with cols[0]:
            if st.button("💰", key="hdr_ap", use_container_width=True, help="Aportes"):
                st.session_state["current_page"]="retiros"; st.rerun()
        with cols[1]:
            if st.button("↔", key="hdr_ret", use_container_width=True, help="Retiros"):
                st.session_state["current_page"]="retiros"; st.rerun()
        with cols[2]:
            if st.button("📄", key="hdr_doc", use_container_width=True, help="Documentos"):
                st.session_state["current_page"]="documentos"; st.rerun()
        with cols[3]:
            if nombre_corto and st.button(f"👤 {nombre_corto}", key="hdr_user",
                                          use_container_width=True, help="Cerrar sesión"):
                cerrar_sesion_a_nps()

    st.markdown("<hr style='margin:0;border-color:#EBEBEB;'>", unsafe_allow_html=True)


# ── Render de página ──────────────────────────────────────────────────────────
def _render_page(current_page: str):
    mod_path, func_name = ROUTE_MAP.get(current_page, ("pages.portal_cliente","render_portal"))
    mod = importlib.import_module(mod_path)
    getattr(mod, func_name)()


# ── NPS post-sesión ───────────────────────────────────────────────────────────
def _render_nps_post_sesion():
    from modules.nlp_categorizer import clasificar_transaccion, detectar_error_probable, analizar_sentimiento
    from modules.chatbot import activar_chatbot

    ctx      = st.session_state.get("nps_contexto", {})
    cliente  = ctx.get("cliente", {})
    escenario= ctx.get("escenario", "libre")
    origen   = ctx.get("pagina_origen", "portal")
    nombre   = cliente.get("nombre","Cliente") if cliente else "Cliente"

    transaccion_map = {
        "retiros":"Solicité un retiro", "cuentas":"Registros de cuentas bancarias",
        "portafolio":"Gestioné mi portafolio", "documentos":"Consulté documentos/certificados",
        "datos":"Actualicé mis datos",
    }
    nps_map = {"A":9, "B":7, "C":5, "libre":8}
    comentario_map = {
        "A":"El asistente IA resolvió mi problema con el retiro de manera muy eficiente.",
        "B":"Tuve un inconveniente con la inscripción de mi cuenta bancaria.",
        "C":"Mi caso fue escalado a la mesa de ayuda, espero resolución pronto.",
        "libre":"",
    }

    # Header
    st.markdown(f"""
    <div style="border-top:4px solid #003087;"></div>
    <div style="background:white;padding:14px 24px;display:flex;align-items:center;gap:12px;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:24px;">
        {SKANDIA_LOGO_HTML}
        <span style="color:#DCDCDC;">|</span>
        <span style="color:#6B6560;font-size:13px;">Encuesta de satisfacción</span>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1,3,1])
    with col_c:
        if escenario != "libre" and cliente:
            esc_desc = {"A":"Retiro completado ✅","B":"Gestión de cuenta bancaria","C":"Cambio de perfil"}
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:18px 22px;
                        box-shadow:0 2px 10px rgba(0,0,0,0.07);margin-bottom:20px;
                        border-left:4px solid #00D261;">
                <div style="font-size:12px;color:#9E9E9E;">Sesión cerrada · {ctx.get('timestamp','')}</div>
                <div style="font-size:17px;font-weight:700;margin-top:2px;">{nombre}</div>
                <div style="font-size:13px;color:#6B6560;">{esc_desc.get(escenario,'Visita al portal')}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### ¿Cómo fue tu experiencia hoy?")
        st.markdown(f"<p style='color:#6B6560;margin-top:-8px;'>Hola <strong>{nombre}</strong>, "
                    "¿qué tan probable es que recomiendes Skandia?</p>", unsafe_allow_html=True)

        puntuacion = st.slider("Calificación (0–10)", 0, 10,
                               nps_map.get(escenario, 8), key="nps_slider_post")

        if puntuacion <= 6:   seg,color = "Detractor","#D32F2F"
        elif puntuacion <= 8: seg,color = "Pasivo",   "#F59E0B"
        else:                 seg,color = "Promotor", "#00D261"

        st.markdown(f"""
        <span style="background:{color};color:white;padding:4px 14px;border-radius:20px;
                     font-size:13px;font-weight:600;">{seg} — {puntuacion}/10</span>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        transacciones = [
            "Solicité un retiro","Realicé un aporte","Consulté mi saldo",
            "Gestioné mi portafolio","Consulté documentos/certificados",
            "Registros de cuentas bancarias","Actualicé mis datos","Otras"
        ]
        trans_default = transaccion_map.get(origen,"Otras")
        idx_t = transacciones.index(trans_default) if trans_default in transacciones else 0
        transaccion = st.selectbox("¿Qué transacción realizaste?", transacciones, index=idx_t)
        comentario  = st.text_area("Cuéntanos tu experiencia:",
                                   value=comentario_map.get(escenario,""),
                                   placeholder="¿Tuviste algún inconveniente?", height=90)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Enviar evaluación", type="primary",
                         use_container_width=True, key="enviar_nps_final"):
                cat = clasificar_transaccion(comentario) if comentario else transaccion
                sent= analizar_sentimiento(comentario)
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:18px 22px;
                            box-shadow:0 2px 10px rgba(0,0,0,0.07);margin-top:14px;">
                    <h4 style="margin:0 0 10px;">✅ ¡Gracias por tu evaluación!</h4>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <span style="background:{color};color:white;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:600;">{seg}</span>
                        <span style="background:#E3F2FD;color:#003087;padding:3px 12px;border-radius:20px;font-size:12px;">📌 {cat}</span>
                        <span style="background:#F3E5F5;color:#6A1B9A;padding:3px 12px;border-radius:20px;font-size:12px;">💭 {sent}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if puntuacion <= 6:
                    st.markdown("""<div class='sk-alert-critical blink-alert' style='margin-top:12px;'>
                        🔴 <strong>Caso prioritario.</strong> Un asesor te contactará en 2 horas hábiles.
                    </div>""", unsafe_allow_html=True)
                    ca, cb = st.columns(2)
                    with ca:
                        if st.button("💬 Chat inmediato", type="primary",
                                     use_container_width=True, key="nps_chat_go"):
                            # Determinar error según escenario o comentario
                            err_map = {"A": "ERR001", "B": "ERR009", "C": "ERR011"}
                            err_id = err_map.get(escenario) or \
                                     detectar_error_probable(comentario, cat).get("error_id", "ERR001")
                            st.session_state.update({
                                "autenticado": True,
                                "cliente_activo": cliente if cliente else CLIENTES_DEMO[0],
                                "current_page": "portal",
                                "tecnico_conectado": False,
                                "chatbot_minimizado": False,
                            })
                            activar_chatbot(err_id, "Encuesta NPS")
                            st.rerun()
                    with cb:
                        if st.button("📞 Solicitar llamada", use_container_width=True, key="nps_call_go"):
                            st.success("📞 Llamada programada en los próximos 10 minutos.")
                else:
                    st.success("🎉 ¡Gracias! Tu satisfacción impulsa nuestra mejora continua.")
        with col2:
            if st.button("🔄 Nueva sesión demo", use_container_width=True, key="nueva_sesion"):
                reset_demo(); st.rerun()


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    init_state()
    apply_styles()

    from modules.chatbot import check_auto_advance, render_chatbot_flotante, render_chatbot_panel

    # Auto-avance de pasos en cada render
    if check_auto_advance():
        st.rerun()

    render_sidebar()

    autenticado  = st.session_state.get("autenticado", False)
    current_page = st.session_state.get("current_page", "login")
    chatbot_activo    = st.session_state.get("chatbot_activo", False)
    chatbot_minimizado= st.session_state.get("chatbot_minimizado", False)

    # ── NPS post-sesión ──
    if current_page == "nps_post":
        _render_nps_post_sesion()
        return

    # ── Login ──
    if not autenticado or current_page == "login":
        from pages.login import render_login
        render_login()
        if chatbot_activo and not chatbot_minimizado:
            st.markdown("---")
            render_chatbot_panel()
        else:
            render_chatbot_flotante()
        return

    # ── Portal autenticado ──
    render_portal_header()

    # Layout: 2 columnas cuando chatbot activo y no minimizado
    if chatbot_activo and not chatbot_minimizado:
        col_main, col_chat = st.columns([62, 38])
        with col_main:
            _render_page(current_page)
        with col_chat:
            st.markdown("""
            <div style="background:white;border-radius:14px;
                        box-shadow:0 4px 24px rgba(0,0,0,0.10);
                        padding:0;overflow:hidden;position:sticky;top:80px;">
            """, unsafe_allow_html=True)
            render_chatbot_panel()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        _render_page(current_page)
        render_chatbot_flotante()

    # Indicador de página en sidebar
    with st.sidebar:
        labels = {
            "portal":"🏠 Mi Portal","retiros":"💰 Retiros","cuentas":"🏦 Cuentas",
            "portafolio":"📊 Portafolio","documentos":"📄 Documentos","datos":"⚙️ Mis Datos",
            "dashboard":"📈 Dashboard","control_tower":"🎯 Control Tower","tecnico":"👨‍💻 Técnico",
        }
        st.markdown(f"""
        <div style="background:#F4F2EE;border-radius:8px;padding:8px 12px;
                    text-align:center;font-size:12px;color:#6B6560;margin-top:8px;">
            📍 {labels.get(current_page, current_page)}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
