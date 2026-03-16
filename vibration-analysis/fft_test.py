import numpy as np
import matplotlib.pyplot as plt


def generate_signal():
    """Generate a simulated machine vibration signal."""
    t = np.linspace(0, 2, 2000)
    dt = t[1] - t[0]

    shaft_speed = 12
    fault_freq = 48

    shaft_signal = 0.8 * np.sin(2 * np.pi * shaft_speed * t)

    fault_signal = (
        1.2 * np.sin(2 * np.pi * fault_freq * t) +
        0.6 * np.sin(2 * np.pi * 2 * fault_freq * t) +
        0.3 * np.sin(2 * np.pi * 3 * fault_freq * t)
    )

    noise = 0.4 * np.random.randn(len(t))
    signal = shaft_signal + fault_signal + noise

    return t, dt, signal


def save_signal_to_csv(t, signal, filename):
    """Save signal data to CSV."""
    data = np.column_stack((t, signal))
    np.savetxt(
        filename,
        data,
        delimiter=",",
        header="time,signal",
        comments=""
    )


def plot_time_signal(t, signal, filename):
    """Plot and save the time-domain signal."""
    plt.plot(t, signal)
    plt.title("Simulated Machine Vibration Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.savefig(filename)
    plt.clf()


def perform_fft(signal, dt):
    """Perform FFT and return positive frequencies and magnitudes."""
    fft_values = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), dt)

    positive_mask = frequencies > 0
    frequencies = frequencies[positive_mask]
    fft_magnitude = np.abs(fft_values[positive_mask])

    return frequencies, fft_magnitude


def detect_peaks(frequencies, fft_magnitude, threshold_ratio=0.15):
    """Detect peaks above a threshold."""
    threshold = max(fft_magnitude) * threshold_ratio
    peak_indices = np.where(fft_magnitude > threshold)[0]

    peak_frequencies = frequencies[peak_indices]
    peak_magnitudes = fft_magnitude[peak_indices]

    return peak_frequencies, peak_magnitudes


def plot_frequency_spectrum(frequencies, fft_magnitude, peak_frequencies, peak_magnitudes, filename):
    """Plot and save the FFT spectrum with labelled peaks."""
    plt.plot(frequencies, fft_magnitude, label="FFT Spectrum")
    plt.scatter(peak_frequencies, peak_magnitudes, marker="x", label="Detected Peaks")

    for freq, mag in zip(peak_frequencies, peak_magnitudes):
        plt.text(freq, mag, f"{freq:.1f} Hz", fontsize=8)

    plt.title("Machine Vibration Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 160)
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.clf()


def main():
    """Run the vibration analysis pipeline."""
    t, dt, signal = generate_signal()

    save_signal_to_csv(t, signal, "vibration-analysis/signal_data.csv")
    plot_time_signal(t, signal, "vibration-analysis/noisy_signal.png")

    frequencies, fft_magnitude = perform_fft(signal, dt)
    peak_frequencies, peak_magnitudes = detect_peaks(frequencies, fft_magnitude)

    print("Detected vibration frequencies:")
    for freq in peak_frequencies:
        print(f"{freq:.2f} Hz")

    plot_frequency_spectrum(
        frequencies,
        fft_magnitude,
        peak_frequencies,
        peak_magnitudes,
        "vibration-analysis/frequency_spectrum.png"
    )

    print("Saved plot as vibration-analysis/frequency_spectrum.png")


if __name__ == "__main__":
    main()