from qgis.core import QgsProject, QgsRasterLayer


def list_raster_layers():
    return [
        lyr
        for lyr in QgsProject.instance().mapLayers().values()
        if isinstance(lyr, QgsRasterLayer)
    ]


def get_layer_by_id(layer_id):
    return QgsProject.instance().mapLayer(layer_id)


def raster_band_items(raster_layer):
    provider = raster_layer.dataProvider()
    items = []

    for band in range(1, provider.bandCount() + 1):
        try:
            name = raster_layer.bandName(band)
        except Exception:
            name = ""

        label = f"{band}: {name}" if name else f"Banda {band}"
        items.append((label, band))

    return items


def format_stats(stats_dict):
    fmt3 = [
        "Cell size x",
        "Cell size y",
        "Min",
        "Max",
        "Range",
        "Mean",
        "Variance",
        "Stddev",
        "Median",
        "p5",
        "p25",
        "p75",
        "p95",
        "IQR",
    ]

    fmt6 = [
        "Skewness",
        "Kurtosis",
        "Coeff_var",
    ]

    formatted = {}

    for key, value in stats_dict.items():
        if value is None:
            formatted[key] = ""
            continue

        if key in fmt3:
            formatted[key] = f"{value:.3f}"
        elif key in fmt6:
            formatted[key] = f"{value:.6f}"
        else:
            formatted[key] = str(value)

    return formatted
