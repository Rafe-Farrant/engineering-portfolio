"""
fft_analysis.py
===============
FFT computation, peak detection, and frequency extraction.
All spectral analysis for the project goes through this module.
"""

import numpy as np


def perform_fft(signal: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Perform FFT on a signal and return positive frequencies and magnitudes.
    Applies Hann window to reduce spectral leakage.
    Returns frequency array (Hz) and magnitude array.
    """
    n = len(signal)
    windowed = signal * np.hanning(n)
    fft_values = np.fft.rfft(windowed)
    frequencies = np.fft.rfftfreq(n, d=dt)
    magnitude = np.abs(fft_values) / n
    magnitude[1:] *= 2
    return frequencies, magnitude


def detect_peaks(frequencies: np.ndarray, magnitude: np.ndarray,
                 threshold_ratio: float = 0.15) -> tuple[np.ndarray, np.ndarray]:
    """
    Detect dominant frequency peaks above a threshold.
    Threshold is set as a fraction of the maximum magnitude.
    Returns arrays of peak frequencies (Hz) and peak magnitudes.
    """
    if magnitude.max() == 0:
        return np.array([]), np.array([])

    threshold = magnitude.max() * threshold_ratio
    peak_indices = []

    for i in range(1, len(magnitude) - 1):
        if magnitude[i] > threshold and magnitude[i] >= magnitude[i-1] and magnitude[i] >= magnitude[i+1]:
            peak_indices.append(i)

    peak_indices = np.array(peak_indices)
    if len(peak_indices) == 0:
        return np.array([]), np.array([])

    return frequencies[peak_indices], magnitude[peak_indices]
