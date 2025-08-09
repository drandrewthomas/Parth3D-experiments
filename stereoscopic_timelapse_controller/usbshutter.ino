/*
usbshutter.ino - A simple example of using a microcontroller as an intervalometer to trigger a
smartphone camera shutter at a pre-defined interval. The code was written for an M5Stack AtomS3
Lite so may need some changes for other chips - note the chip must support being used as a
USB HID keyboard device as not all microcontrollers do.

Sending 0x28 as a standard scan code with keyboard.pressRaw works for Android but not on an iPad
(maybe other OS's too). So we use the consumercontrol interface instead as it allows sending
media keys such as the volume up key needed to activate the shutter in the Android and iOS
camera apps.
*/

#include <FastLED.h>
#include "USB.h"
#include "USBHIDConsumerControl.h"

#define BUTTON_PIN 41
#define RGB_PIN 35

CRGB leds[1];

USBHIDConsumerControl mediakeys;

uint16_t interval = 10; // 10ths of a second
unsigned long lasttime;
boolean running = false;
boolean shutterpressed = false;

void setup()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  mediakeys.begin();
  USB.begin();
  FastLED.addLeds<WS2812, RGB_PIN, GRB>(leds, 1);
  FastLED.setBrightness(50);
  leds[0] = CRGB::Green;
  FastLED.show();
}

void loop()
{
  if(running)
  { // REMEMBER 10ths OF A SECOND!!!
    unsigned long sofar = millis() - lasttime;
    if(sofar >= (interval * 100))
    {
      unsigned long over = sofar - (interval * 100);
      lasttime = millis() - over;
      pressshutter();
    }
  }
  if(digitalRead(BUTTON_PIN) == LOW)
  {
    if(running) stopintervalometer();
    else startintervalometer();
    while(digitalRead(BUTTON_PIN) == LOW);
  }
}

void startintervalometer()
{
  running = true;
  pressshutter();
  leds[0] = CRGB::Blue;
  FastLED.show();
  lasttime = millis();
}

void stopintervalometer()
{
  running = false;
  leds[0] = CRGB::Green;
  FastLED.show();
}

void pressshutter()
{
  if(shutterpressed) return;
  shutterpressed = true;
  leds[0] = CRGB::Red;
  FastLED.show();
  mediakeys.press(CONSUMER_CONTROL_VOLUME_INCREMENT);
  delay(1);
  mediakeys.release();
  if(running) leds[0] = CRGB::Blue;
  else leds[0] = CRGB::Green;
  FastLED.show();
  shutterpressed = false;
}
