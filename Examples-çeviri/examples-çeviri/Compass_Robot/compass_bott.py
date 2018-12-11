#!/usr/bin/env python
##################################################################################################################
# Bu örnek Gopigoyu pusula gibi kullanmaya yarar
#                             
# http://www.dexterindustries.com/GoPiGo      
# Compass module: http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html
#                                                       
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      22 July 14  	Initial Authoring
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
# Refer to the datasheet to add additional functionality https://www.seeedstudio.com/wiki/images/4/42/HMC5883.pdf
#
# Command:
#	l 45	:	45 derece sola döndür
#	r 45	:	45 derece sağa döndür
#
####################################################################################################################

from grove_compass_lib import *# pusula ile ilgili kütüphaneyi import ettik
from gopigo import *
import turtle #turtle komutları bir araya getirerek, karmaşık şekiller ve resimler kolayca çizilebilir.

en_turtle=1		#turtle grafiği aktifleştirir
debug=0			#Hata ayıklamayı pasifleştirir

if en_turtle:
	turtle.Turtle()
	
c=compass()#pusula
divider=4	 #bölücü belirlendi	

set_speed(110) #hızı 110 a ayarla

while True:
	print "CMD:",			#Komut için bekle
	cmd=raw_input()
	print cmd
	try:
		if cmd[0]=='f':		#F girilmişse enkoder sayımı ile ilerle
			dist=int(cmd[2:])/divider
			enc_tgt(1,1,dist)#motor1 motor2 hedef
			fwd()
			if en_turtle:
				turtle.forward(dist*divider)
				
		elif cmd[0]=='l':	#L girilmişse sola çevir
			angle=int(cmd[2:])
			if angle >360 or angle <0:#açı 360 dan büyük veya 0 dan küçükse
				print "Wrong angle" #yanlış açı
				continue
				
			c.update()
			start=360-c.headingDegrees	# Pusula değeri 360 dereceden 0 dereceye doğru dönerse değeri ters çevir
			target= (start+angle)%360	# Sonuç 360 derecen fazla ise 0 yap
			left_rot() # GoPiGo'yu aynı konumda bırakın (her iki motor da ters yönde hareket eder)
			while True:
				current=360-c.headingDegrees # Pusula değeri 360 dereceden 0 dereceye doğru dönerse değeri ters çevir
				if debug:
					print start,target,current
				if target-start>0:		# 0dan başalayarak 360 a kadar ulaşışdıysa dur
					if current>target:
						right_rot()
						time.sleep(.15)
						stop()
						break;
				else:
					if current>target and current <start-5:	#Hedef ıskalandıysa, kontrol durumu değişir ve bir miktar toleransı korur
						right_rot() #GoPiGo'yu aynı konumda sağa döndürün, her iki motor da ters yönde hareket eder
						time.sleep(.15)
						stop()
						break;
				c.update()
				#time.sleep(.1)
			if en_turtle:#turtle modulü ile pusula konumunu ekrana çiz
				turtle.left(angle)			
				
		elif cmd [0]=='r': 				#R basılşmışsa sağa döndür
			angle=int(cmd[2:]) 
			if angle >360 or angle <0:
				print "Wrong angle"
				continue
				
			c.update()
			start=c.headingDegrees #başlığı derecelendir
			target= (start+angle)%360
			right_rot()
			while True:
				current=c.headingDegrees
				if debug:
					print start,target,current
				if target-start>0:
					if current>target:
						stop()
						break;
				else:
					if current>target and current <start-5:
						stop()
						break;
				c.update()
				#time.sleep(.1)
			if en_turtle:
				turtle.right(angle)
				
		elif cmd[0]=='x':	#X e basılmışsa çık
			print "Exiting"
			if en_turtle:
				turtle.bye()
			break
			
		elif cmd[0]=='d':	#Pusuladan mevcut okumayı göster
			c.update()
			print c.headingDegrees,360-c.headingDegrees
		else:
			print "Wrong command"#yanlış komut
	except ValueError:
		print "Wrong command"
	
	time.sleep(.1)
	#print heading
	
	time.sleep(.1)
	
