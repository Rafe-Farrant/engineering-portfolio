"""
filters.py
==========
Low-pass and band-pass filter implementations for vibration signal processing.
All filtering for the project goes through this module.
"""

import numpy as np
from scipy import signal


def low_pass_filter(data: np.ndarray, cutoff: float, sample_rate: float,
                    order: int = 4) -> np.ndarray:
    """
    Apply a Butterworth low-pass filter to a signal.
    Removes high-frequency noise above the cutoff frequency (Hz).
    Returns the filtered signal array.
    """
    nyquist = sample_rate / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype="low", analog=False)
    return signal.filtfilt(b, a, data)


def band_pass_filter(data: np.ndarray, low_cutoff: float, high_cutoff: float,
                     sample_rate: float, order: int = 4) -> np.ndarray:
    """
    Apply a Butterworth band-pass filter to a signal.
    Isolates frequencies between low_cutoff and high_cutoff (Hz).
    Returns the filtered signal array.
    """
    nyquist = sample_rate / 2
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    b, a = signal.butter(order, [low, high], btype="band", analog=False)
    return signal.filtfilt(b, a, data)