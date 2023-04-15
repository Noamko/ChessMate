#include "include/hall.h"

void setup() {
	DDRA = 0; // set all pins of PORTA as input
	DDRC = 0xFF; // set all pins of PORTC as output
	Serial.begin(9600);
}

void loop() {
	uint64_t state = scan_hall_array();
	char hex[19] = {0};
	hall_array_to_hex_string(state, hex);
	Serial.println(hex);
}
