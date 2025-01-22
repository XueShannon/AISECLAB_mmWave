# Frequency Modulated Continuous Wave Radar Implementaion in GNURadio


### GNU-Radio Graph
![GNURADIO Graph](images/FMCW.png)

### Blocks Information

1. Signal Source
    - **Sample Rate:** 25 MHz 
    - **Waveform:** Saw Tooth – Generates a linear frequency sweep for the VCO, essential for FMCW radar operation.
    - **Frequency:** 1 kHz – Sets frequency(inverse of chirp_duration) for the FMCW.
    - **Amplitude:** 1 – Strength to control Chirp Bandwidth.
    
2. Voltage Controlled Oscillation
    - **Sensitivity :** 12.5664M (rad/sec/V) = (2Mhz). This forms the chirp bandwidth necessary for range resolution and calculations related to FMCW.

    Modulates the the sinoid frequency based on the amplitude from Sawtooth Frequency.

3. Multiply Conjugate
    
    This block takes the conjugate of the transmitted signal (from the VCO) and multiplies it with the received signal, producing a beat frequency signal. This signal represents the frequency difference (beat frequency) between the transmitted and received signals, which is proportional to the range of the target.

4. USRP Settings
    - **Center Freq :** 2.8GHz (Converted to 28Ghz by UDbox)
    - **Bandwidth :** 100Mhz



### Signal Processing.

