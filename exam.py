# Разработать приложение для мониторинга нагрузки системы и системных процессов (аналог диспетчера задач).
#
# Обязательные функции в приложении:
#
# Показ общих сведений о системе (в текстовом виде!):
# Название процессора, количество ядер, текущая загрузка
# Общий объём оперативной памяти, текущая загрузка оперативаной памяти
# Количество, жестких дисков + информация по каждому (общий/занятый объём)
# Обеспечить динамический выбор обновления информации (1, 5, 10, 30 сек.)
# Показ работающих процессов
# Показ работающих служб
# Показ задач, которые запускаются с помощью планировщика задач


import sys
import psutil
import platform
import win32com.client
from PySide6 import QtWidgets, QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        self.delay = 1

    def run(self):
        while True:
            cpu_load = psutil.cpu_percent(interval=self.delay)
            cpu_name = platform.processor()
            cpu_count = psutil.cpu_count()
            ram = psutil.virtual_memory()
            ram_load = ram.percent
            disk_info = self.get_disk_info()

            self.systemInfoReceived.emit((cpu_name, cpu_load, ram, ram_load, disk_info))

    def get_disk_info(self):
        disk_info = []
        disks = psutil.disk_partitions()
        for d in disks:
            usage = psutil.disk_usage(d.mountpoint)
            disk_info.append({
                'device': d.device,
                'total': usage.total / (1024 ** 3),
                'used': usage.used / (1024 ** 3),
            })
        return disk_info


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о системе")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QtWidgets.QTabWidget(self)

        self.system_tab = QtWidgets.QWidget()
        self.system_layout = QtWidgets.QVBoxLayout(self.system_tab)

        self.cpu_label = QtWidgets.QLabel("Процессор: ", self)
        self.cores_label = QtWidgets.QLabel("Количество ядер: ", self)
        self.cpu_load_label = QtWidgets.QLabel("Загрузка CPU: 0%", self)
        self.ram_label = QtWidgets.QLabel("Общий объём RAM: 0 ГБ", self)
        self.ram_load_label = QtWidgets.QLabel("Загрузка RAM: 0%", self)
        self.disk_label = QtWidgets.QLabel("Жесткие диски: ", self)

        self.delay_input = QtWidgets.QComboBox(self)
        self.delay_input.addItems(["1", "5", "10", "30"])
        self.delay_input.currentIndexChanged.connect(self.update_delay)

        self.start_btn = QtWidgets.QPushButton("Запустить поток", self)
        self.start_btn.clicked.connect(self.start_system_info_thread)

        self.system_layout.addWidget(self.cpu_label)
        self.system_layout.addWidget(self.cores_label)
        self.system_layout.addWidget(self.cpu_load_label)
        self.system_layout.addWidget(self.ram_label)
        self.system_layout.addWidget(self.ram_load_label)
        self.system_layout.addWidget(self.disk_label)
        self.system_layout.addWidget(QtWidgets.QLabel("Интервал обновления (сек):", self))
        self.system_layout.addWidget(self.delay_input)
        self.system_layout.addWidget(self.start_btn)

        self.tabs.addTab(self.system_tab, "Информация о системе")

        self.process_tab = ProcessInfoWidget()
        self.tabs.addTab(self.process_tab, "Работающие процессы")

        self.service_tab = ServiceInfoWidget()
        self.tabs.addTab(self.service_tab, "Работающие службы")

        self.task_tab = TaskSchedulerWidget()
        self.tabs.addTab(self.task_tab, "Задачи планировщика")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.system_info_thread = SystemInfo()
        self.system_info_thread.systemInfoReceived.connect(self.update_system_info)

    def start_system_info_thread(self):
        self.system_info_thread.delay = int(self.delay_input.currentText())
        self.system_info_thread.start()

    def update_system_info(self, system_info):
        cpu_name, cpu_load, ram, ram_load, disk_info = system_info

        self.cpu_label.setText(f"Процессор: {cpu_name}")
        self.cores_label.setText(f"Количество ядер: {psutil.cpu_count()}")
        self.cpu_load_label.setText(f"Загрузка CPU: {cpu_load}%")
        self.ram_label.setText(f"Общий объём RAM: {ram.total / (1024 ** 3):.2f} ГБ")
        self.ram_load_label.setText(f"Загрузка RAM: {ram_load}%")

        disk_info_text = "Жесткие диски:\n"
        for disk in disk_info:
            disk_info_text += f"{disk['device']}: {disk['total']:.2f} ГБ (общий), {disk['used']:.2f} ГБ (занятый)\n"
        self.disk_label.setText(disk_info_text)

    def update_delay(self):
        self.system_info_thread.delay = int(self.delay_input.currentText())


class ProcessInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.process_table = QtWidgets.QTableWidget(self)
        self.process_table.setColumnCount(1)
        self.process_table.setHorizontalHeaderLabels(["Процесс"])
        self.layout.addWidget(self.process_table)

        self.update_processes()

    def update_processes(self):
        processes = []
        for proc in psutil.process_iter(['name']):
            # print(proc)
            processes.append(proc.info)

        self.process_table.setRowCount(len(processes))
        for row, process in enumerate(processes):
            self.process_table.setItem(row, 1, QtWidgets.QTableWidgetItem(process['name']))

        self.process_table.resizeColumnsToContents()


class ServiceInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.service_table = QtWidgets.QTableWidget(self)
        self.service_table.setColumnCount(2)
        self.service_table.setHorizontalHeaderLabels(["Имя службы", "Статус"])
        self.layout.addWidget(self.service_table)

        self.update_services()

    def update_services(self):
        services = []
        for service in psutil.win_service_iter():
            services.append({
                'name': service.name(),
                'status': service.status(),

            })

        self.service_table.setRowCount(len(services))
        for row, service in enumerate(services):
            self.service_table.setItem(row, 0, QtWidgets.QTableWidgetItem(service['name']))
            self.service_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service['status']))

        self.service_table.resizeColumnsToContents()


class TaskSchedulerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.task_table = QtWidgets.QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Имя задачи", "Следующее выполнение"])
        self.layout.addWidget(self.task_table)

        self.update_tasks()

    def update_tasks(self):
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        tasks = scheduler.GetFolder("\\").GetTasks(0)
        task_list = []
        for task in tasks:
            task_list.append({
                'name': task.Name,
                'next_run': task.NextRunTime
            })

        self.task_table.setRowCount(len(task_list))
        for row, task in enumerate(task_list):
            self.task_table.setItem(row, 0, QtWidgets.QTableWidgetItem(task['name']))
            self.task_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(task['next_run'])))

        self.task_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = SystemInfoWidget()
    widget.show()
    sys.exit(app.exec())
