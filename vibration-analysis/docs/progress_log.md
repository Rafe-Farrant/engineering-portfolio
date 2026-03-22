# Vibration Analysis Project

## Objective
Learn how to simulate vibration signals in Python before analysing real accelerometer data.

## Day 2 Progress
- Generated sine wave signals using Python
- Combined multiple frequencies
- Visualised signals using Matplotlib

## Day 3 Progress
- Applied FFT to a simulated vibration signal
- Converted the signal from the time domain to the frequency domain
- Detected dominant frequencies at 5 Hz and 20 Hz
- Plotted the frequency spectrum

## Day 4 Progress
Added random noise to the simulated vibration signal to better represent real sensor data.

Used FFT to analyse the noisy signal in the frequency domain.

Successfully detected the main frequency components near 5 Hz and 20 Hz despite the added noise.

Generated:
- noisy_signal.png
- frequency_spectrum.png

## Day 5 Progress

Implemented a full data pipeline for vibration analysis.

Steps:
- Generated simulated vibration signal (5 Hz + 20 Hz + noise)
- Saved the signal to a CSV file
- Loaded and analysed the signal using FFT
- Generated frequency spectrum and time-domain plots

Issues:
- Sample was too small so gave Detected frequency components:
50.00 Hz
- Issue was resolved by increased signal duration and number of sample so the FFT had sufficient resolution to identify the correct frequency components.


Output files generated:
- signal_data.csv
- noisy_signal.png
- frequency_spectrum.png

## Day 6 Progress

Simulated a rotating machine vibration signal with:
- shaft rotation frequency at 12 Hz
- fault frequency at 48 Hz
- harmonic content
- added random noise

FFT analysis detected dominant frequencies at:
- 11.99 Hz
- 47.98 Hz
- 95.95 Hz

Also found that if threshold was lowered the 3rd Harmonic at 143.93 Hz could be detected

These correspond closely to the expected shaft speed and fault harmonics.

## Day 7 Progress

Improved the FFT output by automatically detecting and labelling the dominant peaks on the frequency spectrum.

This made the results easier to interpret and more suitable for engineering reporting.

The frequency plot now shows labelled peaks corresponding to the shaft speed and fault harmonics.

## Day 8 Progress

Refactored the vibration analysis script into separate functions to improve readability and structure.

The workflow is now divided into:
- signal generation
- CSV export
- time-domain plotting
- FFT analysis
- peak detection
- spectrum plotting

This makes the project easier to maintain and closer to good engineering software practice.

## Day 9 Progress

Updated the vibration analysis pipeline so it can operate in two modes:
- simulated signal generation
- loading signal data from an external CSV file

This is an important step toward analysing real accelerometer data collected from hardware.

## Day 10 Progress

Set up STM32 development environment for the NUCLEO-G071RB.

Successfully:
- created and built STM32 firmware project
- connected to the board using ST-LINK
- flashed firmware to the target successfully

This establishes the hardware development toolchain required for future sensor integration and UART data streaming.

Issues:
- STM32 software proved difficult and microcontroller had Mbed files on that kept running despite importing of new files

## Day 11 — Python UART Receiver + FFT Pipeline
Built the Python receiver script that will accept accelerometer data streamed from the STM32 over UART.
The script has two modes:

Simulated mode — generates a synthetic vibration signal (12 Hz shaft, 48 Hz fault, harmonics) to test the pipeline without hardware
UART mode — reads real CSV data from the STM32 serial port once the hardware is connected

Ran the script in Codespaces in simulated mode and generated time domain and FFT plots with automatically labelled frequency peaks — reusing the analysis pipeline built in Days 6-8.
Also had to adapt the script for Codespaces since it can't display live Matplotlib windows, so outputs are saved as PNG files instead.
The Python side of the pipeline is now complete. When the STM32 firmware streams data tomorrow, this script just works — no changes needed


## Day 12 — STM32 Firmware: MPU-6050 I2C + UART Stream
Attempted to use STM32CubeIDE but ran into environment issues, so made the decision to switch to Keil Studio with Mbed — a browser-based IDE that's faster to set up and better suited to rapid prototyping.
Written and built firmware for the NUCLEO-G071RB that:

Initialises the MPU-6050 over I2C at 400kHz
Reads raw accelerometer data from all three axes at 125Hz
Converts raw values to g-force
Streams data as CSV over UART at 115200 baud, ready for the Python pipeline

Hardware arrives tomorrow — Day 13 will be wiring it up, flashing the firmware and testing the full end-to-end pipeline with the Python receiver built on Day 11.

## Tools Used
Python
NumPy
Matplotlib
