# Equipment Server for Test Transmitter

## Hardware requirements
1. All raspberry Pis except a RPi 2 Model B, Raspberry A, B, B+

## Installation Instructions
1. Take the latest standard rasbian image and write the .img to an SD card
2. Boot rPi
3. in Text menu do the following
3.1 Option 1 - Expand filesystem
3.2 Option 3 - Boot into Text console
3.3 Option 8 - A4 - Enable SSH
4. Reboot
5. login as pi - raspberry


## Requirements for pifm to run
sudo apt-get install ffmpeg

## Requirements for pirateradio.py to run
sudo apt-get update
sudo apt-get install python3

## Requirements for Python Twisted Network Library to run
sudo apt-get install python-twisted