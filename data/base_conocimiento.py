"""
data/base_conocimiento.py
Base de conocimiento de errores recurrentes del portal Skandia.
Contiene 17 errores con soluciones guiadas para el agente IA.
"""

BASE_CONOCIMIENTO = {
    "ERR001": {
        "titulo": "No se puede inscribir cuenta bancaria activa",
        "categoria": "Cuentas bancarias",
        "descripcion": "El cliente intenta inscribir una cuenta que ya está registrada en otro contrato.",
        "solucion_ia": [
            "Verifica que la cuenta no esté inscrita bajo otro contrato en Mi Perfil > Cuentas.",
            "Si aparece como activa, debes desvincularla primero desde Configuración > Cuentas registradas.",
            "Espera 5 minutos a que el sistema actualice el estado.",
            "Vuelve a Retiros e intenta la inscripción nuevamente."
        ],
        "modulo_destino": "Cuentas Bancarias",
        "icono": "🏦",
        "severidad": "media",
        "tiempo_resolucion_estimado": "10 min"
    },
    "ERR002": {
        "titulo": "Retiro no procesado por fondos insuficientes",
        "categoria": "Retiros",
        "descripcion": "El monto solicitado supera el saldo disponible para retiro en el fondo seleccionado.",
        "solucion_ia": [
            "Verifica el saldo disponible actual en Mi Portafolio > Ver detalle.",
            "Ten en cuenta que el saldo mostrado puede incluir aportes en proceso de confirmación.",
            "Intenta con un monto menor al saldo disponible para retiro (no el saldo total).",
            "Si el saldo es suficiente pero el error persiste, contacta a tu Financial Planner."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "💸",
        "severidad": "media",
        "tiempo_resolucion_estimado": "5 min"
    },
    "ERR003": {
        "titulo": "Retiro bloqueado por perfil de inversión no actualizado",
        "categoria": "Retiros",
        "descripcion": "El perfil de riesgo del cliente está vencido o requiere actualización para procesar retiros.",
        "solucion_ia": [
            "Dirígete a Mi Portafolio > Perfil de inversión.",
            "Completa el cuestionario de actualización de perfil (toma aproximadamente 5 minutos).",
            "Firma electrónicamente la actualización cuando se solicite.",
            "Una vez actualizado, regresa a Retiros e intenta nuevamente."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "⚠️",
        "severidad": "media",
        "tiempo_resolucion_estimado": "15 min"
    },
    "ERR004": {
        "titulo": "No se pueden actualizar datos personales (documento en proceso)",
        "categoria": "Datos personales",
        "descripcion": "El sistema no permite actualizar datos porque hay una modificación anterior en proceso de validación.",
        "solucion_ia": [
            "Verifica en Mis Datos si tienes una solicitud de cambio pendiente de aprobación.",
            "Las actualizaciones de datos pueden tardar hasta 24 horas hábiles en procesarse.",
            "Si la solicitud tiene más de 24 horas, comunícate con tu Financial Planner.",
            "Para cambios urgentes, puedes acudir a cualquier punto de atención Skandia con tu documento de identidad."
        ],
        "modulo_destino": "Mis Datos",
        "icono": "📝",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "24 h"
    },
    "ERR005": {
        "titulo": "Error al cargar extracto / certificado (timeout del servidor)",
        "categoria": "Documentos",
        "descripcion": "El servidor no responde al intentar generar o descargar documentos.",
        "solucion_ia": [
            "Espera 2 minutos y presiona nuevamente el botón de descarga.",
            "Verifica tu conexión a internet — documentos PDF requieren conexión estable.",
            "Intenta en un horario con menor tráfico (antes de las 9am o después de las 6pm).",
            "Si el error persiste más de 1 hora, el sistema puede estar en mantenimiento programado.",
            "Solicita el documento a tu Financial Planner como alternativa temporal."
        ],
        "modulo_destino": "Documentos",
        "icono": "📄",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "30 min"
    },
    "ERR006": {
        "titulo": "Aporte rechazado por límite diario superado",
        "categoria": "Aportes",
        "descripcion": "El monto del aporte supera el límite de transacciones diarias permitido.",
        "solucion_ia": [
            "El límite diario de aportes por portal es de $10.000.000 COP.",
            "Verifica el total de aportes realizados hoy en el historial de transacciones.",
            "Si necesitas realizar un aporte mayor, debes hacerlo en días consecutivos.",
            "Para aportes extraordinarios sin límite, contacta directamente a tu Financial Planner.",
            "También puedes realizar el aporte mediante transferencia bancaria directa a la cuenta fiduciaria."
        ],
        "modulo_destino": "Aportes",
        "icono": "💰",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "1 día"
    },
    "ERR007": {
        "titulo": "Portafolio no muestra saldo actualizado (caché)",
        "categoria": "Portafolio",
        "descripcion": "Los saldos mostrados en el portafolio no corresponden a los valores más recientes.",
        "solucion_ia": [
            "Presiona Ctrl+Shift+R (o Cmd+Shift+R en Mac) para forzar la recarga sin caché.",
            "Cierra sesión completamente y vuelve a ingresar al portal.",
            "Los saldos se actualizan automáticamente cada 4 horas hábiles.",
            "La valoración del cierre del día se publica después de las 6:00 p.m.",
            "Si el saldo parece incorrecto después de las 8am del día siguiente, reporta el caso."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "📊",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "5 min"
    },
    "ERR008": {
        "titulo": "Error de autenticación al acceder al portal (sesión expirada)",
        "categoria": "Acceso al portal",
        "descripcion": "La sesión del usuario expiró o se presentó un error de autenticación.",
        "solucion_ia": [
            "Cierra completamente el navegador y vuelve a abrir el portal.",
            "Asegúrate de no tener varias pestañas del portal abiertas simultáneamente.",
            "Si el problema persiste, limpia las cookies del navegador (Configuración > Privacidad > Borrar datos).",
            "La sesión expira automáticamente después de 15 minutos de inactividad por seguridad.",
            "Vuelve a ingresar con tu documento y contraseña."
        ],
        "modulo_destino": "Login",
        "icono": "🔐",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "5 min"
    },
    "ERR009": {
        "titulo": "Cuenta bancaria en lista de restricción SARLAFT",
        "categoria": "Cuentas bancarias",
        "descripcion": "La cuenta bancaria a inscribir está reportada en el sistema SARLAFT (Sistema de Administración del Riesgo LA/FT).",
        "solucion_ia": [
            "Por regulación, no es posible inscribir cuentas reportadas en SARLAFT automáticamente.",
            "Este proceso requiere validación manual por el área de cumplimiento.",
            "Tu Financial Planner recibirá una notificación y se comunicará contigo en máximo 2 días hábiles.",
            "Puedes presentar documentos de soporte en cualquier punto Skandia para agilizar el proceso.",
            "Este proceso es confidencial y está regulado por la normativa colombiana de prevención de lavado de activos."
        ],
        "modulo_destino": "Cuentas Bancarias",
        "icono": "🚨",
        "severidad": "alta",
        "tiempo_resolucion_estimado": "2-5 días hábiles",
        "es_critico": True
    },
    "ERR010": {
        "titulo": "Retiro no disponible por periodo de bloqueo del fondo",
        "categoria": "Retiros",
        "descripcion": "El fondo seleccionado se encuentra en periodo de bloqueo y no permite retiros en este momento.",
        "solucion_ia": [
            "Algunos fondos tienen períodos mínimos de permanencia que deben cumplirse antes de permitir retiros.",
            "Consulta en Mi Portafolio > Ver detalle la fecha estimada de disponibilidad.",
            "Verifica si tienes otros fondos disponibles desde los cuales puedas realizar el retiro.",
            "Contacta a tu Financial Planner para explorar opciones de liquidez alternativas.",
            "La fecha exacta de liberación del bloqueo aparece en el detalle del fondo."
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "🔒",
        "severidad": "media",
        "tiempo_resolucion_estimado": "Variable (según fondo)"
    },
    "ERR011": {
        "titulo": "Actualización de perfil de riesgo pendiente de aceptación de términos",
        "categoria": "Portafolio",
        "descripcion": "Probable causa: Actualización de perfil de riesgo pendiente de aceptación de términos y condiciones.",
        "solucion_ia": [
            "Dirígete a Mi Portafolio > Perfil de inversión > Ver solicitudes pendientes.",
            "Busca la solicitud de actualización y selecciona 'Aceptar Términos y Condiciones'.",
            "Recibirás un código OTP en tu celular para validar la aceptación de términos y condiciones.",
            "Si el enlace de aceptar términos expiró, deberás iniciar el proceso nuevamente desde el cuestionario.",
            "Aceptar los términos y condiciones es obligatorio por ley para cambios en el perfil de inversión.",
        ],
        "modulo_destino": "Mi Portafolio",
        "icono": "✍️",
        "severidad": "media",
        "tiempo_resolucion_estimado": "15 min"
    },
    "ERR012": {
        "titulo": "Certificado de aportes no generado (periodo fiscal no cerrado)",
        "categoria": "Documentos",
        "descripcion": "El sistema no puede generar el certificado de aportes porque el periodo fiscal aún no ha cerrado.",
        "solucion_ia": [
            "Los certificados de aportes del año fiscal se habilitan a partir del 15 de marzo del año siguiente.",
            "Verifica en Documentos la fecha de disponibilidad del certificado.",
            "Puedes solicitar un certificado parcial de aportes hasta la fecha actual.",
            "Si necesitas el certificado para declaración de renta, tu Financial Planner puede emitir una constancia temporal.",
            "Consulta el calendario tributario en la sección de Ayuda del portal."
        ],
        "modulo_destino": "Documentos",
        "icono": "📅",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "Según calendario fiscal"
    },
    "ERR013": {
        "titulo": "Contraseña incorrecta — bloqueo por intentos",
        "categoria": "Acceso al portal",
        "descripcion": "El cliente ingresó la contraseña incorrecta 3 o más veces consecutivas.",
        "solucion_ia": [
            "Tu portal está bloqueado temporalmente por seguridad tras múltiples intentos fallidos.",
            "Haz clic en '¿Olvidaste tu contraseña?' en la pantalla de login.",
            "Recibirás un correo a tu dirección registrada con el enlace de restablecimiento.",
            "Si no recibes el correo en 5 minutos, revisa la carpeta de spam.",
            "Una vez restablecida, intenta ingresar nuevamente."
        ],
        "modulo_destino": "Login",
        "icono": "🔒",
        "severidad": "media",
        "tiempo_resolucion_estimado": "10 min"
    },
    "ERR014": {
        "titulo": "Portal bloqueado por actividad sospechosa (posible fraude)",
        "categoria": "Seguridad / Fraude",
        "descripcion": "El sistema detectó acceso desde un dispositivo o ubicación inusual.",
        "solucion_ia": [
            "Por tu seguridad, hemos bloqueado el acceso desde este dispositivo.",
            "Recibirás una alerta a tu correo y celular registrado.",
            "Para desbloquear, debes verificar tu identidad respondiendo el correo de seguridad.",
            "Si NO reconoces este intento de acceso, comunícate INMEDIATAMENTE con la línea de fraudes: 601-326-7777.",
            "No compartas tu contraseña ni códigos OTP con nadie, incluyendo asesores."
        ],
        "modulo_destino": "Login",
        "icono": "🚨",
        "severidad": "critica",
        "tiempo_resolucion_estimado": "Inmediato",
        "es_critico": True
    },
    "ERR015": {
        "titulo": "Fallo técnico en el acceso al portal (error 500/timeout)",
        "categoria": "Acceso al portal",
        "descripcion": "El portal no carga o presenta error técnico al intentar ingresar.",
        "solucion_ia": [
            "Intenta limpiar la caché y cookies de tu navegador (Ctrl+Shift+Delete).",
            "Prueba en modo incógnito o en un navegador diferente (Chrome, Firefox, Edge).",
            "Verifica tu conexión a internet o cambia a datos móviles.",
            "Si el problema persiste, el portal puede estar en mantenimiento — verifica el canal oficial.",
            "Intenta nuevamente en 10 minutos."
        ],
        "modulo_destino": "Login",
        "icono": "⚠️",
        "severidad": "media",
        "tiempo_resolucion_estimado": "10-30 min"
    },
    "ERR016": {
        "titulo": "Usuario no encontrado / documento no registrado",
        "categoria": "Acceso al portal",
        "descripcion": "El número de documento ingresado no tiene usuario activo en el portal.",
        "solucion_ia": [
            "Verifica que estás ingresando el número de cédula sin puntos ni espacios.",
            "Si eres cliente nuevo, debes registrarte primero en 'Crear cuenta'.",
            "Si ya te registraste, confirma que usaste el mismo documento con el que firmaste tu contrato.",
            "Si el problema persiste, comunícate con tu Financial Planner asignado."
        ],
        "modulo_destino": "Login",
        "icono": "👤",
        "severidad": "baja",
        "tiempo_resolucion_estimado": "5 min"
    },
    "ERR017": {
        "titulo": "Código OTP no llega al celular o correo",
        "categoria": "Verificación de seguridad",
        "descripcion": "El cliente no recibe el código de verificación de doble factor.",
        "solucion_ia": [
            "Espera hasta 2 minutos — los mensajes pueden tener demora por el operador.",
            "Revisa que el número de celular registrado en tu perfil sea el correcto.",
            "Verifica la carpeta de spam si esperas el código por correo.",
            "Presiona 'Reenviar código' solo una vez — múltiples reenvíos pueden generar bloqueo.",
            "Si tienes otro número registrado, selecciona la opción de recibirlo por correo.",
            "Como última opción, usa 'Verificar con biometría' si está habilitado en tu cuenta."
        ],
        "modulo_destino": "Validación de seguridad",
        "icono": "📱",
        "severidad": "media",
        "tiempo_resolucion_estimado": "5-10 min"
    }
}


def get_error(error_id: str) -> dict:
    """Retorna un error por ID."""
    return BASE_CONOCIMIENTO.get(error_id, {})


def get_errores_por_categoria(categoria: str) -> list:
    """Retorna todos los errores de una categoría."""
    return [
        {"id": k, **v}
        for k, v in BASE_CONOCIMIENTO.items()
        if v.get("categoria", "").lower() == categoria.lower()
    ]


def get_errores_criticos() -> list:
    """Retorna los errores críticos."""
    return [
        {"id": k, **v}
        for k, v in BASE_CONOCIMIENTO.items()
        if v.get("es_critico", False)
    ]
