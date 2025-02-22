# **5G NR Waveform Configuration for QPSK**
## **General Settings**
- **Duplex Mode:** TDD
- **Carrier Frequency:** 28 GHz (Upconverted from 2.8 GHz)
- **Channel Bandwidth:** 20 MHz
- **Subcarrier Spacing (SCS):** 30 kHz
- **Number of Resource Blocks (NRB):** 51
- **Subframes:** 10
- **Layers:** 1
- **Cell Identity:** 1
- **RNTI:** 1

## **SSB/SIB1 Settings**
- **SSB Power:** 6 dB
- **SSB Transmitted Blocks:** `[1 1 0 0]`
- **SIB1:** Disabled

## **PDSCH Settings**
- **Modulation:** QPSK / 16QAM / 64QAM
- **Power:** 3 dB
- **Slot Allocation:** `[1 2 3 4 5 6 10 11 12 13 14 15 16]`
- **Code Rate:** 0.3008
- **PT-RS:** Enabled (Power: 3 dB)

## **DM-RS Settings**
- **DM-RS Configuration Type:** 1
- **DM-RS Power:** 3 dB
- **Additional DM-RS Positions:** 2

## **CSI-RS Settings**
- **Enabled:** Yes
- **Power:** 3 dB
- **Type:** NZP (Non-Zero Power)
- **Periodicity:** 1 Slot
- **RB Coverage:** 51 RBs (Full Bandwidth)
