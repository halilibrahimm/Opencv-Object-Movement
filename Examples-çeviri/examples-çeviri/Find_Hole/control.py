#!/usr/bin/python
'''
This module contains convenience functions to simplify
the coding of simple tasks.

This really needs to be moved to a GoPiGo package
e.g. from gopigo.control import *
'''

from gopigo import *

en_debug=1 #hata ayıklamayı etkinleştirir

## 360 derece dönüş 64 enkoder derecesi//5 derece 
## DPR darbe başına düşen derece sayısı
DPR = 360.0/64
WHEEL_RAD = 3.25 # Tekerlekler 6.5 cm çapındadır
CHASS_WID = 13.5 # Şasi 13.5 cm genişliğindedir

def left_deg(deg=None):
    '''
    Şasiyi belirli bir dereceyle sola çevirin 
    DPR derece/darbe oranı
    Bu fonksiyon enkoderin doğru numaraya ayarlanmasını sağlar
    '''
    if deg is not None:# deg değeri boş değilse
        pulse= int(deg/DPR) #girilen açıdaki enkoder darbe sayısı
        enc_tgt(0,1,pulse)#motor1,motor2,hedef
    left()

def right_deg(deg=None):
    '''
  Şasiyi belirli bir dereceyle sağa döndürün.
     DPR, # derece / darbe (Deg: Darbe oranı)
     Bu fonksiyon enkoderin doğru numaraya ayarlanmasını sağlar
      Atımlar ve daha sonra sağa () çağırır.
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(0,1,pulse)
    right()

def fwd_cm(dist=None):
    '''
 Şasi fwd'sini belirtilen sayıda cm kadar hareket ettirin.
     Bu fonksiyon enkoderin doğru numaraya ayarlanmasını sağlar
      Ve sonra fwd () çağırır.
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()

def bwd_cm(dist=None):
    '''
    Şasiyi belirtilen sayıda cm ile hareket ettirin.
     Bu fonksiyon enkoderin doğru numaraya ayarlanmasını sağlar
      Atımlar ve daha sonra bwd () çağırır.
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist)) #belirli santimetre ilerlemesini sağlar
        enc_tgt(1,1,pulse)
    bwd()

def cm2pulse(dist):
    '''
     hareket ettirmek için darbe sayısını hesaplayın.
     Darbeler = dist * [darbeler / devir] / [dist / devir]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD #[Cm / devir] tekerleğin dönüşü başına değeri
    PPR = 18 # [P / devir] tekerlek devir başına kodlayıcı Darbeler
    pulses = PPR*revs # Dist [cm] 'yi taşımak için gerekli olan [p] encoder pulse'ları.
    if en_debug:
        print 'WHEEL_RAD',WHEEL_RAD
        print 'revs',revs
        print 'pulses',pulses
    return pulses
