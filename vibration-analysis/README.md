# Structural Vibration Monitoring System

A cantilever beam structural health monitoring system using an STM32 NUCLEO-G071RB, MPU-6050 accelerometer, and Python FFT analysis pipeline to detect structural changes via frequency shift and damping ratio estimation.

---

## Problem Statement

Structural damage in beams and other mechanical components causes measurable shifts in natural frequency and damping ratio. This project builds a low-cost sensing system that can detect these shifts automatically, demonstrating the core principles of structural health monitoring (SHM) used in aerospace, civil, and mechanical engineering.

---

## System Architecture

MPU-6050 (I2C) → STM32 NUCLEO-G071RB → UART (115200 baud) → Python Pipeline
                                                                      ↓
                                                              data_io.py (load/save)
                                                                      ↓
                                                              filters.py (low-pass / band-pass)
                                                                      ↓
                                                              fft_analysis.py (FFT + peak detection)
                                                                      ↓
                                                              detection.py (structural change flag)

---

## Key Results

*To be filled in on Day 53 with real experimental data.*

- Baseline natural frequency: X.X ± X.X Hz
- Frequency shift (mass addition): X.X Hz (X.X%)
- Frequency shift (loosened clamp): X.X Hz (X.X%)
- Damping ratio baseline: ζ = X.XXX
- Detection accuracy: ±X%

---

## Repository Structure

vibration-analysis/
├── data/
│   ├── baseline/          # Baseline beam measurements (5 runs)
│   ├── mass_added/        # Mass addition structural change (5 runs)
│   └── loose_clamp/       # Loosened clamp structural change (5 runs)
├── scripts/
│   ├── data_io.py         # CSV loading and saving
│   ├── filters.py         # Low-pass and band-pass filters
│   ├── fft_analysis.py    # FFT computation and peak detection
│   └── detection.py       # Structural change detection logic
├── figures/
│   ├── baseline_spectrum.png
│   ├── comparison_spectrum.png
│   └── damping_decay.png
└── docs/
    ├── success_criteria.md
    ├── cv_bullet_draft.md
    └── progress_log.md

---

## How to Run

Simulated mode (no hardware needed):
python scripts/day11_uart_receiver.py

Live hardware mode:
python scripts/day11_uart_receiver.py --port /dev/ttyACM0 --baud 115200 --axis z

---

## What I Learned / Limitations

*To be completed at end of project (Day 53).*

---

## Hardware

- STM32 NUCLEO-G071RB microcontroller
- MPU-6050 6-axis IMU (accelerometer + gyroscope)
- Cantilever beam (metal ruler, dimensions TBC)
- Sampling rate: 125 Hz

