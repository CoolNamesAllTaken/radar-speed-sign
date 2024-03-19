import numpy as np
import serial

from dotenv import load_dotenv
import os
import math

import sys # for access to command line arguments
import serial
import serial.tools.list_ports

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QToolButton, QComboBox, QVBoxLayout, QToolBar, QCheckBox
import pyqtgraph as pg # for radar FFT plots
import qdarktheme

FFT_NUM_SAMPLES = 1000
FFT_SAMPLE_FREQ_HZ = 48e6 / 6e3
FFT_BIN_FREQ_INCREMENT_HZ = FFT_SAMPLE_FREQ_HZ / FFT_NUM_SAMPLES
FFT_NUM_LABELLED_PEAKS = 5

FFT_VEL_DECT_MAG_THRESHOLD = 200 # Bins with a Y value greater than or equal to this count as a target velocity.

V_HISTORY_NUM_SAMPLES = 100
V_MAX_YLIM_MPH = 30

class SpectrogramWidget(pg.PlotWidget):

    # read_collected = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, data_shape, freq_increment_hz, image_shape):
        """
        @brief Constructor for spectrogram widget.

        @param[in] data_shape Tuple of shape (x_dim, y_dim, z_dim).
            x_dim = X dimension of the spectrogram, number of bins in the FFT.
            y_dim = Y dimension of the spectrogram, number of historic samples to show.
            z_dim = Z dimension of the spectrogram, max value for color resolution.
        @param[in] freq_increment_hz Width of an FFT bin in Hz.
        @param[in] image_shape Tuple of shape (x_dim, y_dim). Used to rescale the spectrogram.
            x_dim = Width of the plot, in pixels.
            y_dim = Height of the plot, in pixels.
        """
        super(SpectrogramWidget, self).__init__()

        self.data_shape = data_shape # shape is (x_dim, y_dim, z_dim), where Z is the vertical height on the screen and Y is the color depth.
        self.freq_increment_hz = freq_increment_hz
        self.image_shape = image_shape

        self.img = pg.ImageItem()
        self.addItem(self.img)

        self.img_array = np.zeros((self.data_shape[0], self.data_shape[1]))

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-50,40])

        # setup the correct scaling for x-axis
        # print(self.image_shape[1] / self.data_shape[1])
        # print(f"img_array shape: {self.img_array.shape}")

        self.img.setImage(self.img_array, autoLevels=False)
        self.img.setRect(0, 0, self.data_shape[0]*self.freq_increment_hz, self.data_shape[1])
        
        
        # freq_bins = np.arange(self.data_shape[0])*self.freq_increment_hz
        # xscale = 1.0/(self.img_array.shape[0]/freq_bins[-1])
        # self.img.scale((1./FS)*self.data_shape[2], xscale)

        self.setLabel('bottom', 'Frequency', units='Hz')

        self.show()
    
    def update(self, data):
        """
        @brief Update function that adds bin values to the spectrogram and rolls it upwards.
        @param[in] data Array of magnitudes for each FFT bin, of dimension data_shape[0].
        """
        self.img_array = np.roll(self.img_array, 1, axis=1)
        # print(f"data={data}")
        self.img_array[:,0] = data
        self.img.setImage(self.img_array, autoLevels=False)

class RadarUtilWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pants for Birds Radar Util")
        self.setMinimumSize(QSize(1000, 800))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        ## Add Serial Port Toolbar
        serial_toolbar = QToolBar()
        self.addToolBar(serial_toolbar)

        self.serial_port_dropdown = QComboBox()
        self.serial_list_ports()
        serial_toolbar.addWidget(self.serial_port_dropdown)

        self.serial_connect_button = QToolButton()
        self.serial_connect_button.setCheckable(True)
        self.serial_connect_button.setChecked(False) # start as disconnected
        self.serial_connect_button.setText("Connect")
        self.serial_connect_button.clicked.connect(self.serial_connect_button_clicked)
        serial_toolbar.addWidget(self.serial_connect_button)

        self.serial_refresh_button = QPushButton("Refresh Serial Ports")
        self.serial_refresh_button.clicked.connect(self.serial_list_ports)
        serial_toolbar.addWidget(self.serial_refresh_button)

        ## Add Plot Toolbar
        self.addToolBarBreak()
        plot_toolbar = QToolBar()
        self.addToolBar(plot_toolbar)

        self.fft_plot_log_button = QCheckBox("Plot FFT as Log")
        plot_toolbar.addWidget(self.fft_plot_log_button)

        ## Add Radar Plots
        self.fft_spectrogram_widget = SpectrogramWidget((math.floor(FFT_NUM_SAMPLES/2), V_HISTORY_NUM_SAMPLES, 2e12 - 1), FFT_BIN_FREQ_INCREMENT_HZ, (1000, 600))
        layout.addWidget(self.fft_spectrogram_widget)

        self.fft_plot_widget = pg.PlotWidget()
        layout.addWidget(self.fft_plot_widget)

        self.velocity_plot_widget = pg.PlotWidget()
        layout.addWidget(self.velocity_plot_widget)
        
        self.fft_data= np.stack((np.arange(100), np.zeros((100,))), axis=-1)
        self.fft_plot_curve = self.fft_plot_widget.plot(self.fft_data, pen=pg.mkPen('w', width=2))
        self.fft_peak_arrows = []
        self.fft_peak_labels = []
        self.velocity_data = np.stack((np.arange(100), np.zeros((100,))), axis=-1)
        self.velocity_plot_curve = self.velocity_plot_widget.plot(self.velocity_data, pen=pg.mkPen('w', width=2))

        ## Set the Layout
        self.central_widget.setLayout(layout)

    def serial_list_ports(self):
        """
        @brief Helper function for populating the serial ports dropdown.
        """
        self.serial_port_dropdown.clear() # remove all items from dropdown
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.serial_port_dropdown.addItem(port.device)

    def serial_connect_button_clicked(self):
        """
        @brief Initiates a serial connection and starts the program if successful.
        """
        if self.serial_connect_button.isChecked():
            # Connecting
            port_name = self.serial_port_dropdown.currentText()
            try:
                self.serial = serial.Serial(port_name, baudrate=9600, timeout=1)
                print(f"Connected to {port_name}")

                self.serial_connect_button.setText("Disconnect")
                # self.serial_connect_button.

                # Start updating the plots
                self.timer = pg.QtCore.QTimer()
                self.timer.timeout.connect(self.update)
                self.timer.start(50) # Update plots at 20Hz.
            except serial.SerialException as e:
                print(f"Failed to connect to {port_name}: {e}")
        else:
            # Disconnecting
            self.serial_connect_button.setText("Connect")

            if self.serial is not None:
                self.serial.close()
                print("Disconnected from serial port.")
                self.serial = None
                self.timer.stop()
    
    # def serial_disconnect(self):


    def update(self):
        """
        @brief Main update function.
        """
        self.read_freq_bins_from_serial()
        self.fft_plot_curve.setData(self.fft_data)
        self.fft_spectrogram_widget.update(self.fft_data[:, 1])
        self.update_velocity()

    def read_freq_bins_from_serial(self):
        """
        @brief Fill data buffers from lines ingested via the serial port.
        """

        line = self.serial.readline()

        data_str_list = line.split()

        # Convert values to int, convert to dB if necessary.
        for i, val in enumerate(data_str_list):
            # Add 1 to each value before logging to avoid divide by zero errors.
            if self.fft_plot_log_button.isChecked():
                data_str_list[i] = 10*np.log10(int(data_str_list[i])+1) 
            else:
                data_str_list[i] = int(data_str_list[i])

        fft_xdata = []
        fft_ydata = []

        # Positive Frequencies: i = 0 to FFT_NUM_SAMPLES/2
        for i in range(0, math.floor(FFT_NUM_SAMPLES/2)):
            fft_ydata.append(data_str_list[i])
            fft_xdata.append(i*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES)

        fft_ygrad = []

        for i, val in enumerate(fft_ydata[1:]):
            fft_ygrad.append(fft_ydata[i] - fft_ydata[i-1])
        
        self.fft_data = np.stack((np.arange(len(fft_ydata)) * FFT_BIN_FREQ_INCREMENT_HZ, fft_ydata), axis=-1)
    
    def update_velocity(self):
        fft_grad_data = [] # List of tuples of form [fft_freq, fft_grad].
        # Note: fft_grad_data[0] has the gradient of slope starting at self.fft_data[0].
        for i in range(1, len(self.fft_data)):
            frequency = self.fft_data[i-1][0]
            gradient = self.fft_data[i][1] - self.fft_data[i-1][1]
            fft_grad_data.append([frequency, gradient])

        # Clear old peak arrows off the FFT curve.
        for i in range(len(self.fft_peak_arrows)):
            self.fft_plot_widget.removeItem(self.fft_peak_arrows[i])
        
        # Clear old peak labels off the FFT curve.
        for i in range(len(self.fft_peak_labels)):
            self.fft_plot_widget.removeItem(self.fft_peak_labels[i])

        fft_gradient_peaks = [] # List of tuples with the form (fft_freq, fft_mag) for each peak.
        for i in range(1, len(fft_grad_data)-1):
            if fft_grad_data[i-1][1] > 0 and fft_grad_data[i+1][1] < 0:
                peak_frequency = self.fft_data[i][0]
                peak_magnitude = self.fft_data[i][1]
                fft_gradient_peaks.append((peak_frequency, peak_magnitude))

        fft_gradient_peaks.sort(key=lambda a: a[1], reverse=True) # sort peaks by magnitude, descending order
        for i, peak in enumerate(fft_gradient_peaks[:FFT_NUM_LABELLED_PEAKS]):
                self.fft_peak_arrows.append(pg.CurveArrow(self.fft_plot_curve, index=i))
                self.fft_plot_widget.addItem(self.fft_peak_arrows[-1])

                self.fft_peak_labels.append(pg.TextItem(f"{peak[0]}, {peak[1]}", angle=90))
                self.fft_peak_labels[-1].setPos(peak[0], peak[1])
                self.fft_plot_widget.addItem(self.fft_peak_labels[-1])
    
    def hz_to_mph(freq_hz):
        return freq_hz / 31.36


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    # Set up pyqtgraph
    pg.setConfigOption('background', '#1F1F1F')

    window = RadarUtilWindow()
    window.show()

    sys.exit(app.exec())