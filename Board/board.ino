#include "defs.h"
#include "hall.h"
#include "led.h"
#include <FastLED.h>

#define TEST 0

typedef int32_t serial_command;

void handle_serial_command(serial_command command);
size_t active_squares(uint64_t state, SquareName arr[]);
void test(uint64_t state);
void state_to_sqaures(uint64_t state, SquareName arr[]);

    struct board_request_msg {
  uint8_t command;
  uint32_t args_len;
  uint64_t* args;
};

struct board_replay_msg {
  uint8_t response;
  uint32_t params_len;
  uint64_t* params;
};

LedControl* led_ctl;

void setup() {
  #ifdef __AVR_ATmega2560__ 
  DDRA = 0;     // set all pins of PORTA as input
  DDRC = 0xFF;  // set all pins of PORTC as output
  #endif
  Serial.begin(115200);
  // LOG("Hello from ChessM %d", "8");
  led_ctl = new LedControl();
}

void loop() {
  uint64_t state = scan_hall_array();
  uint8_t arr[4] = { (uint8_t)(state >> 24), (uint8_t)(state >> 16), (uint8_t)(state >> 8), (uint8_t)state };
  SEND_STATE(arr);
  delay(100);
}

void serialEvent() {
//   // This function is called automatically
//   // by the Arduino framework whenever there
//   // is new serial data available

//   // // read the command
  uint8_t byte;
  Serial.readBytes((char *)&byte, 1);
  if (byte == 0x0) {
    SquareName squares[NUM_LEDS] = {SquareName::a1, SquareName::a2, SquareName::a3, SquareName::a4};
    led_ctl->set(squares, 4, CRGB::Blue, 255);
  }

  if (byte == 0x1) {
    SquareName squares[NUM_LEDS] = {SquareName::a1, SquareName::a2,
                                    SquareName::a3, SquareName::a4};
    led_ctl->set(squares, 4, CRGB::Black, 255);
  }
//   // serial_command command = 0; 
//   // int res = Serial.readBytes((char *)&command, 4);

//   // if (res <= 0) {
//   //   // error
//   //   return;
//   // }

//   // // read the args length
//   // uint32_t args_len = 0;
//   // res = Serial.readBytes((char *)&args_len, 4);
//   // if (res <= 0) {
//   //   // error
//   //   return;
//   // }

//   // uint64_t args[args_len];
//   // res = Serial.readBytes((char*)args, args_len * 8);
//   // if (res <= 0) {
//   //   // error
//   //   return;
//   // }


//   // if (Serial.available() > 0) {
//   //   // error
//   //   return;
//   // }

//   // board_request_msg msg = {command, args_len, args};
  
  
}

void handle_request(board_request_msg msg) {
  switch (msg.command) {
    case SET_LEDS:
      SquareName squares[NUM_LEDS];
      for (int i = 0; i < NUM_LEDS; i++) {
        uint64_t led_state = msg.args[i];
        SquareName sqaures[NUM_LEDS];
        state_to_sqaures(led_state, sqaures);
      }
      led_ctl->set(squares, NUM_LEDS, CRGB::Blue, 255);
      break;
  }
}
void state_to_sqaures(uint64_t state, SquareName arr[]) {
  int index = 0;
  for (int i = 0; i < 64; i++) {
      if ((state >> i) & 1 == 1) {
        arr[index] = (SquareName)i;
        index++;
      }
  }
}

size_t active_squares(uint64_t state, SquareName arr[]) {
  int index = 0;
  for (int i = 0; i < 64; i++) {
    if ((state >> i) & 1 == 1) {
        arr[index] = (SquareName)i;
        index++;
    }
  }
  return index;
}
