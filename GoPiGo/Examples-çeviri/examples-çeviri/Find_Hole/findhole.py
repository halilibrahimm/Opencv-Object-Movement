#!/usr/bin/python
'''
engel
This is inspired by both the Ultrasonic Basic Obstacle Avoider 
and Ultrasonic_Servo examples. 

Esasen, gopigo şunları yapmalıdır:
   - Bir engelden 20 cm içeriye kadar fwd'yi hareket ettirin.
   - Dur
   - Oda tara
   - Engelliler arasında sığacak kadar büyük bir boşluk bulun
   - Bu yönde dönün
   - Bir engelden 20 cm içeriye kadar fwd'yi hareket ettirin.
   - Vb.
'''

from gopigo import *
from control import *
import math
import time

STOP_DIST=20 # Durdurulacak engel öncesi cm cinsinden mesafedir . 
SAMPLES=4 # Her bir okuma için alınması gereken örnek okuma sayısı.
INF=200 # Mesafe, cm, sonsuzluk olarak kabul edilecek.
REPEAT=2
DELAY=.02

def main():
    print "*** Starting Find Hole Example ***"
    for x in range(REPEAT):
        move(STOP_DIST) #haraket et
        readings = scan_room()
        holes = findholes(readings)#okumalar için
        gaps = verify_holes(holes)#delikler için
        if len(gaps) == 0:#eğer boşluk yoksa
            print "Nowhere to go!!"#gitmek için bir yer yok
            stop()
            exit()
        ## Bulunan ilk boşluğu seç
        turn_to(gaps[0][0])
    servo(90)
    stop()

def move(min_dist):#mesafe için fonksiyon
    ## Servoyu düz ilerleyecek şekilde ayarlayın
    servo(90)
    print "ileriye doğru"
    while us_dist(15) > min_dist:
        fwd()
        time.sleep(.02)
    stop()
    print "engel var"
    return

def turn_to(angle):
    '''
    GoPiGo'yu, açısı = 0 olan belirli bir açıyla 90 derece döndürün
     Sağa ve açıyla 180 = sola doğru 90 derece gidilir.
     GoPiGo şu an açı == 90 olarak işaret ediyor.
    '''
    
## <0 sola dönün,> 0 sağa dönün.
    degs = angle-90#derece
    print "Turning craft {} degrees".format(degs),#karakter dizileri biçimlendirmek için
    if degs > 0:
        print "sola"
        left_deg(degs)
    else:
        print "saga"
        right_deg(degs)
    ## hata ayıklama içindir, böylece doğru şekilde döndüğünü doğrulayabilirim
    time.sleep(1)

def verify_holes(holes): #doğrulamak için
    '''
   Bir delik, (açı, uzaklık) tuple'lerin bir listesidir.

     Bir şasinin bir deliğe sığabildiğini doğrulamak için, arasındaki boşluğu hesaplamak gerekir.
     Ilk ve son kümeler
     Tuple'lerin (açı, boşluk mesafesi) bir listesini döndürür.
    '''
    print "boşlukların dogrulanması ... "
    gaps = []#boşluklar için
    for hole in holes:
        print "  Hole:{}".format(hole),
        xy1 = calc_xy(hole[0])# iki kenardaki boşluk
        xy2 = calc_xy(hole[-1])
        gap = calc_gap(xy1,xy2)
        ang1 = hole[0][0]
        ang2 = hole[-1][0]
        middle_ang = (ang2 + ang1)/2#orta kısımdan haraket etmesi için
        print "ang:{},gap:{}".format(middle_ang,gap)   
        if gap >= CHASS_WID:#boşluk yeterli genişlikte ise
            print "    yeterince geniş!"
            gaps.append((middle_ang,gap))#boşlukları geri getir
    return gaps

def findholes(readings):
    '''
   Her okuma, belirli bir açıda bir engele mesafeyi veren bir (açı, uzaklık) tuple olacaktır.
     Bir delik bulmak için, 3 ardışık INF okumasını istiyoruz.
    '''
    print "Delikleri bulmak için okumaları işleme...."
    print readings
    holes = []
    buf = []
    ## Önceki INF olmayan okuma 
    prev = ()
    for (a,d) in readings:
        print "  {}:{}".format(a,d)
        if d < INF:
            # Eğer dist INF değilse, başka bir yere basarız
             ## engel, yani tampon sıfırlayın.
            if len(buf) > 2:
                # Arabellek en az 3 INF okumasına sahipse,
                 ## sonra deliği kaydedin.
                holes.append(buf)
                print "    boşluk var: {}:{}".format(a,d)
            buf = []
            continue
         # # Arabelleğe okuma ekle 
        buf.append((a,d))
    ## Son okumanın INF olduğu durumda
    if len(buf) > 2:
        holes.append(buf)
        print "    Found a hole: {}:{}".format(a,d)
    return holes

def scan_room():
    '''
    0'dan başlayıp artımlarla 180'e geçin.
     @ 20cm uzakta chass için gerekli açısı:
         Derece (atan (CHASS_WID / 20))
     Artımlar açıları bunun 1/2 olmalıdır.
     3 ardışık okuma arıyor.
     3 özlesi yeterince büyük bir delik garantisi vermez
      Çünkü her engel 20cm uzakta olmayacak,
      Ancak başlamak için iyi bir yer ve daha fazlası
      Önemli olan, bize,
      Ölçmek.
    
     İade listesi (açı, dist).
    '''
    ret = []
    inc = int(math.degrees(math.atan(CHASS_WID/20)))
    print "Scanning room in {} degree increments".format(inc)
    for ang in range(0,180,inc):
        print "  Setting angle to {} ... ".format(ang),
        ## resetting ang because I've seen issues with 0 and 180
        if ang == 0: ang = 1
        if ang == 180: ang = 179
        servo(ang)
        buf=[]
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist,
            if dist<INF and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
        print
        ave = math.fsum(buf)/len(buf)
        print "  dist={}".format(ave)
        ret.append((ang,ave))
        ## Hala tutarsız okumalarla ilgili sorunlar yaşıyorsunuz.
         ## Örneğin.
        ## Açıyı 0'a ayarlama ... 18 19 218 49
         ## Açıyı 170'e ayarla ... 1000 1000 45 46
        time.sleep(DELAY)
    ## servonun ön yüzü reset
    servo(90)
    return ret

def calc_xy(meas):
    '''
    Bir açı ve mesafe göz önüne alındığında, dönüş (x, y) tuple.
     X = dist * cos (radyan (açı))
     Y = dist * sin (radyan (açı))
    '''
    a = meas[0]
    d = meas[1]
    x = d*math.cos(math.radians(a))
    y = d*math.sin(math.radians(a))
    return (x,y)

def calc_gap(xy1,xy2):
    '''
(X, y) tuples ile temsil edilen iki nokta göz önüne alındığında,
     İki nokta arasındaki mesafeyi hesapla.
     Dist üçgenin hip'idir.
    
     Dist = sqrt ((x1-x2) ^ 2 + (y1-y2) ^ 2)
    '''
    dist = math.hypot(xy1[0]-xy2[0],xy1[1]-xy2[1])
    return dist

if __name__ == '__main__':
    main()
