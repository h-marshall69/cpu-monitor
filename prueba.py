#   https://chat.openai.com/share/757e1043-3849-4e76-a3c4-c8c0df7a2a5d

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,  QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton
from toolbar.Procesos import Procesos
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

        self.showScreen1()
        self.showScreen2()
        self.showScreen3()

        tab_widget.addTab(self.screen1, 'Procesos')
        tab_widget.addTab(self.screen2, 'Detalles')
        tab_widget.addTab(self.screen3, 'Rendimiento')

        self.setCentralWidget(tab_widget)

        self.show()

    def showScreen1(self):
        procesos = Procesos(self)
        procesos.initScreen1()
    
    def showScreen2(self):
        procesos = Detalles(self)
        procesos.initScreen2()

    def showScreen3(self):
        procesos = Rendimiento(self)
        procesos.initScreen3()


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    app.exec()
