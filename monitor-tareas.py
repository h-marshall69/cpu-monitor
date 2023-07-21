import sys
import psutil
import time
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout


class ResourceMonitor:
    def __init__(self):
        self.available_cpu = psutil.cpu_count() * 100
        self.available_ram = psutil.virtual_memory().total / (1024 ** 3)  # GB
        self.available_disk = psutil.disk_usage("/").total / (1024 ** 3)  # GB

    def allocate_resources(self, cpu_demand, ram_demand, disk_demand):
        if cpu_demand > self.available_cpu or ram_demand > self.available_ram or disk_demand > self.available_disk:
            return False

        self.available_cpu -= cpu_demand
        self.available_ram -= ram_demand
        self.available_disk -= disk_demand
        return True

    def release_resources(self, cpu_demand, ram_demand, disk_demand):
        self.available_cpu += cpu_demand
        self.available_ram += ram_demand
        self.available_disk += disk_demand


class Task:
    def __init__(self, name, cpu_demand, ram_demand, disk_demand, cpu_limit, ram_limit, disk_limit, page_count, page_size, resource_monitor):
        self.name = name
        self.cpu_demand = cpu_demand
        self.ram_demand = ram_demand
        self.disk_demand = disk_demand
        self.cpu_limit = int(cpu_limit)
        self.ram_limit = float(ram_limit)
        self.disk_limit = float(disk_limit)
        self.is_running = False

        # Memory allocation for the task
        self.page_count = page_count
        self.page_size = page_size
        self.memory_allocated = False
        self.pages = [None] * page_count

        self.resource_monitor = resource_monitor

    def allocate_memory(self):
        if not self.memory_allocated:
            for i in range(self.page_count):
                self.pages[i] = f"Page {i + 1} of {self.name}"
            self.memory_allocated = True

    def start(self):
        if not self.is_running and self.resource_monitor.allocate_resources(self.cpu_demand, self.ram_demand, self.disk_demand):
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.resource_monitor.release_resources(self.cpu_demand, self.ram_demand, self.disk_demand)


class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resource_monitor = ResourceMonitor()
        self.tasks = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Task Manager")
        self.setGeometry(200, 200, 500, 400)

        main_layout = QVBoxLayout()

        tab_widget = QTabWidget()

        # Tab 1: Create Tasks
        create_tasks_tab = QWidget()
        self.create_tasks_ui(create_tasks_tab)
        tab_widget.addTab(create_tasks_tab, "Create Tasks")

        # Tab 2: View Tasks
        view_tasks_tab = QWidget()
        self.view_tasks_ui(view_tasks_tab)
        tab_widget.addTab(view_tasks_tab, "View Tasks")

        main_layout.addWidget(tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Update task resources every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_task_resources)
        timer.start(1000)

    def create_tasks_ui(self, parent):
        layout = QVBoxLayout()

        self.task_name_input = QLineEdit()
        self.cpu_demand_input = QLineEdit()
        self.ram_demand_input = QLineEdit()
        self.disk_demand_input = QLineEdit()
        self.cpu_limit_input = QLineEdit()
        self.ram_limit_input = QLineEdit()
        self.disk_limit_input = QLineEdit()
        self.page_count_input = QLineEdit()
        self.page_size_input = QLineEdit()

        self.create_task_button = QPushButton("Create Task")
        self.create_task_button.clicked.connect(self.add_task)

        layout.addWidget(QLabel("Task Name:"))
        layout.addWidget(self.task_name_input)

        layout.addWidget(QLabel("CPU Demand:"))
        layout.addWidget(self.cpu_demand_input)

        layout.addWidget(QLabel("RAM Demand (GB):"))
        layout.addWidget(self.ram_demand_input)

        layout.addWidget(QLabel("Disk Demand (GB):"))
        layout.addWidget(self.disk_demand_input)

        layout.addWidget(QLabel("CPU Limit (%):"))
        layout.addWidget(self.cpu_limit_input)

        layout.addWidget(QLabel("RAM Limit (GB):"))
        layout.addWidget(self.ram_limit_input)

        layout.addWidget(QLabel("Disk Limit (GB):"))
        layout.addWidget(self.disk_limit_input)

        layout.addWidget(QLabel("Page Count:"))
        layout.addWidget(self.page_count_input)

        layout.addWidget(QLabel("Page Size (MB):"))
        layout.addWidget(self.page_size_input)

        layout.addWidget(self.create_task_button)

        parent.setLayout(layout)

    def view_tasks_ui(self, parent):
        layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.show_task_info)
        layout.addWidget(self.task_list)

        self.task_info_label = QLabel()
        self.task_info_label.setWordWrap(True)
        layout.addWidget(self.task_info_label)

        self.close_task_button = QPushButton("Close Task")
        self.close_task_button.clicked.connect(self.close_task)
        layout.addWidget(self.close_task_button)

        parent.setLayout(layout)

    def add_task(self):
        name = self.task_name_input.text()
        cpu_demand = int(self.cpu_demand_input.text())
        ram_demand = float(self.ram_demand_input.text())
        disk_demand = float(self.disk_demand_input.text())
        cpu_limit = self.cpu_limit_input.text()
        ram_limit = self.ram_limit_input.text()
        disk_limit = self.disk_limit_input.text()
        page_count = int(self.page_count_input.text())
        page_size = int(self.page_size_input.text())

        task = Task(name, cpu_demand, ram_demand, disk_demand, cpu_limit, ram_limit, disk_limit, page_count, page_size, self.resource_monitor)
        self.tasks.append(task)

        self.task_list.addItem(name)
        task.allocate_memory()  # Allocate memory for the task

        self.task_name_input.clear()
        self.cpu_demand_input.clear()
        self.ram_demand_input.clear()
        self.disk_demand_input.clear()
        self.cpu_limit_input.clear()
        self.ram_limit_input.clear()
        self.disk_limit_input.clear()
        self.page_count_input.clear()
        self.page_size_input.clear()

    def close_task(self):
        selected_item = self.task_list.currentItem()
        if not selected_item:
            return

        selected_task = selected_item.text()
        for task in self.tasks:
            if task.name == selected_task:
                task.stop()
                self.tasks.remove(task)
                break

        self.update_task_list()

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(task.name)

    def show_task_info(self):
        selected_item = self.task_list.currentItem()
        if not selected_item:
            self.task_info_label.setText("")
            return

        selected_task = selected_item.text()
        for task in self.tasks:
            if task.name == selected_task:
                info = (
                    f"Task: {task.name}\n"
                    f"CPU Demand: {task.cpu_demand}%\n"
                    f"RAM Demand (GB): {task.ram_demand:.2f}\n"
                    f"Disk Demand (GB): {task.disk_demand:.2f}\n"
                    f"CPU Limit: {task.cpu_limit}%\n"
                    f"RAM Limit (GB): {task.ram_limit:.2f}\n"
                    f"Disk Limit (GB): {task.disk_limit:.2f}\n"
                    f"Page Count: {task.page_count}\n"
                    f"Page Size (MB): {task.page_size}\n"
                    f"Running: {'Yes' if task.is_running else 'No'}"
                )
                self.task_info_label.setText(info)
                break

    def update_task_resources(self):
        for task in self.tasks:
            if task.is_running:
                cpu_usage = random.randint(1, task.cpu_demand)
                ram_usage = random.uniform(0.1, task.ram_demand)
                disk_usage = random.uniform(0.5, task.disk_demand)
                if not self.resource_monitor.allocate_resources(cpu_usage, ram_usage, disk_usage):
                    task.stop()
        self.show_task_info()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec_())
