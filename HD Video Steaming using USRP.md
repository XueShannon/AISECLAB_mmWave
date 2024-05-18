# System Requirements
## Hardware Requirements
**USRP-2974**\
**UD Box $\times$ 2**\
**BBox Lite**\
**BBox One**
## Software Requirements
**NI LabVIEW NXG 4.0**\
**TMXLAB Kit**
## Software Installation
### LabVIEW NXG
In order to download and install LabVIEW NXG it is necessary to first have NI Package Manager installed on the computer. There are two ways to get LabVIEW NXG installed:\
**1.Use Download LabVIEW NXG link:**\
This option will first automatically install NI Package Manager, and will automatically select LabVIEW NXG to install.\
**2.Download NI Package Manager and manually select LabVIEW NXG to be installed:**\
Download NI Package Manager and select LabVIEW NXG\
*USRP-2974 only support LabVIEW NXG version 4.0, USRP 2974 setup see USRP.md*
### LTE Application Frame
Download link: https://www.ni.com/en/support/downloads/software-products/download.labview-communications-lte-application-framework.html#330619, the latest version is v19.5\
This is an add-on of LabVIEW NXG
### TMXLAB Kit
Download link:https://tmytek.com/resources/software, the latest version is v3.9.4, this is the software that controls the Tmytek equipments(UD Box, BBox Lite, BBox One)\
*Setup see file TXMLAB KIT.md*
# Hardware Setup
Equipment connection see picture below\
![IMG_1723](https://github.com/XueShannon/AISECLAB_mmWave/assets/82636876/00526ad6-aea5-48de-be89-144eed236af2)
(1. USRP-2974 &emsp;2.UD Box &emsp;3.BBox Lite &emsp;4.BBox One &emsp;5. UD Box)\
Output port of USRP-2974 should be **RF0/TX1**, this is connect to UD Box at it's **IF** port. For both UD Box, the **RF** port is connect to BBox Lite/BBox One using Cable N9927-60024. The input port of USRP-2974 that connect to the UD Box after the loop should be **RF1/RX2**.
# Software Setup
## LabVIEW
Afer success connection between the PC host and USRP-294, the hardware is able to be added in LabVIEW using SystemDesigner in each project(USRP-2974 couldn't be added through MAX). IF not able to be directly match using hostname, click the "add hardware" in the menu and manually add the equipment using it's IP address.\
Within that project, open the LabVIEW top-level host VI in the downlink-only variant, DL Host.gvi in DL Host.gcomp. **Change the designer view of the VI to DL RT Controller**\
Click the Run button on the LabVIEW host VI. If successful, the FPGAReady indicator lights.\
Set eNB TX Frequency and  UE RX Frequency to 2 GHz which would match the frequency later adjust by the UD Box.\
Enable the eNB Transmitter, which implements a DL TX, by setting the switch control to On. If successful, the eNB TX Active indicator lights.\
Enable the UE Receiver, implementing a DL RX, by setting the Switch control to On. If successful, the UE RX Active indicator lights.\
The successful running VI file should look like this:\
![Success VI](https://github.com/XueShannon/AISECLAB_mmWave/assets/82636876/44ec4b88-10c1-4243-a99c-66d2465295cb)
(The output of the PDSCH constellation is not clean enough, due to the noise inside the lab. In the given example of the guide manual, the ideal SNR value should reach 30+)
## TMXLAB Kit
After installe the antenna for BBox Lite and BBox One, the angle of the antenna for both device is able to adjust freely. To aligh the frequency value for UD Box and USRP-2974, the current value for both UD Box should be set to :**RF= 28000 MHz**&emsp;**IF= 2000MHz**&emsp;**LO= 30000 MHz**. Correspond to the setup, change the Mode for BBox Lite and BBox One. According to the hardware setup above, the output is connect to BBox One, thus the mode should be changed to **RX** while the BBox Lite should be in **TX**
# Performe Video Streaming
## Needed Command
## Performance regarding BBox Lite and BBox One
