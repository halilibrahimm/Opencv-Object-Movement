
#Çizgi izleyen
# Dexter Industries Hat sensörü Python Kütüphanesi
# Bu ve örnek, GoPiGo'nun Dexter Industries Hattı takipçisini kullanarak satırı takip etmesini sağlamaktır.

from __future__ import print_function
from __future__ import division
from builtins import input

import line_sensor
import time
import operator
import gopigo
import atexit

atexit.register(gopigo.stop)  # Program sona erdiğinde motorları durdurun.


#başlangıçta değerimiz -1
def get_sensorval():
	while True: 
		val=line_sensor.read_sensor()
		if val[0]!=-1:
			return val
		else:
			#Tamponu temizlemek ve gereksiz değerleri kaldırmak için bir kez daha okuyun
			val=line_sensor.read_sensor()


#Her bir sensöre çoklayıcı ekle
multp=[-100,-50,0,50,100]

#Tüm sensörler white olduğunda okunur
white=[767,815,859,710,700]
#Tüm sensörler black olduğunda okunur
black=[1012,1013,1015,1003,1004]
#Siyah-white arasındaki fark
range_col=list(map(operator.sub, black, white))

#İlk çalıştırmada kalibre edin

gopigo.set_speed(150) #hızı 150 getirir

gpg_en=1
while True:
	curr=get_sensorval()
	#Beyaz ve hat arasında bugünkü farkı bulun
	diff_val=list(map(operator.sub, curr, white))

	#Her sensörün ne kadar siyah çizgi elde edebildiğini bul
	#Botun yerini bul
	#	-10000 	->	tam sol
	#	0		->	orta
	#	10000	-> 	tam sağ
	curr_pos=0
	percent_black_line=[0]*5
	for i in range(5):
		percent_black_line[i]=diff_val[i]*100/range_col[i] #yüzeyde siyah çizgi 
		curr_pos+=percent_black_line[i]*multp[i]
	print(curr_pos)
	
	if curr_pos <-2500:
		print("r")
		if gpg_en:
			gopigo.set_speed(85)
			gopigo.right()
	elif curr_pos >2500:
		print("l")
		if gpg_en:
			gopigo.set_speed(125)
			gopigo.left()
	else:
		print("f")
		if gpg_en:
			gopigo.set_speed(80)
			gopigo.fwd()
	#time.sleep(.01)
		
		
	
