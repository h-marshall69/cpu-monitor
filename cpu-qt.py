import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configurar la ventana principal
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Toolbar de botones')

        menu1 = QAction('Procesos', self)
        menu1.triggered.connect(self.veraccion1)

        menu2 = QAction('Rendimiento', self)
        menu2.triggered.connect(self.veraccion2)

        menu3 = QAction('Detalles', self)
        menu3.triggered.connect(self.veraccion3)

        # Crear la toolbar y agregar las acciones
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(menu1)
        toolbar.addAction(menu2)
        toolbar.addAction(menu3)

        self.show()

    def veraccion1(self):
        print('Abrir archivo - Procesos')

    def veraccion2(self):
        print('Abrir archivo - Rendimiento')

    def veraccion3(self):
        print('Abrir archivo - Detalles')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
