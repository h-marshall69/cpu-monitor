import sys
import psutil
import time
import pywifi
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QWidget, QTabWidget, QStackedWidget, QHeaderView, QTextEdit, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_progress = QProgressBar()
        self.ram_progress = QProgressBar()
        self.swap_progress = QProgressBar()
        self.gpu_progress = QProgressBar()
        self.disk_progress = QProgressBar()
        self.cpu_cores_progress = []
        self.battery_progress = None  # Initialize to None

        self.process_names = set()  # Initialize process_names as an empty set

        self.tab_widget = None  # Inicializar el atributo tab_widget como None

        self.initializeUI()
        self.update_battery_info()

    def initializeUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle('cpu-monitor')

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.tab_widget = QTabWidget()
        self.stacked_widget.addWidget(self.tab_widget)

        # Procesos Tab
        self.screen1 = QWidget()
        self.tab_widget.addTab(self.screen1, 'Procesos')
        self.layout = QVBoxLayout(self.screen1)
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "CPU %", "Memoria %", "Disco %", "Red %"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSortingEnabled(True)

        # Set the size of the columns using a loop
        column_widths = [100, 200, 100, 100, 100]
        for col, width in enumerate(column_widths):
            self.table_widget.setColumnWidth(col, width)

        self.update_system_info()

        # Detalles Tab
        self.screen2 = QWidget()
        self.tab_widget.addTab(self.screen2, 'Detalles')
        self.layout2 = QVBoxLayout(self.screen2)

        self.cpu_label = QLabel(text='Uso de CPU: ')
        self.cpu_progress.setMaximum(100)
        self.cpu_progress.setValue(0)

        self.cpu_cores_label = QLabel(text='Núcleos de CPU:')
        self.cpu_cores_progress = []

        self.ram_label = QLabel(text='Uso de RAM: ')
        self.ram_progress = QProgressBar()
        self.ram_progress.setMaximum(100)
        self.ram_progress.setValue(0)

        self.swap_label = QLabel(text='Uso de Swap: ')
        self.swap_progress = QProgressBar()
        self.swap_progress.setMaximum(100)
        self.swap_progress.setValue(0)

        self.gpu_label = QLabel(text='Información de GPU: ')
        self.gpu_progress = QProgressBar()
        self.gpu_progress.setMaximum(100)
        self.gpu_progress.setValue(0)

        self.disk_label = QLabel(text='Espacio en Disco: ')
        self.disk_progress = QProgressBar()
        self.disk_progress.setMaximum(100)
        self.disk_progress.setValue(0)

        self.layout2.addWidget(self.cpu_label)
        self.layout2.addWidget(self.cpu_progress)
        self.layout2.addWidget(self.cpu_cores_label)
        for i in range(psutil.cpu_count()):
            core_label = QLabel(text=f'Núcleo {i}:')
            core_progress = QProgressBar()
            core_progress.setMaximum(100)
            core_progress.setValue(0)
            self.cpu_cores_label.setText(self.cpu_cores_label.text() + f' {i}')
            self.cpu_cores_progress.append(core_progress)
            self.layout2.addWidget(core_label)
            self.layout2.addWidget(core_progress)
        self.layout2.addWidget(self.ram_label)
        self.layout2.addWidget(self.ram_progress)
        self.layout2.addWidget(self.swap_label)
        self.layout2.addWidget(self.swap_progress)
        self.layout2.addWidget(self.gpu_label)
        self.layout2.addWidget(self.gpu_progress)
        self.layout2.addWidget(self.disk_label)
        self.layout2.addWidget(self.disk_progress)

        # Rendimiento Tab
        self.screen3 = QWidget()
        self.tab_widget.addTab(self.screen3, 'Rendimiento')
        self.layout3 = QVBoxLayout(self.screen3)

        self.cpu_chart_view = QChartView()
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
        self.layout3.addWidget(self.cpu_chart_view)

        # Agregado para otras gráficas
        self.memory_chart_view = QChartView()
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
        self.layout3.addWidget(self.memory_chart_view)

        self.disk_chart_view = QChartView()
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
        self.layout3.addWidget(self.disk_chart_view)

        self.wifi_chart_view = QChartView()
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
        self.layout3.addWidget(self.wifi_chart_view)

        # Virtualizacion Tab
        self.screen4 = QWidget()
        self.tab_widget.addTab(self.screen4, 'Virtualizacion')

        # Battery Tab (added condition to show the tab only on laptops)
        if platform.system() == "Linux":
            self.screen5 = QWidget()
            self.tab_widget.addTab(self.screen5, 'Uso de la batería')
            self.layout5 = QVBoxLayout(self.screen5)

            self.battery_label = QLabel(text='Nivel de batería: ')
            self.battery_progress = QProgressBar()
            self.battery_progress.setMaximum(100)
            self.battery_progress.setValue(0)

            self.layout5.addWidget(self.battery_label)
            self.layout5.addWidget(self.battery_progress)
        
        # Crear la pestaña Historial y registros
        self.screen6 = QWidget()  # Cambié el nombre de la pestaña a screen6 para evitar conflictos
        self.tab_widget.addTab(self.screen6, 'Historial y registros')
        self.layout6 = QVBoxLayout(self.screen6)

        # Crear un QTextEdit para mostrar los registros
        self.text_edit = QTextEdit()
        self.layout6.addWidget(self.text_edit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_process_matrix)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.timeout.connect(self.update_cpu_chart)
        self.timer.timeout.connect(self.update_memory_chart)
        self.timer.timeout.connect(self.update_disk_chart)
        self.timer.timeout.connect(self.update_process_list)
        self.timer.timeout.connect(self.update_wifi_chart)
        self.timer.timeout.connect(self.update_battery_info)  # Connect the method to the timer
        self.timer.start(1000)  # Update every second

    def create_chart(self, chart_view, chart, series, title, axis_label):
        chart_view = QChartView(self)
        chart = QChart()
        series = QLineSeries()
        chart.setTitle(title)
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.axisX().setRange(0, 30)
        chart.axisX().setTitleText("Tiempo (segundos)")
        chart.axisY().setRange(0, 100)
        chart.axisY().setTitleText(axis_label)
        chart_view.setChart(chart)

    def update_process_matrix(self):
        # Obtener la lista de procesos en ejecución
        processes = psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_percent'])

        # Variable para almacenar eventos importantes
        events = []

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
            # Revisar si el proceso es nuevo y agregar un registro al historial
            process_name = process.info['name']
            if process_name not in self.process_names:
                event = f"Proceso nuevo detectado: {process_name}"
                events.append(event)

        # Actualizar el QTextEdit con los eventos importantes
        if events:
            event_text = "\n".join(events)
            self.text_edit.append(event_text)

        # Agregar filas adicionales en la parte superior de la matriz para mostrar los totales
        self.table_widget.insertRow(0)
        self.table_widget.setItem(0, 0, QTableWidgetItem("Total"))
        self.table_widget.setItem(0, 1, QTableWidgetItem(f"{total_cpu_percent:.2f}%"))
        self.table_widget.setItem(0, 2, QTableWidgetItem(f"{total_memory_percent:.2f}%"))
        self.table_widget.setItem(0, 3, QTableWidgetItem(f"{total_disk_percent:.2f}%"))
        self.table_widget.setItem(0, 4, QTableWidgetItem(f"{total_network_percent:.2f}%"))

        # Ajustar el tamaño de las filas automáticamente
        self.table_widget.resizeRowsToContents()

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        self.cpu_progress.setValue(int(cpu_usage))

        cpu_cores_usage = psutil.cpu_percent(percpu=True)
        for i in range(len(self.cpu_cores_progress)):
            self.cpu_cores_progress[i].setValue(int(cpu_cores_usage[i]))

        ram_usage = psutil.virtual_memory().percent
        self.ram_progress.setValue(int(ram_usage))

        swap_usage = psutil.swap_memory().percent
        self.swap_progress.setValue(int(swap_usage))

        disk_usage = psutil.disk_usage('/').percent
        self.disk_progress.setValue(int(disk_usage))
        # Update battery info
        self.update_battery_info()

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

    def update_process_list(self):
        processes = psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_percent'])

        # Clear the table before updating
        self.table_widget.setRowCount(0)

        # Update the table with process data
        for process in processes:
            name = process.info['name']
            cpu_percent = process.info['cpu_percent']
            memory_percent = process.info['memory_percent']

            # Use psutil.disk_usage to get disk usage information
            disk_usage = psutil.disk_usage('/')
            disk_percent = disk_usage.percent

            network_percent = 0.0  # For now, we set network percent to 0.0

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(f"{cpu_percent:.2f}%"))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(f"{memory_percent:.2f}%"))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(f"{disk_percent:.2f}%"))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(f"{network_percent:.2f}%"))

        # Adjust the size of the rows automatically
        self.table_widget.resizeRowsToContents()

    def update_battery_info(self):
        if self.battery_progress is not None:  # Check if the battery_progress attribute exists
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = battery.percent
                self.battery_progress.setValue(int(battery_percent))

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
