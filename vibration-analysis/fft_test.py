import numpy as np
import matplotlib.pyplot as plt

# Time array: 0 to 1 second, 1000 samples
t = np.linspace(0, 1, 1000)
dt = t[1] - t[0]

# Generate two sine wave components
signal1 = np.sin(2 * np.pi * 5 * t)
signal2 = np.sin(2 * np.pi * 20 * t)

# Combine signals
clean_signal = signal1 + signal2

# Add random noise
noise = 0.5 * np.random.randn(len(t))
signal = clean_signal + noise

# Plot noisy signal
plt.plot(t, signal)
plt.title("Noisy Vibration Signal (Time Domain)")
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

# Find peaks above threshold
threshold = max(fft_magnitude) * 0.3
peaks = frequencies[fft_magnitude > threshold]

print("Detected frequency components:")
for freq in peaks[:5]:
    print(f"{freq:.2f} Hz")

# Plot frequency spectrum
plt.plot(frequencies, fft_magnitude)
plt.title("Frequency Spectrum of Simulated Vibration Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.savefig("vibration-analysis/frequency_spectrum.png")
print("Saved plot as vibration-analysis/frequency_spectrum.png")