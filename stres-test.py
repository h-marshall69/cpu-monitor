#   https://chat.openai.com/share/8bdbb2d5-8157-4ec2-878d-3d2c4d4a173b
import sys
import random
import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stress Test - CPU Usage")
        self.setGeometry(100, 100, 800, 600)

        self.chart = QChart()
        self.chart.legend().hide()
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("CPU Usage")
        self.chart.axisX().setTickCount(10)
        self.chart.axisX().setRange(0, 10)
        self.chart.axisY().setRange(0, 100)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)  # Actualiza el gráfico cada segundo

    def update_chart(self):
        # Algoritmo de stress test (simulación)
        cpu_percent = random.randint(70, 100)  # Genera un número aleatorio entre 70 y 100 como porcentaje de uso de CPU
        self.series.append(self.series.count(), cpu_percent)

        if self.series.count() > 10:
            self.chart.axisX().setRange(self.series.count() - 10, self.series.count())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
