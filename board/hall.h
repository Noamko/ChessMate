#ifndef HALL_H
#define HALL_H
#include "config.h"

uint64_t scan_hall_array();
static void hall_array_to_hex_string(uint64_t state, char buffer[]);
#endif
