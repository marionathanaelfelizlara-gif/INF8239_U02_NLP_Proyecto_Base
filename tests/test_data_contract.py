import io
import zipfile

import pandas as pd
import pytest

from inf8239_u02.data import build_dataset_from_uci_zip, validate_dataframe


def test_accepts_valid_dataframe():
    df = pd.DataFrame({"text": ["uno", "dos"], "label": ["a", "b"]})
    validate_dataframe(df, "text", "label")


def test_rejects_missing_target():
    df = pd.DataFrame({"text": ["uno"]})
    with pytest.raises(ValueError, match="Faltan columnas"):
        validate_dataframe(df, "text", "label")


def test_rejects_empty_text():
    df = pd.DataFrame({"text": [""], "label": ["a"]})
    with pytest.raises(ValueError, match="textos vacíos"):
        validate_dataframe(df, "text", "label")


def _fake_uci_zip() -> bytes:
    """Reproduce la estructura real del .zip de UCI (3 .txt separados por tab)."""
    content = {
        "sentiment labelled sentences/amazon_cells_labelled.txt": (
            "Great product, works as expected.\t1\nTerrible, broke after one day.\t0\n"
        ),
        "sentiment labelled sentences/imdb_labelled.txt": (
            "A truly wonderful film.\t1\nBoring and way too long.\t0\n"
        ),
        "sentiment labelled sentences/yelp_labelled.txt": (
            "Best service I've had in years.\t1\nRude staff, never coming back.\t0\n"
        ),
        "sentiment labelled sentences/readme.txt": "ignore me",
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, text in content.items():
            archive.writestr(name, text)
    return buffer.getvalue()


def test_build_dataset_from_uci_zip_combines_three_domains():
    df = build_dataset_from_uci_zip(_fake_uci_zip())
    assert list(df.columns) == ["text", "label", "source"]
    assert len(df) == 6
    assert set(df["source"]) == {"amazon", "imdb", "yelp"}
    assert set(df["label"]) == {"positive", "negative"}
    # la etiqueta numérica se normaliza, nunca debe quedar "0"/"1" en texto
    assert not df["label"].isin(["0", "1"]).any()


def test_build_dataset_from_uci_zip_raises_on_missing_domain():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("amazon_cells_labelled.txt", "ok.\t1\n")
    with pytest.raises(ValueError, match="No se encontró"):
        build_dataset_from_uci_zip(buffer.getvalue())
