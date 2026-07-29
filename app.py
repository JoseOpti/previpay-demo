from pathlib import Path
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.dashboard_service import load_dashboard_data
from ui.components import (
    render_integration_card,
    render_kpi_card,
    render_process_status,
    render_section_header,
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

APP_DIR = Path(__file__).resolve().parent
CSS_PATH = APP_DIR / "ui" / "styles.css"

st.set_page_config(
    page_title="PREVIPAY Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css() -> None:
    """
    Carga la hoja de estilos visuales de PREVIPAY.
    """

    if not CSS_PATH.exists():
        st.error(
            "No se encontró el archivo ui/styles.css. "
            "Verifica la estructura de carpetas."
        )
        st.stop()

    css_content = CSS_PATH.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


load_css()


# ============================================================
# DATOS
# ============================================================

dashboard_data = load_dashboard_data()


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def apply_chart_layout(
    figure,
    height: int = 300,
    show_legend: bool = True,
):
    """
    Aplica una configuración visual común a los gráficos.
    """

    figure.update_layout(
        height=height,
        margin={
            "l": 15,
            "r": 15,
            "t": 15,
            "b": 15,
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "family": "Segoe UI",
            "color": "#6c7d8b",
            "size": 11,
        },
        showlegend=show_legend,
    )

    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
    )

    figure.update_yaxes(
        gridcolor="#edf2f5",
        zeroline=False,
    )

    return figure


def render_page_header(
    title: str,
    subtitle: str,
) -> None:
    """
    Renderiza el encabezado superior de la aplicación.
    """

    st.html(
        f"""
        <div class="page-header">

            <div>
                <div class="page-title">
                    {title}
                </div>

                <div class="page-subtitle">
                    {subtitle}
                </div>
            </div>

            <span class="demo-pill">
                AMBIENTE DEMO
            </span>

        </div>
        """
    )


# ============================================================
# MENÚ LATERAL
# ============================================================

with st.sidebar:

    st.html(
        """
        <div
            class="previpay-logo"
            translate="no"
        >
            PREVI<span>PAY</span>
        </div>

        <div
            class="previpay-tagline"
            translate="no"
        >
            Más que outsourcing
        </div>
        """
    )

    st.divider()

    st.html(
        """
        <div class="sidebar-section">
            Contexto operacional
        </div>
        """
    )

    selected_client = st.selectbox(
        "Cliente",
        options=[
            "Fundación Horizonte Demo",
        ],
    )

    selected_period = st.selectbox(
        "Período",
        options=[
            "Julio 2026",
            "Junio 2026",
            "Mayo 2026",
        ],
    )

    st.html(
        """
        <div class="sidebar-section">
            Perfil
        </div>
        """
    )

    selected_role = st.selectbox(
        "Vista del usuario",
        options=[
            "Ejecutiva",
            "Supervisor PREVIPAY",
            "Analista PREVIPAY",
            "Cliente",
        ],
    )


# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

render_page_header(
    title="PREVIPAY Platform",
    subtitle=(
        f"{selected_client} · "
        f"{selected_period} · "
        f"Vista {selected_role}"
    ),
)


# ============================================================
# PESTAÑAS PRINCIPALES
# ============================================================

dashboard_tab, integrations_tab, control_tab, tickets_tab = st.tabs(
    [
        "📊 Paneles",
        "🔌 Integraciones",
        "⚙️ Control operacional",
        "🎫 Tickets",
    ]
)


# ============================================================
# DASHBOARDS
# ============================================================

with dashboard_tab:

    executive_tab, payroll_tab = st.tabs(
        [
            "Resumen ejecutivo",
            "Analítica de remuneraciones",
        ]
    )

    # --------------------------------------------------------
    # RESUMEN EJECUTIVO
    # --------------------------------------------------------

    with executive_tab:

        render_section_header(
            title="Indicadores ejecutivos",
            subtitle=(
                "Visión consolidada del cumplimiento, "
                "riesgos y estado operacional."
            ),
        )

        kpi_columns = st.columns(6)

        for column, kpi in zip(
            kpi_columns,
            dashboard_data["executive_kpis"],
        ):
            with column:
                render_kpi_card(
                    label=kpi["label"],
                    value=kpi["value"],
                    delta=kpi["delta"],
                    icon=kpi["icon"],
                    color=kpi["color"],
                    delta_warning=kpi[
                        "delta_warning"
                    ],
                )

        st.write("")

        (
            chart_column_1,
            chart_column_2,
            chart_column_3,
            status_column,
        ) = st.columns(
            [
                1.35,
                1.10,
                1.10,
                0.85,
            ]
        )

        # ----------------------------------------------------
        # SLA ÚLTIMOS 6 MESES
        # ----------------------------------------------------

        with chart_column_1:

            render_section_header(
                title="SLA últimos 6 meses"
            )

            sla_data = dashboard_data[
                "sla_history"
            ]

            sla_chart = go.Figure()

            sla_chart.add_trace(
                go.Scatter(
                    x=sla_data["Mes"],
                    y=sla_data[
                        "Cumplimiento SLA"
                    ],
                    mode="lines+markers",
                    name="Cumplimiento SLA",
                    line={
                        "color": "#078896",
                        "width": 3,
                    },
                    marker={
                        "size": 7,
                        "color": "#078896",
                    },
                )
            )

            sla_chart.add_trace(
                go.Scatter(
                    x=sla_data["Mes"],
                    y=sla_data["Meta SLA"],
                    mode="lines",
                    name="Meta SLA (95%)",
                    line={
                        "color": "#ed2472",
                        "width": 2,
                        "dash": "dot",
                    },
                )
            )

            sla_chart.update_yaxes(
                range=[80, 100],
                ticksuffix="%",
            )

            sla_chart.update_layout(
                legend={
                    "orientation": "h",
                    "yanchor": "top",
                    "y": -0.20,
                    "xanchor": "left",
                    "x": 0,
                }
            )

            apply_chart_layout(
                sla_chart,
                height=310,
            )

            st.plotly_chart(
                sla_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # INCIDENCIAS Y REPROCESOS
        # ----------------------------------------------------

        with chart_column_2:

            render_section_header(
                title="Incidencias / reprocesos"
            )

            incidents_data = dashboard_data[
                "incidents_history"
            ]

            incidents_chart = go.Figure()

            incidents_chart.add_trace(
                go.Bar(
                    x=incidents_data["Mes"],
                    y=incidents_data[
                        "Incidencias"
                    ],
                    name="Incidencias",
                    marker_color="#087889",
                )
            )

            incidents_chart.add_trace(
                go.Bar(
                    x=incidents_data["Mes"],
                    y=incidents_data[
                        "Reprocesos"
                    ],
                    name="Reprocesos",
                    marker_color="#ed2472",
                )
            )

            incidents_chart.update_layout(
                barmode="stack",
                legend={
                    "orientation": "h",
                    "yanchor": "top",
                    "y": -0.20,
                    "xanchor": "left",
                    "x": 0,
                },
            )

            apply_chart_layout(
                incidents_chart,
                height=310,
            )

            st.plotly_chart(
                incidents_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # DEUDA PREVISIONAL REGULARIZADA
        # ----------------------------------------------------

        with chart_column_3:

            render_section_header(
                title=(
                    "Deuda previsional "
                    "regularizada"
                )
            )

            debt_data = dashboard_data[
                "regularized_debt_history"
            ]

            debt_chart = go.Figure()

            debt_chart.add_trace(
                go.Scatter(
                    x=debt_data["Mes"],
                    y=debt_data["Monto MM$"],
                    mode="lines+markers",
                    fill="tozeroy",
                    line={
                        "color": "#087889",
                        "width": 3,
                    },
                    marker={
                        "size": 7,
                        "color": "#087889",
                    },
                    fillcolor=(
                        "rgba(7, 136, 150, 0.10)"
                    ),
                )
            )

            debt_chart.update_yaxes(
                title="MM$",
            )

            apply_chart_layout(
                debt_chart,
                height=310,
                show_legend=False,
            )

            st.plotly_chart(
                debt_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # ESTADO POR PROCESO
        # ----------------------------------------------------

        with status_column:

            render_process_status(
                title="Estado por proceso",
                items=dashboard_data[
                    "process_status"
                ],
            )

        st.write("")

        render_section_header(
            title="Pendientes clave",
            subtitle=(
                "Temas que requieren seguimiento "
                "para asegurar el cierre del período."
            ),
        )

        st.dataframe(
            dashboard_data["key_pending_items"],
            use_container_width=True,
            hide_index=True,
            height=220,
        )

    # --------------------------------------------------------
    # ANALÍTICA DE REMUNERACIONES
    # --------------------------------------------------------

    with payroll_tab:

        render_section_header(
            title="Analítica de remuneraciones",
            subtitle=(
                "Indicadores de nómina, costos, "
                "variaciones y eficiencia operacional."
            ),
        )

        (
            metric_1,
            metric_2,
            metric_3,
            metric_4,
        ) = st.columns(4)

        metric_1.metric(
            label="Nómina procesada",
            value="100%",
            delta="+1,2 pp",
        )

        metric_2.metric(
            label="Cumplimiento de plazos",
            value="98,6%",
            delta="+0,8 pp",
        )

        metric_3.metric(
            label="Errores críticos",
            value="7",
            delta="-3 vs mes anterior",
            delta_color="inverse",
        )

        metric_4.metric(
            label="Ahorro estimado",
            value="12,4%",
            delta="+2,1 pp",
        )

        st.write("")

        payroll_chart_1, payroll_chart_2 = (
            st.columns(2)
        )

        # ----------------------------------------------------
        # COSTO LÍQUIDO POR ÁREA
        # ----------------------------------------------------

        with payroll_chart_1:

            render_section_header(
                title="Costo líquido por área"
            )

            area_data = dashboard_data[
                "payroll_by_area"
            ]

            area_chart = px.bar(
                area_data,
                x="Área",
                y="Costo MM$",
                text="Costo MM$",
            )

            area_chart.update_traces(
                marker_color="#087889",
                textposition="outside",
            )

            apply_chart_layout(
                area_chart,
                height=350,
                show_legend=False,
            )

            st.plotly_chart(
                area_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # EVOLUCIÓN MENSUAL DE NÓMINA
        # ----------------------------------------------------

        with payroll_chart_2:

            render_section_header(
                title=(
                    "Evolución mensual de nómina"
                )
            )

            monthly_data = dashboard_data[
                "payroll_monthly_history"
            ]

            monthly_chart = go.Figure()

            monthly_chart.add_trace(
                go.Scatter(
                    x=monthly_data["Mes"],
                    y=monthly_data[
                        "Costo MM$"
                    ],
                    mode="lines+markers",
                    fill="tozeroy",
                    line={
                        "color": "#ed2472",
                        "width": 3,
                    },
                    marker={
                        "color": "#ed2472",
                        "size": 8,
                    },
                    fillcolor=(
                        "rgba(237, 36, 114, 0.08)"
                    ),
                )
            )

            apply_chart_layout(
                monthly_chart,
                height=350,
                show_legend=False,
            )

            st.plotly_chart(
                monthly_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        lower_chart_1, lower_chart_2 = (
            st.columns(2)
        )

        # ----------------------------------------------------
        # COMPOSICIÓN DE REMUNERACIONES
        # ----------------------------------------------------

        with lower_chart_1:

            render_section_header(
                title="Composición de remuneraciones"
            )

            composition_data = pd.DataFrame(
                {
                    "Concepto": [
                        "Sueldo base",
                        "Bonos",
                        "Horas extraordinarias",
                        "Asignaciones",
                        "Otros haberes",
                    ],
                    "Participación": [
                        65,
                        14,
                        8,
                        9,
                        4,
                    ],
                }
            )

            composition_chart = px.pie(
                composition_data,
                names="Concepto",
                values="Participación",
                hole=0.58,
                color_discrete_sequence=[
                    "#00364d",
                    "#078896",
                    "#ed2472",
                    "#f49a0b",
                    "#69bfc7",
                ],
            )

            composition_chart.update_traces(
                textposition="inside",
                textinfo="percent",
            )

            apply_chart_layout(
                composition_chart,
                height=330,
            )

            st.plotly_chart(
                composition_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # VARIACIÓN MENSUAL POR CONCEPTO
        # ----------------------------------------------------

        with lower_chart_2:

            render_section_header(
                title="Variación mensual por concepto"
            )

            variation_data = pd.DataFrame(
                {
                    "Concepto": [
                        "Sueldo base",
                        "Bonos",
                        "Horas extra",
                        "Asignaciones",
                        "Descuentos",
                    ],
                    "Variación %": [
                        1.2,
                        5.4,
                        -3.1,
                        2.7,
                        -0.8,
                    ],
                }
            )

            variation_data["Tipo"] = (
                variation_data[
                    "Variación %"
                ].apply(
                    lambda value: (
                        "Aumento"
                        if value >= 0
                        else "Disminución"
                    )
                )
            )

            variation_chart = px.bar(
                variation_data,
                x="Concepto",
                y="Variación %",
                color="Tipo",
                color_discrete_map={
                    "Aumento": "#078896",
                    "Disminución": "#ed2472",
                },
                text="Variación %",
            )

            variation_chart.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
            )

            apply_chart_layout(
                variation_chart,
                height=330,
            )

            st.plotly_chart(
                variation_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )


# ============================================================
# INTEGRACIONES
# ============================================================

with integrations_tab:

    render_section_header(
        title="Hub de integraciones",
        subtitle=(
            "Conectores, fuentes y estado del "
            "ecosistema tecnológico PREVIPAY."
        ),
    )

    integrations = dashboard_data[
        "integrations"
    ]

    for start_index in range(
        0,
        len(integrations),
        3,
    ):

        integration_columns = st.columns(3)

        integration_group = integrations[
            start_index:start_index + 3
        ]

        for column, integration in zip(
            integration_columns,
            integration_group,
        ):
            with column:
                render_integration_card(
                    name=integration["name"],
                    integration_type=integration[
                        "integration_type"
                    ],
                    status=integration["status"],
                    method=integration["method"],
                    last_sync=integration[
                        "last_sync"
                    ],
                    progress=integration[
                        "progress"
                    ],
                )

        st.write("")

    st.divider()

    render_section_header(
        title="Simulación de sincronización",
        subtitle=(
            "Ejecución demostrativa sin conexión "
            "a sistemas productivos."
        ),
    )

    sync_column_1, sync_column_2 = st.columns(
        [
            1,
            2,
        ]
    )

    with sync_column_1:

        selected_system = st.selectbox(
            "Sistema a sincronizar",
            options=[
                integration["name"]
                for integration in integrations
            ],
            key="integration_system",
        )

        execute_sync = st.button(
            "Ejecutar sincronización",
            type="primary",
            use_container_width=True,
        )

    with sync_column_2:

        st.info(
            "La simulación representa el flujo de "
            "conexión, validación, procesamiento y "
            "registro de trazabilidad."
        )

    if execute_sync:

        progress_bar = st.progress(
            0,
            text=(
                f"Conectando con "
                f"{selected_system}..."
            ),
        )

        stages = [
            (
                15,
                "Validando credenciales simuladas",
            ),
            (
                35,
                "Obteniendo información",
            ),
            (
                60,
                "Normalizando registros",
            ),
            (
                80,
                "Ejecutando controles",
            ),
            (
                100,
                "Registrando trazabilidad",
            ),
        ]

        for progress_value, progress_text in stages:

            time.sleep(0.35)

            progress_bar.progress(
                progress_value,
                text=progress_text,
            )

        st.success(
            f"Sincronización simulada con "
            f"{selected_system} completada."
        )

        (
            result_column_1,
            result_column_2,
            result_column_3,
        ) = st.columns(3)

        result_column_1.metric(
            "Registros procesados",
            "1.200",
        )

        result_column_2.metric(
            "Registros observados",
            "7",
        )

        result_column_3.metric(
            "Duración",
            "00:01:42",
        )

        st.code(
            f"""
RUN_ID: RUN-DEMO-20260729-001
SISTEMA: {selected_system}
ESTADO: COMPLETADO
AMBIENTE: DEMOSTRACIÓN
            """.strip(),
            language="text",
        )


# ============================================================
# CONTROL OPERACIONAL
# ============================================================

with control_tab:

    documents_tab, inconsistencies_tab = st.tabs(
        [
            "Carga de documentos",
            "Inconsistencias",
        ]
    )

    # --------------------------------------------------------
    # CARGA DE DOCUMENTOS
    # --------------------------------------------------------

    with documents_tab:

        render_section_header(
            title="Carga controlada de documentos",
            subtitle=(
                "Recepción, clasificación, validación "
                "y trazabilidad de archivos."
            ),
        )

        form_column_1, form_column_2 = st.columns(2)

        with form_column_1:

            document_type = st.selectbox(
                "Tipo de documento",
                options=[
                    "Novedades del período",
                    "Archivo de trabajadores",
                    "Resultados de remuneraciones",
                    "Archivo contable",
                    "Documento laboral",
                    "Archivo bancario",
                    "Otro",
                ],
            )

            document_origin = st.selectbox(
                "Sistema o canal de origen",
                options=[
                    "BUK",
                    "MAXXA",
                    "FIN700",
                    "Microsoft 365",
                    "Previred",
                    "Banco",
                    "Carga manual",
                ],
            )

        with form_column_2:

            document_period = st.selectbox(
                "Período asociado",
                options=[
                    "Julio 2026",
                    "Junio 2026",
                    "Mayo 2026",
                ],
                key="document_period",
            )

            document_responsible = st.text_input(
                "Responsable de la carga",
                value="Analista PREVIPAY",
            )

        uploaded_file = st.file_uploader(
            "Arrastra o selecciona un archivo",
            type=[
                "csv",
                "xlsx",
                "xls",
                "pdf",
                "json",
                "txt",
            ],
            help=(
                "Para la demostración se admiten "
                "archivos de hasta 10 MB."
            ),
        )

        if uploaded_file is None:

            st.info(
                "Selecciona un archivo para visualizar "
                "el flujo de validación documental."
            )

        else:

            (
                file_column_1,
                file_column_2,
                file_column_3,
            ) = st.columns(3)

            file_column_1.metric(
                "Archivo",
                uploaded_file.name,
            )

            file_column_2.metric(
                "Tamaño",
                (
                    f"{uploaded_file.size / 1024:.1f} KB"
                ),
            )

            extension = (
                uploaded_file.name
                .split(".")[-1]
                .upper()
            )

            file_column_3.metric(
                "Extensión",
                extension,
            )

            validate_document = st.button(
                "Validar y registrar documento",
                type="primary",
            )

            if validate_document:

                validation_progress = st.progress(
                    0,
                    text="Iniciando validación...",
                )

                document_stages = [
                    (
                        20,
                        "Validando extensión",
                    ),
                    (
                        40,
                        "Verificando tamaño",
                    ),
                    (
                        60,
                        "Calculando identificador",
                    ),
                    (
                        80,
                        "Registrando metadatos",
                    ),
                    (
                        100,
                        "Documento validado",
                    ),
                ]

                for (
                    stage_value,
                    stage_text,
                ) in document_stages:

                    time.sleep(0.25)

                    validation_progress.progress(
                        stage_value,
                        text=stage_text,
                    )

                st.success(
                    "Documento validado y registrado "
                    "correctamente en ambiente demo."
                )

                st.json(
                    {
                        "id_trazabilidad": (
                            "DOC-DEMO-20260729-001"
                        ),
                        "archivo": uploaded_file.name,
                        "tipo_documento": document_type,
                        "origen": document_origin,
                        "periodo": document_period,
                        "responsable": (
                            document_responsible
                        ),
                        "estado": "VALIDADO",
                        "ambiente": "DEMO",
                        "controles": {
                            "extension_permitida": True,
                            "tamaño_permitido": True,
                            "archivo_no_vacio": (
                                uploaded_file.size > 0
                            ),
                        },
                    }
                )

        st.write("")

        render_section_header(
            title="Documentos esperados del período"
        )

        expected_documents = pd.DataFrame(
            [
                {
                    "Documento": (
                        "Archivo de trabajadores"
                    ),
                    "Origen": "BUK",
                    "Estado": "Recibido",
                    "Responsable": (
                        "Analista PREVIPAY"
                    ),
                },
                {
                    "Documento": (
                        "Novedades del período"
                    ),
                    "Origen": "BUK",
                    "Estado": "Recibido",
                    "Responsable": (
                        "Analista PREVIPAY"
                    ),
                },
                {
                    "Documento": (
                        "Resultados de remuneraciones"
                    ),
                    "Origen": "BUK",
                    "Estado": "Recibido",
                    "Responsable": (
                        "Supervisor PREVIPAY"
                    ),
                },
                {
                    "Documento": "Archivo contable",
                    "Origen": "MAXXA",
                    "Estado": "Con observaciones",
                    "Responsable": (
                        "Supervisor PREVIPAY"
                    ),
                },
                {
                    "Documento": "Archivo bancario",
                    "Origen": "Banco",
                    "Estado": (
                        "Pendiente aprobación"
                    ),
                    "Responsable": "Cliente",
                },
            ]
        )

        st.dataframe(
            expected_documents,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # INCONSISTENCIAS
    # --------------------------------------------------------

    with inconsistencies_tab:

        render_section_header(
            title="Control de validaciones",
            subtitle=(
                "Alertas, anomalías e inconsistencias "
                "detectadas durante el período."
            ),
        )

        validation_summary = dashboard_data[
            "validation_summary"
        ]

        validation_columns = st.columns(
            len(validation_summary)
        )

        for column, validation in zip(
            validation_columns,
            validation_summary,
        ):
            with column:
                st.metric(
                    label=validation["label"],
                    value=validation["value"],
                )

        st.write("")

        filter_column_1, filter_column_2 = (
            st.columns(2)
        )

        with filter_column_1:

            severity_filter = st.multiselect(
                "Filtrar por tipo",
                options=[
                    "Crítica",
                    "Advertencia",
                    "Informativa",
                ],
                default=[
                    "Crítica",
                    "Advertencia",
                    "Informativa",
                ],
            )

        with filter_column_2:

            status_filter = st.multiselect(
                "Filtrar por estado",
                options=[
                    "Abierta",
                    "En curso",
                    "Resuelta",
                ],
                default=[
                    "Abierta",
                    "En curso",
                ],
            )

        validation_items = dashboard_data[
            "validation_items"
        ]

        filtered_validation_items = (
            validation_items[
                validation_items["Tipo"].isin(
                    severity_filter
                )
                & validation_items["Estado"].isin(
                    status_filter
                )
            ]
        )

        st.dataframe(
            filtered_validation_items,
            use_container_width=True,
            hide_index=True,
            height=250,
        )

        st.write("")

        render_section_header(
            title="Conciliación BUK ↔ MAXXA",
            subtitle=(
                "Comparación de la nómina líquida "
                "con la contabilización del período."
            ),
        )

        (
            reconciliation_1,
            reconciliation_2,
            reconciliation_3,
        ) = st.columns(3)

        reconciliation_1.metric(
            label="Total nómina",
            value="$1.302.000.000",
        )

        reconciliation_2.metric(
            label="Total contabilidad",
            value="$1.301.975.000",
        )

        reconciliation_3.metric(
            label="Diferencia",
            value="$25.000",
            delta="-$25.000",
            delta_color="inverse",
        )

        st.error(
            "La conciliación no puede cerrarse hasta "
            "resolver la diferencia contable detectada."
        )

        with st.expander(
            "Ver trazabilidad de la diferencia"
        ):

            st.markdown(
                """
                **Origen:** MAXXA

                **Control aplicado:** total líquido del
                período versus asiento contable preparado.

                **Resultado:** diferencia detectada de
                $25.000.

                **Posible causa:** centro de costo no
                informado en un movimiento del período.

                **Acción sugerida:** revisar el movimiento
                asociado al trabajador ficticio E009.

                **Responsable actual:** Supervisor PREVIPAY.

                **Estado:** En conciliación.
                """
            )


# ============================================================
# TICKETS
# ============================================================

with tickets_tab:

    render_section_header(
        title="Centro de tickets",
        subtitle=(
            "Gestión de incidencias, solicitudes y "
            "consultas entre el cliente y PREVIPAY."
        ),
    )

    st.info(
        "Este módulo permitirá registrar solicitudes, "
        "hacer seguimiento de incidencias, adjuntar "
        "evidencia y mantener trazabilidad completa "
        "entre el cliente y PREVIPAY."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tickets abiertos",
        "12"
    )

    col2.metric(
        "Tiempo medio respuesta",
        "1h 18m"
    )

    col3.metric(
        "SLA Tickets",
        "98,9%"
    )

    st.dataframe(
        pd.DataFrame(
            [
                ["TK-2418","Error cálculo licencia","Alta","En curso"],
                ["TK-2415","Consulta liquidación","Media","Pendiente"],
                ["TK-2411","Ajuste cotizaciones","Alta","Resuelto"],
            ],
            columns=[
                "Ticket",
                "Asunto",
                "Prioridad",
                "Estado",
            ],
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "PREVIPAY Platform · Prototipo visual con datos "
    "ficticios · Las integraciones son simuladas."
)