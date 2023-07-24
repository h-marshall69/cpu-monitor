import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit, QTabWidget
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QThread

class HypervisorError(Exception):
    pass

class HypervisorConfig(QObject):
    view_event_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.cpu = 1
        self.memory = 4
        self.storage = 100
        self.devices = []
        self.vms = {}  # Cambiar a un diccionario para almacenar varias máquinas virtuales
        self.simulation_running = False
        self.simulation_speed = 1
        self.workload_type = "balanced"
        self.event_log = []
        self.cpu_scheduling_algorithm = "Round Robin"  # Algoritmo de planificación de CPU predeterminado
        self.memory_allocation_algorithm = "First Fit"  # Algoritmo de asignación de memoria predeterminado
        self.vm_utilization = {}  # Diccionario para almacenar la utilización de recursos de las máquinas virtuales

    def pause_simulation(self):
        if not self.simulation_running:
            raise HypervisorError("The simulation is not currently running, so it cannot be paused.")
        self.simulation_running = False

    def stop_simulation(self):
        if not self.simulation_running:
            raise HypervisorError("The simulation is not currently running, so it cannot be stopped.")
        self.simulation_running = False
        self.vm_count = 0
        self.vms = []

    def restart_simulation(self):
        if not self.simulation_running:
            raise HypervisorError("The simulation is not currently running, so it cannot be restarted.")
        self.stop_simulation()
        self.start_simulation()

    def configure_cpu(self, cpu_cores):
        self.cpu = cpu_cores

    def configure_memory(self, memory_gb):
        self.memory = memory_gb

    def configure_storage(self, storage_gb):
        self.storage = storage_gb

    def add_device(self, device_name):
        self.devices.append(device_name)

    def configure_workload(self, workload_type):
        if workload_type in ["balanced", "cpu_intensive", "memory_intensive", "io_intensive"]:
            self.workload_type = workload_type
        else:
            raise ValueError("Invalid workload type. Available options are: balanced, cpu_intensive, memory_intensive, io_intensive")

    def create_virtual_machine(self, vm_name, cpu_cores, memory_gb, storage_gb, devices=None):
        if devices is None:
            devices = []

        if self._check_resources_available(cpu_cores, memory_gb, storage_gb, devices):
            vm_config = {
                'name': vm_name,
                'cpu': cpu_cores,
                'memory': memory_gb,
                'storage': storage_gb,
                'devices': devices
            }
            self.vms[vm_name] = vm_config
            return True
        else:
            return False

    def _check_resources_available(self, cpu_cores, memory_gb, storage_gb, devices):
        cpu_available = self.cpu >= cpu_cores
        memory_available = self.memory >= memory_gb
        storage_available = self.storage >= storage_gb
        devices_available = all(device in self.devices for device in devices)

        return cpu_available and memory_available and storage_available and devices_available

    def get_vm_by_name(self, vm_name):
        return self.vms.get(vm_name)
    
    def get_all_vms(self):
        return list(self.vms.keys())
    
    def configure_resource_management_algorithm(self, algorithm):
        self.cpu_scheduling_algorithm = algorithm

    def update_vm_info(self):
        # Actualizar la información de utilización de recursos para todas las máquinas virtuales
        for vm_name in self.vms:
            # Aquí puedes implementar la lógica para actualizar la utilización de recursos de cada VM
            # y almacenarla en self.vm_utilization.
            # Por ejemplo, puedes generar valores aleatorios para simular la utilización de recursos.
            cpu_usage = 0.7  # Ejemplo: valor aleatorio de utilización de CPU entre 0 y 1 (70%)
            memory_usage = 0.5  # Ejemplo: valor aleatorio de utilización de memoria entre 0 y 1 (50%)
            storage_usage = 0.3  # Ejemplo: valor aleatorio de utilización de almacenamiento entre 0 y 1 (30%)
            self.vm_utilization[vm_name] = {'CPU': cpu_usage, 'Memory': memory_usage, 'Storage': storage_usage}

    def configure_cpu_scheduling_algorithm(self, algorithm):
        self.cpu_scheduling_algorithm = algorithm

class SimulationThread(QThread):
    simulation_finished_signal = pyqtSignal()

    def __init__(self, hypervisor):
        super().__init__()
        self.hypervisor = hypervisor

    def run(self):
        self.hypervisor.simulation_running = True
        while self.hypervisor.simulation_running:
            # Aquí puedes implementar la lógica para la simulación, como actualizar los recursos, realizar el seguimiento de las máquinas virtuales, etc.
            time.sleep(self.hypervisor.simulation_speed)
            self.hypervisor.update_vm_info()

        self.simulation_finished_signal.emit()

class HypervisorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_vm_info_timer = QTimer()  # Agregar esta línea para definir el atributo
        self.init_ui()

        # Crear una instancia de HypervisorConfig y conectar señales
        self.hypervisor = HypervisorConfig()
        self.hypervisor.view_event_signal.connect(self.append_event_to_log)
        self.update_vm_info_timer = QTimer()
        self.update_vm_info_timer.timeout.connect(self.update_vm_info)

        # Diccionario para almacenar las posiciones de las máquinas virtuales
        self.vm_positions = {}

    def init_ui(self):
        self.setWindowTitle("Hypervisor Simulator")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        

        # Pestaña de Configuración
        self.config_tab = QWidget()
        self.central_widget.addTab(self.config_tab, "Configuración")
        layout_config = QVBoxLayout(self.config_tab)

        # Etiqueta y campo de entrada para el nombre de la VM
        self.vm_name_label = QLabel("Nombre de la VM:")
        self.vm_name_input = QLineEdit()
        layout_config.addWidget(self.vm_name_label)
        layout_config.addWidget(self.vm_name_input)

        self.cpu_label = QLabel("CPU Cores:")
        layout_config.addWidget(self.cpu_label)
        self.cpu_input = QComboBox()
        self.cpu_input.addItems(["1", "2", "4", "8"])
        layout_config.addWidget(self.cpu_input)

        self.memory_label = QLabel("Memory (GB):")
        layout_config.addWidget(self.memory_label)
        self.memory_input = QComboBox()
        self.memory_input.addItems(["1", "2", "4", "8", "16", "32", "64"])
        layout_config.addWidget(self.memory_input)

        self.storage_label = QLabel("Storage (GB):")
        layout_config.addWidget(self.storage_label)
        self.storage_input = QComboBox()
        self.storage_input.addItems(["20", "50", "100", "200", "500", "1000"])
        layout_config.addWidget(self.storage_input)

        self.workload_label = QLabel("Select Workload:")
        layout_config.addWidget(self.workload_label)
        self.workload_input = QComboBox()
        self.workload_input.addItems(["balanced", "cpu_intensive", "memory_intensive", "io_intensive"])
        layout_config.addWidget(self.workload_input)

        self.create_vm_btn = QPushButton("Create Virtual Machine")
        layout_config.addWidget(self.create_vm_btn)

        # Pestaña de Control de Simulación
        self.control_tab = QWidget()
        self.central_widget.addTab(self.control_tab, "Control de Simulación")
        layout_control = QVBoxLayout(self.control_tab)

        # Combo box para seleccionar el algoritmo de gestión de recursos
        self.resource_management_label = QLabel("Algoritmo de Gestión de Recursos:")
        layout_control.addWidget(self.resource_management_label)
        self.resource_management_combobox = QComboBox()
        self.resource_management_combobox.addItems(["Round Robin", "First Fit", "Best Fit", "Worst Fit", "Other"])
        layout_control.addWidget(self.resource_management_combobox)

        self.start_btn = QPushButton("Start Simulation")
        layout_control.addWidget(self.start_btn)

        self.pause_btn = QPushButton("Pause Simulation")
        layout_control.addWidget(self.pause_btn)
        self.pause_btn.setEnabled(False)

        self.stop_btn = QPushButton("Stop Simulation")
        layout_control.addWidget(self.stop_btn)
        self.stop_btn.setEnabled(False)

        self.restart_btn = QPushButton("Restart Simulation")
        layout_control.addWidget(self.restart_btn)
        self.restart_btn.setEnabled(False)

        # Atributo event_log agregado
        self.event_log = QTextEdit()
        layout_control.addWidget(self.event_log)

        # Pestaña de Visualización de Recursos
        self.resource_view_tab = QWidget()
        self.central_widget.addTab(self.resource_view_tab, "Visualización de Recursos")
        self.resource_view_layout = QVBoxLayout(self.resource_view_tab)

        self.vm_info_label = QLabel("Información de Máquinas Virtuales:")
        self.resource_view_layout.addWidget(self.vm_info_label)

        self.vm_info_text = QTextEdit()
        self.vm_info_text.setReadOnly(True)
        self.resource_view_layout.addWidget(self.vm_info_text)

        # Conexiones de señales y ranuras
        self.create_vm_btn.clicked.connect(self.create_virtual_machine)
        self.start_btn.clicked.connect(self.start_simulation)
        self.pause_btn.clicked.connect(self.pause_simulation)
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.restart_btn.clicked.connect(self.restart_simulation)

        # Conexiones para la pestaña de Visualización de Recursos
        self.resource_management_combobox.currentTextChanged.connect(self.configure_resource_management_algorithm)
        self.update_vm_info_timer.timeout.connect(self.update_vm_info)

    def create_virtual_machine(self):
        cpu_cores = int(self.cpu_input.currentText())
        memory_gb = int(self.memory_input.currentText())
        storage_gb = int(self.storage_input.currentText())
        devices = []  # Agregar dispositivos si es necesario
        vm_name = self.vm_name_input.text()

        if not vm_name:
            self.event_log.append("Por favor, ingresa un nombre para la Máquina Virtual.")
            return

        if self.hypervisor.create_virtual_machine(vm_name, cpu_cores, memory_gb, storage_gb, devices):
            self.event_log.append(f"Máquina Virtual '{vm_name}' creada con CPU: {cpu_cores} núcleos, Memoria: {memory_gb}GB, Almacenamiento: {storage_gb}GB.")
            self.start_simulation()  # Iniciar la simulación después de crear la VM
        else:
            self.event_log.append("Recursos insuficientes para crear la Máquina Virtual. Ajusta las configuraciones.")

    def start_simulation(self):
        try:
            if not self.hypervisor.vms:
                self.event_log.append("No se han creado máquinas virtuales. Crea al menos una antes de iniciar la simulación.")
                return

            if self.hypervisor.simulation_running:
                self.event_log.append("La simulación ya está en marcha.")
                return

            # Crear e iniciar el hilo de simulación
            self.simulation_thread = SimulationThread(self.hypervisor)
            self._visualize_resource_utilization()
            self.simulation_thread.simulation_finished_signal.connect(self.on_simulation_finished)
            self.simulation_thread.start()

            self.update_vm_info_timer.start(1000)  # Actualizar información cada 1 segundo
            self.event_log.append("Simulación iniciada.")
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.restart_btn.setEnabled(False)
        except HypervisorError as e:
            self.event_log.append(f"Error: {e}")

    def on_simulation_finished(self):
        self.update_vm_info_timer.stop()
        self.event_log.append("Simulación detenida.")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.restart_btn.setEnabled(True)

    def stop_simulation(self):
        try:
            self.update_vm_info_timer.stop()
            self.hypervisor.stop_simulation()
            self.event_log.append("Simulation stopped.")
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.restart_btn.setEnabled(False)
        except HypervisorError as e:
            self.event_log.append(f"Error: {e}")

    def pause_simulation(self):
        try:
            self.hypervisor.pause_simulation()
            self.event_log.append("Simulation paused.")
            self.pause_btn.setEnabled(False)
            self.restart_btn.setEnabled(True)
        except HypervisorError as e:
            self.event_log.append(f"Error: {e}")

    def restart_simulation(self):
        try:
            self.hypervisor.restart_simulation()
            self.event_log.append("Simulation restarted.")
            self.pause_btn.setEnabled(True)
            self.restart_btn.setEnabled(False)
        except HypervisorError as e:
            self.event_log.append(f"Error: {e}")

    def update_vm_info(self):
        vm_info = "Información de Máquinas Virtuales:\n"
        for vm_name, vm_config in self.hypervisor.vms.items():
            cpu_usage = self.hypervisor.vm_utilization.get(vm_name, {}).get('CPU', 0.0)
            memory_usage = self.hypervisor.vm_utilization.get(vm_name, {}).get('Memory', 0.0)
            storage_usage = self.hypervisor.vm_utilization.get(vm_name, {}).get('Storage', 0.0)
            status = "Activa" if vm_name in self.hypervisor.get_all_vms() else "Detenida"
            vm_info += f"{vm_name} (Estado: {status}) - CPU: {cpu_usage:.1%}, Memoria: {memory_usage:.1%}, Almacenamiento: {storage_usage:.1%}\n"
        self.vm_info_text.setPlainText(vm_info)

    def get_vm_resource_usage(self, vm_name, resource):
        # Obtener la utilización de recursos de la máquina virtual especificada
        if vm_name in self.hypervisor.vm_utilization:
            return self.hypervisor.vm_utilization[vm_name][resource]
        else:
            return 0.0

    def is_vm_active(self, vm_name):
        # Implementar la lógica para determinar si la máquina virtual está activa o detenida.
        # Puedes usar datos de simulación almacenados en self.hypervisor.vms para verificar el estado de cada VM.
        return True  # Ejemplo: siempre considerar que las máquinas virtuales están activas.

    def configure_resource_management_algorithm(self, algorithm):
        self.hypervisor.configure_resource_management_algorithm(algorithm)

    def append_event_to_log(self, event_text):
        self.event_log.append(event_text)

    def _visualize_resource_utilization(self):
        try:
            self.hypervisor.configure_workload(self.workload_input.currentText())
            self.hypervisor.start_simulation()
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.restart_btn.setEnabled(False)

            # Almacenar las posiciones de las máquinas virtuales en self.vm_positions
            for vm_name in self.hypervisor.vms:
                self.vm_positions[vm_name] = self.generate_random_position()
        except HypervisorError as e:
            self.event_log.append(f"Error: {e}")

    def generate_random_position(self):
        # Implementar la lógica para generar posiciones aleatorias
        # Puedes usar la librería random para generar coordenadas x e y aleatorias
        import random
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        return x, y

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HypervisorGUI()
    window.show()
    sys.exit(app.exec_())