#include <SpritzCipher.h>

#include "Arduino.h"
#include <FastLED.h>
#include <string.h>
#include <stdlib.h>

#define SERIAL_BAUDRATE 115200
#define SEND_STATE(x) Serial.write(x, 4)
#define PORT_MESSURE_DELAY_MS 10
#define SERIAL_BUFFER_SIZE 100

uint64_t scan_hall_array();
void hall_array_to_hex_string(uint64_t state, char buffer[]);
void handle_serial_command(void (*callback)(char*));
int fetch_command(char buffer[]);

void setup() {
	DDRA = 0;	// set all pins of PORTA as input
	DDRC = 0xFF;	// set all pins of PORTC as output
	Serial.begin(SERIAL_BAUDRATE);
}

void loop() {
	uint64_t state = scan_hall_array();
	uint8_t arr[4] = {(uint8_t)(state >> 24), (uint8_t)(state >> 16), (uint8_t)(state >> 8), (uint8_t)state};
	// SEND_STATE(arr);
	// delay(1000);
}

void serialEvent() {
  // This function is called automatically
  // by the Arduino framework whenever there
  // is new serial data available
  char buffer[5];
  fetch_command(buffer);
  Serial.println(buffer);
  
}

uint64_t scan_hall_array() {
	PORTC = 1 << 0; // SET PCO to HIGH
	delay(PORT_MESSURE_DELAY_MS);
	uint64_t res = (uint64_t)PINA;
	for (int i = 1; i < 8; i++) {
		PORTC = 1 << i;
		delay(PORT_MESSURE_DELAY_MS);
		res |= (uint64_t)PINA << (i * 8);
	}
	return ~res;
}

int fetch_command(char buffer[]) {
        uint8_t strlen = 5;
        //int res = Serial.readBytes(&strlen, 1);
		// Serial.println("got length: " +String(strlen));
		int res = 1;
		if (res <= 0) {
			// error
			return -1;
		}
		// res = Serial.readBytes(buffer, strlen);
		res = Serial.readBytesUntil('\n', buffer, 100);
		if (res <= 0) {
			// error
			return -1;
		}

}
void hall_array_to_hex_string(uint64_t state, char buffer[]) {
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