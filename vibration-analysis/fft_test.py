import numpy as np
import matplotlib.pyplot as plt

# Time array: 2 seconds, 2000 samples (better frequency resolution)
t = np.linspace(0, 2, 2000)
dt = t[1] - t[0]

# Machine parameters
shaft_speed = 12      # Hz (rotational speed)
fault_freq = 48       # Hz (e.g. bearing fault frequency)

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

data = np.column_stack((t, signal))
np.savetxt(
    "vibration-analysis/signal_data.csv",
    data,
    delimiter=",",
    header="time,signal",
    comments=""
)

plt.plot(t, signal)
plt.title("Simulated Machine Vibration Signal")
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

threshold = max(fft_magnitude) * 0.15
peaks = frequencies[fft_magnitude > threshold]

print("Detected vibration frequencies:")
for freq in peaks[:10]:
    print(f"{freq:.2f} Hz")

plt.plot(frequencies, fft_magnitude)
plt.title("Machine Vibration Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.savefig("vibration-analysis/frequency_spectrum.png")
print("Saved plot as vibration-analysis/frequency_spectrum.png")