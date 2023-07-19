import sys
import time
import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QProgressBar


class TaskSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tarea de CPU Simulator")
        self.setGeometry(100, 100, 400, 100)

        self.label = QLabel("Simulando tarea al 50% de CPU...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(50, 10, 300, 20)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 40, 300, 30)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.setInterval(1000)  # Actualizar cada segundo
        self.current_progress = 0
        self.total_seconds = 50

    def start_simulation(self):
        # Limitar el uso de CPU al 50% para el proceso actual
        psutil.Process().cpu_percent(50)

        self.current_progress = 0
        self.progress_bar.setValue(0)
        self.timer.start()

    def update_progress(self):
        self.current_progress += 1
        self.progress_bar.setValue(int((self.current_progress / self.total_seconds) * 100))

        if self.current_progress >= self.total_seconds:
            self.timer.stop()
            self.label.setText("Tarea completada")
            # Restaurar el uso normal de la CPU
            psutil.Process().cpu_percent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskSimulator()
    window.show()

    # Simular la tarea durante 50 segundos
    window.start_simulation()

    sys.exit(app.exec_())
