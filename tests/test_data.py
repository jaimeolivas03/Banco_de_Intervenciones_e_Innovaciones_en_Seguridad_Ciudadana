"""Pruebas de la estructura mínima y reglas del registro."""

import pandas as pd

from banco.config import CAMPOS, CATEGORIAS, TIPOS_EVIDENCIA
from banco.data import csv_bytes, csv_plantilla, filtrar, nuevo_codigo, preparar_registro, registros_demo, reunir_registros


def test_demo_sigue_esquema():
    demo = registros_demo()
    assert list(demo.columns) == CAMPOS
    assert demo["categoria"].isin(CATEGORIAS).all()
    assert demo["tipo_evidencia"].isin(TIPOS_EVIDENCIA).all()
    assert demo["origen_registro"].eq("Demostración ficticia").all()


def test_filtro_sin_regex():
    demo = registros_demo()
    resultado = filtrar(demo, termino="[")
    assert resultado.empty
    assert len(filtrar(demo, categorias=["Buenas prácticas"])) >= 1


def test_codigo_registro_sesion():
    demo = registros_demo()
    codigo = nuevo_codigo(demo)
    nuevo = preparar_registro({"nombre": "Ejemplo", "problema": "Ejemplo"}, codigo)
    registros = reunir_registros([nuevo])
    assert len(registros) == len(demo) + 1
    assert nuevo["estado_revision"] == "Por revisar"
    assert nuevo["origen_registro"] == "Usuario (sesión temporal)"
    assert nuevo_codigo(registros) != codigo


def test_matriz_y_csv_seguro():
    template = pd.read_csv(pd.io.common.BytesIO(csv_plantilla()), encoding="utf-8-sig")
    assert list(template.columns) == CAMPOS
    df = pd.DataFrame([{"nombre": "=2+3"}])
    texto = csv_bytes(df).decode("utf-8-sig")
    assert "'=2+3" in texto
