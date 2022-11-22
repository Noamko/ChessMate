#ifndef BOARD_H
#define BOARD_H

#include <Arduino.h>
#define PORT_MESSURE_DELAY 10
uint64_t read_board_state();
void print_board_state(uint64_t board_state);
#endif