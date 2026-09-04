import os

from qgis.PyQt.QtCore import QCoreApplication, Qt

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog,
    QGraphicsScene,
    QTableWidgetItem,
)

from .histogram_canvas import HistogramCanvas


class RasterStatsPlusDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(
            os.path.dirname(__file__),
            "main_dialog.ui",
        )
        uic.loadUi(ui_path, self)

        # Colore istogramma di default
        self.hist_color = "steelblue"

        # Mostra il colore nel quadratino
        self.labelColorPreview.setStyleSheet(
            "background-color: steelblue; border: 1px solid #444;"
        )

        # Tabella
        self.tableWidgetStat.setColumnCount(2)
        self.tableWidgetStat.setHorizontalHeaderLabels(
            [
                self.tr("Statistica"),
                self.tr("Valore"),
            ]
        )
        self.tableWidgetStat.horizontalHeader().setStretchLastSection(True)

        self.init_empty_table()

        # Istogramma
        self.histCanvas = HistogramCanvas()
        self.scene = QGraphicsScene(self)
        self.scene.addWidget(self.histCanvas)
        self.graphicsViewIsto.setScene(self.scene)

    def fill_table(self, stats_dict):
        table = self.tableWidgetStat

        for row in range(table.rowCount()):
            item = table.item(row, 0)

            if item is None:
                continue

            key = item.data(Qt.ItemDataRole.UserRole)

            if key in stats_dict:
                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(stats_dict[key])),
                )
            else:
                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(""),
                )

    def tr(self, message):
        return QCoreApplication.translate(
            "RasterStatsPlusDialog",
            message,
        )

    def init_empty_table(self):
        labels = [
            ("Cell size x", self.tr("Dim cell x")),
            ("Cell size y", self.tr("Dim cell y")),
            ("Total pixels", self.tr("Totale pixels")),
            ("Valid pixels", self.tr("Pixels validi")),
            ("NoData pixels", self.tr("Pixels NoData")),
            ("Min", self.tr("Min")),
            ("Max", self.tr("Max")),
            ("Range", self.tr("Intervallo")),
            ("Mean", self.tr("Media")),
            ("Stddev", self.tr("Dev.Std")),
            ("Variance", self.tr("Varianza")),
            ("Median", self.tr("Mediana")),
            ("p5", self.tr("p5")),
            ("p25", self.tr("p25")),
            ("p75", self.tr("p75")),
            ("p95", self.tr("p95")),
            ("IQR", self.tr("IQR")),
            ("Skewness", self.tr("Skewness")),
            ("Kurtosis", self.tr("Kurtosis")),
            ("Coeff_var", self.tr("Coeff_var")),
        ]

        self.tableWidgetStat.setRowCount(len(labels))

        for row, (key, label) in enumerate(labels):
            item = QTableWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, key)

            self.tableWidgetStat.setItem(row, 0, item)
            self.tableWidgetStat.setItem(
                row,
                1,
                QTableWidgetItem(""),
            )


    def reset_view(self):
        # Reset tabella
        for row in range(self.tableWidgetStat.rowCount()):
            self.tableWidgetStat.setItem(
                row,
                1,
                QTableWidgetItem(""),
            )

        # Reset grafico
        self.histCanvas.init_empty()
