import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial

from dotenv import load_dotenv
import os
import math

load_dotenv()

SERIAL_PORT = os.getenv('SERIAL_PORT')
ser = serial.Serial(SERIAL_PORT)

FFT_NUM_SAMPLES = 1000
FFT_SAMPLE_FREQ_HZ = 48e6 / 6e3
FFT_BIN_FREQ_INCREMENT_HZ = FFT_SAMPLE_FREQ_HZ / FFT_NUM_SAMPLES
FFT_PLOT_LOG = True
FFT_MAX_YLIM = 50 if FFT_PLOT_LOG else 1000

FFT_VEL_DECT_MAG_THRESHOLD = 200 # Bins with a Y value greater than or equal to this count as a target velocity.

V_HISTORY_NUM_SAMPLES = 100
V_MAX_YLIM_MPH = 30

fig, ax = plt.subplots(2, 1) # figure and axes to plot on
ln = [] # list of lines

# FFT Plot Variables
# fft_xdata, fft_ydata = [], []
# fft_ygrad = [] # will be 1 element shorter than fft_ydata
fft_ln, = ax[0].plot([], [], 'r', linestyle='solid')
ln.append(fft_ln)

# Velocity Plot Variables
v_xdata = [i for i in range(V_HISTORY_NUM_SAMPLES-1, -1, -1)]
v_ydata = [0] * V_HISTORY_NUM_SAMPLES
v_ln, = ax[1].plot([], [], 'b', linestyle='solid')
ln.append(v_ln)

def init():
    # Set limits for FFT plot.
    ax[0].set_ylim(0, FFT_MAX_YLIM)
    ax[0].set_xlim(-FFT_SAMPLE_FREQ_HZ/4, FFT_SAMPLE_FREQ_HZ/4)

    # Set limits for velocity plot.
    ax[1].set_ylim(0, V_MAX_YLIM_MPH)
    ax[1].set_xlim(min(v_xdata), max(v_xdata))

    return ln

def update(frame):
    # Update FFT plot.
    fft_xdata, fft_ydata, fft_ygrad = read_freq_bins_from_serial()
    # print(fft_ydata)
    ln[0].set_data(fft_xdata, fft_ydata)

    # Update velocity plot.
    offset = 10
    fft_max_freq=0
    for i in range(FFT_NUM_SAMPLES-1, math.floor(FFT_NUM_SAMPLES/2), -1):
        if fft_ydata[i] >= FFT_VEL_DECT_MAG_THRESHOLD:
            fft_max_freq=fft_xdata[i]
            break
    # fft_max_freq = fft_xdata[np.argmax(fft_ydata[offset:])+offset]
    # print(fft_max_freq)
    v_ydata.pop(0)
    v_ydata.append(hz_to_mph(fft_max_freq))
    ln[1].set_data(v_xdata, v_ydata)

    return ln

def read_freq_bins_from_serial():
    line = ser.readline()

    data_str_list = line.split()
    # Convert values to dB.
    for i, val in enumerate(data_str_list):
        # Add 1 to each value before logging to avoid divide by zero errors.
        data_str_list[i] = 10*np.log10(int(data_str_list[i])+1) if FFT_PLOT_LOG else int(data_str_list[i])

    fft_xdata = []
    fft_ydata = []

    # Negative Frequencies: i = FFT_NUM_SAMPLES/2 to end
    for i in range(0, math.floor(FFT_NUM_SAMPLES/2)):
        fft_ydata.append(data_str_list[i+math.floor(FFT_NUM_SAMPLES/2)])
        fft_xdata.append((i-math.ceil(FFT_NUM_SAMPLES/2))*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES) 

    # Positive Frequencies: i = 0 to FFT_NUM_SAMPLES/2
    for i in range(0, math.ceil(FFT_NUM_SAMPLES/2)):
        fft_ydata.append(data_str_list[i])
        fft_xdata.append(i*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES)

    fft_ygrad = []

    for i, val in enumerate(fft_ydata[1:]):
        fft_ygrad.append(fft_ydata[i] - fft_ydata[i-1])
    
    return fft_xdata, fft_ydata, fft_ygrad

def hz_to_mph(freq_hz):
    return freq_hz / 31.36

def main():

    ani_fft = FuncAnimation(
        fig, 
        update, 
        interval=10,
        init_func=init, 
        blit=True,
        cache_frame_data=False
    )
    plt.show()

if __name__=="__main__":
    main()

