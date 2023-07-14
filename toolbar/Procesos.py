#   https://chat.openai.com/share/e60d5dff-633b-4f99-94c2-3459ffed4522
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer

class Procesos:

    def __init__(self, ventana):
        self.screen1 = ventana.screen1
        

    def initScreen1(self):
        self.table_widget = QTableWidget(self.screen1)

        # Definir las columnas de la matriz
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "CPU %", "Memoria %", "Disco %", "Red %"])

        # Establecer el tamaño de las columnas
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 200)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 100)
        self.table_widget.setColumnWidth(4, 100)

        # Crear un temporizador para actualizar periódicamente la matriz de procesos
        self.timer = QTimer(self.screen1)
        self.timer.timeout.connect(self.update_process_matrix)
        self.timer.start(1000)  # Actualizar cada 1 segundo

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