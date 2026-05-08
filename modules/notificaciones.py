"""
modules/notificaciones.py
Simulación visual de envío de notificaciones y correos electrónicos.
No envía correos reales — todo es simulado con st.success y st.expander.
"""

import datetime
import streamlit as st


def simular_correo_cliente(cliente: dict, asunto: str, cuerpo: str) -> dict:
    """Genera un correo simulado al cliente."""
    return {
        "de": "notificaciones@skandia.com.co",
        "para": cliente.get("email", "cliente@email.com"),
        "asunto": asunto,
        "cuerpo": cuerpo,
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "enviado"
    }


def simular_correo_fp(fp: dict, asunto: str, cuerpo: str) -> dict:
    """Genera un correo simulado al Financial Planner."""
    return {
        "de": "sistema@skandia.com.co",
        "para": fp.get("email", "fp@skandia.com"),
        "asunto": asunto,
        "cuerpo": cuerpo,
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "enviado"
    }


def simular_correo_mesa(asunto: str, cuerpo: str) -> dict:
    """Genera un correo simulado a la mesa de ayuda."""
    return {
        "de": "sistema@skandia.com.co",
        "para": "mesadeayuda@skandia.com.co",
        "asunto": asunto,
        "cuerpo": cuerpo,
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "enviado"
    }


def generar_correos_escalamiento(cliente: dict, fp: dict, ticket: dict) -> list:
    """Genera los 3 correos de escalamiento (cliente, FP y mesa de ayuda)."""

    numero_ticket = ticket.get("numero", "TICK-2026-001")
    error_titulo = ticket.get("error", {}).get("titulo", "Error técnico")
    ans = ticket.get("ans_horas", "4 a 12 horas hábiles")
    nombre_cliente = cliente.get("nombre", "Cliente")
    nombre_fp = fp.get("nombre", "Financial Planner")

    correo_cliente = simular_correo_cliente(
        cliente,
        asunto=f"Caso escalado con éxito — Ticket {numero_ticket}",
        cuerpo=f"""
Estimado/a {nombre_cliente},

Tu caso ha sido escalado exitosamente con el número de ticket: **{numero_ticket}**

📋 Detalle del caso:
- Error reportado: {error_titulo}
- Prioridad: {ticket.get('prioridad', 'MEDIA')}
- ANS de respuesta: {ans}

Recibirás respuesta de nuestro equipo de soporte especializado en un máximo de {ans}.

Tu Financial Planner {nombre_fp} también ha sido notificado y dará seguimiento a tu caso.

Para consultar el estado de tu ticket, ingresa al portal y ve a Servicio al Cliente > Mis tickets.

Cordialmente,
Equipo de Soporte Skandia
📞 Línea de atención: 601-326-7777
        """.strip()
    )

    correo_fp = simular_correo_fp(
        fp,
        asunto=f"[ACCIÓN REQUERIDA] Caso escalado de tu cliente {nombre_cliente} — {numero_ticket}",
        cuerpo=f"""
Hola {nombre_fp},

Se ha escalado un caso de tu cliente {nombre_cliente} a la mesa de ayuda.

📋 Resumen del caso:
- Ticket: {numero_ticket}
- Cliente: {nombre_cliente} | Contrato: {cliente.get('contrato', 'N/A')}
- Error: {error_titulo}
- Módulo: {ticket.get('error', {}).get('modulo_destino', 'N/A')}
- ANS: {ans}

Por favor, mantente disponible en caso de que el equipo de soporte necesite información adicional del cliente.

Puedes ver el detalle completo del caso en el Panel de Control CX > Casos activos.

Saludos,
Sistema Skandia CX
        """.strip()
    )

    correo_mesa = simular_correo_mesa(
        asunto=f"[NUEVO TICKET {ticket.get('prioridad', 'MEDIA')}] {numero_ticket} — {error_titulo}",
        cuerpo=f"""
NUEVO TICKET DE ESCALAMIENTO

Número: {numero_ticket}
Prioridad: {ticket.get('prioridad', 'MEDIA')}
ANS: {ans}

CLIENTE:
- Nombre: {nombre_cliente}
- Contrato: {cliente.get('contrato', 'N/A')}
- Email: {cliente.get('email', 'N/A')}
- FP Asignado: {nombre_fp} ({fp.get('email', 'N/A')})

ERROR REPORTADO:
- ID: {ticket.get('error_id', 'N/A')}
- Título: {error_titulo}
- Categoría: {ticket.get('error', {}).get('categoria', 'N/A')}
- Severidad: {ticket.get('error', {}).get('severidad', 'N/A')}

Ver informe técnico completo en el sistema de gestión de casos.

Sistema Skandia CX — Generado automáticamente
        """.strip()
    )

    return [correo_cliente, correo_fp, correo_mesa]


def generar_correos_resolucion(cliente: dict, fp: dict, agente: dict, ticket: dict, solucion: str) -> list:
    """Genera los correos de notificación de cierre del caso."""

    numero_ticket = ticket.get("numero", "TICK-2026-001")
    nombre_cliente = cliente.get("nombre", "Cliente")
    nombre_fp = fp.get("nombre", "Financial Planner")
    nombre_agente = agente.get("nombre", "Agente de soporte")

    correo_cliente = simular_correo_cliente(
        cliente,
        asunto=f"✅ Tu caso fue resuelto — Ticket {numero_ticket}",
        cuerpo=f"""
Estimado/a {nombre_cliente},

¡Tu inconveniente ha sido resuelto exitosamente!

🎫 Ticket: {numero_ticket}
✅ Estado: RESUELTO

📝 Solución aplicada:
{solucion}

Si el problema persiste o tienes alguna pregunta adicional, no dudes en contactarnos.

Califica nuestra atención en la sección Encuesta NPS del portal.

Cordialmente,
{nombre_agente}
Equipo de Soporte Skandia
        """.strip()
    )

    correo_fp = simular_correo_fp(
        fp,
        asunto=f"Caso {numero_ticket} del cliente {nombre_cliente} fue RESUELTO",
        cuerpo=f"""
Hola {nombre_fp},

El caso de tu cliente {nombre_cliente} ha sido resuelto.

🎫 Ticket: {numero_ticket}
👤 Resuelto por: {nombre_agente}
✅ Estado: CERRADO

Solución aplicada: {solucion}

El cliente fue notificado. Te recomendamos hacer un seguimiento en los próximos días.

Sistema Skandia CX
        """.strip()
    )

    return [correo_cliente, correo_fp]


def render_correos_simulados(correos: list, titulo: str = "Ver correos enviados"):
    """Renderiza los correos simulados en un expander de Streamlit."""
    with st.expander(f"📧 {titulo}", expanded=False):
        for i, correo in enumerate(correos):
            st.markdown(f"""
            <div style="background:#f8f9fa;border-radius:8px;padding:16px;margin-bottom:12px;
                        border-left:3px solid #00D261;">
                <div style="font-size:12px;color:#6B6560;margin-bottom:8px;">
                    ✉️ <strong>De:</strong> {correo['de']} &nbsp;|&nbsp;
                    <strong>Para:</strong> {correo['para']} &nbsp;|&nbsp;
                    <strong>Fecha:</strong> {correo['fecha']}
                </div>
                <div style="font-weight:600;margin-bottom:8px;color:#2D2926;">
                    📋 {correo['asunto']}
                </div>
                <div style="font-size:13px;color:#4a4a4a;white-space:pre-line;">
                    {correo['cuerpo']}
                </div>
                <div style="margin-top:8px;">
                    <span style="background:#00D261;color:white;padding:2px 8px;
                                 border-radius:10px;font-size:11px;">✓ Enviado</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
