import pandas as pd


def get_executive_kpis() -> list[dict]:
    """
    Datos ficticios para las tarjetas del resumen ejecutivo.
    """

    return [
        {
            "label": "Trabajadores procesados",
            "value": "1.200",
            "delta": "▲ +2,3% vs mes anterior",
            "icon": "👥",
            "color": "#078896",
            "delta_warning": False,
        },
        {
            "label": "Cumplimiento SLA",
            "value": "96,8%",
            "delta": "▲ +1,8 pp vs mes anterior",
            "icon": "✓",
            "color": "#078c48",
            "delta_warning": False,
        },
        {
            "label": "Errores imputables",
            "value": "0,42%",
            "delta": "▼ -0,12 pp vs mes anterior",
            "icon": "!",
            "color": "#f49a0b",
            "delta_warning": False,
        },
        {
            "label": "Reclamos válidos",
            "value": "12",
            "delta": "▲ +2 vs mes anterior",
            "icon": "◆",
            "color": "#ed2472",
            "delta_warning": True,
        },
        {
            "label": "Tickets críticos",
            "value": "5",
            "delta": "▲ +1 vs mes anterior",
            "icon": "!",
            "color": "#e51c31",
            "delta_warning": True,
        },
        {
            "label": "Riesgo de cierre",
            "value": "Medio",
            "delta": "Sin cambios",
            "icon": "◔",
            "color": "#f49a0b",
            "delta_warning": False,
        },
    ]


def get_sla_history() -> pd.DataFrame:
    """
    Evolución ficticia del cumplimiento SLA.
    """

    return pd.DataFrame(
        {
            "Mes": [
                "Ene",
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
            ],
            "Cumplimiento SLA": [
                92.5,
                94.0,
                95.1,
                96.2,
                96.8,
                97.6,
            ],
            "Meta SLA": [
                95,
                95,
                95,
                95,
                95,
                95,
            ],
        }
    )


def get_incidents_history() -> pd.DataFrame:
    """
    Incidencias y reprocesos de los últimos seis meses.
    """

    return pd.DataFrame(
        {
            "Mes": [
                "Ene",
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
            ],
            "Incidencias": [
                48,
                42,
                37,
                34,
                40,
                32,
            ],
            "Reprocesos": [
                30,
                23,
                24,
                20,
                18,
                17,
            ],
        }
    )


def get_regularized_debt_history() -> pd.DataFrame:
    """
    Monto acumulado ficticio de deuda previsional regularizada.
    Valores expresados en millones de pesos.
    """

    return pd.DataFrame(
        {
            "Mes": [
                "Ene",
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
            ],
            "Monto MM$": [
                35,
                55,
                82,
                115,
                143,
                176,
            ],
        }
    )


def get_process_status() -> list[dict]:
    """
    Estado ficticio de los procesos operacionales.
    """

    return [
        {
            "process": "Nómina",
            "status": "Óptimo",
            "color": "#078c48",
        },
        {
            "process": "Previred",
            "status": "Óptimo",
            "color": "#078c48",
        },
        {
            "process": "DT",
            "status": "En alerta",
            "color": "#f49a0b",
        },
        {
            "process": "Finiquitos",
            "status": "Óptimo",
            "color": "#078c48",
        },
        {
            "process": "Licencias",
            "status": "En alerta",
            "color": "#f49a0b",
        },
        {
            "process": "Tickets",
            "status": "Crítico",
            "color": "#e51c31",
        },
    ]


def get_key_pending_items() -> pd.DataFrame:
    """
    Pendientes clave para la tabla ejecutiva.
    """

    return pd.DataFrame(
        [
            {
                "Tema": "Ajuste imposiciones",
                "Descripción": "Diferencias en bases imponibles Previred",
                "Responsable": "PREVIPAY",
                "Vencimiento": "24-07-2026",
                "Días en estado": 5,
                "Prioridad": "Alta",
                "Estado": "En curso",
            },
            {
                "Tema": "Finiquitos pendientes",
                "Descripción": "Finiquitos de excolaboradores",
                "Responsable": "PREVIPAY",
                "Vencimiento": "30-07-2026",
                "Días en estado": 3,
                "Prioridad": "Alta",
                "Estado": "En curso",
            },
            {
                "Tema": "Licencias médicas",
                "Descripción": "Rechazos por documentación incompleta",
                "Responsable": "Cliente",
                "Vencimiento": "27-07-2026",
                "Días en estado": 7,
                "Prioridad": "Media",
                "Estado": "Pendiente",
            },
            {
                "Tema": "Observaciones DT",
                "Descripción": "Ajustes derivados de revisión documental",
                "Responsable": "PREVIPAY",
                "Vencimiento": "01-08-2026",
                "Días en estado": 9,
                "Prioridad": "Media",
                "Estado": "Pendiente",
            },
        ]
    )


def get_integrations() -> list[dict]:
    """
    Catálogo ficticio de integraciones PREVIPAY.
    """

    return [
        {
            "name": "BUK",
            "integration_type": "RR.HH. y remuneraciones",
            "status": "Conectado",
            "method": "API",
            "last_sync": "Hoy, 08:45",
            "progress": 100,
        },
        {
            "name": "MAXXA",
            "integration_type": "Contabilidad y finanzas",
            "status": "Conectado",
            "method": "API / archivo controlado",
            "last_sync": "Hoy, 08:40",
            "progress": 96,
        },
        {
            "name": "FIN700",
            "integration_type": "ERP financiero",
            "status": "Disponible",
            "method": "API / servicio web",
            "last_sync": "Pendiente de configuración",
            "progress": 65,
        },
        {
            "name": "Microsoft 365",
            "integration_type": "Colaboración y documentos",
            "status": "Disponible",
            "method": "Microsoft Graph",
            "last_sync": "Hoy, 08:42",
            "progress": 92,
        },
        {
            "name": "Previred",
            "integration_type": "Previsión social",
            "status": "Disponible",
            "method": "Archivo / SFTP",
            "last_sync": "Ayer, 23:30",
            "progress": 90,
        },
        {
            "name": "Banco",
            "integration_type": "Pago de remuneraciones",
            "status": "Planificado",
            "method": "Archivo cifrado / API",
            "last_sync": "No configurado",
            "progress": 40,
        },
    ]


def get_validation_summary() -> list[dict]:
    """
    Totales ficticios del control de validaciones.
    """

    return [
        {
            "label": "Críticas",
            "value": 7,
        },
        {
            "label": "Advertencias",
            "value": 14,
        },
        {
            "label": "Informativas",
            "value": 32,
        },
        {
            "label": "En revisión",
            "value": 5,
        },
    ]


def get_validation_items() -> pd.DataFrame:
    """
    Bandeja ficticia de inconsistencias.
    """

    return pd.DataFrame(
        [
            {
                "Tipo": "Crítica",
                "Proceso": "Nómina",
                "Descripción": (
                    "Total de imposiciones no coincide "
                    "con reporte Previred"
                ),
                "Origen": "BUK",
                "Detectado": "09:12",
                "Estado": "Abierta",
            },
            {
                "Tipo": "Advertencia",
                "Proceso": "Asistencia",
                "Descripción": "Horas extras sin aprobación",
                "Origen": "BUK",
                "Detectado": "08:47",
                "Estado": "Abierta",
            },
            {
                "Tipo": "Advertencia",
                "Proceso": "Maestros",
                "Descripción": (
                    "RUT duplicado en maestro de trabajadores"
                ),
                "Origen": "BUK",
                "Detectado": "08:31",
                "Estado": "En curso",
            },
            {
                "Tipo": "Informativa",
                "Proceso": "Pagos",
                "Descripción": (
                    "Archivo bancario con dos registros "
                    "sin convenio"
                ),
                "Origen": "Banco",
                "Detectado": "08:05",
                "Estado": "En curso",
            },
        ]
    )


def get_payroll_by_area() -> pd.DataFrame:
    """
    Distribución ficticia del costo líquido por área.
    """

    return pd.DataFrame(
        {
            "Área": [
                "Administración",
                "Operaciones",
                "Finanzas",
                "Tecnología",
                "Comercial",
            ],
            "Costo MM$": [
                185,
                310,
                240,
                290,
                205,
            ],
        }
    )


def get_payroll_monthly_history() -> pd.DataFrame:
    """
    Evolución ficticia de la nómina total.
    """

    return pd.DataFrame(
        {
            "Mes": [
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
                "Jul",
            ],
            "Costo MM$": [
                1210,
                1235,
                1250,
                1268,
                1285,
                1302,
            ],
        }
    )