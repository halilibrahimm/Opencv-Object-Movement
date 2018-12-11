                                                        
#  video akışını ve GoPiGo'yu bir web tarayıcısından denetlemek için yapılmış bir örnek

from __future__ import print_function
from __future__ import division
from builtins import input

import logging

LOG_FILENAME = "/tmp/robot_web_server_log.txt" #yapılan haraketlerin tuttuğu dosya
file_location = "/home/pi/Desktop/GoPiGo/Software/Python/Examples/Browser_Streaming_Robot/www/"
logging.basicConfig( filename=LOG_FILENAME, level=logging.DEBUG )

# Ayrıca stdout'a giriş yap
#stdout Linux da standart çıkış dosyasıdır.Programcı ulaşama ama başka çıktılara yönlendirebilir
consoleHandler = logging.StreamHandler() 
consoleHandler.setLevel( logging.DEBUG )
logging.getLogger( "" ).addHandler( consoleHandler )

import os.path
import math
import time
import signal
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import sockjs.tornado
import threading

import camera_streamer
import robot_controller
import json
import gopigo
import subprocess
import sys
try:
    import Queue as queue
except:
    import queue 
robot = None

cameraStreamer = None
scriptPath = os.path.dirname( __file__ )
webPath = os.path.abspath( file_location)
print (webPath)
robotConnectionResultQueue = queue.Queue()
isClosing = False

#--------------------------------------------------------------------------------------------------- 
def createRobot(resultQueue ):
    
    r = robot_controller.RobotController( )
    resultQueue.put( r )
            
#--------------------------------------------------------------------------------------------------- 
class ConnectionHandler( sockjs.tornado.SockJSConnection ): #bağlantı sınıfı
    
    #-----------------------------------------------------------------------------------------------
    def on_open( self, info ):
        
        pass
        
    #-----------------------------------------------------------------------------------------------
    def on_message( self, message ):
                
        try:
            message = str( message )
        except Exception:
            logging.warning( "Got a message that couldn't be converted to a string" )
			#Bir dize haline dönüştürülemeyen bir mesaj var
            return

        if isinstance( message, str ):
            
            lineData = message.split( " " )
            if len( lineData ) > 0:
                
                if lineData[ 0 ] == "Centre":
                
                    if robot != None:
                        robot.centreNeck()
                
                elif lineData[ 0 ] == "StartStreaming":
                    cameraStreamer.startStreaming()
                    
                elif lineData[ 0 ] == "Shutdown":
                    cameraStreamer.stopStreaming()
                    gopigo.stop()
                    robot.disconnect()
                    sys.exit()
                
                elif lineData[ 0 ] == "Move" and len( lineData ) >= 3:
                    
                    motorJoystickX, motorJoystickY = \
                        self.extractJoystickData( lineData[ 1 ], lineData[ 2 ] )
                    
                    if robot != None:
                        robot.setMotorJoystickPos( motorJoystickX, motorJoystickY )     
                elif lineData[ 0 ] == "PanTilt" and len( lineData ) >= 3:
                    
                    neckJoystickX, neckJoystickY = \
                        self.extractJoystickData( lineData[ 1 ], lineData[ 2 ] )
                        
                    if robot != None:
                        robot.setNeckJoystickPos( neckJoystickX, neckJoystickY )
                        
    #-----------------------------------------------------------------------------------------------
    def on_close( self ):
        logging.info( "SockJS connection closed" )

    def extractJoystickData( self, dataX, dataY ):
        
        joystickX = 0.0
        joystickY = 0.0
        
        try:
            joystickX = float( dataX )
        except Exception:
            pass
        
        try:
            joystickY = float( dataY )
        except Exception:
            pass
            
        return ( joystickX, joystickY )

#--------------------------------------------------------------------------------------------------- 
class MainHandler( tornado.web.RequestHandler ):
    
    #------------------------------------------------------------------------------------------------
    def get( self ):
        self.render( webPath + "/index.html" )
        
#--------------------------------------------------------------------------------------------------- 
def robotUpdate():
    
    global robot
    global isClosing
    
    if isClosing:
        tornado.ioloop.IOLoop.instance().stop()
        return
        
    if robot == None:
        
        if not robotConnectionResultQueue.empty():
            
            robot = robotConnectionResultQueue.get()
        
    else:
                
        robot.update()

#--------------------------------------------------------------------------------------------------- 
def signalHandler( signum, frame ):
    
    if signum in [ signal.SIGINT, signal.SIGTERM ]:
        global isClosing
        isClosing = True
        
        
#--------------------------------------------------------------------------------------------------- 
if __name__ == "__main__":
    
    signal.signal( signal.SIGINT, signalHandler )
    signal.signal( signal.SIGTERM, signalHandler )
    
    # Web sunucusunun yapılandırmasını oluşturun
    router = sockjs.tornado.SockJSRouter(   
        ConnectionHandler, '/robot_control' ) #SockJS protokol yönlendirici sınıfı
    application = tornado.web.Application( router.urls + [ 
        ( r"/", MainHandler ), 
        ( r"/(.*)", tornado.web.StaticFileHandler, { "path": webPath } ),
        ( r"/css/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/css" } ),
        ( r"/css/images/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/css/images" } ),
        ( r"/images/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/images" } ),
        ( r"/js/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/js" } ) ] )
    
    #( r"/(.*)", tornado.web.StaticFileHandler, {"path": scriptPath + "/www" } ) ] \
    
    # Kamera flama oluştur
    cameraStreamer = camera_streamer.CameraStreamer()
    
    # Robotun eş zamanlı olarak bağlanmaya başlanması
    robotConnectionThread = threading.Thread( target=createRobot, 
        args=[ robotConnectionResultQueue ] )
    robotConnectionThread.start()

    # Şimdi web sunucusunu başlat
    logging.info( "Starting web server..." )
    http_server = tornado.httpserver.HTTPServer( application )
	
	#The port number on which the robot control works, change in line 105 in www/index.html too
    http_server.listen( 98 )
    
    robotPeriodicCallback = tornado.ioloop.PeriodicCallback( 
        robotUpdate, 100, io_loop=tornado.ioloop.IOLoop.instance() )
    robotPeriodicCallback.start()
    
    cameraStreamerPeriodicCallback = tornado.ioloop.PeriodicCallback( 
        cameraStreamer.update, 1000, io_loop=tornado.ioloop.IOLoop.instance() )
    cameraStreamerPeriodicCallback.start()
    
    tornado.ioloop.IOLoop.instance().start()
    
    #  kodu kapatır
    robotConnectionThread.join()
    
    if robot != None:
        robot.disconnect()
    else:
        if not robotConnectionResultQueue.empty():
            robot = robotConnectionResultQueue.get()
            robot.disconnect()
            
    cameraStreamer.stopStreaming()