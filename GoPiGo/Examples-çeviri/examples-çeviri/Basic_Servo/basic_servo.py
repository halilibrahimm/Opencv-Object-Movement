#!/usr/bin/env python
########################################################################                                                                  
# Bu örnek gopigo motor kontrolü için 
# Servo motoru klavye ile kontrol edeceğiz
# this example from the command line, you'll be prompted for input
# Press a key (a, d, or s) to move the servo.  The data is collected, 
#                            
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
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

servo_pos=90 #servo pozisyonunu orta noktaya ayarla
print "KONTROLLER"
print "a: Motoru sola döndür"
print "d: Motoru sağa döndür"
print "s: Servoyu normal konumuna al"
print "Gopigoya gönderilecek komutları girin"


#
while True:
	#Kullanıcıdan alınan değerlere göre servo açılarını değiştir
	inp=raw_input()				# Klavyeden girişi al
	# Bu aşamama klavyeden girilen değerler ne yapılacağına karar verilir
	if inp=='a':
		servo_pos=servo_pos+10	# A ya basılmışsa servoyu 10 derece ilerletir(sola döndürür)
	elif inp=='d':
		servo_pos=servo_pos-10	# D ye basılmışsa servoyu 10 derece terse dönderir(sağa döndürür)
	elif inp=='s':
		servo_pos=90 #Servoyu eski konumuna getir
	
	#servoyu 0 ile 180 aralığında kontrolünü sağlamak için
	if servo_pos>180:
		servo_pos=180
	if servo_pos<0:
		servo_pos=0
		
	servo(servo_pos)		# Bu fonksiyon servo sürücüyü en son konumuyla günceller
	time.sleep(.1)			# Her işlem arası 0.1 saniye ara verir
	