#include "led.h"
#include "utils.h"
#include "config.h"

static uint8_t swap_bits(uint8_t b) {
  uint8_t result = 0;
  for (int i = 0; i < 8; i++) {
    result |= ((b >> i) & 0x1) << (7 - i);
  }
  return result;
}

static uint64_t board_state_to_led_state(board_state_t board_state) {
  LOG("got board state: %x%x", board_state & 0xffffffff, board_state >> 32);
  uint64_t leds_state = 0;
  for (int i = 0; i < 8; i++) {
    if (i % 2 != 0) {
      leds_state |= ((uint64_t)(board_state >> 8 * i) & 0xff) << i * 8;
    }
    else {
      leds_state |= (swap_bits(((uint8_t)(board_state >> i * 8) >> i * 8) & 0xff)) << i * 8;
    }
  }
  LOG("leds state: %x%x", leds_state >> 32, leds_state & 0xffffffff);
  return leds_state;
}

LedControl::LedControl() {
  FastLED.addLeds<WS2812B, STRIP_PIN, GRB>(this->leds, NUM_LEDS);
  for (int i = 0; i < NUM_LEDS; i++) {
    this->leds[i] = color_t::Black;
  }
}

void LedControl::set(square_t square, color_t color, int brightness) {
  this->reset();
  this->leds[(int)square] = color;
  FastLED.setBrightness(brightness);
  FastLED.show();
}

void LedControl::set(square_t square[], int num_of_squares, color_t color,
                     int brightness) {
  // Turn off all leds
  this->reset();

  for (int i = 0; i < num_of_squares; i++) {
    int index = (int)square[i];
    this->leds[index] = color;
    FastLED.show();
  }
  FastLED.setBrightness(brightness);
  FastLED.show();
}

void LedControl::set(uint64_t leds, color_t color, int brightness) {
  // state = a1b1c1d1e1f1g1 a2...g2 a3...g3 ..... a8...g8
  // leds  = a1...a8 b8...b1 c
  this->reset();
  for (int i = 0; i < NUM_LEDS; i++) {
    if ((leds >> i) & 0x1) {
      this->leds[i] = color;
    } else {
      this->leds[i] = color_t::Black;
    }
  }
  FastLED.setBrightness(brightness);
  FastLED.show();
}
void LedControl::reset() {
  for (int i = 0; i < NUM_LEDS; i++) {
    this->leds[i] = color_t::Black;
  }
  FastLED.show();
}
