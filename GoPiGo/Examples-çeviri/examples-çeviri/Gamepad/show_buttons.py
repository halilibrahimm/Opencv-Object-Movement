#!/usr/bin/python
 #buton gösterimi için kod
###############################################################                                                                  
# Displays gamepad button keycodes
#
# History
# ------------------------------------------------
# Author                Date      		Comments
# Eric Goebelbecker     Jun 6 2015 		Initial Authoring
# 			                                                         
'''

#tuş kodlarını görüntüler

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
###############################################################
from select import select#linuxta belirli işlevlere ulaşmayı sağlar
from evdev import InputDevice, categorize, ecodes, KeyEvent #cihaz özelliklerini listelemeyi sağlar
gamepad = InputDevice('/dev/input/event0')#Oyun alanındaki ABXY düğmelerini kullanarak robotu kontrol etmek için kullanabileceğimiz bir senaryo yazalım
# Evdev, Linux çekirdeğinde genel bir giriş olayı arabirimidir;
# aygıt sürücülerinden gelen ham giriş olaylarını geralize eder ve bunları / dev / input dizinindeki karakter aygıtları aracılığıyla
# kullanılabilir hale getirir.
# Bu, robotlarımızı kontrol etmek için gamepad kullanımı gerçekleştirir
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)#kategorilere ayır
        if keyevent.keystate == KeyEvent.key_down:#
            print keyevent.keycode

