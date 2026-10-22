"""Carga de datos de demostración y gestión temporal por sesión.

El piloto deliberadamente NO escribe registros en GitHub ni promete persistencia.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import io
import re

import pandas as pd

from banco.config import CAMPOS

ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "data" / "intervenciones_demo.csv"


def registros_demo() -> pd.DataFrame:
    """Devuelve las fichas simuladas incluidas solo para comprobar la interfaz."""
    return pd.read_csv(DEMO_PATH, dtype=str, keep_default_na=False)[CAMPOS]


def reunir_registros(registros_sesion: list[dict] | None = None) -> pd.DataFrame:
    """Combina CSV demostrativo y fichas de la sesión activa del navegador."""
    base = registros_demo()
    if not registros_sesion:
        return base
    agregados = pd.DataFrame.from_records(registros_sesion).reindex(columns=CAMPOS, fill_value="")
    return pd.concat([base, agregados], ignore_index=True)


def nuevo_codigo(registros: pd.DataFrame) -> str:
    """Identificador demostrativo; no constituye numeración institucional concurrente."""
    nums = []
    for codigo in registros["codigo"].astype(str):
        encontrado = re.fullmatch(r"BII-2026-(\d{4})", codigo)
        if encontrado:
            nums.append(int(encontrado.group(1)))
    siguiente = max(nums, default=0) + 1
    return f"BII-2026-{siguiente:04d}"


def preparar_registro(datos: dict, codigo: str) -> dict:
    """Normaliza las claves del formulario al esquema de la matriz preliminar."""
    registro = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS}
    registro.update({
        "codigo": codigo,
        "estado_revision": "Por revisar",
        "origen_registro": "Usuario (sesión temporal)",
        "fecha_registro": date.today().isoformat(),
    })
    return registro


def filtrar(
    df: pd.DataFrame,
    termino: str = "",
    categorias: list[str] | None = None,
    evidencias: list[str] | None = None,
    departamentos: list[str] | None = None,
) -> pd.DataFrame:
    """Filtra por nombre, contenido y taxonomías sin perder filas vacías."""
    resultado = df.copy()
    if termino.strip():
        texto = termino.strip()
        columnas = ["codigo", "nombre", "problema", "descripcion", "entidad_responsable"]
        coincide = resultado[columnas].fillna("").astype(str).apply(
            lambda col: col.str.contains(texto, case=False, regex=False)
        ).any(axis=1)
        resultado = resultado.loc[coincide]
    if categorias:
        resultado = resultado[resultado["categoria"].isin(categorias)]
    if evidencias:
        resultado = resultado[resultado["tipo_evidencia"].isin(evidencias)]
    if departamentos:
        resultado = resultado[resultado["departamento"].isin(departamentos)]
    return resultado


def _celda_segura(valor: object) -> str:
    """Reduce la interpretación de fórmulas al abrir CSV en Excel/Calc."""
    texto = "" if pd.isna(valor) else str(valor)
    if texto.lstrip().startswith(("=", "+", "-", "@")) or texto[:1] in ("\t", "\r", "\n"):
        return "'" + texto
    return texto


def csv_bytes(df: pd.DataFrame) -> bytes:
    seguro = df.copy().astype(object)
    for col in seguro.columns:
        seguro[col] = seguro[col].map(_celda_segura)
    return seguro.to_csv(index=False).encode("utf-8-sig")


def csv_plantilla() -> bytes:
    return csv_bytes(pd.DataFrame(columns=CAMPOS))
