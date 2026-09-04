# RasterStatsPlus — Changelog

## [1.1.0] — 2026-09-04
- Fixed Flake8 code quality and style issues across the plugin.
- Corrected blank-line formatting and removed trailing whitespace.
- Fixed inline statements that violated PEP 8 (E701).
- Improved code formatting and import organization.
- Reformatted long function calls and expressions for better readability.
- Improved exception handling in raster band utilities.
- Fixed the translation helper in histogram export to use the correct function signature.
- No functional changes to raster statistics, histogram generation, or data export.

## [1.0.1]— 2026-04-21
### Improved CRS handling and raster statistics robustness
- Added explicit import of `QgsRasterBandStats` for QGIS 4 compatibility.
- Fixed crash caused by uninitialized variables (`value_range`, `var`, `iqr`) when raster contains only NoData.
- Improved NoData detection:
  - Now reads both provider NoData and user-defined NoData ranges.
  - Correctly counts NoData pixels in all raster formats.
- Added automatic resolution conversion for geographic CRS (e.g., EPSG:4326):
  - Pixel size is now computed in meters using on‑the‑fly transformation to EPSG:3857.
  - Prevents `Cell size x = 0` and `Cell size y = 0` issues in lat/long rasters.
- Improved statistical computation:
  - Safe initialization of all metrics.
  - Robust handling of constant-value rasters.
  - More stable skewness and kurtosis computation.
- General code cleanup and improved numerical stability.

---

## [1.0.0] — 2026-03-23
### Aggiunto
- Prima release per la versione 4 di QGIS in Qt6 pubblica del plugin RasterStatsPlus.
- Calcolo statistiche raster (min, max, media, deviazione standard, varianza, somma, conteggio).
- Generazione istogramma dei valori raster con Matplotlib.
- Selettore colore istogramma con anteprima.
- Interfaccia grafica ottimizzata per QGIS 4.
- Icona del plugin in stile flat QGIS‑like (128×128, sfondo trasparente).
- Supporto a raster multibanda (selezione banda).
- Gestione errori migliorata per raster non validi o non caricati.

---

## Struttura del versionamento
Il plugin segue il formato **MAJOR.MINOR.PATCH**:
- **MAJOR**: cambiamenti incompatibili o nuove funzionalità importanti.
- **MINOR**: aggiunte retro‑compatibili.
- **PATCH**: correzioni di bug e miglioramenti minori.

---

## Note
Per richieste, segnalazioni o contributi: aprire una issue nel repository del plugin.
