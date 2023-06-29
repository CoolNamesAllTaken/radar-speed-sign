#ifndef HB100_H
#define HB100_H

#include <Arduino.h>

#define SPEED_BUF_SIZE 100

class HB100 {
    public:
        // sad sad, these are exposed because I need to hit them in an ISR
        volatile uint32_t last_pulse_period{0};
        volatile uint32_t last_pulse_us{0};

        HB100(){}

        uint16_t calc_speed();
    private:
        uint16_t _speed_buf[SPEED_BUF_SIZE] = {0};
        size_t _speed_buf_index = 0;
};

#endif /* HB100_H */