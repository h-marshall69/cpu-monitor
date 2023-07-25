# Autor
-Hildebrandt Quispe Ramos

# PyWifi 

PyWifi es una biblioteca de Python que proporciona una interfaz para interactuar con interfaces inalámbricas y redes WiFi. Con PyWifi, los desarrolladores pueden realizar diversas tareas relacionadas con redes inalámbricas, como escanear redes WiFi disponibles, conectarse a una red específica, obtener información sobre la señal de una red, y más.

# PyQt5

PyQt5 es una biblioteca de Python que permite crear aplicaciones de escritorio con una interfaz gráfica de usuario (GUI). Se basa en la biblioteca Qt, que es una herramienta popular y poderosa para desarrollar aplicaciones multiplataforma.

Con PyQt5, los desarrolladores pueden crear ventanas, diálogos, botones, menús, barras de herramientas y otros elementos de la GUI de manera sencilla. Ofrece una amplia gama de widgets y funcionalidades para crear aplicaciones con una apariencia y comportamiento profesionales.

# PyQtChart

PyQtChart es una extensión de la biblioteca PyQt5 que proporciona capacidades de trazado de gráficos y visualización de datos en aplicaciones de escritorio. Esta biblioteca permite a los desarrolladores crear gráficos interactivos y personalizados dentro de sus interfaces gráficas de usuario (GUI) basadas en PyQt.

Al utilizar PyQtChart, los programadores pueden representar datos en diferentes tipos de gráficos, como gráficos de barras, gráficos de líneas, gráficos de dispersión y más. La biblioteca ofrece una variedad de opciones para personalizar la apariencia de los gráficos y brinda soporte para animaciones y zoom, lo que mejora la experiencia del usuario.

# Psutil

Psutil es una biblioteca de Python multiplataforma que proporciona una interfaz sencilla para recuperar información sobre el sistema operativo y los recursos del sistema. Su nombre proviene de "system utilities" (utilidades del sistema).

## Instalación

Copiar y pegar la siguiente línea de comandos para instalar todas librería usadas para este proyecto

```bash
pip install -r requirements.txt
```

## Uso para app.py

```python
import sys
import psutil
import time
import pywifi
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QWidget, QTabWidget, QStackedWidget, QHeaderView, QTextEdit, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries
```

## Uso de monitor-h.py

```python
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit, QTabWidget
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QThread
```

## Propósito del proyecto

El presente proyecto tiene como objetivo integrar un Monitor de CPU en un Simulador de Hipervisor, con el propósito de proporcionar una herramienta de monitoreo en tiempo real del uso de la CPU dentro de entornos virtuales. Un hipervisor es un software que permite la ejecución de múltiples máquinas virtuales en un único host físico. El monitor de CPU permitirá a los usuarios visualizar y analizar la carga de trabajo y el rendimiento de las máquinas virtuales, identificar posibles cuellos de botella y optimizar el uso de recursos.
