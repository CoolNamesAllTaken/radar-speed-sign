import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QComboBox, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
import serial

class SerialConnectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Connection")
        self.setGeometry(100, 100, 600, 400)

        self.serial_port_combo = QComboBox()
        self.populate_serial_ports()

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_serial)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.addWidget(self.serial_port_combo)
        self.toolbar.addWidget(self.connect_button)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.plot_widget1 = pg.PlotWidget()
        layout.addWidget(self.plot_widget1)

        self.plot_widget2 = pg.PlotWidget()
        layout.addWidget(self.plot_widget2)

        self.plot_data1 = np.random.normal(size=(100,))
        self.plot_data2 = np.random.normal(size=(100,))
        self.plot_curve1 = self.plot_widget1.plot(self.plot_data1, pen=pg.mkPen('b', width=2))
        self.plot_curve2 = self.plot_widget2.plot(self.plot_data2, pen=pg.mkPen('r', width=2))

    def populate_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.serial_port_combo.addItem(port.device)

    def connect_to_serial(self):
        port_name = self.serial_port_combo.currentText()
        try:
            self.serial = serial.Serial(port_name, baudrate=9600, timeout=1)
            print(f"Connected to {port_name}")

            # Start updating the plots
            self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(self.update_plots)
            self.timer.start(50)  # Update plots every 50 milliseconds

        except serial.SerialException as e:
            print(f"Failed to connect to {port_name}: {e}")

    def update_plots(self):
        # Example: updating plots with random data
        new_data1 = np.random.normal(size=(100,))
        new_data2 = np.random.normal(size=(100,))
        self.plot_data1 = np.roll(self.plot_data1, -len(new_data1))
        self.plot_data2 = np.roll(self.plot_data2, -len(new_data2))
        self.plot_data1[-len(new_data1):] = new_data1
        self.plot_data2[-len(new_data2):] = new_data2
        self.plot_curve1.setData(self.plot_data1)
        self.plot_curve2.setData(self.plot_data2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialConnectionWindow()
    window.show()
    sys.exit(app.exec())
