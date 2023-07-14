from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Detalles:

    def __init__(self, ventana):
        self.screen2 = ventana.screen2
        self.initScreen2()

    def initScreen2(self):
        layout = QVBoxLayout()
        label = QLabel('Pantalla 2')
        button = QPushButton('Botón de la pantalla 2')
        layout.addWidget(label)
        layout.addWidget(button)
        self.screen2.setLayout(layout)
