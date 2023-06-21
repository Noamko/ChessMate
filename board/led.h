#pragma once
#include "config.h"
#include <FastLED.h>

typedef CRGB color_t;

class LedControl {
public:
  LedControl();
  void set(square_t square[],int count, color_t color, int brightness);
  void set(square_t square, color_t color, int brightness);
  void set(uint64_t leds, color_t color, int brightness);

  void reset();

private:
  color_t leds[NUM_LEDS];
};

