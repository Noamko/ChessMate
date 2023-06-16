#include "led.h"
#include "FastLED.h"
#include "defs.h"

LedControl::LedControl() {
  FastLED.addLeds<WS2812B, STRIP_PIN, GRB>(this->leds, NUM_LEDS);
  for (int i = 0; i < NUM_LEDS; i++) {
    this->leds[i] = color_t::Black;
  }
}

void LedControl::set(SquareName square, color_t color, int brightness) {
  SquareName arr[1] = {square};
  this->set(arr, 1, color, brightness);
}


void LedControl::set(SquareName square[], int num_of_squares, color_t color,
                     int brightness) {
  // Turn off all leds
  this->reset();

  for (int i = 0; i < num_of_squares; i++) {
    LOG("number of squares %d", num_of_squares);
    int index = (int)square[i];
    LOG("Setting led %d to color %d", index, color);
    this->leds[index] = color;
    FastLED.show();
  }
  FastLED.setBrightness(brightness);
  FastLED.show();
}

void LedControl::fade(SquareName square[], color_t color, int brightness,
                      int duration) {
  // Turn off all leds
  this->reset();
  int num_of_squares =3;
  for (int i = 0; i < num_of_squares; i++) {
    LOG("number of squares %d", num_of_squares);
    int index = (int)square[i];
    LOG("Setting led %d to color %d", index, color);
    this->leds[index] = color;
    // FastLED.show();
  }
  for (int i = 0; i < duration; i++) {
    // FastLED.setBrightness((i));
    FastLED.clear();
    FastLED.show(i);
    delay(100);
    LOG("brightness %d", int(i));
  }
}

void LedControl::reset() {
  for (int i = 0; i < NUM_LEDS; i++) {
    this->leds[i] = color_t::Black;
  }
  FastLED.show();
}