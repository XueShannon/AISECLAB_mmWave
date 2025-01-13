[Manual Book](https://www.ni.com/docs/en-US/bundle/usrp-2974-getting-started/page/overview.html#)

1. Go to [here](ni.com/info) and search NIPMDownload and download NI package management.
  
2. Use the NI package marnagement download LabVIEW Communications System Design Suite
  
3. Open the NI NXG. Now we can configure the USRP. [Labview NXG Start Video](https://www.youtube.com/watch?v=9lY_wgf4w40)

4. We can use the sample project in the template to familar with the USRP-2497.

> LabView NXG use G Web Development Software. [Getting Start with G Web](https://www.ni.com/docs/zh-CN/bundle/getting-started-with-labview-nxg/page/gslv.html)
>
> NI also has some examples in the github, which have more details.[GitHub Link](https://github.com/ni/webvi-examples)
>
> Don't know the reason why. The ip address of USRP-2497 must be set to **169.254.10.85**. Or the computer can't find the device
>
>For the example in the sample project. When you change the configuration of the USRP, you must restart the program or the change can't take any effect.

---

## Signal generating
In it's provided driver. They use **Generate Waveform** VI to generate the signal. We can modify this file to generate the signal we want.
 
 ![图片alt](./image/LabView/Conifgure_TX-Generate_Waveform.png "图片title")

In this USRP, the driver directly obtains a one-dimensional integer array as the input of iq signal, so we need to generate a one-dimensional array ourselves to generate the signal we need.
 ![图片alt](./image/LabView/IQ%20input.png "图片title")

At the same time, ni nxg software does not provide complete modules to modulate and demodulate signals like other software. It only provides fragments of many puzzles. As for complete functions, you need to build them yourself. Here I found the relevant videos modulated by labview ask. Although the versions may different, the corresponding components also contained in the labview.[ASK Modulation and Demodulation using Labview2018](https://www.youtube.com/watch?v=S5m7Y4H8jtA)

## File transmite
Despite we use labview to control the usrp to generate the signal, the programm is running on the USRP. So the data is also saved on it. So we also need to know how to upload the data from USRP to PC.

We need to install the SSH client on the USRP. Install SSH Server on the computer. For the windows, we also need to set **Firewall rule** or the ssh connection can't be established.

Then we can use scp to upload the file from usrp to PCL:

`scp source_file_path username@ip_address:destination_path`

The source file will be send to the destination_path.

If we don't config ssh key. We will need to enter password every time.

## Static IP Setting

NI also provide some method to set Static IP address:
1. [Set up IP directly on USRP](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000g1PVSAY&l=en-VI)
2. [Use your host PC](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000g0KFSAY&l=en-VI)

---


## Error List
1. Ip must set to a fix ip. When the device restart, you need to set again.
2. When you run application, you can't change any input. It will not take any effect.
