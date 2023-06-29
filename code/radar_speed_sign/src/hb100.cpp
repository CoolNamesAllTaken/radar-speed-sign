#include "hb100.hh"

uint16_t HB100::calc_speed() {
    uint16_t curr_speed = 31360 / last_pulse_period; // V = Fd / 31.36, Fd = 1 / last_pulse_period[s]
    _speed_buf[_speed_buf_index] = curr_speed;
    _speed_buf_index++;
    if (_speed_buf_index >= SPEED_BUF_SIZE) {
        _speed_buf_index = 0; // wrap
    }
    uint32_t averaged_speed = 0;
    uint16_t max_speed = 0;
    for (size_t i = 0; i < SPEED_BUF_SIZE; i++) {
        averaged_speed += _speed_buf[i];
        if (_speed_buf[i] > max_speed) {
            max_speed = _speed_buf[i];
        }
    }
    // return (uint16_t)(averaged_speed / SPEED_BUF_SIZE);
    return max_speed;
}