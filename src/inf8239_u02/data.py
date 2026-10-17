from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

import pandas as pd

from .config import settings


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    selected = path or settings.dataset_path
    if not selected.exists():
        raise FileNotFoundError(f"Dataset no encontrado: {selected}")
    return pd.read_csv(selected)


def validate_dataframe(df: pd.DataFrame, text_column: str, target_column: str) -> None:
    missing = {text_column, target_column} - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")
    if df.empty:
        raise ValueError("El dataset está vacío")
    if df[text_column].fillna("").astype(str).str.strip().eq("").any():
        raise ValueError("Existen textos vacíos")
    if df[target_column].nunique(dropna=True) < 2:
        raise ValueError("Se requieren al menos dos clases")


# --- Dataset aprobado: UCI "Sentiment Labelled Sentences" (Kotzias et al., KDD 2015) ---
# https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences — CC BY 4.0
#
# El .zip oficial de UCI no trae un CSV único: contiene tres archivos de texto
# separados por tabulador (oración<TAB>etiqueta), uno por dominio de reseña
# (Amazon, IMDb, Yelp). Esta función hace la combinación que el resto del
# proyecto espera: un único DataFrame con columnas text/label/source.
_UCI_SOURCE_FILES: dict[str, str] = {
    "amazon_cells_labelled.txt": "amazon",
    "imdb_labelled.txt": "imdb",
    "yelp_labelled.txt": "yelp",
}
_UCI_LABEL_MAP: dict[str, str] = {"0": "negative", "1": "positive"}


def build_dataset_from_uci_zip(zip_bytes: bytes) -> pd.DataFrame:
    """Combina los 3 archivos del .zip de UCI Sentiment Labelled Sentences.

    Extrae en memoria amazon_cells_labelled.txt, imdb_labelled.txt y
    yelp_labelled.txt, normaliza la etiqueta numérica (0/1) a
    'negative'/'positive' y agrega una columna 'source' para trazar el
    dominio de origen de cada oración (requerido para el diccionario de
    datos y el análisis de riesgos del Dataset Card).

    Lanza ValueError si algún archivo esperado no está dentro del .zip,
    para fallar de forma explícita en vez de producir un dataset parcial.
    """
    frames: list[pd.DataFrame] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        names = archive.namelist()
        for filename, source in _UCI_SOURCE_FILES.items():
            matches = [name for name in names if name.endswith(filename)]
            if not matches:
                raise ValueError(
                    f"No se encontró '{filename}' dentro del .zip descargado. "
                    f"Archivos presentes: {names}"
                )
            raw = archive.read(matches[0]).decode("utf-8", errors="replace")
            rows = []
            for line in raw.splitlines():
                if not line.strip():
                    continue
                parts = line.rsplit("\t", 1)
                if len(parts) != 2:
                    continue
                text, score = parts
                label = _UCI_LABEL_MAP.get(score.strip(), score.strip())
                rows.append({"text": text.strip(), "label": label, "source": source})
            frames.append(pd.DataFrame(rows, columns=["text", "label", "source"]))

    if not frames:
        raise ValueError("No se pudo construir el dataset: el .zip no contenía archivos válidos")

    combined = pd.concat(frames, ignore_index=True)
    return combined
