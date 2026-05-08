"""
modules/nlp_categorizer.py
Lógica NLP para categorización de transacciones y detección de errores probables.
No usa APIs externas — clasificación basada en palabras clave y reglas.
"""

from data.base_conocimiento import BASE_CONOCIMIENTO

# Mapa de categorías con palabras clave
CATEGORIAS_KEYWORDS = {
    "Consulté mi saldo": [
        "saldo", "balance", "cuánto tengo", "cuanto tengo", "valor cuenta",
        "ver saldo", "consultar saldo", "mi dinero", "disponible"
    ],
    "Solicité un retiro": [
        "retiro", "retirar", "sacar dinero", "desembolso", "retiré",
        "solicite retiro", "quiero retirar", "retirar dinero"
    ],
    "Realicé un aporte": [
        "aporte", "consignar", "depositar", "inversión", "cotización",
        "aporté", "deposité", "consigné", "inversion", "cuota"
    ],
    "Gestioné mi portafolio": [
        "portafolio", "fondos", "cambio de fondo", "reasignación", "reasignar",
        "cambiar fondo", "distribuir", "portafolios", "inversiones"
    ],
    "Consulté mi información": [
        "información", "datos", "contrato", "estado cuenta", "ver contrato",
        "mi perfil", "informacion", "ver datos", "estado del contrato"
    ],
    "Consulté documentos/certificados": [
        "certificado", "extracto", "documento", "constancia", "descargar",
        "bajar documento", "certificados", "extractos", "documentos"
    ],
    "Actualicé mis datos": [
        "actualizar", "cambiar datos", "teléfono", "dirección", "correo",
        "actualicé", "actualice", "cambié", "cambie", "actualizar datos",
        "telefono", "direccion", "email"
    ],
    "Certifiqué mis aportes": [
        "certificación", "certificar", "aportes", "retención en la fuente",
        "retencion", "certificar aportes", "certificado de aportes", "renta"
    ],
    "Registros de cuentas bancarias": [
        "cuenta", "banco", "inscribir", "registrar cuenta", "bancaria",
        "cuenta bancaria", "inscribir cuenta", "agregar cuenta", "añadir cuenta"
    ]
}

# Mapa de categoría → errores más probables
CATEGORIA_ERRORES_PROBABLES = {
    "Solicité un retiro": ["ERR001", "ERR002", "ERR003", "ERR010"],
    "Registros de cuentas bancarias": ["ERR001", "ERR009"],
    "Actualicé mis datos": ["ERR004"],
    "Consulté documentos/certificados": ["ERR005", "ERR012"],
    "Certifiqué mis aportes": ["ERR012", "ERR006"],
    "Realicé un aporte": ["ERR006"],
    "Gestioné mi portafolio": ["ERR003", "ERR007", "ERR011", "ERR010"],
    "Consulté mi saldo": ["ERR007", "ERR008"],
    "Consulté mi información": ["ERR004", "ERR008"],
    "Otras": ["ERR008", "ERR015"]
}

# Señales de problema en comentarios
SENALES_PROBLEMA = {
    "ERR001": ["ya inscrita", "ya registrada", "activa en otro", "cuenta activa", "inscrita en otro contrato"],
    "ERR002": ["fondos insuficientes", "no tengo saldo", "saldo insuficiente", "no alcanza", "monto mayor"],
    "ERR003": ["perfil", "actualizar perfil", "perfil vencido", "riesgo no actualizado"],
    "ERR004": ["no puedo actualizar", "no actualiza", "documento en proceso", "en proceso"],
    "ERR005": ["timeout", "no carga", "error al descargar", "no descarga", "error del servidor"],
    "ERR006": ["límite", "limite diario", "rechazado", "superado el límite"],
    "ERR007": ["saldo desactualizado", "no actualiza", "caché", "cache", "no muestra el saldo real"],
    "ERR008": ["sesión expirada", "sesion", "no puedo ingresar", "error de acceso", "no me deja entrar"],
    "ERR009": ["sarlaft", "restricción", "bloqueada", "no permite inscribir", "restriccion"],
    "ERR010": ["bloqueado", "periodo de bloqueo", "no disponible", "bloqueo del fondo"],
    "ERR011": ["firma electrónica", "firma digital", "pendiente firmar", "no firma"],
    "ERR012": ["certificado no generado", "no genera certificado", "periodo fiscal", "no está disponible"],
    "ERR013": ["contraseña incorrecta", "bloqueado", "intentos fallidos", "no puedo entrar"],
    "ERR009": ["sarlaft", "fraude", "sospechoso"],
    "ERR017": ["no llega el código", "código otp", "no recibo", "otp no llega"]
}


def clasificar_transaccion(comentario: str) -> str:
    """
    Clasifica el comentario del cliente en una categoría de transacción.
    Retorna la categoría detectada o 'Otras' como fallback.
    """
    if not comentario or not isinstance(comentario, str):
        return "Otras"

    texto = comentario.lower().strip()

    puntuaciones = {}
    for categoria, keywords in CATEGORIAS_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in texto)
        if score > 0:
            puntuaciones[categoria] = score

    if not puntuaciones:
        return "Otras"

    return max(puntuaciones, key=puntuaciones.get)


def detectar_error_probable(comentario: str, categoria: str) -> dict:
    """
    Analiza el comentario y la categoría para detectar el error más probable.
    Retorna: {"error_id": "ERR003", "confianza": 0.87, "datos": {...}}
    """
    if not comentario:
        errores_categoria = CATEGORIA_ERRORES_PROBABLES.get(categoria, ["ERR008"])
        error_id = errores_categoria[0] if errores_categoria else "ERR008"
        return {
            "error_id": error_id,
            "confianza": 0.45,
            "datos": BASE_CONOCIMIENTO.get(error_id, {})
        }

    texto = comentario.lower()

    # Buscar señales específicas en el comentario
    puntuaciones_error = {}
    for error_id, senales in SENALES_PROBLEMA.items():
        score = sum(1 for senal in senales if senal.lower() in texto)
        if score > 0:
            puntuaciones_error[error_id] = score

    if puntuaciones_error:
        mejor_error = max(puntuaciones_error, key=puntuaciones_error.get)
        max_score = puntuaciones_error[mejor_error]
        total_senales = len(SENALES_PROBLEMA.get(mejor_error, [1]))
        confianza = min(0.95, 0.5 + (max_score / total_senales) * 0.45)
        return {
            "error_id": mejor_error,
            "confianza": round(confianza, 2),
            "datos": BASE_CONOCIMIENTO.get(mejor_error, {})
        }

    # Fallback por categoría
    errores_posibles = CATEGORIA_ERRORES_PROBABLES.get(categoria, ["ERR008"])
    error_id = errores_posibles[0]
    return {
        "error_id": error_id,
        "confianza": 0.55,
        "datos": BASE_CONOCIMIENTO.get(error_id, {})
    }


def analizar_sentimiento(comentario: str) -> str:
    """Análisis básico de sentimiento basado en palabras clave."""
    if not comentario:
        return "neutral"

    texto = comentario.lower()

    palabras_negativas = [
        "mal", "pésimo", "terrible", "error", "fallo", "problema", "no funciona",
        "imposible", "frustrado", "molesto", "demora", "lento", "bloqueado",
        "no pude", "no puedo", "rechazado", "fallido"
    ]
    palabras_positivas = [
        "excelente", "bueno", "perfecto", "fácil", "rápido", "bien", "gracias",
        "satisfecho", "funciona", "resuelto", "exitoso", "genial", "recomiendo"
    ]

    score_neg = sum(1 for p in palabras_negativas if p in texto)
    score_pos = sum(1 for p in palabras_positivas if p in texto)

    if score_neg > score_pos:
        return "negativo"
    elif score_pos > score_neg:
        return "positivo"
    return "neutral"


def get_categorias_disponibles() -> list:
    """Retorna lista de categorías disponibles."""
    return list(CATEGORIAS_KEYWORDS.keys()) + ["Otras"]
