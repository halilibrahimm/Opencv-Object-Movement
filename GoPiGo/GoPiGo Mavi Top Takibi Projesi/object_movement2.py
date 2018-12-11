# # Gerekli paketleri içe aktar
from collections import deque #Nesenin izlendiği n adet noktanın verimli şekilde depolanması için deque veri tipi kullanıldı
import numpy as np #Hızlı çalışan dizi kullanımı için içe aktarıldı
import argparse # Ekrana yönleri yazdırmak için kullanıldı
import imutils #Döndürme, yeniden boyutlandırma,konturları sıralama, kenarları algılama gibi g.işleme işlevlerini gerçekleştirmek için içe aktarıldı
import cv2 #opencv kütüphanesinden gerekli fonksiyonları içe aktarır
from picamera import PiCamera #picamera modülünün temel fonksiyonlarını içe aktarır
from picamera.array import PiRGBArray 
import os #Dizin oluştıma silme değiştirme ve çeşitli işletim sistemleriin komutlarını python içinde kullanılmasını sağlar
from gopigo import *	#GoPigo kontrolü için temel fonksiyonların olduğu modül
import sys	#Çalışan programı kapatmak için kullanılır
import io #Herhangi bir giriş çıkış türleri için kullanılır
import time 
state=False
# argümanları ayırma işlemleri
os.system("v4l2-ctl --set-fmt-video=width=600,height=600,pixelformat=1")
os.system("v4l2-ctl --set-parm=32") #fps 32 olarak ayarlandı
os.system("sudo modprobe bcm2835-v4l2") #Kamera için v4l2 sürücüsünü aktif ettik

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# yeşil renginin alt ve üst sınırları belirlendi
# topun HSV renk alanı
greenLower = (110,50,50)
greenUpper = (130,255,255)

# istenen noktaların listesini başlat,çerçeve sayıcı
# koordinat deltaları
pts = deque(maxlen=args["buffer"])
print ("Pts ",pts)
counter = 0
(dX, dY) = (0, 0)
direction = ""

# eğer bir video yolu sağlanmadıysa referans olarak al
# picamera default ayarları yapıldı
if not args.get("video", False):
	camera = PiCamera()
	camera.sharpness = 0
        camera.contrast = 0
        camera.brightness = 50
        camera.saturation = 0
        camera.ISO = 0
        camera.video_stabilization = False
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        camera.awb_mode = 'auto'
        camera.image_effect = 'none'
        camera.color_effects = None
        camera.rotation = 0
        camera.hflip = False
        camera.vflip = False
       # camera.crop = (0.0, 0.0, 1.0, 1.0)
	camera.resolution=(320,240)
	#fps=FPS().start()
	#vs=PiVideoStream().start()
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
        


#keep looping
frame=None


radius=0
while True:
     
        c=cv2.waitKey(1)%0x100
        if c==120:
                state=True
                print("Stop")
        elif c==10:
                state=False
                print("Start")

        if state == True:
                stop()
                continue
            
	# Geçerli çerçeveyi yakala
	# Eğer çerçeve yakalanmadıysa
	# ve videpunu sonuna ulaşıldıysa
	# çerçeveyi yeniden boyutlandır,bulanıklaştır ve HSV'ye dönüştür
	# renk alanı
        #frame=vs.read()
	rawCapture=PiRGBArray(camera,size=(320,240))
	backstream=io.BytesIO()
	camera.capture(backstream,format='jpeg',use_video_port=True)
	datapak=np.fromstring(backstream.getvalue(),dtype=np.uint8)

	frame=cv2.imdecode(datapak,1)
        

	# Mavi rengi için bir maske oluştur erode ve dilate işlemi gerçekleştir
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Mavi rengi için bir maske oluştur erode ve dilate işlemi gerçekleştir
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# Maskede kontur(çevre) bulma ve mevcut
	# (x, y) topun ortası
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# En az bir kontur bulunursa devam et
	if len(cnts) > 0:
		# Maskedeki en büyük konturu bulup kullan. En az çevreleyen çevreyi hesapla
		#radius=0
		tRadius =radius
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            
                
                
		# Eğer yarıçap minimum boyuta ulaşırsa devam et
		if radius > 10:			
			# Çemberi ve çemberin merkezini çiz
			# Sonra izlenen noktaların listesini güncelle
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
			durum=1
		if (radius)<10:
                        print ("Stop")
                        stop()
                        continue

			
		#print('radius = ',radius)
		#print("T radius =  ",tRadius)
		#print("FRAK = ",(tRadius-radius))
        else:
                stop()
                continue
	# İzlenen noktalar kümesi üzerinden döngü
	for i in np.arange(1, len(pts)):
		# İzlenen noktalardan biri yok ise, yoksay
	
		if pts[i - 1] is None or pts[i] is None:
			continue
                try:
                        t= pts[-10]
                except IndexError:
                        break
		# Tampon içinde yeterli nokta birikmiş olup olmadığını kontrol et
		if counter >= 10 and i == 1 and pts[-10] is not None:

			# X ve y arasındaki farkı hesapla
			# Yönü koordine et ve yeniden başlat
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
			if np.abs(dX) > 20:
				left() if np.sign(dX) == 1 else right()

			# Hareket varsa
			# X-yönü
			#gopigoyu doğu ve batı yönünde ilerlet
			#else 
			# Hareket varsa
			# Y-yönü
			#gopigoyu kuzey ve güney yönünde ilerlet
			
			
##			if np.abs(dY) > 20:
##				fwd() if np.sign(dY) == 1 else bwd()
##
##			if dirX != "" and dirY != "":
##				direction = "{}-{}".format(dirY, dirX)
##
##			# otherwise, only one direction is non-empty
##			else:
##				direction = dirX if dirX != "" else dirY
                                

			# ensure there is significant movement in the
			# x-direction
			#stop()
##############################################################			
			if np.abs(dX) > 20:
##                                print ("dx = ",np.sign(dX))
##                                print ("dy = ",np.sign(dY))
##                                print ("ileriiii = ",(tRadius-radius))
##                              

                                if np.sign(dX) == 1:  
                                        dirX = "Left"
                                        print("Left")
                                        right() #sağ motoru çalıştırıp sola döner
                                        continue
                                elif np.sign(dY) == 1:
                                        dirX="Right"
                                        print("Right")
                                        left() #sol motoru çalıştırıp sağa döner
                                        continue 
                                elif (tRadius-radius) > 0:
                                        dirX="FWD"
                                        print("ileri") 
                                        fwd() #iki motoruda ileri yönde çalıştırır 
                                        continue
                                elif (tRadius-radius) < 0:
                                        dirt="BWD"
                                        print("Geri")
                                        bwd() #iki motorda geri yönde çalışır.
                                        continue
                                else:
                                        stop() #diğer durumlarda durur
                                        continue #continue yapıp tekrar işi başa alır.
                        else:
                                stop()
                                continue
                        if dirX != "" and dirY != "":
			# Her iki yön de boş olmadığında işle
				direction = "{}-{}".format(dirY, dirX)
			# Aksi halde, yalnızca bir yönde boşluk yoktur
			
			else:
				direction = dirX if dirX != "" else dirY          
##                                   
#############################################################
		
###                           if np.sign(dX) == 1: 
                          
			# ensure there is significant movement in the
			# y-direction
##			if np.abs(dY) > 0:
##                                
##			  
##			  if np.sign(dY) == 1:
##                                  dirY = "North"
##                                  fwd()
                                  

			# handle when both directions are non-empty
##			if dirX != "" and dirY != "":
##				print('dirY= '+dirY)
##				print('dirX= '+ dirX)
##
##				direction = "{}-{}".format(dirY, dirX)

			# otherwise, only one direction is non-empty
		

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)

		# diğer durumlarda hattın kalınlığını hesapla
		# bağlantı çizgilerini çiz
		
		# Çerçevenin hareket deltalarını ve hareket yönünü göster
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# q tuşuna basınca döngüden çık
	if key == ord("q"):
		break
# kamerayı temizle ve açık pencereleri kapat
camera.release()
cv2.destroyAllWindows()
