# Banco de Intervenciones e Innovaciones de Seguridad Ciudadana

**Piloto Streamlit, versión 0.1.** Desarrollo incremental basado en la presentación conceptual y metodológica del **22 de octubre de 2026**. No es un sistema institucional final ni un repositorio oficial de intervenciones evaluadas.

## Funcionalidades implementadas

- Inicio con cuatro categorías, ciclo institucional y visualización básica.
- Catálogo consultable y filtros por texto, categoría, tipo de evidencia y ámbito.
- Fichas de caracterización y fuente documental.
- Registro provisional mediante formulario y descarga de CSV.
- Comparación descriptiva entre dos fichas.
- Sección metodológica y hoja de ruta inicial.

**Datos de ejemplo:** las seis fichas incluidas son completamente ficticias y se usan para probar la interfaz. No afirman resultados, efectos causales ni efectividad de intervenciones reales.

## Ejecutar en tu computadora

Necesitas Python 3.10 o superior, Git (opcional) e Internet para instalar paquetes.

```bash
# Dentro de la carpeta del proyecto:
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Streamlit abrirá una página local, habitualmente `http://localhost:8501`.

## Publicar en GitHub

1. Crea un repositorio de GitHub, por ejemplo `banco-intervenciones-seguridad-ciudadana`.
2. Sube el **contenido de esta carpeta** (no solo el archivo ZIP). Conserva `app.py`, `requirements.txt`, `banco/`, `data/` y `.streamlit/` en la raíz.
3. Alternativamente, ejecuta los comandos siguientes después de crear un repositorio vacío:

```bash
git init
git add .
git commit -m "MVP Streamlit 0.1 - Banco de Intervenciones"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

Reemplaza `TU_USUARIO` y `TU_REPOSITORIO` por los tuyos. El repositorio no se ha creado automáticamente.

## Publicar en Streamlit Community Cloud

1. Ingresa a https://share.streamlit.io/ e inicia sesión con GitHub.
2. Elige crear una aplicación, selecciona tu repositorio y la rama `main`.
3. Indica `app.py` como archivo principal.
4. Despliega. La plataforma resolverá las dependencias desde `requirements.txt`.

**Aviso:** la publicación pública puede exponer las fichas de demostración. No se debe incorporar información reservada, personal o sujeta a restricciones de acceso. El alojamiento y uso deben evaluarse antes de manejar información institucional.

## Limitaciones explícitas de esta versión

- Los registros nuevos se almacenan exclusivamente en `st.session_state`: **desaparecen al cerrar o reiniciar la sesión** y no son compartidos entre usuarios.
- El CSV se exporta para respaldo manual; no se guarda en GitHub ni constituye un repositorio central.
- No existen roles, inicio de sesión, aprobación de fichas ni trazabilidad de ediciones.
- No hay conexión a bases institucionales ni API externas.
- La clasificación empírica/práctica/científica es **descriptiva**, no una valoración de calidad o efectividad.
- La matriz de campos, los estados y los ejemplos necesitan validación con la entidad promotora.
- El código de registro es provisional: no debe usarse como identificador único en un entorno multiusuario.

## Arquitectura

```text
app.py                         # Vistas de Streamlit
banco/config.py                # Taxonomías y campos provisionales
banco/data.py                  # Filtros, datos y exportación segura
banco/ui.py                    # Estilos institucionales
data/intervenciones_demo.csv   # Fichas ficticias
.streamlit/config.toml         # Colores de la PPT
requirements.txt               # Dependencias
tests/test_data.py             # Pruebas básicas
.github/workflows/tests.yml    # Tests automatizados en GitHub
```

## Próxima iteración sugerida

Validar la matriz con las oficinas informantes, definir quién registra/revisa/aprueba, precisar campos obligatorios y desarrollar la persistencia con una base de datos y controles de acceso apropiados.
