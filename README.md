# INF-8239 · Unidad 02 · Proyecto NLP

Autor académico: Nathanael

Proyecto base para LAB04–LAB06. No sustituya la comprensión por ejecución mecánica.

## Inicio rápido

```cmd
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
```

`uv sync` crea el entorno virtual (`.venv`) automáticamente — no se necesita ningún paso manual
de activación ni variables de entorno adicionales. Cree `.env` a partir de `.env.example` (ya
viene configurado con el dataset aprobado, ver sección Dataset). `scripts/download_data.py`
descarga el `.zip` oficial y construye `data/raw/dataset.csv`.

## Dataset

**Aprobado:** [UCI Sentiment Labelled Sentences](https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences)
(Kotzias et al., KDD 2015) — CC BY 4.0, 3,000 oraciones en inglés (1,000 cada una de Amazon, Yelp e
IMDb), etiqueta binaria positive/negative, sin datos personales.

La comparación de candidatos y la justificación de por qué se aceptó este dataset y se descartó el
otro está en `docs/dataset_candidates.csv`. El detalle completo (diccionario de datos, procedimiento
de obtención, riesgos y usos prohibidos) está en `docs/DATASET_CARD.md`.
El archivo `data/sample/demo_text.csv` solamente comprueba la arquitectura; no es el dataset de
entrega.

## Entrenamiento

```cmd
uv run python scripts/train_text.py
uv run streamlit run app/streamlit_app.py
```

## Notebook ejecutable

`notebooks/01_corpus_clasificador.ipynb` integra, de forma interactiva, la carga del dataset, el
análisis exploratorio, el entrenamiento y comparación de los 3 modelos, la matriz de confusión, el
análisis de errores y el desempeño por dominio (amazon/yelp/imdb). Reutiliza el código de
`src/inf8239_u02/`, no duplica lógica. Córralo con:

```cmd
uv run jupyter notebook notebooks/01_corpus_clasificador.ipynb
```

Después de ejecutarlo, categorice manualmente al menos 20 errores en
`reports/error_analysis.csv` (el notebook los extrae pero no los categoriza — eso requiere
criterio humano).

## Requirements

Después de `uv sync`, genere el `requirements.txt` exigido por el mandato a partir del lockfile
real del proyecto:

```cmd
uv export --format requirements.txt --no-dev --output-file requirements.txt
```

## Declaración de uso de IA

`docs/USO_DE_IA.md` — herramienta usada, qué se le pidió, qué se verificó con pruebas y
ejecución real (no por confianza), y qué correcciones se le hicieron.

## Interpretación

Toda conclusión debe separar observación, evidencia, interpretación y decisión.
