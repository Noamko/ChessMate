#include "utils.h"
#define DEBUG 1

#if DEBUG
void print_uint64_t(uint64_t num) {
    if (num == 0) {
        Serial.println("0x0");
        return;
    }
    Serial.print("0x");
    Serial.print((uint32_t)(num >> 32), HEX);
    Serial.println((uint32_t)num, HEX);
}
#endif