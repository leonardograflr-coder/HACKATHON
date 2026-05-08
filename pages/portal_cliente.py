"""
pages/portal_cliente.py
Páginas del portal cliente: Dashboard, Retiros, Cuentas, Portafolio, Documentos, Mis Datos, NPS.
"""

import streamlit as st
import datetime
import plotly.graph_objects as go
from modules.chatbot import activar_chatbot
from modules.report_generator import registrar_accion_log
from data.clientes_demo import get_fp_by_id, HISTORIAL_RETIROS


@st.dialog("✅ Retiro procesado exitosamente")
def _popup_retiro_exitoso(monto: float):
    """Modal de confirmación con detalles completos del retiro."""
    cliente  = st.session_state.get("cliente_activo", {})
    cuentas  = cliente.get("cuentas_bancarias", [])
    cuenta   = cuentas[0] if cuentas else {"banco": "Banco Demo", "tipo": "Ahorros", "numero": "****0000"}
    txn_num  = st.session_state.setdefault(
        "retiro_txn_num",
        f"TXN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    now       = datetime.datetime.now()
    fecha_dis = (now + datetime.timedelta(days=2)).strftime("%d/%m/%Y")

    st.markdown("""
    <div style="text-align:center;padding:6px 0 14px;">
        <div style="width:60px;height:60px;background:#E8F5E9;border-radius:50%;
                    display:inline-flex;align-items:center;justify-content:center;
                    font-size:30px;margin-bottom:10px;">✅</div>
        <p style="color:#6B6560;font-size:13px;margin:0;">Tu solicitud fue registrada exitosamente.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:10px;padding:14px;margin-bottom:14px;">
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;width:50%;">N° Transacción</td>
                <td style="font-weight:600;color:#2D2926;text-align:right;">{txn_num}</td>
            </tr>
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;">Monto</td>
                <td style="font-weight:700;font-size:15px;color:#2D2926;text-align:right;">${monto:,.2f} COP</td>
            </tr>
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;">Contrato</td>
                <td style="font-weight:500;text-align:right;">#{cliente.get('numero_contrato','')}</td>
            </tr>
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;">Cuenta destino</td>
                <td style="font-weight:500;text-align:right;">{cuenta.get('banco','')} · {cuenta.get('numero','')}</td>
            </tr>
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;">Fecha solicitud</td>
                <td style="font-weight:500;text-align:right;">{now.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
            <tr style="border-bottom:1px solid #F0F0F0;">
                <td style="color:#9E9E9E;padding:6px 0;">Fecha disponible</td>
                <td style="font-weight:500;text-align:right;">{fecha_dis}</td>
            </tr>
            <tr>
                <td style="color:#9E9E9E;padding:6px 0;">Estado</td>
                <td style="text-align:right;">
                    <span style="background:#E8F5E9;color:#00A84F;padding:3px 10px;
                                 border-radius:12px;font-weight:600;font-size:12px;">✅ Procesado</span>
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Aceptar", type="primary", use_container_width=True, key="popup_retiro_aceptar"):
        st.session_state["retiro_exitoso"]  = False
        st.session_state["retiro_paso"]     = 1
        st.session_state["retiro_otp_modal"]= False
        st.session_state.pop("retiro_txn_num", None)
        st.session_state["current_page"]    = "portal"
        st.rerun()


@st.dialog("📋 Solicitudes pendientes — Perfil de inversión")
def _popup_solicitudes_pendientes():
    st.markdown("""
    <div style="text-align:center;padding:10px 0 16px;">
        <div style="font-size:48px;margin-bottom:10px;">📋</div>
        <h4 style="color:#2D2926;margin:0 0 8px;">Solicitudes pendientes</h4>
    </div>
    """, unsafe_allow_html=True)
    st.info("No tienes solicitudes pendientes de aceptación de términos y condiciones en este momento.")
    st.markdown("""
    <p style="color:#6B6560;font-size:13px;text-align:center;margin-top:8px;">
        Es posible que la solicitud de cambio de perfil no haya quedado registrada correctamente.
        Por favor procede a aceptar los Términos y Condiciones para continuar.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Entendido", type="primary", use_container_width=True, key="popup_sol_ok"):
        st.session_state["err011_vio_solicitudes"] = True
        st.rerun()


@st.dialog("📋 Términos y Condiciones — Cambio de Perfil de Inversión")
def _popup_terminos_condiciones():
    st.markdown("""
    <div style="background:#F8F9FA;border-radius:10px;padding:14px;margin-bottom:14px;
                max-height:180px;overflow-y:auto;font-size:12px;color:#4a4a4a;line-height:1.6;">
        <strong>TÉRMINOS Y CONDICIONES PARA CAMBIO DE PERFIL DE INVERSIÓN</strong><br><br>
        Al aceptar estos términos usted confirma que:<br>
        1. Ha leído y comprendido las condiciones del nuevo perfil de inversión.<br>
        2. Entiende los riesgos y su tolerancia al riesgo asociada.<br>
        3. Autoriza a Skandia Colombia S.A. a reasignar sus fondos según el nuevo perfil.<br>
        4. Esta decisión es voluntaria y modificable siguiendo el proceso establecido.<br>
        5. Skandia Colombia S.A. no se responsabiliza por pérdidas derivadas del perfil elegido.<br><br>
        Normativa: Circular Externa 006/2016 SFC y Decreto 2555/2010.
    </div>
    """, unsafe_allow_html=True)
    acepto = st.checkbox(
        "Acepto los términos y condiciones del cambio de perfil de inversión",
        key="tc_err011_checkbox"
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", use_container_width=True, key="tc_cancelar_btn"):
            st.rerun()
    with col2:
        if st.button(
            "Aceptar y continuar →", type="primary",
            use_container_width=True, key="tc_aceptar_btn",
            disabled=not acepto
        ):
            st.session_state["err011_acepto_tc"] = True
            st.session_state["_show_otp_tc"] = True
            st.rerun()


@st.dialog("🔐 Validación OTP — Aceptación de Términos")
def _popup_otp_tc():
    st.markdown("""
    <div style="text-align:center;padding:8px 0 14px;">
        <div style="font-size:44px;margin-bottom:10px;">🔐</div>
        <p style="color:#6B6560;font-size:13px;margin:0;">
            Ingresa el código enviado a tu celular y correo registrados para validar la aceptación.
        </p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("form_otp_tc"):
        codigo = st.text_input("Código OTP", placeholder="Ej: 123456", max_chars=6)
        col1, col2 = st.columns(2)
        with col1:
            reenviar = st.form_submit_button("🔄 Reenviar", use_container_width=True)
        with col2:
            verificar = st.form_submit_button("✅ Verificar", type="primary", use_container_width=True)
    if verificar:
        if codigo == "123456":
            st.session_state["err011_otp_verificado"] = True
            st.session_state.pop("_show_otp_tc", None)
            st.rerun()
        else:
            st.error("❌ Código incorrecto. Intenta nuevamente.")
    if reenviar:
        st.success("📱 Código reenviado a tu celular y correo registrado.")
    st.info("💡 Demo: código válido → `123456`")


def _cerrar_sesion():
    """Cierra sesión y navega a la encuesta NPS — sin circular import."""
    st.session_state["nps_contexto"] = {
        "cliente":       st.session_state.get("cliente_activo", {}),
        "escenario":     st.session_state.get("escenario_demo", "libre"),
        "pagina_origen": st.session_state.get("current_page", "portal"),
        "timestamp":     datetime.datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state["autenticado"]  = False
    st.session_state["current_page"] = "nps_post"
    st.rerun()


# ─────────────────────────────────────────────
# PÁGINA 1: MI PORTAL
# ─────────────────────────────────────────────
def render_portal():
    cliente = st.session_state.get("cliente_activo", {})
    if not cliente:
        st.warning("No hay cliente seleccionado.")
        return

    nombre = cliente.get("nombre", "Cliente")
    fp = get_fp_by_id(cliente.get("fp_asignado", "FP001"))
    escenario = st.session_state.get("escenario_demo", "libre")

    # Bienvenida
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:20px 24px;
                box-shadow:0 2px 12px rgba(0,0,0,0.07);margin-bottom:20px;
                border-left:4px solid #00D261;">
        <div style="font-size:20px;font-weight:700;color:#2D2926;">👋 Bienvenido/a, {nombre}</div>
        <div style="color:#6B6560;font-size:13px;margin-top:4px;">
            Contrato: <strong>{cliente.get('contrato','')}</strong> &nbsp;·&nbsp;
            FP: <strong>{fp.get('nombre','')}</strong> &nbsp;·&nbsp;
            <span style="color:#00D261;font-weight:600;">● {cliente.get('estado_contrato','Activo')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Accesos rápidos — 3 columnas iguales
    col1, col2, col3 = st.columns(3)
    for col, icon, label, page in [
        (col1, "💰", "APORTES",   "retiros"),
        (col2, "↔",  "RETIROS",   "retiros"),
        (col3, "📄", "DOCUMENTOS","documentos"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:20px;text-align:center;
                        box-shadow:0 2px 8px rgba(0,0,0,0.07);border:1.5px solid #F0F0F0;
                        margin-bottom:8px;">
                <div style="font-size:32px;margin-bottom:8px;">{icon}</div>
                <div style="font-weight:700;font-size:13px;letter-spacing:0.04em;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ir a {label.title()}", key=f"btn_{page}_{label}_home",
                         use_container_width=True, type="secondary"):
                st.session_state["current_page"] = page
                st.rerun()

    st.markdown("---")

    # Métricas
    saldo = cliente.get("saldo", 0)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("💼 Saldo estimado",    f"${saldo:,.0f} COP",  delta="+2.3%")
    with m2: st.metric("📥 Último aporte",     f"${cliente.get('ultimo_aporte',0):,.0f} COP")
    with m3: st.metric("📤 Último retiro",     f"${cliente.get('ultimo_retiro',0):,.0f} COP" if cliente.get("ultimo_retiro") else "Sin retiros")
    with m4: st.metric("📋 Estado contrato",   cliente.get("estado_contrato", "Activo"))

    # Mini portafolio
    st.markdown("---")
    st.markdown("#### Distribución del portafolio")
    portafolio = cliente.get("portafolio", [])
    if portafolio:
        col_g, col_t = st.columns([1, 1])
        with col_g:
            fig = go.Figure(go.Pie(
                labels=[p["fondo"] for p in portafolio],
                values=[p["porcentaje"] for p in portafolio],
                marker_colors=["#00D261", "#2D2926", "#003087", "#F0EEE9"],
                hole=0.42, textinfo="percent"
            ))
            fig.update_layout(margin=dict(t=20,b=20,l=0,r=0), height=220,
                              showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        with col_t:
            for p in portafolio:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:7px 0;
                            border-bottom:1px solid #F5F5F5;font-size:13px;">
                    <span>🟢 {p['fondo']}</span>
                    <span style="font-weight:600;">{p['porcentaje']}%</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Botones de acción — misma fila, mismo ancho
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🎬 Simular error del escenario", use_container_width=True, type="primary", key="sim_error_home"):
            _simular_error_por_escenario(escenario)
    with col_b:
        if st.button("📊 Ver Dashboard Analítico", use_container_width=True, key="ir_dashboard_home"):
            st.session_state["current_page"] = "dashboard"; st.rerun()
    with col_c:
        if st.button("🚪 Cerrar sesión", use_container_width=True, key="logout_home"):
            _cerrar_sesion()


def _simular_error_por_escenario(escenario: str):
    if escenario == "A":
        activar_chatbot("ERR001", "Mi Portal")
        st.session_state["current_page"] = "retiros"
    elif escenario == "B":
        activar_chatbot("ERR009", "Mi Portal")
        st.session_state["current_page"] = "cuentas"
    elif escenario == "C":
        activar_chatbot("ERR011", "Mi Portal")
        st.session_state["current_page"] = "portafolio"
    else:
        activar_chatbot("ERR002", "Mi Portal")
        st.session_state["current_page"] = "retiros"
    log = registrar_accion_log(f"Simulación iniciada — Escenario {escenario}")
    st.session_state.setdefault("chatbot_log", []).append(log)
    st.rerun()


# ─────────────────────────────────────────────
# PÁGINA 2: RETIROS
# ─────────────────────────────────────────────
def render_retiros():
    cliente = st.session_state.get("cliente_activo", {})
    if not cliente:
        st.warning("No hay cliente seleccionado.")
        return

    # Mostrar popup modal si el retiro fue confirmado
    if st.session_state.get("retiro_exitoso", False):
        _popup_retiro_exitoso(st.session_state.get("retiro_monto", 0))

    if "retiro_paso" not in st.session_state:
        st.session_state["retiro_paso"] = 1

    paso    = st.session_state["retiro_paso"]
    saldo   = cliente.get("saldo", 0)
    contrato = cliente.get("numero_contrato", "667463")
    cuentas = cliente.get("cuentas_bancarias", [])

    # Layout 2 columnas — izquierda decorativa, derecha formulario
    col_izq, col_der = st.columns([4, 6])

    with col_izq:
        st.markdown(f"""
        <div style="background:#E8F5E9;border-radius:12px;padding:36px 20px;
                    min-height:440px;text-align:center;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;">
            <div style="font-size:64px;margin-bottom:16px;">💸</div>
            <h3 style="color:#2D2926;margin:0 0 8px;">Retiros</h3>
            <p style="color:#6B6560;font-size:13px;line-height:1.5;max-width:200px;">
                Gestiona el desembolso de tu dinero de forma ágil, fácil y segura.
            </p>
            <a href="#" style="color:#00D261;font-size:13px;margin-top:16px;text-decoration:none;">
                ⓪ Ayuda
            </a>
            <div style="margin-top:24px;background:white;border-radius:10px;padding:14px 20px;width:100%;">
                <div style="font-size:11px;color:#9E9E9E;text-transform:uppercase;letter-spacing:0.06em;">
                    Saldo disponible
                </div>
                <div style="font-size:22px;font-weight:700;color:#2D2926;margin-top:2px;">
                    ${saldo:,.2f}
                </div>
                <div style="font-size:11px;color:#9E9E9E;">COP</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        # Barra de progreso
        pct = {1: 33, 2: 66, 3: 100}[paso]
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:13px;color:#6B6560;font-weight:500;">Paso {paso} de 3</span>
            <span style="font-size:12px;color:#9E9E9E;">{pct}%</span>
        </div>
        <div style="background:#ECECEC;border-radius:4px;height:6px;margin-bottom:24px;">
            <div style="background:#00D261;width:{pct}%;height:6px;border-radius:4px;
                        transition:width 0.3s ease;"></div>
        </div>
        """, unsafe_allow_html=True)

        if paso == 1:
            _render_retiro_paso1(cliente, saldo, contrato)
        elif paso == 2:
            _render_retiro_paso2(cliente, saldo, cuentas)
        elif paso == 3:
            _render_retiro_paso3(cliente, cuentas)

    st.markdown("---")
    st.markdown("#### 📋 Historial de retiros")
    _render_historial_retiros(cliente)


def _render_retiro_paso1(cliente, saldo, contrato):
    st.markdown("#### ¿De dónde vas a retirar?")

    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:10px;padding:16px;margin:12px 0;
                border:1.5px solid #E8F5E9;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="color:#00D261;font-size:18px;">⬤</span>
            <div>
                <div style="font-weight:600;font-size:14px;">Potencializar mi inversión</div>
                <div style="font-size:12px;color:#6B6560;">P. Voluntaria | Ahorro e inversión | #{contrato}</div>
                <div style="font-size:20px;font-weight:700;color:#2D2926;margin-top:4px;">
                    ${saldo:,.2f} COP
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    vivienda = st.toggle("¿Retiro para vivienda con beneficio tributario?", value=False)
    st.session_state["retiro_vivienda"] = vivienda

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", key="cancel_retiro_1", use_container_width=True):
            st.session_state["current_page"] = "portal"; st.rerun()
    with col2:
        if st.button("Empezar →", key="empezar_retiro", type="primary", use_container_width=True):
            log = registrar_accion_log(f"Inicio proceso de retiro — #{contrato}")
            st.session_state.setdefault("chatbot_log",[]).append(log)
            st.session_state["retiro_paso"] = 2
            st.rerun()


def _render_retiro_paso2(cliente, saldo, cuentas):
    contrato = cliente.get("numero_contrato","667463")

    st.markdown(f"""
    <div style="font-size:12px;color:#9E9E9E;margin-bottom:12px;">
        Inicio / Retiros / P. Voluntaria #{contrato}
    </div>
    <div style="margin-bottom:4px;font-size:13px;color:#6B6560;">Saldo total disponible</div>
    <div style="font-size:28px;font-weight:700;color:#2D2926;margin-bottom:4px;">${saldo:,.2f} COP</div>
    <a href="#" style="color:#00D261;font-size:13px;">Ver detalle</a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ¿Qué tipo de retiro harás?")

    tipo = st.radio(
        "Tipo:",
        ["especifico", "total"],
        format_func=lambda x: "💵 Retirar un monto específico" if x == "especifico" else "💸 Retiro total",
        horizontal=True
    )
    st.session_state["retiro_tipo"] = tipo

    disponible = saldo * 0.997
    if tipo == "especifico":
        monto = st.number_input(
            "Monto (COP)",
            min_value=50000, max_value=int(disponible),
            value=min(500000, int(disponible)), step=50000, format="%d"
        )
        st.session_state["retiro_monto"] = monto
        st.markdown(f"""
        <div style="font-size:12px;color:#6B6560;margin-top:4px;">
            Disponible para retirar: <strong>${disponible:,.2f} COP</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        monto = disponible
        st.session_state["retiro_monto"] = disponible

    fecha_disp = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d/%m/%Y")
    st.markdown(f"""
    <div style="background:#E3F2FD;border-radius:8px;padding:10px 14px;margin:14px 0;font-size:13px;">
        📅 Tu retiro estará disponible el <strong>{fecha_disp}</strong> después de las 3:00 p.m.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="back_paso2", use_container_width=True):
            st.session_state["retiro_paso"] = 1; st.rerun()
    with col2:
        if st.button("Continuar →", key="continuar_paso2", type="primary", use_container_width=True):
            _verificar_paso2(cliente, tipo, monto, cuentas, saldo)


def _verificar_paso2(cliente, tipo, monto, cuentas, saldo):
    escenario = st.session_state.get("escenario_demo", "libre")
    # Si no tiene cuentas, activar ERR001 (aplica para escenario A y B inicial)
    if not cuentas:
        activar_chatbot("ERR001", "Retiros")
        log = registrar_accion_log("ERROR: Sin cuenta bancaria inscrita")
        st.session_state.setdefault("chatbot_log",[]).append(log)
        st.rerun(); return
    if monto > saldo:
        activar_chatbot("ERR002", "Retiros")
        st.rerun(); return
    log = registrar_accion_log(f"Paso 2 OK — ${monto:,.0f} COP ({tipo})")
    st.session_state.setdefault("chatbot_log",[]).append(log)
    st.session_state["retiro_paso"] = 3
    st.rerun()


def _render_retiro_paso3(cliente, cuentas):
    contrato = cliente.get("numero_contrato","667463")
    nombre   = cliente.get("nombre","")
    monto    = st.session_state.get("retiro_monto", 500000)
    cargos   = monto * 0.004
    fecha_disp = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d/%m/%Y")
    cuenta   = cuentas[0] if cuentas else {"banco":"Banco Demo","tipo":"Ahorros","numero":"****0000"}

    st.markdown(f"""
    <div style="font-size:12px;color:#9E9E9E;margin-bottom:12px;">
        Inicio / Retiros / P. Voluntaria #{contrato} / Confirmar
    </div>
    """, unsafe_allow_html=True)

    # Banner advertencia
    st.markdown("""
    <div style="background:#FFF8E1;border:1px solid #FFB300;border-radius:8px;
                padding:12px 16px;margin-bottom:16px;font-size:13px;display:flex;gap:8px;">
        ⚠️ <span>Una vez en proceso de tramitado, <strong>no se podrá modificar ni cancelar</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # Resumen
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:20px 24px;
                box-shadow:0 2px 12px rgba(0,0,0,0.07);">
        <div style="font-size:14px;font-weight:700;margin-bottom:14px;color:#2D2926;">
            Resumen de tu retiro
        </div>
        <table style="width:100%;font-size:14px;border-collapse:collapse;">
            <tr style="border-bottom:1px solid #F5F5F5;">
                <td style="color:#9E9E9E;padding:8px 0;width:45%;">Especie</td>
                <td style="font-weight:500;">FPV Strategist Liquidez Col</td>
            </tr>
            <tr style="border-bottom:1px solid #F5F5F5;">
                <td style="color:#9E9E9E;padding:8px 0;">Fecha esperada</td>
                <td style="font-weight:500;">{fecha_disp}</td>
            </tr>
            <tr style="border-bottom:1px solid #F5F5F5;">
                <td style="color:#9E9E9E;padding:8px 0;">Valor del retiro</td>
                <td style="font-size:18px;font-weight:700;color:#2D2926;">${monto:,.2f} COP</td>
            </tr>
            <tr style="border-bottom:1px solid #F5F5F5;">
                <td style="color:#9E9E9E;padding:8px 0;">Cargos e impuestos</td>
                <td style="color:#D32F2F;">${cargos:,.2f} COP</td>
            </tr>
            <tr style="border-bottom:1px solid #F5F5F5;">
                <td style="color:#9E9E9E;padding:8px 0;">Destinatario</td>
                <td style="font-weight:500;">{cuenta['banco']} | {cuenta['numero']} | {cuenta['tipo']}</td>
            </tr>
            <tr>
                <td style="color:#9E9E9E;padding:8px 0;">Titular</td>
                <td style="font-weight:500;">{nombre}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="back_paso3", use_container_width=True):
            st.session_state["retiro_paso"] = 2; st.rerun()
    with col2:
        if st.button("🔐 Solicitar código de verificación", key="solicitar_otp",
                     type="primary", use_container_width=True):
            st.session_state["retiro_otp_modal"] = True; st.rerun()

    if st.session_state.get("retiro_otp_modal", False):
        _render_modal_otp_retiro(monto)


def _render_modal_otp_retiro(monto: float):
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:28px 24px;
                box-shadow:0 4px 20px rgba(0,0,0,0.10);margin-top:16px;text-align:center;
                border:1px solid #E8F5E9;">
        <div style="font-size:52px;margin-bottom:12px;">🔐</div>
        <h4 style="color:#2D2926;margin:0 0 8px;">Validación de seguridad</h4>
        <p style="color:#6B6560;font-size:13px;margin:0;">
            Ingresa el código enviado a tu celular y correo registrados.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#E3F2FD;border-radius:8px;padding:10px;text-align:center;
                margin:12px 0;font-size:13px;">
        ⏱️ Código válido por: <strong style="color:#003087;">04:58</strong>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_otp_retiro"):
        codigo = st.text_input("Código de verificación", placeholder="123456", max_chars=6)
        col1, col2 = st.columns(2)
        with col1:
            reenviar = st.form_submit_button("🔄 Reenviar código", use_container_width=True)
        with col2:
            verificar = st.form_submit_button("✅ Verificar", type="primary", use_container_width=True)

    if verificar:
        if codigo == "123456":
            st.session_state["retiro_otp_modal"] = False
            st.session_state["retiro_exitoso"] = True
            log = registrar_accion_log(f"Retiro confirmado — ${monto:,.2f} COP")
            st.session_state.setdefault("chatbot_log",[]).append(log)
            st.rerun()
        else:
            st.error("❌ Código incorrecto.")
            activar_chatbot("ERR017", "Retiros")

    if reenviar:
        st.success("📱 Código reenviado.")

    st.markdown("""
    <a href="#" style="color:#00D261;font-size:12px;display:block;text-align:center;margin-top:8px;">
        ¿No has recibido el código de seguridad?
    </a>
    """, unsafe_allow_html=True)
    st.info("💡 **Demo:** Código válido → `123456`")

    if st.button("✖ Cancelar", key="cancel_otp_retiro"):
        st.session_state["retiro_otp_modal"] = False; st.rerun()



def _render_historial_retiros(cliente):
    historial = [h for h in HISTORIAL_RETIROS if h.get("cliente_id") == cliente.get("id")]
    if not historial:
        st.info("No hay retiros registrados.")
        return

    # Encabezado tabla
    cols = st.columns([2, 2, 2, 2, 1])
    for col, head in zip(cols, ["Fecha","Tipo","Monto","Estado","Acción"]):
        with col:
            st.markdown(f"<div style='font-size:12px;color:#9E9E9E;font-weight:600;padding:4px 0;'>{head}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)

    for h in historial:
        color = {"Procesado":"#00D261","En trámite":"#F57C00","Rechazado":"#D32F2F"}.get(h["estado"],"#6B6560")
        icon  = {"Procesado":"✅","En trámite":"🟡","Rechazado":"❌"}.get(h["estado"],"●")
        c1,c2,c3,c4,c5 = st.columns([2,2,2,2,1])
        with c1: st.markdown(f"<div style='font-size:13px;padding:6px 0;'>{h['fecha']}</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div style='font-size:13px;padding:6px 0;'>{h['tipo']}</div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div style='font-size:13px;padding:6px 0;font-weight:600;'>${h['monto']:,.0f}</div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div style='font-size:13px;padding:6px 0;color:{color};font-weight:600;'>{icon} {h['estado']}</div>", unsafe_allow_html=True)
        with c5:
            if st.button("Ver", key=f"ver_{h['fecha']}_{h['monto']}", use_container_width=True):
                st.info(f"**{h['tipo']}** · {h['fecha']} · ${h['monto']:,.0f} COP · {h['estado']}")
        st.markdown("<hr style='margin:2px 0;border-color:#F5F5F5;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PÁGINA 3: CUENTAS BANCARIAS
# ─────────────────────────────────────────────
def render_cuentas():
    cliente = st.session_state.get("cliente_activo", {})
    if not cliente: return

    cuentas = cliente.get("cuentas_bancarias", [])
    if "cuentas_paso" not in st.session_state:
        st.session_state["cuentas_paso"] = "lista"

    col_izq, col_der = st.columns([4, 6])

    with col_izq:
        st.markdown("""
        <div style="background:#E8F5E9;border-radius:12px;padding:36px 20px;
                    min-height:400px;text-align:center;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;">
            <div style="font-size:64px;margin-bottom:16px;">🏦</div>
            <h3 style="color:#2D2926;margin:0 0 8px;">Cuentas bancarias</h3>
            <p style="color:#6B6560;font-size:13px;line-height:1.5;max-width:190px;">
                Administra tus cuentas para recibir desembolsos de forma rápida y segura.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        paso = st.session_state.get("cuentas_paso","lista")

        if paso == "lista":
            pct = 33
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:13px;color:#6B6560;font-weight:500;">Paso 1 de 3</span>
            </div>
            <div style="background:#ECECEC;border-radius:4px;height:6px;margin-bottom:24px;">
                <div style="background:#00D261;width:{pct}%;height:6px;border-radius:4px;"></div>
            </div>
            <h4 style="margin-bottom:16px;">¿A dónde quieres enviar tu dinero?</h4>
            """, unsafe_allow_html=True)

            # Tabs estilo
            st.markdown("""
            <div style="display:flex;gap:0;border-bottom:2px solid #E0E0E0;margin-bottom:16px;">
                <div style="padding:8px 20px;font-size:13px;font-weight:700;color:#00D261;
                            border-bottom:3px solid #00D261;margin-bottom:-2px;">Cuenta bancaria</div>
                <div style="padding:8px 20px;font-size:13px;font-weight:500;color:#9E9E9E;">Cheque</div>
            </div>
            """, unsafe_allow_html=True)

            if not cuentas:
                st.markdown("""
                <div style="text-align:center;padding:32px 0;">
                    <div style="width:72px;height:72px;background:#F5F5F5;border-radius:50%;
                                display:inline-flex;align-items:center;justify-content:center;
                                font-size:32px;margin-bottom:12px;">🏦</div>
                    <p style="color:#6B6560;font-size:14px;margin:0;">Aún no has agregado ninguna cuenta.</p>
                    <p style="font-size:12px;color:#9E9E9E;margin-top:4px;">
                        Agrega tu cuenta para poder realizar retiros.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for c in cuentas:
                    st.markdown(f"""
                    <div style="background:#F8F9FA;border-radius:10px;padding:14px 16px;margin:8px 0;
                                border:1.5px solid #E8F5E9;display:flex;align-items:center;gap:12px;">
                        <span style="color:#00D261;font-size:18px;">⬤</span>
                        <div>
                            <div style="font-weight:600;font-size:14px;">{c['banco']}</div>
                            <div style="font-size:12px;color:#6B6560;">{c['tipo']} — {c['numero']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Regresar", key="back_cuentas", use_container_width=True):
                    st.session_state["current_page"] = "portal"; st.rerun()
            with col2:
                if st.button("+ Agregar cuenta", key="agregar_cuenta", type="primary", use_container_width=True):
                    st.session_state["cuentas_paso"] = "formulario"; st.rerun()

        elif paso == "formulario":
            _render_formulario_cuenta()
        elif paso == "biometria":
            _render_biometria()
        elif paso == "exito":
            _render_cuenta_registrada(cuentas)


def _render_formulario_cuenta():
    st.markdown("""
    <div style="text-align:center;margin-bottom:20px;">
        <div style="width:64px;height:64px;background:#E8F5E9;border-radius:50%;
                    display:inline-flex;align-items:center;justify-content:center;font-size:28px;
                    margin-bottom:12px;">🏦</div>
        <h4 style="color:#2D2926;margin:0 0 6px;">Agrega tu cuenta bancaria</h4>
        <p style="color:#6B6560;font-size:13px;margin:0;">
            Solo cuentas a tu nombre. Verificación biométrica requerida.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_cuenta"):
        tipo_titular = st.selectbox("Tipo", ["Cuenta personal","Cuenta de tercero"])
        banco = st.selectbox("Banco", [
            "BANCO DAVIVIENDA","BANCOLOMBIA","BANCO DE BOGOTÁ",
            "BBVA COLOMBIA","BANCO POPULAR","NEQUI","DAVIPLATA","AV VILLAS"
        ])
        tipo_cuenta = st.radio("Tipo de cuenta", ["Ahorros","Corriente"], horizontal=True)
        numero_cuenta = st.text_input("Número de cuenta", placeholder="Número completo sin espacios")
        ciudad = st.selectbox("Ciudad", ["BOGOTA D.C.","MEDELLÍN","CALI","BARRANQUILLA","BUCARAMANGA"])

        col1, col2 = st.columns(2)
        with col1:
            regresar = st.form_submit_button("← Regresar", use_container_width=True)
        with col2:
            continuar = st.form_submit_button("Validación biométrica →", type="primary", use_container_width=True)

    if regresar:
        st.session_state["cuentas_paso"] = "lista"; st.rerun()
    if continuar:
        escenario = st.session_state.get("escenario_demo","libre")
        if escenario == "B" and not st.session_state.get("sarlaft_resuelto", False):
            activar_chatbot("ERR009","Cuentas Bancarias")
            st.rerun(); return
        st.session_state["cuentas_paso"] = "biometria"
        st.session_state["nueva_cuenta"] = {
            "banco": banco, "tipo": tipo_cuenta,
            "numero": f"****{numero_cuenta[-4:] if len(numero_cuenta)>=4 else '0000'}",
            "numero_completo": numero_cuenta, "estado": "Activa"
        }
        st.rerun()


def _render_biometria():
    st.markdown("#### Antes de comenzar la biometría")
    col1,col2,col3 = st.columns(3)
    for col, icon, titulo, desc in [
        (col1,"📄","Documentos","Ten a la mano tu documento de identidad vigente."),
        (col2,"📷","Cámara",   "Asegúrate de que la cámara de tu dispositivo funcione."),
        (col3,"🌐","Navegador","No cierres la ventana durante el proceso."),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:16px;text-align:center;
                        box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <div style="font-size:32px;margin-bottom:8px;">{icon}</div>
                <div style="font-weight:700;font-size:13px;margin-bottom:4px;">{titulo}</div>
                <div style="font-size:12px;color:#6B6560;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:12px;color:#9E9E9E;text-align:center;margin-top:12px;">
        Al continuar autorizas el tratamiento de datos biométricos según nuestra
        <a href="#" style="color:#00D261;">política de privacidad</a>.
    </p>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="back_bio", use_container_width=True):
            st.session_state["cuentas_paso"] = "formulario"; st.rerun()
    with col2:
        if st.button("Continuar →", key="continuar_bio", type="primary", use_container_width=True):
            st.session_state["cuentas_paso"] = "exito"; st.rerun()


def _render_cuenta_registrada(cuentas_actuales):
    nueva = st.session_state.get("nueva_cuenta", {})
    escenario = st.session_state.get("escenario_demo", "libre")

    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:32px 24px;
                box-shadow:0 2px 12px rgba(0,0,0,0.08);text-align:center;
                border:1.5px solid #00D261;">
        <div style="width:72px;height:72px;background:#E8F5E9;border-radius:50%;
                    display:inline-flex;align-items:center;justify-content:center;
                    font-size:36px;margin-bottom:16px;">✅</div>
        <h4 style="color:#2D2926;margin:0 0 8px;">¡Registro exitoso!</h4>
        <p style="color:#6B6560;font-size:14px;margin:0 0 16px;">Tu cuenta se registró correctamente.</p>
        <div style="background:#F8F9FA;border-radius:8px;padding:14px;text-align:left;margin-bottom:16px;">
            <div style="font-size:13px;margin:4px 0;"><strong>Banco:</strong> {nueva.get('banco','')}</div>
            <div style="font-size:13px;margin:4px 0;"><strong>Tipo:</strong> {nueva.get('tipo','')}</div>
            <div style="font-size:13px;margin:4px 0;"><strong>Número:</strong> {nueva.get('numero','')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def _registrar_cuenta():
        if "nueva_cuenta" in st.session_state:
            cliente = st.session_state.get("cliente_activo", {})
            if cliente:
                cliente.setdefault("cuentas_bancarias", []).append(st.session_state["nueva_cuenta"])
        st.session_state.pop("nueva_cuenta", None)

    if escenario in ("A", "B"):
        # Flujo retiro pendiente — ir directo a completar el retiro
        st.markdown("""
        <div style="background:#E3F2FD;border-radius:8px;padding:10px 14px;
                    font-size:13px;margin-top:8px;border-left:3px solid #003087;">
            💡 Tu cuenta está lista. Ahora puedes completar tu retiro.
        </div>
        """, unsafe_allow_html=True)
        if st.button("💸 Ir a completar mi retiro →", type="primary",
                     use_container_width=True, key="ir_retiros_cuenta"):
            _registrar_cuenta()
            st.session_state["cuentas_paso"] = "lista"
            st.session_state["retiro_paso"] = 1
            st.session_state["current_page"] = "retiros"
            st.rerun()
    else:
        if st.button("Continuar →", type="primary", use_container_width=True,
                     key="continuar_exito_cuenta"):
            _registrar_cuenta()
            st.session_state["cuentas_paso"] = "lista"
            st.rerun()


# ─────────────────────────────────────────────
# PÁGINA 4: MI PORTAFOLIO
# ─────────────────────────────────────────────
def _render_err011_section():
    """Sección interactiva del flujo ERR011 — aceptación de términos y condiciones."""
    pasos_completados = st.session_state.get("chatbot_pasos_completados", [])

    # Mostrar popups según flags
    if st.session_state.pop("_show_popup_solicitudes", False):
        _popup_solicitudes_pendientes()
    if st.session_state.pop("_show_popup_tc", False):
        _popup_terminos_condiciones()
    if st.session_state.pop("_show_otp_tc", False):
        _popup_otp_tc()

    st.markdown("---")
    st.markdown("#### 📋 Gestión de Perfil de Inversión")

    vio_solicitudes = st.session_state.get("err011_vio_solicitudes", False) or 0 in pasos_completados
    acepto_tc = st.session_state.get("err011_acepto_tc", False) or 1 in pasos_completados

    col_a, col_b = st.columns(2)
    with col_a:
        lbl1 = "✅ Solicitudes revisadas" if vio_solicitudes else "📋 Ver solicitudes pendientes"
        if st.button(lbl1, use_container_width=True, key="err011_ver_sol",
                     type="secondary", disabled=vio_solicitudes):
            st.session_state["_show_popup_solicitudes"] = True
            st.rerun()

    with col_b:
        lbl2 = "✅ Términos aceptados" if acepto_tc else "✍️ Aceptar Términos y Condiciones"
        tipo = "secondary" if acepto_tc else ("primary" if vio_solicitudes else "secondary")
        if st.button(lbl2, use_container_width=True, key="err011_tc",
                     type=tipo, disabled=not vio_solicitudes or acepto_tc):
            st.session_state["_show_popup_tc"] = True
            st.rerun()

    # Mostrar OTP automáticamente cuando T&C fue aceptado y OTP aún no verificado
    if acepto_tc and not (st.session_state.get("err011_otp_verificado", False) or 2 in pasos_completados):
        if st.button("🔐 Validar con código OTP", type="primary", use_container_width=True, key="err011_otp_btn"):
            st.session_state["_show_otp_tc"] = True
            st.rerun()


def render_portafolio():
    cliente = st.session_state.get("cliente_activo",{})
    if not cliente: return

    portafolio = cliente.get("portafolio",[])
    saldo  = cliente.get("saldo",0)
    perfil = cliente.get("perfil_riesgo","Moderado")

    st.markdown("## 📊 Mi Portafolio")

    m1,m2,m3 = st.columns(3)
    with m1: st.metric("Saldo total",       f"${saldo:,.0f} COP")
    with m2: st.metric("Perfil de riesgo",  perfil)
    with m3: st.metric("Fondos activos",    len(portafolio))

    col_g, col_d = st.columns([1,1])
    with col_g:
        fig = go.Figure(go.Pie(
            labels=[p["fondo"] for p in portafolio],
            values=[p["porcentaje"] for p in portafolio],
            marker_colors=["#00D261","#2D2926","#003087","#9E9E9E"],
            hole=0.42, textinfo="percent+label"
        ))
        fig.update_layout(title="Distribución actual", margin=dict(t=40,b=20,l=0,r=0),
                          height=300, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col_d:
        st.markdown("**Detalle por fondo:**")
        for p in portafolio:
            st.markdown(f"""
            <div style="background:white;border-radius:8px;padding:12px 14px;margin:6px 0;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="font-weight:600;font-size:13px;">🟢 {p['fondo']}</div>
                <div style="font-size:12px;color:#6B6560;">{p['porcentaje']}% — ${p['valor']:,.0f} COP</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Cambiar perfil de inversión", type="primary", use_container_width=True, key="cambiar_perfil"):
            escenario = st.session_state.get("escenario_demo","libre")
            if escenario == "C" or "Pendiente" in perfil:
                activar_chatbot("ERR011","Mi Portafolio")
            else:
                activar_chatbot("ERR003","Mi Portafolio")
            st.rerun()
    with col2:
        if st.button("📊 Reasignar portafolio", use_container_width=True, key="reasignar_portafolio"):
            activar_chatbot("ERR007","Mi Portafolio")
            st.rerun()

    # ERR011 interactive flow
    if st.session_state.get("error_id_actual") == "ERR011":
        _render_err011_section()


# ─────────────────────────────────────────────
# PÁGINA 5: DOCUMENTOS
# ─────────────────────────────────────────────
def render_documentos():
    st.markdown("## 📄 Documentos")

    docs = [
        {"nombre":"Certificado de aportes 2025","tipo":"Certificado","fecha":"2025-12-31","disponible":True},
        {"nombre":"Extracto Q4 2025",           "tipo":"Extracto",   "fecha":"2025-12-31","disponible":True},
        {"nombre":"Certificado de aportes 2026","tipo":"Certificado","fecha":"2026-12-31","disponible":False},
        {"nombre":"Extracto Q1 2026",           "tipo":"Extracto",   "fecha":"2026-03-31","disponible":True},
        {"nombre":"Constancia de vinculación",  "tipo":"Constancia", "fecha":"2024-01-15","disponible":True},
    ]

    # Encabezado
    cols = st.columns([3,1.5,1.5,1.5])
    for col, head in zip(cols,["Documento","Tipo","Fecha","Acción"]):
        with col:
            st.markdown(f"<div style='font-size:12px;color:#9E9E9E;font-weight:600;padding:4px 0;'>{head}</div>",
                        unsafe_allow_html=True)
    st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)

    for doc in docs:
        c1,c2,c3,c4 = st.columns([3,1.5,1.5,1.5])
        with c1: st.markdown(f"<div style='font-size:13px;padding:6px 0;'>📃 {doc['nombre']}</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div style='font-size:12px;color:#6B6560;padding:6px 0;'>{doc['tipo']}</div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div style='font-size:12px;color:#6B6560;padding:6px 0;'>{doc['fecha']}</div>", unsafe_allow_html=True)
        with c4:
            if doc["disponible"]:
                if st.button("⬇ Descargar", key=f"dl_{doc['nombre']}", use_container_width=True):
                    if "2026" in doc["nombre"] and "Certificado" in doc["tipo"]:
                        activar_chatbot("ERR012","Documentos")
                    else:
                        activar_chatbot("ERR005","Documentos")
                    st.rerun()
            else:
                st.markdown("<div style='font-size:12px;color:#D32F2F;padding:6px 0;'>No disponible</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:2px 0;border-color:#F5F5F5;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col2:
        if st.button("🚪 Cerrar sesión", use_container_width=True, key="logout_docs"):
            _cerrar_sesion()


# ─────────────────────────────────────────────
# PÁGINA 6: MIS DATOS
# ─────────────────────────────────────────────
def render_datos():
    cliente = st.session_state.get("cliente_activo",{})
    if not cliente: return

    st.markdown("## ⚙️ Mis Datos")

    with st.form("form_datos"):
        col1,col2 = st.columns(2)
        with col1:
            st.text_input("Nombre completo",   value=cliente.get("nombre",""))
            st.text_input("Documento",         value=cliente.get("documento",""), disabled=True)
            st.text_input("Correo electrónico",value=cliente.get("email",""))
        with col2:
            st.text_input("Teléfono celular",  value=cliente.get("telefono",""))
            st.text_input("Ciudad",            value=cliente.get("ciudad",""))
            st.text_input("Perfil de riesgo",  value=cliente.get("perfil_riesgo",""), disabled=True)

        col_a,col_b = st.columns(2)
        with col_a:
            guardar  = st.form_submit_button("💾 Guardar cambios", type="primary", use_container_width=True)
        with col_b:
            cancelar = st.form_submit_button("Cancelar", use_container_width=True)

    if guardar:
        activar_chatbot("ERR004","Mis Datos"); st.rerun()
    if cancelar:
        st.session_state["current_page"] = "portal"; st.rerun()


# ─────────────────────────────────────────────
# PÁGINA 7: ENCUESTA NPS (in-portal)
# ─────────────────────────────────────────────
def render_nps():
    from modules.nlp_categorizer import clasificar_transaccion, detectar_error_probable, analizar_sentimiento

    cliente = st.session_state.get("cliente_activo",{})
    nombre  = cliente.get("nombre","Cliente") if cliente else "Cliente"

    st.markdown("## 📋 Encuesta de satisfacción (NPS)")
    st.markdown(f"**{nombre}**, ¿cómo fue tu experiencia en el portal hoy?")

    puntuacion = st.slider("Probabilidad de recomendar Skandia (0–10)", 0, 10, 8)

    if puntuacion <= 6:
        seg = "Detractor"; seg_color = "#D32F2F"
    elif puntuacion <= 8:
        seg = "Pasivo";    seg_color = "#F57C00"
    else:
        seg = "Promotor";  seg_color = "#00D261"

    st.markdown(f"""
    <span style="background:{seg_color};color:white;padding:4px 14px;border-radius:20px;
                 font-size:13px;font-weight:600;">{seg} — {puntuacion}/10</span>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    transacciones = [
        "Solicité un retiro","Realicé un aporte","Consulté mi saldo",
        "Gestioné mi portafolio","Consulté documentos/certificados",
        "Registros de cuentas bancarias","Actualicé mis datos","Otras"
    ]
    transaccion = st.selectbox("¿Qué transacción realizaste?", transacciones)
    comentario  = st.text_area("Cuéntanos tu experiencia:",
                               placeholder="¿Tuviste algún inconveniente?...", height=100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Enviar evaluación", type="primary", use_container_width=True, key="enviar_nps_portal"):
            categoria  = clasificar_transaccion(comentario) if comentario else transaccion
            sentimiento= analizar_sentimiento(comentario)

            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:20px 24px;
                        box-shadow:0 2px 12px rgba(0,0,0,0.07);margin-top:16px;">
                <h4 style="margin-top:0;">✅ Gracias por tu evaluación</h4>
                <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    <span style="background:{seg_color};color:white;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:600;">{seg}</span>
                    <span style="background:#E3F2FD;color:#003087;padding:3px 12px;border-radius:20px;font-size:12px;">📌 {categoria}</span>
                    <span style="background:#F3E5F5;color:#6A1B9A;padding:3px 12px;border-radius:20px;font-size:12px;">💭 {sentimiento}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if puntuacion <= 6:
                st.markdown("""
                <div class='sk-alert-critical blink-alert' style='margin-top:12px;'>
                    🔴 <strong>Caso marcado como prioritario.</strong> Un asesor te contactará en 2 horas hábiles.
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💬 Chat en línea", type="primary", use_container_width=True, key="nps_chat_portal"):
                        st.session_state["current_page"] = "tecnico"
                        st.session_state["tecnico_conectado"] = True
                        st.rerun()
                with c2:
                    if st.button("📞 Solicitar llamada", use_container_width=True, key="nps_llamada_portal"):
                        st.success("📞 Llamada programada en los próximos 10 minutos.")
            else:
                st.success(f"🎉 ¡Gracias, {nombre}! Tu opinión nos ayuda a mejorar.")
    with col2:
        if st.button("🚪 Cerrar sesión", use_container_width=True, key="logout_nps"):
            _cerrar_sesion()

