#   https://chat.openai.com/share/757e1043-3849-4e76-a3c4-c8c0df7a2a5d

import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow,  QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
from toolbar.Detalles import Detalles
from toolbar.Rendimiento import Rendimiento

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('cpu-monitor')
        tab_widget = QTabWidget(self)

        self.screen1 = QWidget()
        self.screen2 = QWidget()
        self.screen3 = QWidget()

        tab_widget.addTab(self.screen1, 'Procesos')
        tab_widget.addTab(self.screen2, 'Detalles')
        tab_widget.addTab(self.screen3, 'Rendimiento')

        self.showScreen1()
        self.showScreen2()
        self.showScreen3()

        self.setCentralWidget(tab_widget)

    def showScreen1(self):
        self.table_widget = QTableWidget(self.screen1)
        #self.setCentralWidget(self.table_widget)

        # Definir las columnas de la matriz
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "CPU %", "Memoria %", "Disco %", "Red %"])

        # Establecer el tamaño de las columnas
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 200)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 100)
        self.table_widget.setColumnWidth(4, 100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_process_matrix)
        self.timer.start(1000)  # Actualizar cada segundo
        
    
    def showScreen2(self):
        procesos = Detalles(self)
        procesos.initScreen2()

    def showScreen3(self):
        self.central_widget = QWidget(self.screen3)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.cpu_chart_view = QChartView(self.screen3)
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

    def update_process_matrix(self):
        # Obtener la lista de procesos en ejecución
        processes = psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_percent'])

        # Limpiar la matriz antes de actualizarla
        self.table_widget.setRowCount(0)

        # Variables para almacenar los totales
        total_cpu_percent = 0.0
        total_memory_percent = 0.0
        total_disk_percent = 0.0
        total_network_percent = 0.0

        # Actualizar la matriz con los datos de los procesos
        for process in processes:
            name = process.info['name']
            cpu_percent = process.info['cpu_percent']
            memory_percent = process.info['memory_percent']
            disk_percent = 0.0  # Valor inicial de disco como float
            network_percent = 0.0  # Valor inicial de red como float

            total_cpu_percent += cpu_percent
            total_memory_percent += memory_percent
            total_disk_percent += disk_percent
            total_network_percent += network_percent

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(cpu_percent)))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(memory_percent)))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(disk_percent)))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(str(network_percent)))

        # Agregar filas adicionales en la parte superior de la matriz para mostrar los totales
        self.table_widget.insertRow(0)
        self.table_widget.setItem(0, 0, QTableWidgetItem("Total"))
        self.table_widget.setItem(0, 1, QTableWidgetItem(f"{total_cpu_percent}%"))
        self.table_widget.setItem(0, 2, QTableWidgetItem(f"{total_memory_percent}%"))
        self.table_widget.setItem(0, 3, QTableWidgetItem(f"{total_disk_percent}%"))
        self.table_widget.setItem(0, 4, QTableWidgetItem(f"{total_network_percent}%"))

        # Ajustar el tamaño de las filas automáticamente
        self.table_widget.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
