
# Dexter Industries hat sensörü kontrol örneği
# Bu program hat izleyicisi için I2C veri yolunu kontrol eder ve ayrıca sensor hattının düzgün çalışıp çalışmadığından emin olmak için bir okuma işlemi yapar
#I2C arduino sensorlerle haberleşmek için kullanılan haberleşme protokollerinden biridir.seri haberleşme türlerinden senkron haberleşmeye örnektir
#I2C Haberleşme için toprak hattı dışında SDA ve SCL olmak üzere iki hatta ihtiyaç duyulmaktadır.
import line_sensor
import time
import subprocess
from timeit import default_timer as timer

debug=0

def get_sensorval():
	while True:
		val=line_sensor.read_sensor()
		if val[0]<>-1:
			return val
def check_line_sensor():
	output = subprocess.check_output(['i2cdetect', '-y','1'])  #çıktıyı kontrol eder
	#i2cdetect', '-y','1' komutu rassberry pi ile çalışan cihazın(arduino) bağlı olup olmadıgını kontrol eder
	if output.find('06') >=0:			#hat sensorunu arıyor 
		print "--> Line sensor found\n" #bulundu
		if debug:
			print output
	else:
		print "--> Line sensor not found"  #buluamadı
		print output
		print ""

check_line_sensor()
start=timer()
l0,l1,l2,l3,l4=get_sensorval() #arduino pin ayakları
end=timer()
print "Time:\t%.4f s" %(end-start)
print "IR1:\t%d /1023 " %(l0) #volt olarak degerini yazdırıyor
print "IR2:\t%d /1023 " %(l1)
print "IR3:\t%d /1023 " %(l2)
print "IR4:\t%d /1023 " %(l3)
print "IR5:\t%d /1023 " %(l4)
