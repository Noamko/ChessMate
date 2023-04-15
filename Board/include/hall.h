#pragma once
#include <Arduino.h>

#define PORT_MESSURE_DELAY_MS 10 
uint64_t scan_hall_array();
void hall_array_to_hex_string(uint64_t state, char str[]);
