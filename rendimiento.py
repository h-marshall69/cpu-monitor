import sys
import psutil
import time
import pywifi
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actividad de la CPU, Memoria, Disco y WiFi")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.cpu_chart_view = QChartView(self)
        self.cpu_chart = QChart()
        self.cpu_series = QLineSeries()
        self.cpu_chart.setTitle("Actividad de la CPU")
        self.cpu_chart.addSeries(self.cpu_series)
        self.cpu_chart.createDefaultAxes()
        self.cpu_chart.axisX().setRange(0, 30)
        self.cpu_chart.axisX().setTitleText("Tiempo (segundos)")
        self.cpu_chart.axisY().setRange(0, 100)
        self.cpu_chart.axisY().setTitleText("Uso de CPU (%)")
        self.cpu_chart_view.setChart(self.cpu_chart)
        self.layout.addWidget(self.cpu_chart_view)

        # Atributos agregados para las otras gráficas
        self.memory_chart_view = QChartView(self)
        self.memory_chart = QChart()
        self.memory_series = QLineSeries()
        self.memory_chart.setTitle("Actividad de la Memoria")
        self.memory_chart.addSeries(self.memory_series)
        self.memory_chart.createDefaultAxes()
        self.memory_chart.axisX().setRange(0, 30)
        self.memory_chart.axisX().setTitleText("Tiempo (segundos)")
        self.memory_chart.axisY().setRange(0, 100)
        self.memory_chart.axisY().setTitleText("Uso de Memoria (%)")
        self.memory_chart_view.setChart(self.memory_chart)
        self.layout.addWidget(self.memory_chart_view)

        self.disk_chart_view = QChartView(self)
        self.disk_chart = QChart()
        self.disk_series = QLineSeries()
        self.disk_chart.setTitle("Actividad del Disco")
        self.disk_chart.addSeries(self.disk_series)
        self.disk_chart.createDefaultAxes()
        self.disk_chart.axisX().setRange(0, 30)
        self.disk_chart.axisX().setTitleText("Tiempo (segundos)")
        self.disk_chart.axisY().setRange(0, 100)
        self.disk_chart.axisY().setTitleText("Uso de Disco (%)")
        self.disk_chart_view.setChart(self.disk_chart)
        self.layout.addWidget(self.disk_chart_view)

        self.wifi_chart_view = QChartView(self)
        self.wifi_chart = QChart()
        self.wifi_series = QLineSeries()
        self.wifi_chart.setTitle("Actividad de WiFi")
        self.wifi_chart.addSeries(self.wifi_series)
        self.wifi_chart.createDefaultAxes()
        self.wifi_chart.axisX().setRange(0, 30)
        self.wifi_chart.axisX().setTitleText("Tiempo (segundos)")
        self.wifi_chart.axisY().setRange(0, 100)
        self.wifi_chart.axisY().setTitleText("Intensidad de la señal WiFi (%)")
        self.wifi_chart_view.setChart(self.wifi_chart)
        self.layout.addWidget(self.wifi_chart_view)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Actualizar cada segundo

    def get_wifi_signal_strength(self):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(0.5)
        result = iface.scan_results()
        ssid = "Your_WiFi_SSID"  # Reemplaza "Your_WiFi_SSID" con el SSID de tu red WiFi
        for wifi_data in result:
            if ssid in wifi_data.ssid:
                signal_strength = wifi_data.signal
                return signal_strength
        return 0

    def update_cpu_chart(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_series.append(self.cpu_series.count(), cpu_percent)
        if self.cpu_series.count() > 30:
            self.cpu_series.removePoints(0, 1)

    def update_memory_chart(self):
        memory_percent = psutil.virtual_memory().percent
        self.memory_series.append(self.memory_series.count(), memory_percent)
        if self.memory_series.count() > 30:
            self.memory_series.removePoints(0, 1)

    def update_disk_chart(self):
        disk_percent = psutil.disk_usage('/').percent
        self.disk_series.append(self.disk_series.count(), disk_percent)
        if self.disk_series.count() > 30:
            self.disk_series.removePoints(0, 1)

    def update_wifi_chart(self):
        wifi_strength = self.get_wifi_signal_strength()
        self.wifi_series.append(self.wifi_series.count(), wifi_strength)
        if self.wifi_series.count() > 30:
            self.wifi_series.removePoints(0, 1)

    def update(self):
        self.update_cpu_chart()
        self.update_memory_chart()
        self.update_disk_chart()
        self.update_wifi_chart()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
