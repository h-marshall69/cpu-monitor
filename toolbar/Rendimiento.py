from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Rendimiento:

    def __init__(self, ventana):
        self.screen3 = ventana.screen3
        self.initScreen3()

    def initScreen3(self):
        layout = QVBoxLayout()
        label = QLabel('Pantalla 3')
        button = QPushButton('Botón de la pantalla 3')
        layout.addWidget(label)
        layout.addWidget(button)
        self.screen3.setLayout(layout)
