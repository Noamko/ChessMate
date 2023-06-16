#pragma once
#include "defs.h"
#include <FastLED.h>

#define STRIP_PIN 8
#define NUM_LEDS 4
typedef CRGB color_t;

class LedControl {
public:
  LedControl();
  void set(SquareName square[], int num_of_squares, color_t color,
                             int brightness);
  void set(SquareName square, color_t color,
           int brightness);
  void fade(SquareName square[], color_t color, int brightness,
                   int duration);

  void reset();

private:
  color_t leds[NUM_LEDS];
};

