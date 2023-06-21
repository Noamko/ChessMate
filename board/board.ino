#include "Arduino.h"
#include "commands.h"
#include "config.h"
#include "hall.h"
#include "led.h"
#include <FastLED.h>


void monitor_board_state();
void handle_request(board_msg msg);
int fetch_request(struct board_msg *msg);

LedControl *led_ctl;
int loop_delay_ms = 10;
void setup() {
  #ifdef __AVR_ATmega2560__ 
  DDRA = 0;     // set all pins of PORTA as input
  DDRC = 0xFF;  // set all pins of PORTC as output
  #endif
  Serial.begin(SERIAL_BAUDRATE);
  led_ctl = new LedControl();
  led_ctl->reset();
  LOG("Hello from ChessMate");
}

uint64_t prev_state = 1;

void loop() {
  delay(PORT_MESSURE_DELAY_MS);
  monitor_board_state();
}

void monitor_board_state() {
  board_state_t state = 0x8080808080808081;//scan_hall_array();
  if (state != prev_state) {
    prev_state = state;
    board_msg replay = {0};
    replay.id = BOARD_STATE_CHANGED;
    replay.data_len = 8;
    for (int i = 0; i < 8; i++) {
      replay.data[i] = (state >> (8 * i)) & 0xff;
    }
    Serial.write((uint8_t *)&replay, MESSAGE_HEADER_SIZE + replay.data_len);
    Serial.flush();
  }
}
void serialEvent() {
  board_msg msg = {0};
  int res = fetch_request(&msg);
  if (res != 0) {
    board_msg replay = {ERROR, 0, NULL};
    Serial.write((uint8_t*)&replay, 1);
    return;
  }
  handle_request(msg);
}

int fetch_request(struct board_msg* msg) {
  msg_identfier_t id = 0;
  int res = Serial.readBytes((char *)&id, sizeof(msg_identfier_t));

  // read the args length
  length_t len = 0;
  res = Serial.readBytes((char *)&len, sizeof(length_t));

  res = Serial.readBytes(msg->data, len);

  if (Serial.available() > 0) { // Not all feilds were read, or serial is dirty
    LOG("Error fetching request: buffer not empty: %d", Serial.available());
    return -1;
  }
  msg->id = id;
  msg->data_len = len;
  LOG("Fetched request: id: %d, len: %d", id, len);
  return 0;
}
void handle_request(board_msg msg) {
  board_msg replay = {0};
  switch (msg.id) {
  case PING_REQUEST:
    replay = {PING_RESPONSE, 0, NULL};
    Serial.write((uint8_t *)&replay, sizeof(replay));
    break;

  case SET_LEDS_STATE_REQUEST:
    // uint64_t squares_raw = msg.args[0];
    // led_ctl->set(CELL_A1, NUM_LEDS, CRGB::Red, 200);
    // replay = {SET_LEDS_STATE_RESPONSE, 0, NULL};
    // Serial.write((uint8_t *)&replay, 1);
    break;
  }
}
