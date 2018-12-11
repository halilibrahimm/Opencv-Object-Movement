                                                         
# Bu örnek, video akışını ve GoPiGo'yu bir web tarayıcısından denetlemek için
      
#
# This example is derived from the Dawn Robotics Raspberry Pi Camera Bot
# https://bitbucket.org/DawnRobotics/raspberry_pi_camera_bot
#############################################################################################################


from __future__ import print_function
from __future__ import division
from builtins import input
# Pyton 3 için uyumluluğu için
import logging
import math
import time
try:
	import Queue as queue #kuyruk yapısı tanımlanıyor ilk gelen ilk çıkar
except:
	import queue 
import threading
import gopigo
#--------------------------------------------------------------------------------------------------- 
debug=0
class RobotController:
  
	MAX_UPDATE_TIME_DIFF = 0.25 #max günelleme zamanı 0.25 olarak ayarlanıyor
	TIME_BETWEEN_SERVO_SETTING_UPDATES = 1.0 #servo ayar guncellemeleri arasındaki zaman
	
	JOYSTICK_DEAD_ZONE = 0.1 
	
	MOTION_COMMAND_TIMEOUT = 2.0 #bu zaman aralığında motor herhangi bir komut almazsa hızı 0 olarak ayarlanır.
	
	speed_l=200
	speed_r=200
	#-----------------------------------------------------------------------------------------------
	def __init__( self ):
		gopigo.set_speed(200)
		gopigo.stop()
		#gopigo.fwd()
		
		self.lastServoSettingsSendTime = 0.0 #son servo ayarları gonderme suresi 
		self.lastUpdateTime = 0.0  #son guncelleme zamanı 
		self.lastMotionCommandTime = time.time() #son hareket komutunun geldiği zaman 
	
	#-----------------------------------------------------------------------------------------------
	def __del__( self ):
		
		self.disconnect() #bağlantıyı kes
	
	#-----------------------------------------------------------------------------------------------
	def disconnect( self ):
		print ("Closing")
	   
	def normaliseJoystickData( self, joystickX, joystickY ): #joystick verilerini normallerştiren fonk.
		stickVectorLength = math.sqrt( joystickX**2 + joystickY**2 ) 
		if stickVectorLength > 1.0:
			joystickX /= stickVectorLength
			joystickY /= stickVectorLength
		
		if stickVectorLength < self.JOYSTICK_DEAD_ZONE:
			joystickX = 0.0
			joystickY = 0.0
			
		return ( joystickX, joystickY )

	def centreNeck( self ):
		#gopigo.set_right_speed(0)
		pass
	
	def setMotorJoystickPos( self, joystickX, joystickY ):
		joystickX, joystickY = self.normaliseJoystickData( joystickX, joystickY )#normalize etmiş (0-1)
		if debug:
			print( "Left joy",joystickX, joystickY)
			#print self.speed_l*joystickY
		#gopigo.set_left_speed(int(self.speed_l*joystickY))
		#gopigo.fwd()
		if joystickX > .5:
			print( "Left")
			gopigo.left() 
		elif joystickX <-.5:
			print ("Right")
			gopigo.right()
		elif joystickY > .5:
			print ("Fwd")
			gopigo.fwd()
		elif joystickY < -.5:
			print ("Back")
			gopigo.bwd()
		else:
			print ("Stop")
			gopigo.stop()
		
	def setNeckJoystickPos( self, joystickX, joystickY ):
		#print ("g")
		joystickX, joystickY = self.normaliseJoystickData( joystickX, joystickY )
		if debug:	
			print ("Right joy",joystickX, joystickY)
			

	def update( self ):
		if debug:	
			print ("Updating")
		curTime = time.time()
		timeDiff = min( curTime - self.lastUpdateTime, self.MAX_UPDATE_TIME_DIFF )
		
		# Bir süre hareket komutu almadıysak motorları kapatın
		#zaman ölçümü yapılıyor

		self.lastUpdateTime = curTime