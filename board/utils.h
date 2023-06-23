#pragma once
#include "config.h"
#include <Arduino.h>
static void state_to_active_sqaures(uint64_t state, square_t arr[]);
static int active_squares(uint64_t state, square_t arr[]);
// static uint64_t board_state_to_led_state(board_state_t board_state);