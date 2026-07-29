from html import escape

import streamlit as st


def render_kpi_card(
    label: str,
    value: str,
    delta: str,
    icon: str,
    color: str,
    delta_warning: bool = False,
) -> None:
    """
    Renderiza una tarjeta KPI reutilizable.
    """

    delta_class = (
        "kpi-delta-warning"
        if delta_warning
        else ""
    )

    html_content = f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div
                class="kpi-icon"
                style="background-color: {escape(color)};"
            >
                {escape(icon)}
            </div>

            <div class="kpi-label">
                {escape(label)}
            </div>
        </div>

        <div class="kpi-value">
            {escape(value)}
        </div>

        <div class="kpi-delta {delta_class}">
            {escape(delta)}
        </div>
    </div>
    """

    st.html(html_content)


def render_process_status(
    title: str,
    items: list[dict],
) -> None:
    """
    Renderiza una tarjeta con estados por proceso.
    """

    rows_html = ""

    for item in items:
        process = escape(
            str(item["process"])
        )
        status = escape(
            str(item["status"])
        )
        color = escape(
            str(item["color"])
        )

        rows_html += f"""
        <div class="status-row">
            <div class="status-process">
                {process}
            </div>

            <div class="status-value">
                <span
                    class="status-dot"
                    style="background-color: {color};"
                ></span>

                {status}
            </div>
        </div>
        """

    html_content = f"""
    <div class="content-card">
        <div class="section-title">
            {escape(title)}
        </div>

        {rows_html}
    </div>
    """

    st.html(html_content)


def render_badge(
    text: str,
    badge_type: str = "info",
) -> str:
    """
    Devuelve un badge HTML seguro.
    """

    allowed_types = {
        "success",
        "warning",
        "danger",
        "info",
        "pink",
    }

    if badge_type not in allowed_types:
        badge_type = "info"

    return f"""
    <span class="badge badge-{badge_type}">
        {escape(text)}
    </span>
    """


def render_integration_card(
    name: str,
    integration_type: str,
    status: str,
    method: str,
    last_sync: str,
    progress: int,
) -> None:
    """
    Renderiza una tarjeta de integración.
    """

    status_map = {
        "Conectado": "success",
        "Disponible": "info",
        "Planificado": "warning",
        "Error": "danger",
        "No configurado": "pink",
    }

    badge_type = status_map.get(
        status,
        "info",
    )

    badge_html = render_badge(
        text=status,
        badge_type=badge_type,
    )

    safe_progress = max(
        0,
        min(int(progress), 100),
    )

    html_content = f"""
    <div class="integration-card">

        <div class="integration-header">

            <div>
                <div class="integration-name">
                    {escape(name)}
                </div>

                <div class="integration-type">
                    {escape(integration_type)}
                </div>
            </div>

            <div>
                {badge_html}
            </div>

        </div>

        <div class="integration-label">
            Método de integración
        </div>

        <div class="integration-value">
            {escape(method)}
        </div>

        <div class="integration-label">
            Última sincronización
        </div>

        <div class="integration-value">
            {escape(last_sync)}
        </div>

        <div class="progress-track">
            <div
                class="progress-fill"
                style="width: {safe_progress}%;"
            ></div>
        </div>

    </div>
    """

    st.html(html_content)


def render_section_header(
    title: str,
    subtitle: str | None = None,
) -> None:
    """
    Renderiza el título de una sección.
    """

    subtitle_html = ""

    if subtitle:
        subtitle_html = f"""
        <div class="section-subtitle">
            {escape(subtitle)}
        </div>
        """

    html_content = f"""
    <div class="section-title">
        {escape(title)}
    </div>

    {subtitle_html}
    """

    st.html(html_content)


def render_demo_notice() -> None:
    """
    Muestra el distintivo de ambiente demostrativo.
    """

    st.html(
        """
        <span class="demo-pill">
            AMBIENTE DEMO
        </span>
        """
    )