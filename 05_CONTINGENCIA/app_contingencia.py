from __future__ import annotations

import io

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="PREVIPAY | Contingencia",
    page_icon="🧮",
    layout="wide",
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .previpay-header {
        background: linear-gradient(135deg, #003B4A 0%, #075E6B 100%);
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        color: white;
    }

    .previpay-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }

    .previpay-header p {
        margin: 0.45rem 0 0 0;
        opacity: 0.90;
    }

    .demo-box {
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.2rem;
        background: #FFFFFF;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COLUMNAS OBLIGATORIAS
# ============================================================

REQUIRED_COLUMNS = [
    "RUT_TRABAJADOR",
    "NOMBRE_TRABAJADOR",
    "SUELDO_BASE",
    "DIAS_TRABAJADOS",
    "HORAS_EXTRA",
    "VALOR_HORA_EXTRA",
    "BONOS",
    "COMISIONES",
    "OTROS_HABERES",
    "DESCUENTO_PREVISIONAL",
    "DESCUENTO_SALUD",
    "IMPUESTO",
    "OTROS_DESCUENTOS",
]

NUMERIC_COLUMNS = [
    "SUELDO_BASE",
    "DIAS_TRABAJADOS",
    "HORAS_EXTRA",
    "VALOR_HORA_EXTRA",
    "BONOS",
    "COMISIONES",
    "OTROS_HABERES",
    "DESCUENTO_PREVISIONAL",
    "DESCUENTO_SALUD",
    "IMPUESTO",
    "OTROS_DESCUENTOS",
]


# ============================================================
# FUNCIONES
# ============================================================

def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normaliza los encabezados del archivo."""

    df = dataframe.copy()

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )

    return df


def validate_file(dataframe: pd.DataFrame) -> list[str]:
    """Identifica las columnas obligatorias que faltan."""

    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]


def calculate_payroll(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta un cálculo demostrativo de remuneraciones."""

    df = normalize_columns(dataframe)

    missing_columns = validate_file(df)

    if missing_columns:
        raise ValueError(
            "Faltan las siguientes columnas obligatorias: "
            + ", ".join(missing_columns)
        )

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        ).fillna(0)

    if (df["DIAS_TRABAJADOS"] < 0).any():
        raise ValueError(
            "DIAS_TRABAJADOS no puede contener valores negativos."
        )

    if (df["DIAS_TRABAJADOS"] > 30).any():
        raise ValueError(
            "DIAS_TRABAJADOS no puede ser superior a 30."
        )

    monetary_columns = [
        column
        for column in NUMERIC_COLUMNS
        if column != "DIAS_TRABAJADOS"
    ]

    if (df[monetary_columns] < 0).any().any():
        raise ValueError(
            "La planilla contiene montos negativos."
        )

    df["SUELDO_PROPORCIONAL"] = (
        df["SUELDO_BASE"]
        * df["DIAS_TRABAJADOS"]
        / 30
    ).round(0)

    df["PAGO_HORAS_EXTRA"] = (
        df["HORAS_EXTRA"]
        * df["VALOR_HORA_EXTRA"]
    ).round(0)

    df["TOTAL_HABERES"] = (
        df["SUELDO_PROPORCIONAL"]
        + df["PAGO_HORAS_EXTRA"]
        + df["BONOS"]
        + df["COMISIONES"]
        + df["OTROS_HABERES"]
    ).round(0)

    df["TOTAL_DESCUENTOS"] = (
        df["DESCUENTO_PREVISIONAL"]
        + df["DESCUENTO_SALUD"]
        + df["IMPUESTO"]
        + df["OTROS_DESCUENTOS"]
    ).round(0)

    df["LIQUIDO_A_PAGO"] = (
        df["TOTAL_HABERES"]
        - df["TOTAL_DESCUENTOS"]
    ).round(0)

    df["ESTADO"] = "CALCULADO"

    df.loc[
        df["LIQUIDO_A_PAGO"] < 0,
        "ESTADO",
    ] = "REVISAR"

    result_columns = [
        "RUT_TRABAJADOR",
        "NOMBRE_TRABAJADOR",
        "SUELDO_BASE",
        "DIAS_TRABAJADOS",
        "SUELDO_PROPORCIONAL",
        "PAGO_HORAS_EXTRA",
        "BONOS",
        "COMISIONES",
        "OTROS_HABERES",
        "TOTAL_HABERES",
        "DESCUENTO_PREVISIONAL",
        "DESCUENTO_SALUD",
        "IMPUESTO",
        "OTROS_DESCUENTOS",
        "TOTAL_DESCUENTOS",
        "LIQUIDO_A_PAGO",
        "ESTADO",
    ]

    return df[result_columns]


def format_clp(value: float) -> str:
    """Formatea montos en pesos chilenos."""

    return f"${value:,.0f}".replace(",", ".")


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="previpay-header">
        <h1>PREVIPAY | Continuidad operacional</h1>
        <p>
            Procesamiento alternativo de remuneraciones ante una
            indisponibilidad temporal del sistema principal.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Ambiente demostrativo con datos ficticios. "
    "Esta calculadora utiliza los descuentos informados en la planilla "
    "y no reemplaza las validaciones legales, tributarias, contractuales "
    "ni previsionales de un sistema productivo."
)


# ============================================================
# CARGA DE ARCHIVO
# ============================================================

st.subheader("1. Cargar planilla de trabajadores")

uploaded_file = st.file_uploader(
    "Arrastra o selecciona una planilla",
    type=["xlsx", "xls", "csv"],
    help="Utiliza la plantilla demostrativa PREVIPAY.",
)


if uploaded_file is None:

    st.info(
        "Carga la plantilla ficticia para comenzar la demostración."
    )

    st.markdown(
        """
        ### Flujo de contingencia

        1. Recepción de la planilla estandarizada.
        2. Validación de estructura y campos obligatorios.
        3. Ejecución del cálculo.
        4. Revisión de resultados y alertas.
        5. Descarga del consolidado.
        """
    )

else:

    try:

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            payroll_input = pd.read_csv(
                uploaded_file,
                sep=None,
                engine="python",
            )
        else:
            payroll_input = pd.read_excel(
                uploaded_file,
                sheet_name="CARGA_REMUNERACIONES",
            )

        payroll_input = normalize_columns(payroll_input)

        missing_columns = validate_file(payroll_input)

        if missing_columns:
            st.error(
                "La planilla no cumple con la estructura requerida."
            )

            st.write("Columnas faltantes:")

            for column in missing_columns:
                st.write(f"- {column}")

            st.stop()

        st.success(
            f"Archivo cargado correctamente: {uploaded_file.name}"
        )

        metric_1, metric_2, metric_3 = st.columns(3)

        with metric_1:
            st.metric(
                "Trabajadores cargados",
                len(payroll_input),
            )

        with metric_2:
            st.metric(
                "Columnas detectadas",
                len(payroll_input.columns),
            )

        with metric_3:
            st.metric(
                "Validación estructural",
                "Correcta",
            )

        with st.expander(
            "Vista previa de la planilla",
            expanded=False,
        ):
            st.dataframe(
                payroll_input.head(10),
                hide_index=True,
                use_container_width=True,
            )

        st.subheader("2. Ejecutar cálculo")

        if st.button(
            "Calcular remuneraciones",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["payroll_result"] = calculate_payroll(
                payroll_input
            )

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(
            "No fue posible procesar el archivo. "
            "Verifica que corresponda a la plantilla PREVIPAY."
        )

        with st.expander("Detalle técnico"):
            st.code(str(error))


# ============================================================
# RESULTADOS
# ============================================================

if "payroll_result" in st.session_state:

    payroll_result = st.session_state["payroll_result"]

    st.divider()

    st.subheader("3. Resultado del procesamiento")

    total_workers = len(payroll_result)
    total_earnings = payroll_result["TOTAL_HABERES"].sum()
    total_deductions = payroll_result["TOTAL_DESCUENTOS"].sum()
    total_net = payroll_result["LIQUIDO_A_PAGO"].sum()

    result_1, result_2, result_3, result_4 = st.columns(4)

    with result_1:
        st.metric(
            "Trabajadores",
            total_workers,
        )

    with result_2:
        st.metric(
            "Total haberes",
            format_clp(total_earnings),
        )

    with result_3:
        st.metric(
            "Total descuentos",
            format_clp(total_deductions),
        )

    with result_4:
        st.metric(
            "Líquido a pagar",
            format_clp(total_net),
        )

    records_to_review = payroll_result[
        payroll_result["ESTADO"] == "REVISAR"
    ]

    if records_to_review.empty:
        st.success(
            "Procesamiento finalizado. "
            "No se detectaron líquidos negativos."
        )
    else:
        st.warning(
            f"Existen {len(records_to_review)} registros que requieren revisión."
        )

    st.dataframe(
        payroll_result,
        hide_index=True,
        use_container_width=True,
    )

    output_buffer = io.BytesIO()

    with pd.ExcelWriter(
        output_buffer,
        engine="openpyxl",
    ) as writer:
        payroll_result.to_excel(
            writer,
            index=False,
            sheet_name="RESULTADO_REMUNERACIONES",
        )

    output_buffer.seek(0)

    st.download_button(
        label="Descargar resultado en Excel",
        data=output_buffer,
        file_name="PREVIPAY_RESULTADO_CONTINGENCIA.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
    )
