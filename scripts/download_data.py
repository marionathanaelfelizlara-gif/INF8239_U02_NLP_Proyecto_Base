from __future__ import annotations

import sys
from pathlib import Path

import requests

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import build_dataset_from_uci_zip, sha256


def main() -> int:
    if settings.data_source == "local":
        print(f"Modo local. Archivo configurado: {settings.dataset_path}")
        return 0
    if settings.data_source != "url" or not settings.dataset_url:
        print("Configure DATA_SOURCE=url y DATASET_URL en .env", file=sys.stderr)
        return 2

    output = ROOT / "data/raw/dataset.csv"
    output.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(settings.dataset_url, timeout=60)
    response.raise_for_status()

    if settings.dataset_url.endswith(".zip"):
        # Dataset aprobado: UCI Sentiment Labelled Sentences viene como .zip con
        # tres archivos .txt (uno por dominio). build_dataset_from_uci_zip los
        # combina en el único CSV text/label/source que espera el resto del proyecto.
        df = build_dataset_from_uci_zip(response.content)
        df.to_csv(output, index=False)
    else:
        output.write_bytes(response.content)

    print(f"Guardado: {output}")
    print(f"SHA-256: {sha256(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
