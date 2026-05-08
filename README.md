# 🍃 Skandia Portal Clientes 2026 — Hackathon Demo

Aplicación web completa de experiencia de cliente (CX) con IA conversacional para el portal Skandia.

## 🚀 Instalación y ejecución

```bash
cd C:\Users\wreyes\Desktop\HACKATHON
pip install -r requirements.txt
streamlit run app.py
```

## 👤 Credenciales de acceso (demo)

| Usuario | Contraseña |
|---------|-----------|
| `80123456` | `1234` |
| `52234567` | `1234` |
| `19345678` | `1234` |
| `demo` | `demo` |

**Código OTP de verificación:** `123456`

## 🎬 Escenarios demo

| Escenario | Cliente | Error | Resultado |
|-----------|---------|-------|-----------|
| **A** | Carlos Mendoza | ERR001 — Cuenta bancaria activa | IA resuelve exitosamente ✅ |
| **B** | María López | ERR009 — Restricción SARLAFT | Técnico resuelve el caso ✅ |
| **C** | Roberto Sánchez | ERR011 — Firma electrónica pendiente | Escalado a mesa de ayuda 🎫 |

## 📁 Estructura del proyecto

```
HACKATHON/
├── app.py                    # Router principal
├── requirements.txt
├── config/
│   └── brand.py              # Colores y CSS Skandia
├── data/
│   ├── base_conocimiento.py  # 17 errores con soluciones IA
│   └── clientes_demo.py      # 5 clientes + 4 agentes ficticios
├── modules/
│   ├── nlp_categorizer.py    # Clasificación NLP sin API
│   ├── chatbot.py            # Agente IA flotante
│   ├── report_generator.py   # Informes técnicos automáticos
│   └── notificaciones.py     # Simulación de correos
└── pages/
    ├── login.py              # Login + OTP + fraude
    ├── portal_cliente.py     # Dashboard, Retiros, Cuentas, etc.
    ├── dashboard.py          # Big Data NPS
    ├── control_tower.py      # Panel CX en tiempo real
    └── tecnico.py            # Interfaz del técnico
```

## 🔧 Módulos implementados

- **Módulo 1** — Identidad visual completa Skandia
- **Módulo 2** — Carga y procesamiento de datos CSV/sintéticos
- **Módulo 3** — Base de datos demo (5 clientes, 4 agentes, 17 errores)
- **Módulo 4** — NLP de categorización sin API externa
- **Módulo 5** — Portal completo (Login, Portal, Retiros, Cuentas, Portafolio, Docs, Datos, NPS)
- **Módulo 6** — Chatbot IA flotante contextual
- **Módulo 7** — Interfaz del técnico en tiempo real
- **Módulo 8** — Escalamiento a mesa de ayuda con tickets
- **Módulo 9** — Dashboard analítico Big Data con Plotly
- **Módulo 10** — Control Tower CX
- **Módulo 11** — 3 escenarios demo guionados
- **Módulo 12** — Gestión de estado con session_state
