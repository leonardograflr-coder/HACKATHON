"""
pages/login.py
Página de login del portal Skandia con OTP, manejo de errores y simulación de fraude.
"""

import streamlit as st
import time
from modules.chatbot import activar_chatbot


USUARIOS_DEMO = {
    "80123456":   {"password": "1234", "cliente_id": "CLI001"},
    "52234567":   {"password": "1234", "cliente_id": "CLI002"},
    "19345678":   {"password": "1234", "cliente_id": "CLI003"},
    "43456789":   {"password": "1234", "cliente_id": "CLI004"},
    "71567890":   {"password": "1234", "cliente_id": "CLI005"},
    "1033799087": {"password": "1234", "cliente_id": "CLI006"},
    "demo":       {"password": "demo", "cliente_id": "CLI001"},
}

DOCUMENTO_ESCENARIO = {
    "80123456": "A",
    "52234567": "B",
    "19345678": "C",
}

OTP_VALIDO = "123456"


def render_login():
    """Renderiza la página de login completa."""
    from data.clientes_demo import get_cliente_by_id

    if "login_intentos" not in st.session_state:
        st.session_state["login_intentos"] = 0
    if "login_step" not in st.session_state:
        st.session_state["login_step"] = "credenciales"
    if "login_doc_temp" not in st.session_state:
        st.session_state["login_doc_temp"] = ""

    # Detectar simulación de fraude desde sidebar
    simular_fraude = st.session_state.get("simular_fraude", False)
    if simular_fraude:
        _render_alerta_fraude()
        return

    if st.session_state["login_step"] == "credenciales":
        _render_form_credenciales()
    elif st.session_state["login_step"] == "otp":
        _render_verificacion_otp()
    elif st.session_state["login_step"] == "exito":
        _render_login_exitoso()


def _render_form_credenciales():
    """Renderiza el formulario de credenciales."""
    intentos = st.session_state.get("login_intentos", 0)
    bloqueado = intentos >= 3

    # Layout centrado con logo
    from config.brand import SKANDIA_LOGO_HTML
    st.markdown(f"""
    <div style="border-top: 4px solid #003087; margin-bottom: 0;"></div>
    <div style="background:white; padding: 14px 32px; display:flex; align-items:center; gap:16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        {SKANDIA_LOGO_HTML}
        <span style="color:#ddd;margin:0 4px;">|</span>
        <span style="color:#6B6560;font-size:15px;">Portal Clientes</span>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

        # Card de login
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:40px 36px;
                    box-shadow:0 4px 24px rgba(0,0,0,0.10);max-width:460px;margin:auto;">
        """, unsafe_allow_html=True)

        from config.brand import SKANDIA_LOGO_HTML_LARGE as _LOGO_L
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:24px;padding-bottom:8px;
                    border-bottom:1px solid #F0F0F0;">
            {_LOGO_L}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Bienvenido")
        st.markdown("<p style='color:#6B6560;margin-top:-12px;'>Ingresa a tu portal de inversiones</p>", unsafe_allow_html=True)

        if bloqueado:
            st.markdown("""
            <div class='sk-alert-critical blink-alert' style='margin:12px 0;'>
                🔒 <strong>Portal bloqueado por seguridad</strong><br>
                <span style='font-size:13px;'>Demasiados intentos fallidos. Recupera tu contraseña para continuar.</span>
            </div>
            """, unsafe_allow_html=True)
            activar_chatbot("ERR013", "Login")

        with st.form("form_login", clear_on_submit=False):
            recordar = st.checkbox("Recordar mi usuario", value=False)
            documento = st.text_input(
                "Número de documento",
                placeholder="Ingresa tu cédula sin puntos",
                disabled=bloqueado
            )
            contrasena = st.text_input(
                "Contraseña",
                type="password",
                placeholder="••••••••",
                disabled=bloqueado
            )

            submitted = st.form_submit_button(
                "Ingresar" if not bloqueado else "🔒 Portal bloqueado",
                use_container_width=True,
                type="primary",
                disabled=bloqueado
            )

        if submitted and not bloqueado:
            _procesar_login(documento.strip(), contrasena.strip())

        # Links secundarios
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("¿Olvidaste tu contraseña?", key="forgot_pwd"):
                st.info("📧 Te enviamos un correo a tu dirección registrada con el enlace de restablecimiento.")
        with col_b:
            if st.button("Regístrate aquí", key="register_btn"):
                st.info("🔗 Para registrarte necesitas tu número de contrato Skandia. Contacta a tu Financial Planner.")

        if bloqueado:
            if st.button("🔑 Recuperar contraseña", type="primary", use_container_width=True, key="recover_btn"):
                st.success("📧 Correo de recuperación enviado a tu dirección registrada. Revisa tu bandeja en 5 minutos.")
                st.session_state["login_intentos"] = 0
                st.session_state["chatbot_activo"] = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Hint demo
        with st.expander("💡 Credenciales de demo"):
            st.markdown("""
            | Usuario | Contraseña | Escenario |
            |---------|-----------|-----------|
            | `80123456` | `1234` | A — Carlos (ERR001) |
            | `52234567` | `1234` | B — María (ERR009) |
            | `19345678` | `1234` | C — Roberto (ERR011) |
            | `1033799087` | `1234` | Libre — Andres |
            | `demo` | `demo` | Libre |
            """)


def _procesar_login(documento: str, contrasena: str):
    """Valida credenciales y maneja el flujo de login."""
    from data.clientes_demo import get_cliente_by_id

    usuario = USUARIOS_DEMO.get(documento)

    if usuario and usuario["password"] == contrasena:
        cliente = get_cliente_by_id(usuario["cliente_id"])
        st.session_state["cliente_activo"] = cliente
        st.session_state["login_doc_temp"] = documento
        st.session_state["login_step"] = "otp"
        st.session_state["login_intentos"] = 0
        # Auto-asignar escenario según documento
        escenario = DOCUMENTO_ESCENARIO.get(documento, "libre")
        st.session_state["escenario_demo"] = escenario
        st.session_state["escenario_anterior"] = None  # fuerza _aplicar_escenario
        st.rerun()
    else:
        st.session_state["login_intentos"] = st.session_state.get("login_intentos", 0) + 1
        intentos = st.session_state["login_intentos"]

        if intentos >= 3:
            st.error("🔒 Portal bloqueado. Has superado el número máximo de intentos.")
            activar_chatbot("ERR013", "Login")
        else:
            restantes = 3 - intentos
            st.error(f"❌ Credenciales incorrectas. Te quedan {restantes} intento(s).")


def _render_verificacion_otp():
    """Renderiza la pantalla de verificación OTP."""
    from config.brand import SKANDIA_LOGO_HTML
    st.markdown(f"""
    <div style="border-top: 4px solid #003087; margin-bottom: 0;"></div>
    <div style="background:white; padding: 14px 32px; display:flex; align-items:center; gap:16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        {SKANDIA_LOGO_HTML}
        <span style="color:#ddd;margin:0 4px;">|</span>
        <span style="color:#6B6560;font-size:15px;">Verificación de seguridad</span>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.2, 1])

    with col_center:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:white;border-radius:16px;padding:40px 36px;
                    box-shadow:0 4px 24px rgba(0,0,0,0.10);text-align:center;">
            <div style="font-size:64px;margin-bottom:16px;">🔐</div>
            <h3 style="color:#2D2926;">Validación de seguridad</h3>
            <p style="color:#6B6560;">Ingresa el código enviado a tu celular y correo registrados.</p>
        </div>
        """, unsafe_allow_html=True)

        # Timer simulado
        st.markdown("""
        <div style="background:#f0f7ff;border-radius:8px;padding:12px;text-align:center;
                    margin:16px 0;border:1px solid #E3F2FD;">
            ⏱️ Código válido por: <strong style="color:#003087;">04:58</strong>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_otp"):
            codigo = st.text_input(
                "Escribe el código de verificación",
                placeholder="Ej: 123456",
                max_chars=6
            )
            col1, col2 = st.columns(2)
            with col1:
                reenviar = st.form_submit_button("🔄 Reenviar código", use_container_width=True)
            with col2:
                verificar = st.form_submit_button("✅ Verificar", use_container_width=True, type="primary")

        if verificar:
            if codigo == OTP_VALIDO:
                st.session_state["login_step"] = "exito"
                st.rerun()
            else:
                st.error("❌ Código incorrecto. Verifica e intenta nuevamente.")
                activar_chatbot("ERR017", "Validación de seguridad")

        if reenviar:
            st.success("📱 Código reenviado a tu celular y correo registrado.")

        st.markdown(
            "<p style='text-align:center;margin-top:12px;'>"
            "<a href='#' style='color:#00D261;font-size:13px;'>¿No has recibido el código de seguridad?</a>"
            "</p>",
            unsafe_allow_html=True
        )

        # Hint demo
        st.info("💡 **Demo:** El código válido es **`123456`**")

        if st.button("← Volver al login", key="back_login"):
            st.session_state["login_step"] = "credenciales"
            st.rerun()


def _render_login_exitoso():
    """Renderiza la pantalla de éxito de login y redirige al portal."""
    cliente = st.session_state.get("cliente_activo", {})
    nombre = cliente.get("nombre", "Cliente") if cliente else "Cliente"

    col_l, col_center, col_r = st.columns([1, 1.2, 1])
    with col_center:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:40px 36px;
                    box-shadow:0 4px 24px rgba(0,0,0,0.10);text-align:center;margin-top:60px;">
            <div style="width:80px;height:80px;background:#E8F5E9;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 16px;font-size:40px;">✅</div>
            <h3 style="color:#2D2926;">¡Validación exitosa!</h3>
            <p style="color:#6B6560;">Tu identidad ha sido validada con éxito.</p>
            <p style="color:#6B6560;font-size:13px;">Ahora puedes continuar con el portal.</p>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"¡Bienvenido/a, **{nombre}**! Redirigiendo al portal...")
        time.sleep(1)

        st.session_state["autenticado"] = True
        st.session_state["current_page"] = "portal"
        st.rerun()


def _render_alerta_fraude():
    """Renderiza la alerta de actividad fraudulenta detectada."""
    st.markdown("""
    <div style="background:#FFEBEE;border:2px solid #D32F2F;border-radius:12px;
                padding:32px;text-align:center;margin:20px 0;">
        <div style="font-size:64px;">🚨</div>
        <h2 style="color:#D32F2F;">¡Actividad sospechosa detectada!</h2>
        <p style="color:#2D2926;font-size:16px;">
            Se detectó un intento de acceso desde un dispositivo o ubicación inusual.
            <br>Tu cuenta ha sido <strong>bloqueada temporalmente</strong> por seguridad.
        </p>
        <div style="background:white;border-radius:8px;padding:16px;margin:16px 0;text-align:left;">
            <p>📍 Ubicación detectada: <strong>IP Desconocida</strong></p>
            <p>💻 Dispositivo: <strong>Nuevo — no reconocido</strong></p>
            <p>🕐 Hora del intento: <strong>Ahora</strong></p>
        </div>
        <p style="color:#D32F2F;font-weight:600;">
            📞 Línea de fraudes: 601-326-7777 (disponible 24/7)
        </p>
    </div>
    """, unsafe_allow_html=True)

    activar_chatbot("ERR014", "Login")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 Llamar a línea de fraudes", type="primary", use_container_width=True):
            st.info("Conectando con la línea de fraudes: 601-326-7777")
    with col2:
        if st.button("✅ Fui yo — Verificar identidad", use_container_width=True):
            st.session_state["simular_fraude"] = False
            st.session_state["login_step"] = "otp"
            st.rerun()

    if st.button("← Cancelar simulación de fraude"):
        st.session_state["simular_fraude"] = False
        st.rerun()
