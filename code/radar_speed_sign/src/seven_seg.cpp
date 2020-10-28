#include "seven_seg.hh"

void SevenSeg::init() {
    // Initialize 7-segment Display.
    pinMode(_spi_rclk_pin, OUTPUT);
    SPI.begin();
}

/**
 * Converts a single digit value to a segment map.
 * 
 * @param digit Digit value.
 * @retval Segment map.
 **/
uint8_t SevenSeg::digit_to_seg(uint8_t digit, bool decimal=false) {
    // Serial.print("\tdigit: ");
    // Serial.println(digit);
    uint8_t seg_map = SEVEN_SEG_F;
    switch (digit) {
        case 0:
            seg_map = SEVEN_SEG_0;
            break;
        case 1:
            seg_map = SEVEN_SEG_1;
            break;
        case 2:
            seg_map = SEVEN_SEG_2;
            break;
        case 3:
            seg_map = SEVEN_SEG_3;
            break;
        case 4:
            seg_map =SEVEN_SEG_4;
            break;
        case 5:
            seg_map = SEVEN_SEG_5;
            break;
        case 6:
            seg_map = SEVEN_SEG_6;
            break;
        case 7:
            seg_map = SEVEN_SEG_7;
            break;
        case 8:
            seg_map = SEVEN_SEG_8;
            break;
        case 9:
            seg_map = SEVEN_SEG_9;
            break;
    }
    return decimal ? seg_map & ~(1<<7) : seg_map;
}

void SevenSeg::write(uint8_t value, bool decimal=false) {
    uint8_t ones_value = value % 10;
    uint8_t tens_value = value / 10;
    uint8_t ones_digit;
    uint8_t tens_digit;

    if (ones_value == 0 && tens_value == 0) {
        // save power when speed is zero
        ones_digit = SEVEN_SEG_BLANK;
        tens_digit = SEVEN_SEG_BLANK;
    } else {
        ones_digit = digit_to_seg(ones_value);
        // don't display leading zero
        tens_digit = tens_value == 0 ? SEVEN_SEG_BLANK : digit_to_seg(tens_value);
    }

    uint16_t seg_map = (ones_digit << 8) | tens_digit;
    String map_str = String(seg_map, BIN);
    
    digitalWrite(_spi_rclk_pin, LOW);
    SPI.transfer16(seg_map);
    digitalWrite(_spi_rclk_pin, HIGH);
    // strobe RCLK to transfer registers onto output
    
    
}