import pickle
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import godirect.gdx as gdx
import matplotlib.pyplot as plt
import numpy as np

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
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Force")
    ax.set_xlim(0, 600)  # 30 seconds at 20 Hz = 600 samples
    ax.set_ylim(0, 12)  # Adjust these limits based on expected Force values
    ax.set_title("Breathing Pattern")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Breath Pattern (Chest Force - N)")
    ax.legend()
    plt.ion()
    plt.show()
    while time.time() - time_start < 30:
        remaining_time = 30 - (time.time() - time_start)
        sys.stdout.write(f"\rRemaining time: {remaining_time:.2f} s")
        sample = gdx_device.read()
        if sample:
            force.append(sample[0])
            if isinstance(sample[1], (int, float)) and sample[1] >= 0:
                bpm.append(sample[1])
            line.set_data(np.arange(len(force)), force)
            ax.set_xlim(0, max(600, len(force)))  # Dynamically update x-axis limit
            plt.pause(0.01)
        # time.sleep(0.05)
except KeyboardInterrupt:
    print("\nForce quit")
    exit()
    
finally:
    print("\n\n************************************************************\n\n")
    print(len(bpm))
    print(bpm)
    
    print(len(force))
    # print(force)
    gdx_device.stop()
    gdx_device.close()
    plt.ioff()
    plt.close()


pattern_fft = np.fft.fft(force)
pattern_fft = np.fft.fftshift(pattern_fft)
pattern_fft_mag = np.abs(pattern_fft)
pattern_freqs = np.fft.fftfreq(len(force), 1/20)
pattern_freqs = np.fft.fftshift(pattern_freqs)

fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].plot(np.arange(len(force)), force)
ax[0].set_title("Breathing Pattern")
ax[0].set_xlabel("Samples")


mask = (pattern_freqs >= 0.1) & (pattern_freqs <= 0.5)
peak = pattern_freqs[mask][np.argmax(pattern_fft_mag[mask])]
ax[1].plot(pattern_freqs[mask], pattern_fft_mag[mask])
ax[1].plot(peak, pattern_fft_mag[mask][np.argmax(pattern_fft_mag[mask])], "ro", label=f"Breath Frequncy {peak:.4f} Hz")
ax[1].set_title("Breathing Rate")
ax[1].set_xlabel("Frequency (Hz)")
ax[1].legend()
# ax[1].set_xlim(0.2, 0.5)


fig.tight_layout()
plt.show()
plt.close()

# Save data
save = False

save = input("Do you want to save the data? (y/n): ")
if save.lower() == "n":
    exit()

num = input("Enter the number of breaths: ")
time_struct = time.localtime(time_start)

file_name = f'./RespirationBeltData/breath_pattern_{time.strftime("%d%b%H%M%S",time_struct)}_{num}_breaths.pkl'

with open(file_name, "wb") as f:
    pickle.dump(force, f)

print(f"Data saved to {file_name}")
