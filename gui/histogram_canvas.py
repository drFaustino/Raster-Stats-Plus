from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from qgis.PyQt.QtCore import QCoreApplication


class HistogramCanvas(Canvas):
    def __init__(self):
        # 1) Crea la figura (600x480 px)
        self.fig = Figure(figsize=(6.0, 5.8), dpi=100)
        super().__init__(self.fig)

        # 2) Canvas Qt fisso
        self.setFixedSize(650, 629)

        # 3) Asse
        self.ax = self.fig.add_subplot(111)

        # 4) Margini iniziali (grafico vuoto)
        self._set_margins(empty=True)

        # 5) Grafico iniziale
        self.init_empty()

    def tr(self, message):
        return QCoreApplication.translate(
            "HistogramCanvas",
            message,
        )

    def _set_margins(self, empty=False):
        """
        Margini dinamici:
        - empty=True → margini più stretti (grafico vuoto)
        - empty=False → margini più ampi (etichette lunghe)
        """
        if empty:
            left = 0.10
            right = 0.95
            bottom = 0.10
            top = 0.9
        else:
            # Margini più ampi per etichette Y lunghe
            left = 0.15
            right = 0.95
            bottom = 0.10
            top = 0.9

        self.fig.subplots_adjust(
            left=left,
            right=right,
            bottom=bottom,
            top=top,
        )

    def init_empty(self):
        self._set_margins(empty=True)
        self.ax.clear()
        self.ax.set_title(
            self.tr("Istogramma valori raster"),
            fontweight="bold",
        )
        self.ax.set_xlabel(
            self.tr("Valore dei pixel"),
            fontweight="bold",
        )
        self.ax.set_ylabel(
            self.tr("Frequenza"),
            fontweight="bold",
        )
        self.ax.grid(True)
        self.draw()

    def plot_histogram(self, values, bins=50, color="steelblue"):
        self._set_margins(empty=False)
        self.ax.clear()

        # Usa il colore passato
        self.ax.hist(
            values,
            bins=bins,
            color=color,
            edgecolor="black",
        )

        self.ax.set_title(
            self.tr("Istogramma valori raster"),
            fontweight="bold",
        )
        self.ax.set_xlabel(
            self.tr("Valore dei pixel"),
            fontweight="bold",
        )
        self.ax.set_ylabel(
            self.tr("Frequenza"),
            fontweight="bold",
        )
        self.ax.grid(True)

        self.draw()

    def get_figure(self):
        return self.fig
