import numpy as np
import matplotlib.pyplot as plt

# Time array: 0 to 1 second, 1000 samples
t = np.linspace(0, 1, 1000)
dt = t[1] - t[0]

# Generate two sine wave components
signal1 = np.sin(2 * np.pi * 5 * t)
signal2 = np.sin(2 * np.pi * 20 * t)

# Combine into one signal
signal = signal1 + signal2

# Perform FFT
fft_values = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), dt)

# Keep only positive frequencies
positive_mask = frequencies > 0
frequencies = frequencies[positive_mask]
fft_magnitude = np.abs(fft_values[positive_mask])

# Find the two largest peaks
peak_indices = np.argsort(fft_magnitude)[-2:]
dominant_frequencies = frequencies[peak_indices]

print("Dominant frequencies detected:")
for freq in sorted(dominant_frequencies):
    print(f"{freq:.2f} Hz")

# Plot frequency spectrum
plt.plot(frequencies, fft_magnitude)
plt.title("Frequency Spectrum of Simulated Vibration Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.savefig("vibration-analysis/frequency_spectrum.png")
print("Saved plot as vibration-analysis/frequency_spectrum.png")