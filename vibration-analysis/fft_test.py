import numpy as np
import matplotlib.pyplot as plt

# Generate time array
t = np.linspace(0, 1, 1000)
dt = t[1] - t[0]

# Generate signal
signal1 = np.sin(2 * np.pi * 5 * t)
signal2 = np.sin(2 * np.pi * 20 * t)
noise = 0.5 * np.random.randn(len(t))

signal = signal1 + signal2 + noise

# Save to CSV
data = np.column_stack((t, signal))
np.savetxt("vibration-analysis/signal_data.csv", data,
           delimiter=",", header="time,signal", comments="")

# Plot time signal
plt.plot(t, signal)
plt.title("Simulated Vibration Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.savefig("vibration-analysis/noisy_signal.png")
plt.clf()

# FFT
fft_values = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), dt)

positive_mask = frequencies > 0
frequencies = frequencies[positive_mask]
fft_magnitude = np.abs(fft_values[positive_mask])

threshold = max(fft_magnitude) * 0.3
peaks = frequencies[fft_magnitude > threshold]

print("Detected frequency components:")
for freq in peaks[:5]:
    print(f"{freq:.2f} Hz")

plt.plot(frequencies, fft_magnitude)
plt.title("Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.savefig("vibration-analysis/frequency_spectrum.png")