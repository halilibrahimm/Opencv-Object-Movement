#!/usr/bin/env python
#############################################################################################################                                                                  
# Klavye ile gopigo kontrolü  İçin Grafiksel Arayüz
# Contributed by casten on Gitub https://github.com/DexterInd/GoPiGo/pull/112
#
#Bilgisayardan Kontrol Sağlayan Kod Parçacığı
#
#  Kontroller:
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
# Karan		27 June 14			Code cleanup                                                    
# Casten	31 Dec  15			Added async io, action until keyup
# Karan		04 Jan	16			Cleaned up the GUI

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
##############################################################################################################

from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Çalışan programı kapatmak içn kullanılan kütüphane


#Pygame,Python dilini kullanarak kolay bir şekilde multimedya 
#yazılımları geliştirmemizi sağlayan,platform bağımsız bir kütüphanedir
import pygame #Key up key down olaylarını çalıştırmak için çağrılan kütüphane


pygame.init()#Pygame yazılımını başlatan kod parçaçığı
screen = pygame.display.set_mode((700, 400))#Pygame ekran ayarı yapıyor 
pygame.display.set_caption('Uzak Bağlantı Penceresi')#Geçerli pencere başlığını ayarlama

background = pygame.Surface(screen.get_size())#yüzey boyutlarını al
background = background.convert()#arka plan dönüştürme
background.fill((250, 250, 250))#arka plan dolgu

# Ekrana Aşağıdaki Metni Yazdırıyor
instructions = '''#talimatlar
                      BASIC GOPIGO CONTROL GUI

This is a basic example for the GoPiGo Robot control 

(Be sure to put focus on thi window to control the gopigo!)

Press:
      ->w: Move GoPiGo Robot forward
      ->a: Turn GoPiGo Robot left
      ->d: Turn GoPiGo Robot right
      ->s: Move GoPiGo Robot backward
      ->t: Increase speed
      ->g: Decrease speed
      ->z: Exit
''';
size_inc=22 #
index=0
for i in instructions.split('\n'):#/n görünce böl 
	font = pygame.font.Font(None, 36)#Font ayarı
	text = font.render(i, 1, (10, 10, 10))
	background.blit(text, (10,10+size_inc*index))#arka plana aldığı text değerini uyguluyor
	index+=1


screen.blit(background, (0, 0))
pygame.display.flip()#Tam Ekran Yüzeyi'ni ekrana güncelleyin


#Gopigo kontrolü için grafiksel arayüzün kullanıcıya tanıtımı
while True:
	event = pygame.event.wait();#kuyruktan alınan tek bir etkinliği bekle
	if (event.type == pygame.KEYUP):# keyup klavyeyi temsil eder.klavyedeki bir değer girildiğinde keydown, işlem yapmaya başlar. 
	#keyup fonksiyonundan farkı, keyup parmağınızı tuştan kaldırdığımız anda, keydown tuşa bastığımız anda aktif olur.
		stop();
		continue;
	if (event.type != pygame.KEYDOWN):
		continue;	
	char = event.unicode;
	if char=='w':
		fwd()	;# Move forward
	elif char=='a':
		left();	# Turn left
	elif char=='d':
		right();# Turn Right
	elif char=='s':
		bwd();# Move back
	elif char=='t':
		increase_speed();	# GoPiGo'nun hızı 0-255 arasında olabilir. 
		#Varsayılan hız 200'tür. GoPiGo hızını 10 arttırmak için increase_speed () işlevini kullanırız
	elif char=='g':
		decrease_speed();	# yavaşlatmak için
	elif char=='z':
		print "\nExiting";		# Exit
		sys.exit();
#Gopigo kontrolü için grafiksel arayüzün kullanıcıya tanıtımı