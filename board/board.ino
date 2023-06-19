#include "Arduino.h"
#include "defs.h"
#include "hall.h"
#include "led.h"
#include <FastLED.h>
#include "commands.h"

typedef uint8_t cmd_identfier_t;
typedef uint64_t* msg_data_t;

struct board_request_msg {
  cmd_identfier_t id;
  uint32_t args_len;
  msg_data_t args;
};

struct board_replay_msg {
  cmd_identfier_t id;
  uint32_t params_len;
  msg_data_t params;
};

void test(uint64_t state);
void handle_request(board_request_msg msg);
void state_to_sqaures(uint64_t state, SquareName arr[]);
int active_squares(uint64_t state, SquareName arr[]);
int get_request(struct board_request_msg *msg);

LedControl *led_ctl;
int loop_delay_ms = 100;
void setup() {
  // #ifdef __AVR_ATmega2560__ 
  DDRA = 0;     // set all pins of PORTA as input
  DDRC = 0xFF;  // set all pins of PORTC as output
  // #endif
  Serial.begin(115200);
  led_ctl = new LedControl();
  led_ctl->reset();
}

uint64_t prev_state = 1;
void loop() {
  uint64_t state = scan_hall_array();
  if (state != prev_state) {
    prev_state = state;
    board_replay_msg replay = {BOARD_STATE_CHANGED, 1, &state};
   Serial.write((uint8_t *)&replay, 1 + 4 + 8 * 1);
    // Serial.flush();
    // Se
  }
  delay(loop_delay_ms);
}

void serialEvent() {
  board_request_msg msg = {0};
  int res = get_request(&msg);
  if (res != 0) {
    board_replay_msg replay = {ERROR, 0, NULL};
    Serial.write((uint8_t*)&replay, 1);
    return;
  }
  handle_request(msg);
}

int get_request(struct board_request_msg* msg) {
  cmd_identfier_t command = 0;
  int res = Serial.readBytes((char *)&command, 4);

  // read the args length
  uint32_t args_len = 0;
  res = Serial.readBytes((char *)&args_len, 4);

  uint64_t args[args_len];
  res = Serial.readBytes((char *)args, args_len * 8);

  if (Serial.available() > 0) { // Not all feilds were read, or serial is dirty
    return -1;
  }
  msg->id = command;
  msg->args_len = args_len;
  msg->args = args;
  return 0;
}
void handle_request(board_request_msg msg) {
  board_replay_msg replay;
  switch (msg.id) {
  case PING_REQUEST:
    replay = {PING_RESPONSE, 0, NULL};
    Serial.write((uint8_t *)&replay, 5);
    break;

  case SET_LEDS_STATE_REQUEST:
    uint64_t squares_raw = msg.args[0];
    // all squares
    SquareName squares[NUM_LEDS] = {SquareName::a1, SquareName::a2, SquareName::a3, SquareName::a4, SquareName::a5};
    led_ctl->set(1, CRGB::Red, 200);
    replay = {SET_LEDS_STATE_RESPONSE, 0, NULL};
    Serial.write((uint8_t *)&replay, 1);
    break;
  }
}
void state_to_sqaures(uint64_t state, SquareName arr[]) {
  int index = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
      if ((state >> i) & 1 == 1) {
        arr[index] = (SquareName)i;
        index++;
      }
  }
}

int active_squares(uint64_t state, SquareName arr[]) {
  int index = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
    if ((state >> i) & 1 == 1) {
        arr[index] = (SquareName)i;
        index++;
    }
  }
  return index;
}
