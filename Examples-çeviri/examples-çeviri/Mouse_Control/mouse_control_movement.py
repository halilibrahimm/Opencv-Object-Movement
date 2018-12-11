#!/usr/bin/env python
########################################################################                                                                  
# This example is for controlling the GoPiGo robot from a mouse scroll                          
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      20 Aug 14 		Initial Authoring
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

#Fareden gelen verilerin akışını açın#Open the stream of data coming from the mouse
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
a=raw_input()	#başlangıç inputu beklemekte#Wait for an input to start
set_speed(speed)#hızını ayarlama
stop()
while( 1 ):
	[l,m,r,x,y]=getMouseEvent()	#Fareden alınan girişler	#Get the inputs from the mouse
	if debug:
		print l,m,r,x,y
	print x,"\t",y
	
	#Eger yukarı dogru bir fare hareketi varsa(positive y-axis)#If there is a signinficant mouse movement Up (positive y-axis)
	if y >20:
		fwd()	#ileri git#Move forward

	#Eger asagı dogru bir fare hareketi varsa(negative y-axis)#If there is a signinficant mouse movement Down (negative y-axis)
	elif y<-20:
		bwd()	#geri dön#Move Back

	#Eger sola dogru bir fare hareketi varsa (positive x-axis)#If there is a signinficant mouse movement Left (positive x-axis)
	elif x<-20:
		left()	#sola dön#Move left

	#Eger sağa dogru bir fare hareketi varsa(negative x-axis)#If there is a signinficant mouse movement Right (negative x-axis)
	elif x>20:
		right()	#sağa dön#Move Right

	#Eger sol fare tuşuna basıldıysa gopigo yu durdur #Stop the GoPiGo if left mouse button pressed
	if l:
		stop()
	time.sleep(.01)#0.1 saniye beklemek
