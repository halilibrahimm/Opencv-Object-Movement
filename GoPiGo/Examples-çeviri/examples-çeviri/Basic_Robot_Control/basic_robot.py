#!/usr/bin/env python
#############################################################################################################                                                                  
# //Klavye ile gopigo kontrolü
# Kontroller:
# 	w:	İleri 
#	a:	Sol
#	d:	Sağ
#	s:	Geri
#	x:	Dur
#	t:	Hızı Arttır
#	g:	Hızı Azalt
#	z: 	Çık
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments  
# Karan			27 June 14		Code cleanup                                                    
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
##############################################################################################################

from gopigo import *	#Gopigo'yu kontrol etmek için temel işlevlerin olduğu kütüphane
import sys	#Çalışan programı kapatmak içn kullanılan kütüphane
print "Bu gopigo kontrolü için temel bir örnektir"
print "Basın:\n\t w: Gopigoyu İleri Götür \n\t a:Gopigoyu sola döndür \n\t d: Gopigoyu sağa Döndür \n\t s: Gopigoyu Geri Götür \n\t t Hızı Arttır\n\t g: Hızı Azalt\n\t x: gopigoyu Durdur\n\t z: Çıkış\n"
while True:
	print "Komutları Gir",
	a=raw_input()	# İnput değeri alındı
	if a=='w':
		fwd()	# Gopigoyu İleri Götürecek Fonksiyon
	elif a=='a':
		left()	# Gopigoyu Sola Çeviricek Fonksiyon
	elif a=='d':
		right()	# Gopigoyu Sağa Çevirecek Fonksiyon
	elif a=='s':
		bwd()	# Gopigoyu Geri Götürecek Fonksiyon
	elif a=='x':
		stop()	# Gopigoyu Durdur
	elif a=='t':
		increase_speed()	# Gopigoyu Hızlandıran Fonksiyon
	elif a=='g':
		decrease_speed()	# Gopigoyu Yavaşlatan Fonksiyon
	elif a=='z':
		print "Çıkış"		# Çıkış
		sys.exit()
	else:
		print "Yanlış Komut Lütfen Tekrar Giriniz"
	time.sleep(.1)