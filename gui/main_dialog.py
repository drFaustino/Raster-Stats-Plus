import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QCoreApplication
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
            label = table.item(row, 0).text()
            if label in stats_dict:
                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(stats_dict[label])),
                )
            else:
                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(""),
                )

    def tr(self, message):
        return QCoreApplication.translate("RasterStatsPlus", message)

    def init_empty_table(self):
        labels = [
            "Cell size x",
            "Cell size y",
            "Total pixels",
            "Valid pixels",
            "NoData pixels",
            "Min",
            "Max",
            "Range",
            "Mean",
            "Stddev",
            "Variance",
            "Median",
            "p5",
            "p25",
            "p75",
            "p95",
            "IQR",
            "Skewness",
            "Kurtosis",
            "Coeff_var",
        ]

        self.tableWidgetStat.setRowCount(len(labels))

        for row, label in enumerate(labels):
            self.tableWidgetStat.setItem(
                row,
                0,
                QTableWidgetItem(label),
            )
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
