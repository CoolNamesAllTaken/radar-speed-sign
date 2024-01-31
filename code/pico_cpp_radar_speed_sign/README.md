# Overview

This folder includes code used for programming the Pi Pico radar speed sign using C++ and the Pico SDK, which enables more advanced functionarlity than can be achieved when programming with MicroPython.

Compilation is done in the included docker environment, and debugging is currently set up to work with a J-Link debugger peripheral via the J-Link GDB Server application.

# Getting Started

1. Initialize git submodules with `git submodule update --recursive --remote`.
2. Build the development docker container with `docker build -t pico_cpp_radar_speed_sign .` from this folder.

### Run the Docker Container

`docker compose up`