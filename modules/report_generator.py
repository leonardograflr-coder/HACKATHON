"""
modules/report_generator.py
Generación de informes técnicos automáticos y tickets de escalamiento.
"""

import datetime
import streamlit as st


def generar_informe_tecnico(
    cliente: dict,
    error: dict,
    error_id: str,
    pasos_completados: list,
    log_acciones: list,
    fp: dict,
    modulo_origen: str
) -> str:
    """Genera el informe técnico completo del caso como texto descargable."""

    ahora = datetime.datetime.now()
    fecha_str = ahora.strftime("%d/%m/%Y %H:%M:%S")

    lineas = [
        "=" * 60,
        "       INFORME TÉCNICO DE CASO — SKANDIA",
        "=" * 60,
        "",
        f"Fecha y hora del evento: {fecha_str}",
        f"Cliente: {cliente.get('nombre', 'N/A')} | Contrato: {cliente.get('contrato', 'N/A')}",
        f"Documento: {cliente.get('documento', 'N/A')}",
        f"Email: {cliente.get('email', 'N/A')}",
        f"Módulo donde ocurrió: {modulo_origen}",
        f"Error identificado: {error_id} — {error.get('titulo', 'N/A')}",
        f"Categoría: {error.get('categoria', 'N/A')}",
        f"Severidad: {error.get('severidad', 'N/A').upper()}",
        f"Financial Planner asignado: {fp.get('nombre', 'N/A')} ({fp.get('email', 'N/A')})",
        "",
        "-" * 60,
        "DESCRIPCIÓN DEL ERROR:",
        error.get('descripcion', 'N/A'),
        "",
        "-" * 60,
        "ACCIONES REALIZADAS POR IA:",
    ]

    pasos = error.get("solucion_ia", [])
    for i, paso in enumerate(pasos):
        completado = i in pasos_completados
        estado = "✓ COMPLETADO" if completado else "✗ NO COMPLETADO"
        lineas.append(f"  [{estado}] Paso {i+1}: {paso}")

    lineas += [
        "",
        "-" * 60,
        "LOG DE EXPERIENCIA DEL CLIENTE:",
    ]

    for accion in log_acciones:
        ts = accion.get("timestamp", "")
        desc = accion.get("descripcion", "")
        lineas.append(f"  [{ts}] {desc}")

    lineas += [
        "",
        "-" * 60,
        f"ESTADO ACTUAL: Escalado a técnico | Pendiente resolución",
        f"Tiempo de atención IA: {len(pasos_completados)} pasos completados de {len(pasos)}",
        "=" * 60,
    ]

    return "\n".join(lineas)


def generar_ticket_escalamiento(
    cliente: dict,
    error: dict,
    error_id: str,
    informe_tecnico: str,
    acciones_tecnico: list,
    fp: dict
) -> dict:
    """Genera el ticket de escalamiento a mesa de ayuda."""

    ahora = datetime.datetime.now()
    anio = ahora.strftime("%Y")

    # Secuencial basado en session_state
    secuencial = st.session_state.get("ticket_counter", 1)
    st.session_state["ticket_counter"] = secuencial + 1

    numero_ticket = f"TICK-{anio}-{str(secuencial).zfill(3)}"

    ticket = {
        "numero": numero_ticket,
        "fecha_creacion": ahora.strftime("%d/%m/%Y %H:%M:%S"),
        "fecha_creacion_obj": ahora,
        "cliente": cliente,
        "error_id": error_id,
        "error": error,
        "fp": fp,
        "informe_tecnico": informe_tecnico,
        "acciones_tecnico": acciones_tecnico,
        "estado": "ESCALADO - PENDIENTE MESA DE AYUDA",
        "ans_horas": "4 a 12 horas hábiles",
        "asignado_a": "Mesa de Ayuda Skandia",
        "prioridad": _calcular_prioridad(error),
        "resolucion": None,
        "fecha_resolucion": None
    }

    return ticket


def _calcular_prioridad(error: dict) -> str:
    """Calcula la prioridad del ticket según la severidad del error."""
    severidad = error.get("severidad", "baja")
    if severidad == "critica" or error.get("es_critico", False):
        return "CRÍTICA"
    elif severidad == "alta":
        return "ALTA"
    elif severidad == "media":
        return "MEDIA"
    return "BAJA"


def generar_texto_ticket(ticket: dict) -> str:
    """Genera el texto completo del ticket para visualización o descarga."""

    lineas = [
        "=" * 60,
        "       TICKET DE ESCALAMIENTO — SKANDIA",
        "=" * 60,
        "",
        f"NÚMERO DE TICKET: {ticket['numero']}",
        f"Fecha de creación: {ticket['fecha_creacion']}",
        f"Estado: {ticket['estado']}",
        f"Prioridad: {ticket['prioridad']}",
        f"ANS de respuesta: {ticket['ans_horas']}",
        "",
        "-" * 60,
        "INFORMACIÓN DEL CLIENTE:",
        f"  Nombre: {ticket['cliente'].get('nombre', 'N/A')}",
        f"  Contrato: {ticket['cliente'].get('contrato', 'N/A')}",
        f"  Email: {ticket['cliente'].get('email', 'N/A')}",
        f"  FP Asignado: {ticket['fp'].get('nombre', 'N/A')}",
        "",
        "-" * 60,
        "ERROR REPORTADO:",
        f"  ID: {ticket['error_id']}",
        f"  Título: {ticket['error'].get('titulo', 'N/A')}",
        f"  Categoría: {ticket['error'].get('categoria', 'N/A')}",
        "",
        "-" * 60,
        "INFORME TÉCNICO:",
        ticket.get("informe_tecnico", ""),
        "",
        "=" * 60,
    ]

    return "\n".join(lineas)


def registrar_accion_log(descripcion: str) -> dict:
    """Crea una entrada de log con timestamp actual."""
    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "descripcion": descripcion
    }
