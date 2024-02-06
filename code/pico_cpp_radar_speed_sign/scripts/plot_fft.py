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
FFT_MAX_YLIM = 1000

V_HISTORY_NUM_SAMPLES = 100
V_MAX_YLIM_MPH = 5

fig, ax = plt.subplots(2, 1) # figure and axes to plot on
ln = [] # list of lines

# FFT Plot Variables
fft_xdata, fft_ydata = [], []
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
    read_freq_bins_from_serial()

    # Update FFT plot.
    fft_xdata, fft_ydata = read_freq_bins_from_serial()
    print(fft_ydata)
    ln[0].set_data(fft_xdata, fft_ydata)

    # Update velocity plot.
    offset = 10
    fft_max_freq = fft_xdata[np.argmax(fft_ydata[offset:])+offset]
    v_ydata.pop(0)
    v_ydata.append(hz_to_mph(fft_max_freq))
    ln[1].set_data(v_xdata, v_ydata)

    return ln

def read_freq_bins_from_serial():
    line = ser.readline()
    # print(f"line={line}")

    data_str_list = line.split()
    fft_xdata = []
    fft_ydata = []

    # Negative Frequencies: i = FFT_NUM_SAMPLES/2 to end
    for i in range(0, math.floor(FFT_NUM_SAMPLES/2)):
        fft_ydata.append(int(data_str_list[i+math.floor(FFT_NUM_SAMPLES/2)]))
        fft_xdata.append((i-math.ceil(FFT_NUM_SAMPLES/2))*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES) 

    # Positive Frequencies: i = 0 to FFT_NUM_SAMPLES/2
    for i in range(1, math.ceil(FFT_NUM_SAMPLES/2)):
        fft_ydata.append(int(data_str_list[i]))
        fft_xdata.append(i*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES)
    # for i, data_str in enumerate(data_str_list):
    #     if i < FFT_NUM_SAMPLES / 2:
    #         fft_ydata.append(int(data_str))
    #         fft_xdata.append(i*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES)
    #     else:
    #        fft_ydata.append(int(data_str))
    #        fft_xdata.append((i-FFT_NUM_SAMPLES)*FFT_SAMPLE_FREQ_HZ/FFT_NUM_SAMPLES) 
    
    return fft_xdata, fft_ydata

def init_v():
    ax[1].set_ylim(0, V_MAX_YLIM_MPH)
    ax[1].set_xlim(min(v_xdata), max(v_xdata))

    return v_ln,

def update_v():
    return v_ln,


def hz_to_mph(freq_hz):
    return freq_hz / 31.36

def main():

    ani_fft = FuncAnimation(
        fig, 
        update, 
        interval=100,
        init_func=init, 
        blit=True,
        cache_frame_data=False
    )
    # v_fft = FuncAnimation(
    #     fig, 
    #     update_v, 
    #     interval=100,
    #     init_func=init_v, 
    #     blit=True,
    #     cache_frame_data=False
    # )
    plt.show()

if __name__=="__main__":
    main()

