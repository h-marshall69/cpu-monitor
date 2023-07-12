import psutil
import platform
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QProgressBar
from PyQt5.QtCore import QTimer


class SystemMonitorApp(QApplication):

    def __init__(self, sys_argv):
        super(SystemMonitorApp, self).__init__(sys_argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.cpu_label = QLabel(text='Uso de CPU: ')
        self.cpu_progress = QProgressBar()
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

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.cpu_progress)
        self.layout.addWidget(self.cpu_cores_label)
        for i in range(psutil.cpu_count()):
            core_label = QLabel(text=f'Núcleo {i}:')
            core_progress = QProgressBar()
            core_progress.setMaximum(100)
            core_progress.setValue(0)
            self.cpu_cores_label.setText(self.cpu_cores_label.text() + f' {i}')
            self.cpu_cores_progress.append(core_progress)
            self.layout.addWidget(core_label)
            self.layout.addWidget(core_progress)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.ram_progress)
        self.layout.addWidget(self.swap_label)
        self.layout.addWidget(self.swap_progress)
        self.layout.addWidget(self.gpu_label)
        self.layout.addWidget(self.gpu_progress)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.disk_progress)

        self.window.setLayout(self.layout)

        self.update_system_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)

        self.window.show()

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

        gpu_info = 'No disponible'
        gpu_usage = 0  # Asumiendo que no hay GPU

        try:
            import GPUtil
            gpu_devices = GPUtil.getGPUs()
            if gpu_devices:
                gpu_usage = gpu_devices[0].load * 100
                gpu_info = f'Modelo: {gpu_devices[0].name}, Uso de GPU: {gpu_usage:.2f}%'
        except ImportError:
            pass

        self.gpu_progress.setValue(int(gpu_usage))

        disk_usage = psutil.disk_usage('/').percent
        self.disk_progress.setValue(int(disk_usage))

        self.cpu_label.setText(f'Uso de CPU: {cpu_usage}%')
        self.ram_label.setText(f'Uso de RAM: {ram_usage}%')
        self.swap_label.setText(f'Uso de Swap: {swap_usage}%')
        self.gpu_label.setText(f'Información de GPU: {gpu_info}')
        self.disk_label.setText(f'Espacio en Disco: {disk_usage}% utilizado')


if __name__ == '__main__':
    import sys
    app = SystemMonitorApp(sys.argv)
    sys.exit(app.exec_())
