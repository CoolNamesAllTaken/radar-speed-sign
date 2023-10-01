# radar-speed-sign
How much zoom is too much zoom?

![Radar speed sign mounted to my wall](images/radar_speed_sign.jpg)

This is a DIY radar speed sign based on an HB100 doppler radar sensor and a cheap microcontroller (originally an Arduino Nano, now a Pi Pico). The detection range with the stock HB100 antenna is too short for reading speeds of cars, but works well for pedestrians at close range!

This repository includes firmware for both the original project, which used Arduino (C++), and the updated kit version of the project, which runs MicroPython on a Pi Pico. PCB design and fabrication files are also included. Have fun!

[Project Writeup](https://johnmcnelly.com/arduino-radar-speed-sign/)

[Electronics Kit Store Link](https://pantsforbirds.com/product/radar-speed-sign/)

## Software (Python)
Note: Radar speed sign kits ship with a Pi Pico that has been pre-flashed with MicroPython and the latest version of the Pico Radar Speed Sign firmware. Follow the instructions below for updating to new versions of the Pico Radar Speed Sign firmeware or for flashing a Pi Pico from scratch.

### Setting up MicroPython
First time setup with a blank Pi Pico? Follow [these instructions](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)!

### Updating Firmware
Firmware in the `code/pico_radar_speed_sign` directory can be uploaded to the Pi Pico using Thonny or the [Pico W-Go Extension](https://github.com/paulober/MicroPico) for VSCode. If uploading code using VSCode, open the `code/pico_radar_speed_sign` directory with VSCode in order to automatically use the settings configured in the `.vscode` directory and the `.micropico` file.

## Software (Arduino C++)
The original radar speed sign used code written in Arduino C++. This can be found in the `code/radar_speed_sign` directory, and is intended to be edited using the PlatformIO extension for VSCode.