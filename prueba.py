from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QTabWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        tab_widget = QTabWidget(self)
        text_edit1 = QTextEdit()
        text_edit2 = QTextEdit()

        tab_widget.addTab(text_edit1, 'Pestaña 1')
        tab_widget.addTab(text_edit2, 'Pestaña 2')

        self.setCentralWidget(tab_widget)

        # Agregar contador en la pestaña 2
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCounter)
        self.timer.start(1000)  # Actualizar cada segundo

        self.show()

    def updateCounter(self):
        self.counter += 1
        self.centralWidget().widget(1).setText(f'Contador: {self.counter}')

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    app.exec()
