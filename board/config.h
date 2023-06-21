
#ifndef __CONFIG_H__
#define __CONFIG_H__
// Configuration
#include <Arduino.h>
#include <avr/pgmspace.h>
#include <stdarg.h>
#include "commands.h"

#define SERIAL_BAUDRATE 115200
#define PORT_MESSURE_DELAY_MS 100
#define STRIP_PIN 8
#define NUM_LEDS 64
#define MESSAGE_HEADER_SIZE 5

typedef uint64_t board_state_t;
typedef uint8_t msg_identfier_t;
typedef uint32_t length_t;
typedef uint8_t data_t;

struct board_msg {
  msg_identfier_t id;
  length_t data_len;
  data_t data[400];
};

// Commands
#define SET_LEDS 0

typedef char square_t;
#define CELL_A1 0
#define CELL_B1 1
#define CELL_C1 2
#define CELL_D1 3
#define CELL_E1 4
#define CELL_F1 5
#define CELL_G1 6
#define CELL_H1 7
#define CELL_A2 8
#define CELL_B2 9
#define CELL_C2 10
#define CELL_D2 11
#define CELL_E2 12
#define CELL_F2 13
#define CELL_G2 14
#define CELL_H2 15
#define CELL_A3 16
#define CELL_B3 17
#define CELL_C3 18
#define CELL_D3 19
#define CELL_E3 20
#define CELL_F3 21
#define CELL_G3 22
#define CELL_H3 23
#define CELL_A4 24
#define CELL_B4 25
#define CELL_C4 26
#define CELL_D4 27
#define CELL_E4 28
#define CELL_F4 29
#define CELL_G4 30
#define CELL_H4 31
#define CELL_A5 32
#define CELL_B5 33
#define CELL_C5 34
#define CELL_D5 35
#define CELL_E5 36
#define CELL_F5 37
#define CELL_G5 38
#define CELL_H5 39
#define CELL_A6 40
#define CELL_B6 41
#define CELL_C6 42
#define CELL_D6 43
#define CELL_E6 44
#define CELL_F6 45
#define CELL_G6 46
#define CELL_H6 47
#define CELL_A7 48
#define CELL_B7 49
#define CELL_C7 50
#define CELL_D7 51
#define CELL_E7 52
#define CELL_F7 53
#define CELL_G7 54
#define CELL_H7 55
#define CELL_A8 56
#define CELL_B8 57
#define CELL_C8 58
#define CELL_D8 59
#define CELL_E8 60
#define CELL_F8 61
#define CELL_G8 62
#define CELL_H8 63
#endif

#define LOG(x, ...)                                                            \
  do {                                                                         \
    char buf[400];                                                             \
    sprintf(buf, x, ##__VA_ARGS__);                                            \
    int len = strlen(buf);                                                     \
    board_msg msg = {0};                                      \
    memcpy(msg.data, buf, len); \
    msg.id = SEND_LOG;                                                         \
    msg.data_len = len;                                                        \
    Serial.write((uint8_t *)&msg, MESSAGE_HEADER_SIZE + len);                  \
    Serial.flush();                                                            \
  } while (0)
