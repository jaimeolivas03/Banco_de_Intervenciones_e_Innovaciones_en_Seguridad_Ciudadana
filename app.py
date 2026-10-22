"""Banco de Intervenciones e Innovaciones de Seguridad Ciudadana.

MVP 0.1 en Streamlit. Modelo funcional provisional según PPT del 22/10/2026.
Ejecutar: streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from banco.config import CATEGORIAS, FASES, NIVELES_GOBIERNO, TIPOS_EVIDENCIA
from banco.data import csv_bytes, csv_plantilla, filtrar, nuevo_codigo, preparar_registro, reunir_registros
from banco.ui import aplicar_estilos, etiqueta_piloto, hero, paso


st.set_page_config(
    page_title="Banco de Intervenciones | Seguridad Ciudadana",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_estilos()

if "registros_temporales" not in st.session_state:
    st.session_state["registros_temporales"] = []

registros = reunir_registros(st.session_state["registros_temporales"])

with st.sidebar:
    st.markdown("## 🛡️ Banco de Intervenciones")
    st.caption("Seguridad ciudadana · Plataforma piloto")
    st.divider()
    pagina = st.radio(
        "Navegación",
        [
            "Inicio",
            "Explorar intervenciones",
            "Registrar intervención",
            "Comparar fichas",
            "Metodología y hoja de ruta",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("**Estado del desarrollo:** piloto funcional 0.1")
    st.caption("Almacenamiento: exclusivamente en esta sesión. No publicar información reservada.")
    st.caption("Paleta extraída de la presentación del 22/10/2026.")


def detalle_ficha(ficha: pd.Series) -> None:
    st.subheader(str(ficha["nombre"]))
    st.caption(f'Código: {ficha["codigo"]} · Origen: {ficha["origen_registro"]}')
    a, b, c = st.columns(3)
    a.write(f'**Categoría**  \n{ficha["categoria"]}')
    b.write(f'**Evidencia declarada**  \n{ficha["tipo_evidencia"]}')
    c.write(f'**Estado documental**  \n{ficha["estado_revision"]}')
    st.divider()
    campos = [
        ("Problema público", "problema"),
        ("Objetivo", "objetivo"),
        ("Descripción", "descripcion"),
        ("Población objetivo", "poblacion_objetivo"),
        ("Ámbito territorial", "departamento"),
        ("Provincia / distrito", "provincia_distrito"),
        ("Nivel de gobierno", "nivel_gobierno"),
        ("Entidad responsable", "entidad_responsable"),
        ("Componentes principales", "componentes"),
        ("Resultados reportados", "resultados"),
        ("Indicador disponible", "indicador"),
        ("Fuente documental", "fuente"),
        ("Año de referencia", "anio"),
        ("Fase de gestión", "fase_gestion"),
        ("Condiciones de replicabilidad", "replicabilidad"),
    ]
    for titulo, clave in campos:
        valor = str(ficha.get(clave, "")).strip()
        st.markdown(f"**{titulo}:** {valor if valor else 'No consignado'}")
    st.info(
        "La clasificación del tipo de evidencia es descriptiva. "
        "No equivale a una calificación de eficacia, calidad metodológica o impacto causal."
    )


def inicio() -> None:
    hero(
        "Banco de Intervenciones e Innovaciones de Seguridad Ciudadana",
        "Herramienta de gestión del conocimiento para identificar, sistematizar, "
        "evaluar y compartir intervenciones que orienten decisiones de los gobiernos regionales y locales.",
    )
    etiqueta_piloto()

    a, b, c, d = st.columns(4)
    a.metric("Fichas en el piloto", len(registros))
    b.metric("Categorías previstas", len(CATEGORIAS))
    c.metric("Tipos de evidencia", len(TIPOS_EVIDENCIA))
    d.metric("Registros de esta sesión", len(st.session_state["registros_temporales"]))

    st.markdown("### Ámbitos del Banco")
    cols = st.columns(4)
    descripciones = [
        "Objetivos, componentes y coordinación entre actores.",
        "Instrumentos distritales sujetos a revisión y categorización.",
        "Infraestructura, tecnología y capacidades públicas.",
        "Experiencias empíricas que requieren documentación y valoración.",
    ]
    for columna, categoria, descripcion in zip(cols, CATEGORIAS, descripciones):
        with columna:
            with st.container(border=True):
                st.markdown(f"**{categoria}**")
                st.caption(descripcion)

    st.markdown("### Ciclo de gestión y aprendizaje institucional")
    cols = st.columns(4)
    textos = [
        "Reconocer problemas, actores y experiencias.",
        "Ordenar y documentar información comparable.",
        "Examinar procesos, resultados e impacto, según evidencia disponible.",
        "Difundir aprendizajes y orientar su transferencia.",
    ]
    for indice, (columna, fase, descripcion) in enumerate(zip(cols, FASES, textos), 1):
        with columna:
            paso(f"0{indice}", fase, descripcion)

    st.markdown("### Distribución de fichas por categoría")
    st.caption("Conteos de datos simulados y registros añadidos en esta sesión; no representan cobertura real del Banco.")
    cuentas = registros["categoria"].value_counts().reindex(CATEGORIAS, fill_value=0).reset_index()
    cuentas.columns = ["Categoría", "Registros"]
    st.bar_chart(cuentas.set_index("Categoría"), horizontal=True, color="#CF0000")


def explorar() -> None:
    hero("Catálogo de intervenciones", "Consulta y filtrado de fichas piloto mediante criterios comunes.")
    etiqueta_piloto()
    busqueda = st.text_input("Buscar por nombre, problema, entidad o código", placeholder="Ej.: prevención, patrullaje, videovigilancia")
    col1, col2, col3 = st.columns(3)
    with col1:
        categorias = st.multiselect("Categoría", CATEGORIAS)
    with col2:
        evidencias = st.multiselect("Tipo de evidencia declarado", TIPOS_EVIDENCIA)
    with col3:
        departamentos = st.multiselect("Departamento / ámbito", sorted(registros["departamento"].dropna().unique()))

    seleccion = filtrar(registros, busqueda, categorias, evidencias, departamentos)
    st.caption(f"{len(seleccion)} ficha(s) que cumplen los filtros")
    if seleccion.empty:
        st.warning("No hay fichas con estos criterios. Modifique los filtros.")
        return

    columnas = ["codigo", "nombre", "categoria", "tipo_evidencia", "departamento", "estado_revision"]
    st.dataframe(
        seleccion[columnas].rename(columns={
            "codigo": "Código", "nombre": "Intervención", "categoria": "Categoría",
            "tipo_evidencia": "Evidencia", "departamento": "Ámbito", "estado_revision": "Estado",
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Descargar resultados filtrados (CSV)",
        data=csv_bytes(seleccion),
        file_name="catalogo_filtrado_banco.csv",
        mime="text/csv",
    )
    opciones = seleccion["codigo"].tolist()
    codigo = st.selectbox(
        "Abrir ficha de intervención",
        opciones,
        format_func=lambda valor: f'{valor} · {seleccion.loc[seleccion["codigo"] == valor, "nombre"].iloc[0]}',
    )
    st.divider()
    detalle_ficha(seleccion.loc[seleccion["codigo"] == codigo].iloc[0])


def registrar() -> None:
    hero("Registro y sistematización", "Matriz preliminar de recojo de información. Los campos podrán ajustarse durante la validación metodológica.")
    st.warning(
        "Los datos ingresados se mantienen solo durante la sesión del navegador. "
        "Descargue el CSV si desea conservarlos. No existe base de datos persistente ni control de acceso en esta versión."
    )
    st.download_button(
        "Descargar matriz vacía (CSV)",
        data=csv_plantilla(),
        file_name="matriz_recojo_informacion.csv",
        mime="text/csv",
    )
    with st.form("form_nueva_intervencion", clear_on_submit=True):
        st.markdown("#### Identificación")
        nombre = st.text_input("Nombre de la intervención *")
        categoria = st.selectbox("Categoría *", CATEGORIAS)
        a, b = st.columns(2)
        with a:
            tipo_evidencia = st.selectbox("Tipo de evidencia declarado *", TIPOS_EVIDENCIA)
            departamento = st.text_input("Departamento / ámbito territorial")
            nivel_gobierno = st.selectbox("Nivel de gobierno", NIVELES_GOBIERNO)
        with b:
            anio = st.number_input("Año de referencia", min_value=1990, max_value=2100, value=2026, step=1)
            provincia_distrito = st.text_input("Provincia / distrito")
            entidad_responsable = st.text_input("Entidad responsable")
        poblacion_objetivo = st.text_input("Población objetivo")

        st.markdown("#### Caracterización y resultados")
        problema = st.text_area("Problema público que aborda *")
        objetivo = st.text_area("Objetivo de la intervención")
        descripcion = st.text_area("Descripción de la intervención")
        componentes = st.text_area("Componentes o actividades principales")
        resultados = st.text_area("Resultados disponibles (sin atribuir causalidad no acreditada)")
        indicador = st.text_input("Indicador de seguimiento o evaluación")
        fuente = st.text_input("Fuente documental / referencia verificable")
        replicabilidad = st.text_area("Condiciones necesarias para replicabilidad")
        fase_gestion = st.selectbox("Fase actual del ciclo", FASES)
        enviar = st.form_submit_button("Guardar ficha en esta sesión", type="primary")

    if enviar:
        if not nombre.strip() or not problema.strip():
            st.error("Complete los campos obligatorios: nombre y problema público.")
        else:
            codigo = nuevo_codigo(registros)
            datos = {
                "nombre": nombre, "categoria": categoria, "tipo_evidencia": tipo_evidencia,
                "problema": problema, "objetivo": objetivo, "descripcion": descripcion,
                "poblacion_objetivo": poblacion_objetivo, "departamento": departamento,
                "provincia_distrito": provincia_distrito, "nivel_gobierno": nivel_gobierno,
                "entidad_responsable": entidad_responsable, "componentes": componentes,
                "resultados": resultados, "indicador": indicador, "fuente": fuente,
                "anio": str(anio), "fase_gestion": fase_gestion, "replicabilidad": replicabilidad,
            }
            st.session_state["registros_temporales"].append(preparar_registro(datos, codigo))
            st.success(f"Ficha {codigo} registrada temporalmente. Puede consultarla en el catálogo.")

    if st.session_state["registros_temporales"]:
        st.divider()
        st.markdown("#### Respaldo de fichas de esta sesión")
        solo_sesion = pd.DataFrame(st.session_state["registros_temporales"])
        st.download_button(
            "Descargar fichas ingresadas (CSV)",
            data=csv_bytes(solo_sesion),
            file_name="fichas_registradas_sesion.csv",
            mime="text/csv",
        )


def comparar() -> None:
    hero("Comparación de fichas", "Contraste descriptivo de condiciones de implementación y documentación disponible.")
    if len(registros) < 2:
        st.info("Se requieren al menos dos fichas.")
        return
    nombres = dict(zip(registros["codigo"], registros["nombre"]))
    a, b = st.columns(2)
    with a:
        codigo_a = st.selectbox("Primera intervención", list(nombres), index=0, format_func=lambda x: f"{x} · {nombres[x]}")
    with b:
        codigo_b = st.selectbox("Segunda intervención", list(nombres), index=1, format_func=lambda x: f"{x} · {nombres[x]}")
    if codigo_a == codigo_b:
        st.info("Seleccione intervenciones diferentes para la comparación.")
        return
    ficha_a = registros.loc[registros["codigo"] == codigo_a].iloc[0]
    ficha_b = registros.loc[registros["codigo"] == codigo_b].iloc[0]
    comparables = [
        ("Categoría", "categoria"), ("Tipo de evidencia declarado", "tipo_evidencia"),
        ("Problema", "problema"), ("Objetivo", "objetivo"),
        ("Territorio", "departamento"), ("Población objetivo", "poblacion_objetivo"),
        ("Entidad responsable", "entidad_responsable"), ("Resultados", "resultados"),
        ("Indicador", "indicador"), ("Fuente", "fuente"),
        ("Condiciones de replicabilidad", "replicabilidad"),
    ]
    comparacion = pd.DataFrame([
        {
            "Dimensión": etiqueta,
            f"{codigo_a}": ficha_a[campo] or "No consignado",
            f"{codigo_b}": ficha_b[campo] or "No consignado",
        }
        for etiqueta, campo in comparables
    ])
    st.dataframe(comparacion, use_container_width=True, hide_index=True)
    st.caption("Esta tabla no establece cuál intervención es más eficaz ni determina su replicabilidad.")


def metodologia() -> None:
    hero("Metodología y hoja de ruta", "Criterios preliminares derivados del diseño conceptual y metodológico.")
    st.markdown("### Tipos de evidencia")
    col1, col2, col3 = st.columns(3)
    contenidos = [
        ("Evidencia empírica", "Prácticas de campo, saberes tácitos y experiencias que podrían no estar formalizadas."),
        ("Evidencia práctica", "Planes, proyectos y programas con registros de ejecución y gestión."),
        ("Evidencia científica", "Estudios evaluativos rigurosos, artículos y síntesis científicas verificables."),
    ]
    for col, (titulo, cuerpo) in zip((col1, col2, col3), contenidos):
        with col:
            with st.container(border=True):
                st.markdown(f"**{titulo}**")
                st.write(cuerpo)
    st.info(
        "La categoría documental no determina, por sí sola, la efectividad. "
        "El protocolo de evaluación, las escalas de calidad y los requisitos de validación aún deben definirse."
    )
    st.markdown("### Flujo preliminar de información")
    st.write(
        "Solicitud de información → recepción → registro → revisión → evaluación "
        "→ actualización → difusión. Esta secuencia está en fase de diseño y no "
        "representa un procedimiento institucional aprobado."
    )
    st.markdown("### Próximos pasos propuestos en la presentación")
    for titulo, texto in [
        ("1. Construir la matriz de recojo de información", "Definir variables, campos, criterios y responsables."),
        ("2. Solicitar información a oficinas informantes", "Precisar necesidades documentales, formato y plazos de atención."),
        ("3. Elaborar fichas piloto", "Validar estructura, criterios de análisis y utilidad del Banco."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{titulo}**")
            st.write(texto)
    st.markdown("### Decisiones pendientes")
    st.write(
        "Están pendientes la validación de la matriz, definición de usuarios y permisos, "
        "fuentes oficiales, protocolo de revisión y evaluación, mecanismos de actualización "
        "y una solución de almacenamiento seguro y persistente."
    )


PAGINAS = {
    "Inicio": inicio,
    "Explorar intervenciones": explorar,
    "Registrar intervención": registrar,
    "Comparar fichas": comparar,
    "Metodología y hoja de ruta": metodologia,
}
PAGINAS[pagina]()

st.divider()
st.caption("Banco de Intervenciones e Innovaciones de Seguridad Ciudadana · Prototipo académico y funcional · v0.1")
