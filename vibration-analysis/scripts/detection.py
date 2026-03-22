"""
detection.py
============
Structural change detection rule and threshold logic.
Compares current frequency against baseline to flag anomalies.
"""

import numpy as np


def calculate_frequency_shift(baseline_freq: float,
                               current_freq: float) -> tuple[float, float]:
    """
    Calculate the frequency shift between baseline and current measurement.
    Returns shift in Hz and shift as a percentage of baseline.
    """
    shift_hz = abs(baseline_freq - current_freq)
    shift_pct = (shift_hz / baseline_freq) * 100
    return shift_hz, shift_pct


def detect_structural_change(baseline_freq: float, current_freq: float,
                              baseline_std: float,
                              multiplier: float = 3.0) -> tuple[bool, float, float]:
    """
    Flag a structural change if frequency shift exceeds threshold.
    Threshold is set at multiplier × baseline standard deviation.
    Returns detection flag, shift in Hz, and shift as a percentage.
    """
    threshold = multiplier * baseline_std
    shift_hz, shift_pct = calculate_frequency_shift(baseline_freq, current_freq)
    detected = shift_hz > threshold
    return detected, shift_hz, shift_pct


def summarise_detection(baseline_freq: float, current_freq: float,
                        baseline_std: float) -> None:
    """
    Print a summary of the detection result to the console.
    Shows baseline, current frequency, shift, and pass/fail status.
    """
    detected, shift_hz, shift_pct = detect_structural_change(
        baseline_freq, current_freq, baseline_std
    )
    print(f"Baseline frequency : {baseline_freq:.2f} Hz")
    print(f"Current frequency  : {current_freq:.2f} Hz")
    print(f"Shift              : {shift_hz:.2f} Hz ({shift_pct:.1f}%)")
    print(f"Detection flag     : {'CHANGE DETECTED' if detected else 'No change'}")