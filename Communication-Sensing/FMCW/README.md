# Frequency Modulated Continuous Wave Radar Implementaion in GNURadio


### GNU-Radio Graph
![GNURADIO Graph](images/FMCW.png)

### Blocks Information

1. Signal Source
    - **Sample Rate:** 1 MHz 
    - Waveform: Saw Tooth – Generates a linear frequency sweep for the VCO, essential for FMCW radar operation.
    - **Frequency:** 1 kHz – Sets the rate of frequency modulation.
    - **Amplitude:** 1 – Provides enough strength to control the VCO’s frequency shift.
    
2. Voltage Controlled Oscillation
    - **Sensitivity (2\*pi\*samp_rate):** 6.28318×10<sup>4</sup> (rad/sec/V).

    Modulates the Sawtooth Frequency.

3. Hilbert Filter
    
    Applies a 64-tap FIR filter to create an analytic signal, which helps in extracting the instantaneous frequency and phase information needed for range measurements in radar.

4. Low Pass Filter
    - **Cutoff Frequency:** 20 kHz – Filters out frequencies above 20 kHz, focusing on the beat frequency range.
    - **Transition Width:** 5 kHz – Defines the roll-off width, balancing sharpness and filter stability.

5. Multiply Conjugate
    
    This block takes the conjugate of the transmitted signal (from the VCO) and multiplies it with the received signal, producing a beat frequency signal. This signal represents the frequency difference (beat frequency) between the transmitted and received signals, which is proportional to the range of the target.

6. USRP Settings
    - **Center Freq :** 2.8GHz (Converted to 28Ghz by UDbox)
    - **Bandwidth :** 100Mhz
