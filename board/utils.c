#include "utils.h"

static void state_to_active_sqaures(uint64_t state, square_t arr[]) {
  int index = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
    if ((state >> i) & 1 == 1) {
      arr[index] = i;
      index++;
    }
  }
}

static int active_squares(uint64_t state, square_t arr[]) {
  int index = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
    if ((state >> i) & 1 == 1) {
      arr[index] = i;
      index++;
    }
  }
  return index;
}

