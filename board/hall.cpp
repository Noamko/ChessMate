#include "hall.h"


uint64_t scan_hall_array() {
#ifdef __AVR_ATmega2560__
  PORTC = 1 << 0; // SET PCO to HIGH
  delay(PORT_MESSURE_DELAY_MS);
  uint64_t res = (uint64_t)PINA;
  for (int i = 1; i < 8; i++) {
    PORTC = 1 << i;
    delay(PORT_MESSURE_DELAY_MS);
    res |= (uint64_t)PINA << (i * 8);
  }
  return ~res;
  #else
  return 0;
#endif
}

static void hall_array_to_hex_string(uint64_t state, char buffer[]) {
  buffer[0] = '0';
  buffer[1] = 'x';
  for (int i = 0; i < 16; i++) {
    uint8_t val = (state >> (i * 4)) & 0xF;
    if (val < 10) {
      buffer[17 - i] = val + '0';
    } else {
      buffer[17 - i] = val - 10 + 'A';
    }
  }
  buffer[18] = 0;
}
