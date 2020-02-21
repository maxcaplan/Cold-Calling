# Cold-Calling
An Electronic Literature project.


# Documentation

***Work in progress***

----

## Table of Contents
- [Materials](#Materials)
- [Build](#Build)
  * [Software](#Software)
    + [Raspbian](#Raspbian) 
      * [Headless](#Headless)
      * [Desktop](#Desktop)
    + [Python and Packages](#Python)
  * [Wiring](#Wiring)
- [Notes](#Notes)

----

## Materials:

* Raspberry Pi 3
* Raspberry Pi graded PSU 
* Micro SD Card (About 8gb)
* Rotary Phone <sup>1</sup>
* Assorted Wires
* Soldering Iron
* Momentary Switch <sup>2</sup>
* 3.5mm TRRS Audio Plug <sup>3</sup>


>1. It is likely that your phones internals will vary from other models, however the phone should work as long as all the electronics are easily accessible and the dial uses >electric pulses to input numbers. This will be covered more thoroughly later

>2. Depending on the internals of your particular phone you may be able to use the built in switch for the handset hook/cradle, otherwise you will have to >mount your own switch to the inside of the phone that gets pressed by the handset hook/cradle

>3. The TRRS plug is used to connect to the wires of the handset speaker so that it can be plugged directly into the Raspberry Pi's audio jack. This can also be salvaged from an old pair of headphones or an aux cable. Alternatively the speaker wires can be soldered directly to the audio jack pins on the >underside of the Pi's PCB 

---

# Build:

## Software

The first step is to load the Raspberry Pi with all the required software, starting with the OS. <br>
For this project Raspbian Lite was used in a headless configuration, this means the OS has no GUI and is only interfaced with through the command line. If you are not comfortable with the linux terminal or prefer working in a graphical environment than you can use the normal desktop configuration of Raspbian on your Raspberry Pi, however, this will require an external monitor and keyboard.

### Raspbian:

#### Headless
First, download a copy of the latest version of Raspbian Lite [here](https://www.raspberrypi.org/downloads/raspbian/). <br><br> 

Insert the Micro SD Card into your computer and write the Raspbian OS image using a programme such as [BalenaEtcher](https://www.balena.io/etcher/). _Note: this may require you to extract the contents of the downloaded zip file._ <br> <br>

Next we need to enable SSH (Secure Shell) for Raspbian so we can connect to the Raspberry Pi over the network. To do this, go into the root of the Micro SD Card that you wrote Raspbian to and add a new _empty_ file called `ssh` without any file extension. <br><br>

After that we need to configure wifi. To do this, create a new file in the root of the Micro SD Card called `wpa_supplicant.conf`. Paste the following into this file:

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```

make sure to replace NETWORK-NAME and NETWORK-PASSWORD with the name and password of your wifi respectively <br><br>

Now you can remove the Micro SD Card from your computer and put it into the Raspberry Pi. Plug the Raspberry Pi into the PSU, this should cause it to automatically power on. _Note: at this step it is useful to use an external monitor to make sure the Raspberry Pi boots properly the first time turning it on_ <br><br>

Next we need the local IP address of the Raspberry Pi so we can use SSH to interface with it over the network. There are two ways to do this. <br>
The first way requires and external monitor and keyboard plugged into the Raspberry Pi. When you power on the Raspberry Pi, you should be prompted to login, the default credentials on a new install is:

```
Username: pi
Password: raspberry
```

Once you are logged in, run the command `ifconfig`, this should give a similar output to the following:

```bash
eno1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 34:e6:d7:10:60:5c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 20  memory 0xf7400000-f7420000  

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 9367  bytes 922205 (922.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 9367  bytes 922205 (922.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlp2s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.10.11.203  netmask 255.255.248.0  broadcast 10.10.15.255
        inet6 fe80::162:ffe1:31b4:89b1  prefixlen 64  scopeid 0x20<link>
        ether 80:19:34:e4:86:f8  txqueuelen 1000  (Ethernet)
        RX packets 858851  bytes 1072154569 (1.0 GB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 293742  bytes 47835235 (47.8 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

This will give a lot of network information, however, we are just interested in the local ip address which is listed after `inet`. There will probably be 2 addresses listed, we are only interested in the one that is _not_ `127.0.0.1`, which in this case is `10.10.11.203` <br>
write this address down somewhere as this will be how we connect to the Raspberry Pi in the future. <br><br>

The other way you can get your Raspberry Pi's IP address is through your router's DHCP (Dynamic Host Configuration Protocol). <br>
Open a web browser on your computer and type the IP address of your router. If you do not have the IP address of your router you'll either be able to find it on the back of your router or you'll have to go through the specific steps for your OS to find the address on your computer. <br><br>
Once you have navigated to your routers IP, you should see a webpage with information and settings for your router. Depending on your router model and internet provider, your interface will be different. All routers will have a section where all the devices on the network are listed along with there IP's, navigate to this section and search for a device called `raspberrypi`. <br>
write the address for `raspberrypi` down somewhere as this will be how we connect to the Raspberry Pi in the future. <br><br>

#### Desktop
If you'd rather a regular desktop configuration of Raspbian then download the latest version of Raspbian [here](https://www.raspberrypi.org/downloads/raspbian/) and follow the installation instructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

----

### Python

This project is built with Python so we need to make sure we have the proper packages installed to run the provided scripts<br>
first run the command `sudo apt-get update` to make sure everything is up to date<br><br>

Next we need to check that the proper version of python is installed. This project uses Python 3, so we need to check that it's installed by running the command `python3 --version`. This should output something similar to the following:

```bash
Python 3.x.x
```

If it returns `Command 'python3' not found` or something similar, then run the command `sudo apt-get install python3` <br><br>

Now we need to install PIP to manage our python packages. To do this, run the command `sudo apt install python3-pip` <br><br>

To install the necessary python package run the command `pip install pygame`

----
## Wiring

A general wiring diagram for a Raspberry Pi's interface with a phone: <br> 
<img src="./assets/wiring_diagram.png" alt="Markdown Monster icon" width="800"/>

----

## Notes:
* Audio files are not currently available through this repository
* All audio files must be within the subfolder `Audio/`