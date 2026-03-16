import matplotlib
matplotlib.use('Agg')

"""
Day 11 - Vibration Analysis: UART Receiver + FFT Pipeline
==========================================================
Reads accelerometer data streamed from STM32 over UART.
Expected format per line:  timestamp_ms,ax,ay,az
  e.g.  1024,0.012,-0.003,9.814

Falls back to SIMULATED data if the serial port is unavailable,
so the pipeline can be tested without hardware.

Usage:
  python day11_uart_receiver.py                  # simulated mode
  python day11_uart_receiver.py --port COM3      # Windows
  python day11_uart_receiver.py --port /dev/ttyACM0  # Linux/Mac
  python day11_uart_receiver.py --port /dev/ttyACM0 --baud 115200 --axis z
"""

import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# ── Try to import pyserial (optional) ────────────────────────────────────────
try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False


# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

SAMPLE_RATE      = 1000      # Hz — must match STM32 sampling rate
BUFFER_SECONDS   = 2         # seconds of data to hold in buffer
FFT_THRESHOLD    = 0.05      # minimum normalised amplitude to label a peak
UPDATE_INTERVAL  = 500       # ms between plot refreshes

# Simulated signal parameters (used when no serial port is connected)
SIM_FREQS        = [12, 48, 96]   # Hz  (shaft, fault, 2nd harmonic)
SIM_AMPS         = [1.0, 0.5, 0.25]
SIM_NOISE        = 0.15


# ═════════════════════════════════════════════════════════════════════════════
# SIGNAL GENERATION (simulation fallback)
# ═════════════════════════════════════════════════════════════════════════════

def generate_simulated_sample(t: float) -> float:
    """Return one simulated accelerometer sample at time t (seconds)."""
    signal = sum(
        A * np.sin(2 * np.pi * f * t)
        for f, A in zip(SIM_FREQS, SIM_AMPS)
    )
    signal += np.random.normal(0, SIM_NOISE)
    return signal


# ═════════════════════════════════════════════════════════════════════════════
# UART PARSING
# ═════════════════════════════════════════════════════════════════════════════

def parse_line(line: str, axis: str) -> float | None:
    """
    Parse one CSV line from the STM32.
    Expected format:  timestamp_ms,ax,ay,az
    Returns the requested axis value, or None if the line is malformed.
    """
    axis_map = {"x": 1, "y": 2, "z": 3}
    try:
        parts = line.strip().split(",")
        if len(parts) < 4:
            return None
        idx = axis_map.get(axis.lower(), 3)   # default to Z (vertical)
        return float(parts[idx])
    except (ValueError, IndexError):
        return None


# ═════════════════════════════════════════════════════════════════════════════
# FFT ANALYSIS  (reused from Days 6-8)
# ═════════════════════════════════════════════════════════════════════════════

def run_fft(buffer: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Return positive-frequency bins and their normalised magnitudes."""
    n = len(buffer)
    windowed = buffer * np.hanning(n)          # Hann window reduces spectral leakage
    fft_vals  = np.fft.rfft(windowed)
    freqs     = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    magnitude = np.abs(fft_vals) / n
    magnitude[1:] *= 2                         # single-sided correction
    return freqs, magnitude


def detect_peaks(freqs: np.ndarray, magnitude: np.ndarray,
                 threshold: float) -> list[tuple[float, float]]:
    """Return (frequency, amplitude) pairs above the threshold."""
    norm = magnitude / magnitude.max() if magnitude.max() > 0 else magnitude
    peaks = []
    for i in range(1, len(norm) - 1):
        if norm[i] > threshold and norm[i] >= norm[i-1] and norm[i] >= norm[i+1]:
            peaks.append((freqs[i], magnitude[i]))
    peaks.sort(key=lambda p: p[1], reverse=True)
    return peaks[:10]   # top 10 peaks


# ═════════════════════════════════════════════════════════════════════════════
# LIVE PLOT
# ═════════════════════════════════════════════════════════════════════════════

class LivePlot:
    def __init__(self, sample_rate: int, buffer_size: int, axis: str, mode: str):
        self.sample_rate = sample_rate
        self.axis        = axis.upper()
        self.mode        = mode
        self.buffer      = deque(maxlen=buffer_size)

        # Pre-fill with zeros so the plot starts immediately
        self.buffer.extend([0.0] * buffer_size)

        self.fig, (self.ax_time, self.ax_freq) = plt.subplots(
            2, 1, figsize=(12, 7), facecolor="#0f0f0f"
        )
        self.fig.suptitle(
            f"Vibration Analysis — Live UART Stream  [{mode}]",
            color="#e0e0e0", fontsize=13, fontweight="bold"
        )
        self._style_axes()
        self._init_lines()

    def _style_axes(self):
        for ax, title in zip(
            [self.ax_time, self.ax_freq],
            [f"Time Domain  (Axis {self.axis})", "Frequency Spectrum (FFT)"]
        ):
            ax.set_facecolor("#1a1a2e")
            ax.tick_params(colors="#aaaaaa")
            ax.spines[:].set_color("#333355")
            ax.set_title(title, color="#ccccee", fontsize=10)
            ax.grid(True, color="#222244", linewidth=0.5)

        self.ax_time.set_xlabel("Time (s)", color="#888888")
        self.ax_time.set_ylabel("Acceleration (g)", color="#888888")
        self.ax_freq.set_xlabel("Frequency (Hz)", color="#888888")
        self.ax_freq.set_ylabel("Amplitude", color="#888888")

    def _init_lines(self):
        buf_size  = self.buffer.maxlen
        t_axis    = np.linspace(-buf_size / self.sample_rate, 0, buf_size)
        self.line_time, = self.ax_time.plot(
            t_axis, np.zeros(buf_size), color="#00d4ff", linewidth=0.8
        )
        self.line_freq, = self.ax_freq.plot([], [], color="#ff6b35", linewidth=1.2)
        self.peak_labels = []
        plt.tight_layout(rect=[0, 0, 1, 0.95])

    def update(self, new_sample: float):
        """Add a sample and refresh the plot."""
        self.buffer.append(new_sample)
        arr = np.array(self.buffer)

        # ── Time domain ──────────────────────────────────────────────────────
        buf_size = self.buffer.maxlen
        t_axis   = np.linspace(-buf_size / self.sample_rate, 0, buf_size)
        self.line_time.set_ydata(arr)
        self.line_time.set_xdata(t_axis)
        self.ax_time.relim()
        self.ax_time.autoscale_view()

        # ── FFT ──────────────────────────────────────────────────────────────
        freqs, magnitude = run_fft(arr, self.sample_rate)
        self.line_freq.set_xdata(freqs)
        self.line_freq.set_ydata(magnitude)
        self.ax_freq.relim()
        self.ax_freq.autoscale_view()

        # ── Peak labels ───────────────────────────────────────────────────────
        for lbl in self.peak_labels:
            lbl.remove()
        self.peak_labels.clear()

        peaks = detect_peaks(freqs, magnitude, FFT_THRESHOLD)
        for f, a in peaks:
            lbl = self.ax_freq.annotate(
                f"{f:.1f} Hz",
                xy=(f, a),
                xytext=(0, 8),
                textcoords="offset points",
                fontsize=7,
                color="#ffdd57",
                ha="center",
            )
            self.peak_labels.append(lbl)



# ═════════════════════════════════════════════════════════════════════════════
# DATA SOURCE CLASSES
# ═════════════════════════════════════════════════════════════════════════════

class SimulatedSource:
    """Generates synthetic vibration samples in real time."""
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self._t          = 0.0
        self._dt         = 1.0 / sample_rate

    def read_sample(self) -> float:
        val    = generate_simulated_sample(self._t)
        self._t += self._dt
        return val

    def close(self):
        pass


class UARTSource:
    """Reads samples from a serial port."""
    def __init__(self, port: str, baud: int, axis: str):
        self.axis = axis
        self.ser  = serial.Serial(port, baudrate=baud, timeout=1)
        print(f"[UART] Connected to {port} @ {baud} baud")

    def read_sample(self) -> float | None:
        try:
            raw  = self.ser.readline().decode("utf-8", errors="ignore")
            return parse_line(raw, self.axis)
        except Exception as e:
            print(f"[UART] Read error: {e}")
            return None

    def close(self):
        self.ser.close()
        print("[UART] Port closed.")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Day 11 — UART Vibration Receiver")
    parser.add_argument("--port",  type=str,   default=None,        help="Serial port (e.g. COM3 or /dev/ttyACM0)")
    parser.add_argument("--baud",  type=int,   default=115200,      help="Baud rate (default 115200)")
    parser.add_argument("--axis",  type=str,   default="z",         help="Accelerometer axis to analyse: x, y, or z")
    parser.add_argument("--rate",  type=int,   default=SAMPLE_RATE, help="Sample rate in Hz (must match STM32)")
    args = parser.parse_args()

    # ── Choose data source ────────────────────────────────────────────────────
    if args.port and SERIAL_AVAILABLE:
        try:
            source = UARTSource(args.port, args.baud, args.axis)
            mode   = f"UART  {args.port}"
        except Exception as e:
            print(f"[WARN] Could not open {args.port}: {e}")
            print("[WARN] Falling back to simulated data.")
            source = SimulatedSource(args.rate)
            mode   = "SIMULATED"
    elif args.port and not SERIAL_AVAILABLE:
        print("[WARN] pyserial not installed. Run:  pip install pyserial")
        print("[WARN] Falling back to simulated data.")
        source = SimulatedSource(args.rate)
        mode   = "SIMULATED"
    else:
        print("[INFO] No port specified — running in simulated mode.")
        source = SimulatedSource(args.rate)
        mode   = "SIMULATED"

    # ── Set up plot ───────────────────────────────────────────────────────────
    buffer_size = args.rate * BUFFER_SECONDS
    plot        = LivePlot(args.rate, buffer_size, args.axis, mode)

    # ── Animation loop ────────────────────────────────────────────────────────
    samples_per_update = max(1, args.rate * UPDATE_INTERVAL // 1000)

    def animate(_frame):
        for _ in range(samples_per_update):
            sample = source.read_sample()
            if sample is not None:
                plot.update(sample)
        # Throttle simulation to real time
        if isinstance(source, SimulatedSource):
            time.sleep(samples_per_update / args.rate)

    ani = animation.FuncAnimation(
        plot.fig,
        animate,
        interval=UPDATE_INTERVAL,
        cache_frame_data=False,
    )

    try:
        # Fill the buffer with simulated data before saving
        buffer_size = args.rate * BUFFER_SECONDS
        for _ in range(buffer_size):
            sample = source.read_sample()
            if sample is not None:
                plot.update(sample)
        plt.savefig('day11_output.png')
        print("[INFO] Saved day11_output.png")
    finally:
        source.close()
        print("[INFO] Done.")


if __name__ == "__main__":
    main()