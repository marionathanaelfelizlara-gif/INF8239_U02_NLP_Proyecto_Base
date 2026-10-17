# Dataset Card

## Identificación
- Nombre: UCI Sentiment Labelled Sentences
- Fuente original: UCI Machine Learning Repository — https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences
- Responsable: Dimitrios Kotzias, Misha Denil, Nando de Freitas, Padhraic Smyth (From Group to Individual Labels using Deep Features, KDD 2015). Hospedado por UC Irvine (UCI ML Repository, DOI 10.24432/C57604).
- Versión o fecha: Publicado en 2015; descargado para este proyecto el 2026-10-17.
- Licencia: CC BY 4.0 (uso y redistribución permitidos citando la fuente).
- Idioma: Inglés.

## Propósito y variable objetivo
Clasificación binaria de sentimiento (positivo/negativo) sobre oraciones cortas de reseñas reales,
tomadas de tres dominios distintos: productos de Amazon, reseñas de restaurantes/servicio de Yelp
y críticas de películas de IMDb. La variable objetivo es `label`, con dos clases balanceadas:
`positive` y `negative` (remapeadas desde la codificación original 1/0 del dataset). El dominio de
origen de cada oración se conserva en la columna `source` (amazon / yelp / imdb) para poder analizar
el desempeño del clasificador por dominio, no solo de forma agregada.

## Diccionario de datos

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
| text | string | Oración de reseña en inglés, ya segmentada por los autores originales | Texto libre, 1 oración por fila |
| label | string | Sentimiento asociado a la oración | `positive`, `negative` |
| source | string | Dominio de origen de la reseña | `amazon`, `yelp`, `imdb` |

## Procedimiento de obtención
1. Descarga directa del archivo oficial `.zip` publicado por UCI (sin autenticación ni API key):
   `https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip`.
2. El `.zip` contiene tres archivos de texto separados por tabulador (`oración<TAB>etiqueta`), uno
   por dominio: `amazon_cells_labelled.txt`, `imdb_labelled.txt`, `yelp_labelled.txt`.
3. `scripts/download_data.py` (con `DATA_SOURCE=url`) descarga el `.zip` y llama a
   `inf8239_u02.data.build_dataset_from_uci_zip`, que extrae los tres archivos en memoria, normaliza
   la etiqueta numérica (0/1) a texto (`negative`/`positive`) y los combina en un único
   `data/raw/dataset.csv` con columnas `text,label,source`.
4. Trazabilidad: el SHA-256 del CSV combinado se imprime al final de la descarga y debe registrarse
   en `reports/` al ejecutar `scripts/audit_data.py`, para poder verificar que el dataset usado en el
   entrenamiento es exactamente el descargado.

## Calidad observada
Verificado ejecutando `scripts/audit_data.py` sobre la copia real descargada
(SHA-256 `90995f55973a470ad7a67d9c34337ce1f4348dcb6bd5e08c6012c50ac6427a4f`):

- 3,000 filas, 3 columnas (`text`, `label`, `source`).
- Clases perfectamente balanceadas: 1,500 `positive` / 1,500 `negative` (50% / 50%).
- Sin valores nulos en `text` ni `label` (0 en ambas columnas).
- 18 textos duplicados (0.6% de las 3,000 filas) — no se eliminaron: dado el tamaño pequeño del
  corpus, podrían corresponder a frases cortas y genéricas que coinciden entre dominios (p. ej.
  "Great product." podría repetirse); se deja constancia aquí en vez de ocultarlo, y `train_text.py`
  sí deduplica por texto antes de entrenar.
- Longitud de texto (caracteres): media 64.6, mediana 55, percentil 90 en 121, percentil 99 en 213,
  mínimo 5, máximo 477 — oraciones cortas en su mayoría, con una cola de reseñas más largas
  (sobre todo del dominio IMDb).

## Población cubierta y excluida
Cubre opiniones en **inglés** sobre tres dominios de consumo (producto físico, restaurante/servicio,
película), escritas por consumidores reales entre fines de los 2000 y principios de los 2010. Excluye
explícitamente: reseñas en español u otros idiomas, reseñas de servicios regulados o financieros,
y cualquier oración que los autores originales descartaran por ambigüedad en la anotación humana
(el dataset ya llega pre-filtrado a solo oraciones con sentimiento claro).

## Riesgos, sesgos y usos prohibidos
- No contiene identificadores de usuario, nombres de perfil ni metadatos personales: cada fila es
  únicamente `texto + etiqueta + dominio`.
- Sesgo de época y dominio: el lenguaje y los productos/películas reflejan el período de recolección
  (≈2005–2015) y los tres dominios elegidos por los autores; no debe asumirse representatividad de
  sentimiento en dominios distintos (p. ej. servicios de salud o finanzas) ni en idiomas distintos al
  inglés.
- Al estar pre-balanceado y pre-filtrado por los autores originales, no refleja la proporción real de
  sentimiento positivo/negativo que tendría un flujo de reseñas sin curar — no debe usarse para
  estimar tasas base de satisfacción de un negocio real.
- Uso prohibido: no debe emplearse para perfilar, identificar o tomar decisiones sobre personas
  reales (no hay en el dataset vínculo con individuos identificables), ni presentarse como medición
  de satisfacción de un servicio actual sin advertir la antigüedad y el origen sintético-curado de
  los datos.
