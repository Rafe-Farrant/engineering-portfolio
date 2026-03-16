import numpy as np
import matplotlib.pyplot as plt

# Time array: 0 to 1 second, 1000 samples
t = np.linspace(0, 1, 1000)

# Generate two sine wave components
signal1 = np.sin(2 * np.pi * 5 * t)
signal2 = np.sin(2 * np.pi * 20 * t)

# Combine into one signal
signal = signal1 + signal2

# Plot
plt.plot(t, signal)
plt.title("Simulated Vibration Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()
