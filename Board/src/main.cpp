#include <Arduino.h>
#include "utils.h"
#include "board.h"

void setup() {
  DDRA = 0; // set all pins of PORTA as input
  DDRC = 0xFF; // set all pins of PORTC as output
  Serial.begin(9600); // initialize serial communication
}

void loop() {
  uint64_t state = read_board_state(); // read the state of the board
  // print_uint64_t(state); // print the state
}
