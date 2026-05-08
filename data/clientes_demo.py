"""
data/clientes_demo.py
Base de datos de demo: clientes, Financial Planners y agentes técnicos.
"""

CLIENTES_DEMO = [
    {
        "id": "CLI001",
        "nombre": "Carlos Mendoza",
        "contrato": "SKD-2024-001",
        "numero_contrato": "667463",
        "email": "carlos.mendoza@email.com",
        "telefono": "300-111-2233",
        "documento": "80123456",
        "fp_asignado": "FP001",
        "saldo": 1414977.14,
        "ultimo_aporte": 250000.00,
        "ultimo_retiro": 500000.00,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Moderado",
        "ciudad": "Bogotá D.C.",
        "historial": [
            "Consulta saldo",
            "Intento retiro fallido",
            "Actualización datos"
        ],
        "cuentas_bancarias": [],
        "portafolio": [
            {"fondo": "FPV Strategist Liquidez Col", "porcentaje": 60, "valor": 848986.28},
            {"fondo": "FPV Renta Fija Colombia", "porcentaje": 30, "valor": 424493.14},
            {"fondo": "FPV Acciones Colombia", "porcentaje": 10, "valor": 141497.71},
        ]
    },
    {
        "id": "CLI002",
        "nombre": "María López",
        "contrato": "SKD-2024-002",
        "numero_contrato": "778542",
        "email": "maria.lopez@email.com",
        "telefono": "311-222-3344",
        "documento": "52234567",
        "fp_asignado": "FP001",
        "saldo": 3250000.00,
        "ultimo_aporte": 500000.00,
        "ultimo_retiro": 0,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Conservador",
        "ciudad": "Medellín",
        "historial": [
            "Consulta saldo",
            "Intento inscribir cuenta bancaria",
            "Error SARLAFT"
        ],
        "cuentas_bancarias": [],
        "portafolio": [
            {"fondo": "FPV Strategist Liquidez Col", "porcentaje": 80, "valor": 2600000.00},
            {"fondo": "FPV Renta Fija Colombia", "porcentaje": 20, "valor": 650000.00},
        ]
    },
    {
        "id": "CLI003",
        "nombre": "Roberto Sánchez",
        "contrato": "SKD-2023-003",
        "numero_contrato": "889631",
        "email": "roberto.sanchez@email.com",
        "telefono": "315-333-4455",
        "documento": "19345678",
        "fp_asignado": "FP002",
        "saldo": 7800000.00,
        "ultimo_aporte": 1000000.00,
        "ultimo_retiro": 2000000.00,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Agresivo — Pendiente actualización",
        "ciudad": "Cali",
        "historial": [
            "Cambio perfil de inversión",
            "Error firma electrónica",
            "Consulta portafolio"
        ],
        "cuentas_bancarias": [
            {
                "banco": "Bancolombia",
                "tipo": "Corriente",
                "numero": "****7823",
                "numero_completo": "2019782300001234",
                "estado": "Activa"
            }
        ],
        "portafolio": [
            {"fondo": "FPV Acciones Colombia", "porcentaje": 50, "valor": 3900000.00},
            {"fondo": "FPV Strategist Crecimiento", "porcentaje": 30, "valor": 2340000.00},
            {"fondo": "FPV Renta Fija Colombia", "porcentaje": 20, "valor": 1560000.00},
        ]
    },
    {
        "id": "CLI004",
        "nombre": "Lucía Fernández",
        "contrato": "SKD-2025-004",
        "numero_contrato": "990712",
        "email": "lucia.fernandez@email.com",
        "telefono": "318-444-5566",
        "documento": "43456789",
        "fp_asignado": "FP002",
        "saldo": 980000.00,
        "ultimo_aporte": 100000.00,
        "ultimo_retiro": 0,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Conservador",
        "ciudad": "Barranquilla",
        "historial": [
            "Consulta certificado de aportes",
            "Error descarga extracto",
        ],
        "cuentas_bancarias": [
            {
                "banco": "Banco de Bogotá",
                "tipo": "Ahorros",
                "numero": "****2201",
                "numero_completo": "4501220100009876",
                "estado": "Activa"
            }
        ],
        "portafolio": [
            {"fondo": "FPV Strategist Liquidez Col", "porcentaje": 100, "valor": 980000.00},
        ]
    },
    {
        "id": "CLI006",
        "nombre": "Andres Mendoza",
        "contrato": "SKD-2025-006",
        "numero_contrato": "334901",
        "email": "andres.mendoza@email.com",
        "telefono": "322-666-7788",
        "documento": "1033799087",
        "fp_asignado": "FP001",
        "saldo": 2100000.00,
        "ultimo_aporte": 300000.00,
        "ultimo_retiro": 0,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Moderado",
        "ciudad": "Bogotá D.C.",
        "historial": [
            "Consulta saldo",
            "Primer aporte",
        ],
        "cuentas_bancarias": [],
        "portafolio": [
            {"fondo": "FPV Strategist Liquidez Col", "porcentaje": 70, "valor": 1470000.00},
            {"fondo": "FPV Renta Fija Colombia", "porcentaje": 30, "valor": 630000.00},
        ]
    },
    {
        "id": "CLI005",
        "nombre": "Jorge Ramírez",
        "contrato": "SKD-2023-005",
        "numero_contrato": "112845",
        "email": "jorge.ramirez@email.com",
        "telefono": "320-555-6677",
        "documento": "71567890",
        "fp_asignado": "FP001",
        "saldo": 12500000.00,
        "ultimo_aporte": 2000000.00,
        "ultimo_retiro": 5000000.00,
        "estado_contrato": "Activo",
        "perfil_riesgo": "Moderado",
        "ciudad": "Bogotá D.C.",
        "historial": [
            "Retiro parcial",
            "Cambio portafolio",
            "Actualización datos personales"
        ],
        "cuentas_bancarias": [
            {
                "banco": "BBVA Colombia",
                "tipo": "Ahorros",
                "numero": "****5544",
                "numero_completo": "7734554400001122",
                "estado": "Activa"
            }
        ],
        "portafolio": [
            {"fondo": "FPV Strategist Crecimiento", "porcentaje": 45, "valor": 5625000.00},
            {"fondo": "FPV Acciones Colombia", "porcentaje": 35, "valor": 4375000.00},
            {"fondo": "FPV Renta Fija Colombia", "porcentaje": 20, "valor": 2500000.00},
        ]
    }
]

AGENTES_DEMO = [
    {
        "id": "FP001",
        "nombre": "Ana García",
        "email": "ana.garcia@skandia.com",
        "telefono": "601-111-2222",
        "rol": "Financial Planner",
        "clientes": ["CLI001", "CLI002", "CLI005"]
    },
    {
        "id": "FP002",
        "nombre": "Juan Martínez",
        "email": "juan.martinez@skandia.com",
        "telefono": "601-333-4444",
        "rol": "Financial Planner",
        "clientes": ["CLI003", "CLI004"]
    },
    {
        "id": "AGT001",
        "nombre": "Luis Herrera",
        "email": "luis.herrera@skandia.com",
        "telefono": "601-555-6666",
        "rol": "Agente Técnico"
    },
    {
        "id": "AGT002",
        "nombre": "Sofía Castro",
        "email": "sofia.castro@skandia.com",
        "telefono": "601-777-8888",
        "rol": "Agente Técnico"
    }
]

HISTORIAL_RETIROS = [
    {
        "fecha": "2026-04-15",
        "contrato": "SKD-2024-001",
        "tipo": "Retiro parcial",
        "monto": 500000,
        "estado": "Procesado",
        "cliente_id": "CLI001"
    },
    {
        "fecha": "2026-03-28",
        "contrato": "SKD-2024-001",
        "tipo": "Retiro parcial",
        "monto": 250000,
        "estado": "Procesado",
        "cliente_id": "CLI001"
    },
    {
        "fecha": "2026-02-10",
        "contrato": "SKD-2024-001",
        "tipo": "Retiro total",
        "monto": 1000000,
        "estado": "En trámite",
        "cliente_id": "CLI001"
    },
    {
        "fecha": "2026-01-05",
        "contrato": "SKD-2024-001",
        "tipo": "Retiro parcial",
        "monto": 300000,
        "estado": "Rechazado",
        "cliente_id": "CLI001"
    },
]


def get_cliente_by_id(cliente_id: str) -> dict:
    """Retorna el cliente por ID."""
    for c in CLIENTES_DEMO:
        if c["id"] == cliente_id:
            return c
    return CLIENTES_DEMO[0]


def get_fp_by_id(fp_id: str) -> dict:
    """Retorna el FP/agente por ID."""
    for a in AGENTES_DEMO:
        if a["id"] == fp_id:
            return a
    return AGENTES_DEMO[0]
