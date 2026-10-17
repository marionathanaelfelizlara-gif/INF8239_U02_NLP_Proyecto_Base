# Declaración de uso de herramientas de IA — U02.E03

## Herramienta utilizada
Claude (Anthropic), vía Cowork, con acceso directo (lectura/escritura) a los archivos de este
proyecto en `C:\INF8239_U02_NLP_Proyecto_Base` a través del puente de dispositivo de Cowork, y a
un entorno aislado en la nube para probar código antes de guardarlo. No se usó ningún asistente
de autocompletado de IDE adicional.

## Qué se le pidió (prompts relevantes, resumidos)
- Comparar y vetar dos datasets candidatos para el tema "reseñas o sentimiento de servicio" según
  los criterios del LAB04 (pertinencia, licencia, representatividad, calidad, reproducibilidad,
  riesgo).
- Implementar la descarga y combinación del dataset aprobado (el `.zip` de UCI, que no trae un
  CSV único sino 3 archivos de texto separados por dominio).
- Completar `docs/DATASET_CARD.md` y `docs/dataset_candidates.csv` con la información real
  verificada de cada candidato.
- Construir un notebook ejecutable adicional que reutilice el código de `src/inf8239_u02/` para
  cargar el dataset, entrenar los 3 modelos de `build_models`, generar la matriz de confusión, el
  análisis de errores y un desglose de desempeño por dominio.
- Ayuda con los comandos de entorno (`uv`) y de Git/GitHub para dejar el repositorio público.

## Qué se verificó (no se aceptó por confianza)
- La función `build_dataset_from_uci_zip` (que combina los 3 archivos del `.zip` de UCI) se probó
  contra un `.zip` sintético que reproduce exactamente la estructura real (mismos nombres de
  archivo, mismo formato `oración<TAB>etiqueta`) antes de guardarla, incluyendo un caso de error
  (archivo faltante). Las 5 pruebas de `tests/test_data_contract.py` se corrieron en un entorno
  aislado y pasaron (5/5) antes de entregarse.
- El notebook adicional (`notebooks/01_corpus_clasificador.ipynb`) se probó celda por celda,
  ejecutando su código real contra un dataset sintético de 120 filas con la misma forma que el
  real (columnas `text,label,source`, 3 dominios), para confirmar que corre sin errores de punta
  a punta (carga, EDA, partición, entrenamiento de los 3 modelos, matriz de confusión, análisis de
  errores, desglose por dominio) antes de guardarlo en el repositorio.
- No se pudo descargar el `.zip` real de UCI desde el entorno de pruebas de Claude (su salida a
  internet solo permite gestores de paquetes, no `archive.ics.uci.edu`), así que la ejecución real
  del notebook y de `scripts/download_data.py`/`train_text.py` con los datos reales la hizo el
  estudiante en su propia máquina — los números finales de `reports/` y las celdas ejecutadas del
  notebook son resultado de esa ejecución real, no de la IA.

## Correcciones realizadas
- El `README.md` original traía `Autor académico: Edwin Ramón José Nolasco` — un nombre de
  plantilla del material del curso, no el del estudiante. Se corrigió a Nathanael.
- Se detectó que el mandato exige explícitamente un archivo `requirements.txt`, mientras el
  proyecto solo traía `pyproject.toml`/`uv.lock` y `requirements-colab.txt`; se documentó el
  comando exacto (`uv export --format requirements.txt --no-dev --output-file requirements.txt`)
  para generarlo a partir del lockfile real del estudiante, en vez de fabricar uno a mano.
- Se detectó una inconsistencia entre el entorno virtual que el estudiante ya tenía creado
  (`env`, con `python -m venv`) y el flujo documentado en el README (`uv sync`, que por defecto
  usa `.venv`). Un primer intento de solución fue documentar `set UV_PROJECT_ENVIRONMENT=env`
  como paso explícito del README; en la práctica esto causó un problema real al reconstruir ese
  entorno preexistente en Windows (`uv sync` no pudo reemplazar archivos de un venv activo,
  dejando la carpeta `env` a medio reconstruir). A pedido del estudiante, de que la reproducción
  fuera "lo más simple posible... sin complicaciones" para cualquiera que clone el repositorio, se
  revirtió esa decisión: se eliminó la carpeta `env` y se volvió al flujo estándar de `uv sync`
  (crea `.venv` automáticamente, sin pasos ni variables de entorno adicionales).

## Lo que la IA NO hizo
No se fabricaron métricas, capturas de pantalla ni salidas de notebook. Ningún número que aparece
en `reports/` o en las celdas ejecutadas del notebook fue generado por la IA sin ejecución real:
los resultados reales provienen de correr el pipeline sobre el dataset real, en la máquina del
estudiante.
