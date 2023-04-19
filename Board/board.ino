#include <FastLED.h>
#include <string.h>

#define SERIAL_BAUDRATE 115200
#define SEND_STATE(x) Serial.write(x, 4)
#define PORT_MESSURE_DELAY_MS 10
#define SERIAL_BUFFER_SIZE 100
#define FETCH_COMMAND(x) Serial.readBytesUntil('\n', x, SERIAL_BUFFER_SIZE)

uint64_t scan_hall_array();
void hall_array_to_hex_string(uint64_t state, char buffer[]);
void handle_serial_command(void (*callback)(char*));
void fetch_commands();

void setup() {
	DDRA = 0;	// set all pins of PORTA as input
	DDRC = 0xFF;	// set all pins of PORTC as output
	Serial.begin(SERIAL_BAUDRATE);
}

void loop() {
	uint64_t state = scan_hall_array();
	uint8_t arr[4] = {(uint8_t)(state >> 24), (uint8_t)(state >> 16), (uint8_t)(state >> 8), (uint8_t)state};
	SEND_STATE(arr);
}

void serialEvent() {
  // This function is called automatically
  // by the Arduino framework whenever there
  // is new serial data available
  char buffer[SERIAL_BUFFER_SIZE];
  size_t read = FETCH_COMMAND(buffer);
  if (read > 0) {
	// We have a command!
	// Do something with it
  }
  else if (strcmp(buffer, "test")) {
	Serial.write("test ok");
  }
}

void fetch_commands() {
	while (Serial.available()) {
		char c = Serial.read();
		if (c == 0 ) {
			handle_serial_command([](char* cmd) {
				Serial.println(cmd);
			});
		}
	}
} 
/* scan_hall_array()
- exmaple output: 0xC3C3C3C3C3C3C3C3
= 110000011 110000011 110000011 110000011 110000011 110000111 110000001 110000011

=   1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0
    0 0 0 0 0 1 0 0
    1 1 1 1 1 1 1 1
    1 1 1 1 1 1 0 1
*/
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
