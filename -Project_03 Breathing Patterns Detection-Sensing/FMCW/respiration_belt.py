import godirect.gdx as gdx
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys

gdx_device = gdx.gdx()

gdx_device.open_ble("GDX-RB 0K600659")  # Open Respiratory Belt

gdx_device.select_sensors([1, 2])  # Force and Respiration Rate Channels
# select sensors for GDX-RB 0K600659 BLE -51
# Sensor Channels:
# 1: Force (N)
# 2: Respiration Rate (bpm)
# 4: Steps (steps)
# 5: Step Rate (spm)


gdx_device.start(period=50)  # Period in ms ie. sensor update sensitivity. 1000/50 = 20 Hz Sampling Rate

force = []
bpm = []

time_start = time.time()
try:
    while time.time() - time_start < 30:
        remaining_time = 30 - (time.time() - time_start)
        sys.stdout.write(f"\rRemaining time: {remaining_time:.2f} s")
        sample = gdx_device.read()
        if sample:
            force.append(sample[0])
            if isinstance(sample[1], (int, float)) and sample[1] >= 0:
                bpm.append(sample[1])
        # time.sleep(0.05)
except KeyboardInterrupt:
    gdx_device.stop()
    gdx_device.close()
    exit()
finally:
    print("\n\n************************************************************\n\n")
    print(len(bpm))
    print(bpm)
    print(len(force))
    # print(force)
    gdx_device.stop()
    gdx_device.close()


pattern_fft = np.fft.fft(force)
pattern_fft = np.fft.fftshift(pattern_fft)
pattern_fft_mag = np.abs(pattern_fft)
pattern_freqs = np.fft.fftfreq(len(force), 0.05)
pattern_freqs = np.fft.fftshift(pattern_freqs)

fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].plot(np.arange(len(force)), force)
ax[0].set_title("Breathing Pattern")
ax[0].set_xlabel("Samples")


mask = (pattern_freqs >= 0.2) & (pattern_freqs <= 0.5)
ax[1].plot(pattern_freqs[mask], pattern_fft_mag[mask])
ax[1].set_title("Breathing Rate")
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_xlim(0.2, 0.5)


fig.tight_layout()
plt.show()
plt.close()

# Save data
save = False

save = input("Do you want to save the data? (y/n): ")
if save.lower() == "n":
    exit()

num = input("Enter the number of breaths: ")

file_name = f'breath_pattern_{time.strftime("%d%b%H%M%S")}_{num}_breaths.pkl'

with open(file_name, "wb") as f:
    pickle.dump(force, f)

print(f"Data saved to {file_name}")
