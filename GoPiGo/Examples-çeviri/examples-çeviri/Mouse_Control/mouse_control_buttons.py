#!/usr/bin/env python
########################################################################                                                                  
# This example is for controlling the GoPiGo robot from a mouse buttons                        
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      13 June 14 	Initial Authoring
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
import struct
import sys
from gopigo import *

#Fareden gelen verilerin akışını açın #Open the stream of data coming from the mouse
file = open( "/dev/input/mice", "rb" );
speed=150#hızı 150 ayarlandı 

debug = 0	#Hata ayıklarken raw valuesleri yazdırın #Print raw values when debugging

#Parse through the fata coming from mouse
#Döndürülenler: [sol tuşa basıldığında,
# Orta düğmeye basıldığında,
# Sağ tuşa basıldı,
# X-ekseninde pozisyon değişikliği,
# Y-eksende pozisyon değişikliği]
#Parse through the fata coming from mouse
#Returns: 	[left button pressed,
#		middle button pressed,
#		right button pressed,
#		change of position in x-axis,
#		change of position in y-axis]
def getMouseEvent():
	buf = file.read(3)#dosyayı oku 
	button = ord( buf[0] )
	bLeft = button & 0x1#sol tusu kontrol eden degisken
	bMiddle = ( button & 0x4 ) > 0#orta tuşu kontrol eden degisken
	bRight = ( button & 0x2 ) > 0#sag tuşu kontrol eden degisken
	x,y = struct.unpack( "bb", buf[1:] )
	if debug:
		print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
	return [bLeft,bMiddle,bRight,x,y]
	
flag=0
print "Press Enter to start"
a=raw_input()	#başlangıç inputu beklemekte #Wait for an input to start
set_speed(speed)#hızını ayarlama
stop()
while( 1 ):
	[l,m,r,x,y]=getMouseEvent()	#Fareden alınan girişler #Get the inputs from the mouse
	if debug:
	if debug:
		print l,m,r,x,y
		
	if flag==1: # Sola veya sağa fare basılmazsa, ileri hareket edin #If left or right mouse not pressed, move forward
		fwd()
		flag=0
	if l:		#Fare sol düğmesine basılırsa sola döner #If left mouse buton pressed, turn left
		left()
		flag=1
	if m:		#Fare orta düğmesine basılırsa, durur #If middle mouse button pressed, stop
		stop()
	if r:		#Fare sağ düğmesine basılırsa, sağa döner #If right mouse button presses, turn right
		right()
		flag=1
	if l and r:	#Farenin sol ve sağ  tuşuna aynı anda basılırsa, geri döner #If both the left and right mouse buttons pressed, go back
		bwd()
