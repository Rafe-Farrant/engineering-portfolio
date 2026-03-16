import numpy as np
import matplotlib.pyplot as plt

# Time array: 2 seconds, 2000 samples
t = np.linspace(0, 2, 2000)
dt = t[1] - t[0]

# Machine parameters
shaft_speed = 12
fault_freq = 48

# Base vibration from rotating shaft
shaft_signal = 0.8 * np.sin(2 * np.pi * shaft_speed * t)

# Fault vibration and harmonics
fault_signal = (
    1.2 * np.sin(2 * np.pi * fault_freq * t) +
    0.6 * np.sin(2 * np.pi * 2 * fault_freq * t) +
    0.3 * np.sin(2 * np.pi * 3 * fault_freq * t)
)

# Random noise
noise = 0.4 * np.random.randn(len(t))

# Combined vibration signal
signal = shaft_signal + fault_signal + noise

# Save signal to CSV
data = np.column_stack((t, signal))
np.savetxt(
    "vibration-analysis/signal_data.csv",
    data,
    delimiter=",",
    header="time,signal",
    comments=""
)

# Plot time-domain signal
plt.plot(t, signal)
plt.title("Simulated Machine Vibration Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.savefig("vibration-analysis/noisy_signal.png")
plt.clf()

# Perform FFT
fft_values = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), dt)

# Keep only positive frequencies
positive_mask = frequencies > 0
frequencies = frequencies[positive_mask]
fft_magnitude = np.abs(fft_values[positive_mask])

# Peak detection
threshold = max(fft_magnitude) * 0.15
peak_indices = np.where(fft_magnitude > threshold)[0]

peak_frequencies = frequencies[peak_indices]
peak_magnitudes = fft_magnitude[peak_indices]

print("Detected vibration frequencies:")
for freq in peak_frequencies:
    print(f"{freq:.2f} Hz")

# Plot FFT spectrum with labelled peaks
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
plt.savefig("vibration-analysis/frequency_spectrum.png")
print("Saved plot as vibration-analysis/frequency_spectrum.png")