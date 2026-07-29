from data.mock_data import (
    get_executive_kpis,
    get_incidents_history,
    get_integrations,
    get_key_pending_items,
    get_payroll_by_area,
    get_payroll_monthly_history,
    get_process_status,
    get_regularized_debt_history,
    get_sla_history,
    get_validation_items,
    get_validation_summary,
)


def load_dashboard_data() -> dict:
    """
    Punto único de acceso a los datos del dashboard.

    Hoy utiliza datos ficticios.
    En el futuro podrá consumir una API o base de datos
    sin modificar las pantallas.
    """

    return {
        "executive_kpis": get_executive_kpis(),
        "sla_history": get_sla_history(),
        "incidents_history": get_incidents_history(),
        "regularized_debt_history": (
            get_regularized_debt_history()
        ),
        "process_status": get_process_status(),
        "key_pending_items": get_key_pending_items(),
        "integrations": get_integrations(),
        "validation_summary": get_validation_summary(),
        "validation_items": get_validation_items(),
        "payroll_by_area": get_payroll_by_area(),
        "payroll_monthly_history": (
            get_payroll_monthly_history()
        ),
    }