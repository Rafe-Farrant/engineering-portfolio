"""
data_io.py
==========
Functions for loading and saving vibration signal data.
All file I/O for the project goes through this module.
"""

import numpy as np


def load_signal_from_csv(filename: str) -> tuple[np.ndarray, float, np.ndarray]:
    """
    Load time and signal data from a CSV file.
    Expects columns: time, signal.
    Returns time array, timestep dt, and signal array.
    """
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    t = data[:, 0]
    signal = data[:, 1]
    dt = t[1] - t[0]
    return t, dt, signal


def save_signal_to_csv(t: np.ndarray, signal: np.ndarray, filename: str) -> None:
    """
    Save time and signal arrays to a CSV file.
    Output columns: time, signal.
    """
    data = np.column_stack((t, signal))
    np.savetxt(
        filename,
        data,
        delimiter=",",
        header="time,signal",
        comments=""
    )