#pragma once
#include <Arduino.h>
#include "defs.h"

uint64_t scan_hall_array();
void hall_array_to_hex_string(uint64_t state, char buffer[]);
