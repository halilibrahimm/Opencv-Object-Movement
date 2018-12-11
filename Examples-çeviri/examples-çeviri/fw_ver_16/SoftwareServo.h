#ifndef SoftwareServo_h
#define SoftwareServo_h

#include <Arduino.h>
#include <inttypes.h>

class SoftwareServo
{
  private:
    uint8_t pin;       
    uint8_t angle;       // in degrees// derecelerde
    uint16_t pulse0;     // pulse width in TCNT0 counts// TCNT0 sayımındaki darbe genişliği
    uint8_t min16;       // minimum darbe, 16uS birimler (varsayılan 34'tür)// minimum pulse, 16uS units  (default is 34)
    uint8_t max16;       // maksimum darbe, 16uS birimler, 0-4ms aralık (varsayılan 150'dir)// maximum pulse, 16uS units, 0-4ms range (default is 150)
    class SoftwareServo *next;
    static SoftwareServo* first;
  public:
    SoftwareServo();
    uint8_t attach(int);     // attach to a pin, sets pinMode, returns 0 on failure, won't
                             // position the servo until a subsequent write() happens
    void detach();
    void write(int);         // specify the angle in degrees, 0 to 180
    uint8_t read();
    uint8_t attached();
    void setMinimumPulse(uint16_t);  // pulse length for 0 degrees in microseconds, 540uS default
    void setMaximumPulse(uint16_t);  // pulse length for 180 degrees in microseconds, 2400uS default
    static void refresh();    // must be called at least every 50ms or so to keep servo alive
                              // you can call more often, it won't happen more than once every 20ms
};

#endif
