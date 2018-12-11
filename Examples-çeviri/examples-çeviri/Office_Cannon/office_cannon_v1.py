#!/usr/bin/env python
########################################################################                                                                  
# This example controls the GoPiGo and Rocket Launcher with a wireless mouse on the USB port.
# The GoPiGo motion is controlled by the buttons of the.
# The Rocket Launcher is controlled by the motion of the mouse.
# The Rocket Launcher is fired by pressing the middle button.  
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# John Cole  	April 14  		Initial Authoring    
# Karan			27 June 14		Code cleanup and made more responsive   
# 				25 Aug  14		USB high current mode for Raspberry Pi Model B+ added        
#                                       
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
########################################################################
from gopigo import *
import struct
import os

import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util

#Model B+ için geçerli ve Model B için geçerli değildir
model_b_plus=True	#Office Cannon çalışabilmesi için gerekli model model B+ dır.
					# This can be left on for the Model B and not cause problems.
					#Bu, GPIO 38'i yüksek, USB aşırı akım ayarını geçersiz kılacak şekilde çeker.
					# Bu set ile, USB 1.2 Amp'a kadar çıkabilir.

# Protokol komut baytları
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

file = open( "/dev/input/mice", "rb" );# adresteki dosyayı aç
debug = 0

#Office Cannon kurulumu
def setup_usb():
    global DEVICE 
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)#DEVICE cihazını bulur ve satıcı ve ürün kimliğini kaydeder

    if DEVICE is None:#DEVICE cihazını bulamazsa
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)#DEVICE cihazını bulur ve satıcı ve ürün kimliğini kaydeder
        if DEVICE is None:#DEVICE cihazını bulamazsa
            raise ValueError('Missile device not found')#error mesajı verildi(Cihaz bulunamadı)
        else:#bulunursa
            DEVICE_TYPE = "Original"#cihaz tipine orjinal 
    else:#bulunursa
        DEVICE_TYPE = "Thunder"#cihaz tipi gürültü

    # Linux de önce usb HID'i çıkarmamız gerekiyorwe need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # önceden kaydedilmemiş    
    DEVICE.set_configuration()

#Office cannon komutunu gönder
def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

#office cannon üzerindeki LED'i kontrol etmek için komut gönder
def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

#office cannon u taşımak için komut gönder
def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)

def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        #Atış öncesinde dengeleyin, daha sonra tekrar yükleme süresine izin verin.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command

def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)

#Farenin degerini al
def getMouseEvent():
	buf = file.read(3)
	button = ord( buf[0] )
	bLeft = button & 0x1
	bMiddle = ( button & 0x4 ) > 0
	bRight = ( button & 0x2 ) > 0
	x,y = struct.unpack( "bb", buf[1:] )
	if debug:
		print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
	return [bLeft,bMiddle,bRight,x,y]
  
  
flag=0
#Office Cannon kurulumu
def control():
	global flag
	[bLeft,bMiddle,bRight,x,y]=getMouseEvent()  #Fareden alınan girişler

	#GoPiGo control
	if flag==1: 			# Sola veya sağa fare basılmazsa, ileri hareket edin
		fwd()
		flag=0
	if bLeft:    			#Fare sol düğmesine basılırsa sola döner
		left()
		flag=1
  
	if bRight:    			#Fare orta düğmesine basılırsa, durur
		right()
		flag=1
	if bLeft and bRight:  	#Farenin sol ve sağ  tuşuna aynı anda basılırsa, geri döner
		stop()
		flag=0
 
	#Office cannon kontrol
	tdelay=80
	if bMiddle > 0:
		print "fire rockets"
		run_command("fire", tdelay)

	#Cannon sola taşımak için fareyi sola getirin
	#Cannon saga taşımak için fareyi saga getirin
	#Orta düğmeye basarak ateşleyin
	
	if x == 0:
		print "Stop rockets"
	elif x > 10:
		print "Left rockets"
		run_command("left", tdelay)
	elif x < -10:
		print "Right rockets"
		run_command("right", tdelay)
	if y == 0:
		print "Stop Rockets Y"
	elif y > 10:
		print "Up Rockets"
		run_command("up", tdelay)
	elif y < -10:
		print "Down rockets"
		run_command("down", tdelay)

	time.sleep(.1)
	return
  
try:
	print "Setting up"
	print "Left Mouse button- Turn left\nRight mouse button- Turn right\nBoth left and right- Stop\nMiddle mouse button- Fire rocket\nMove mouse to control the launcher"
	setup_usb()
	
	#Enable USB to give supply upto 1.2A on model B+
	if model_b_plus:
		os.system("gpio -g write 38 0")
		os.system("gpio -g mode 38 out")
		os.system("gpio -g write 38 1")
	
	run_command("zero", 100)
	stop()
	print "Start\n............."
	while True:
	  control()
except KeyboardInterrupt:
	#Çıkmadan önce USB üzerinde yüksek akım modunu devre dışı bırakın
	if model_b_plus:
		os.system("gpio -g write 38 0")
	
