#include "board.h"

uint64_t read_board_state() {
    PORTC = 1 << 0; // set PC0 to HIGH
    delay(PORT_MESSURE_DELAY);
    uint64_t state = (uint64_t)PINA;
    for (int i = 1; i < 8; i++) {
        PORTC = 1 << i; // set PCi to HIGH
        delay(PORT_MESSURE_DELAY); // wait for the signal to settle
        state |= (uint64_t)PINA << (i * 8); // shift PINA to the left and add it to state
    }
    return ~state; // invert the state because the board is active low
    // 00000000 00000000 00000000 00000000 00000000 00000000 00110001 10001000
}

void print_uint64_t(uint64_t state) {
    if (state == 0) {
        Serial.println("0x0");
        return;
    }
    Serial.print("0x");
    Serial.print((uint32_t)(state >> 32), HEX);
    Serial.println((uint32_t)state, HEX);
}