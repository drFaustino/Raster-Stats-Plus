import math
import numpy as np

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMessageLog,
    QgsPointXY,
    QgsProject,
    QgsRasterBandStats,
)


def compute_raster_stats(raster, band_idx, progress_callback=None):
    provider = raster.dataProvider()

    if progress_callback:
        progress_callback(5)

    # Base statistics from QGIS provider
    stats = provider.bandStatistics(
        band_idx,
        QgsRasterBandStats.All,
        raster.extent(),
        0,
    )

    # Pixel resolution (initial, in CRS units)
    res_x = raster.rasterUnitsPerPixelX()
    res_y = raster.rasterUnitsPerPixelY()

    # Convert resolution to meters if CRS is geographic (EPSG:4326 etc.)
    crs = raster.crs()
    if crs.isGeographic():
        original_res_x = res_x
        original_res_y = res_y

        transform = QgsCoordinateTransform(
            crs,
            QgsCoordinateReferenceSystem("EPSG:3857"),
            QgsProject.instance(),
        )

        try:
            # Two adjacent points in pixel space
            p1 = transform.transform(
                QgsPointXY(
                    raster.extent().xMinimum(),
                    raster.extent().yMinimum(),
                )
            )
            p2 = transform.transform(
                QgsPointXY(
                    raster.extent().xMinimum() + res_x,
                    raster.extent().yMinimum() + res_y,
                )
            )

            res_x = abs(p2.x() - p1.x())
            res_y = abs(p2.y() - p1.y())

        except Exception as error:
            # Keep the original CRS units if the transformation fails.
            res_x = original_res_x
            res_y = original_res_y
            QgsMessageLog.logMessage(
                f"Raster resolution transformation failed: {error}",
                "RasterStatsPlus",
            )

    total_pixels = raster.width() * raster.height()

    # Read raster block
    block = provider.block(
        band_idx,
        raster.extent(),
        raster.width(),
        raster.height(),
    )

    # NoData handling (provider + user-defined)
    nodata = provider.sourceNoDataValue(band_idx)

    if nodata is None:
        user_nodata = provider.userNoDataValues(band_idx)
        if user_nodata:
            nodata = user_nodata[0].min()

    if progress_callback:
        progress_callback(25)

    # Extract valid values
    values = []

    for col in range(block.width()):
        for row in range(block.height()):
            v = block.value(row, col)

            if nodata is not None and (
                math.isclose(v, nodata) or v == nodata
            ):
                continue

            if math.isnan(v):
                continue

            values.append(v)

    if progress_callback:
        progress_callback(60)

    arr = np.array(values, dtype=float)
    valid_pixels = arr.size
    nodata_count = total_pixels - valid_pixels

    # Initialize all statistics safely
    median = p5 = p25 = p75 = p95 = float("nan")
    skewness = kurtosis = coeff_var = float("nan")
    iqr = float("nan")
    var = float("nan")
    value_range = float("nan")

    if valid_pixels > 0:
        median = float(np.median(arr))
        p5 = float(np.percentile(arr, 5))
        p25 = float(np.percentile(arr, 25))
        p75 = float(np.percentile(arr, 75))
        p95 = float(np.percentile(arr, 95))
        iqr = p75 - p25

        std = arr.std()
        var = arr.var()
        mean = arr.mean()

        value_range = stats.maximumValue - stats.minimumValue

        skewness = (
            float(((arr - mean) ** 3).mean() / (std ** 3))
            if std != 0
            else float("nan")
        )
        kurtosis = (
            float(((arr - mean) ** 4).mean() / (var ** 2))
            if var != 0
            else float("nan")
        )
        coeff_var = (
            float(std / mean)
            if mean != 0
            else float("nan")
        )

    if progress_callback:
        progress_callback(90)

    stats_dict = {
        "Cell size x": res_x,
        "Cell size y": res_y,
        "Total pixels": total_pixels,
        "Valid pixels": valid_pixels,
        "NoData pixels": nodata_count,
        "Min": stats.minimumValue,
        "Max": stats.maximumValue,
        "Range": value_range,
        "Mean": stats.mean,
        "Stddev": stats.stdDev,
        "Variance": var,
        "Median": median,
        "p5": p5,
        "p25": p25,
        "p75": p75,
        "p95": p95,
        "IQR": iqr,
        "Skewness": skewness,
        "Kurtosis": kurtosis,
        "Coeff_var": coeff_var,
    }

    if progress_callback:
        progress_callback(100)

    return stats_dict, arr
