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

## Tools Used
Python
NumPy
Matplotlib

## Next Step
Use FFT to detect the frequencies present in the signal.
