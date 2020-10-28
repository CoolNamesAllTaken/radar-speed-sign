#ifndef SEVEN_SEG_H
#define SEVEN_SEG_H

#include <Arduino.h>
#include <SPI.h>

#define SPI_RCLK_PIN_DEFAULT 10
#define SPI_RATE_HZ_DEFAULT 1400000

// Little Endian
#define SEVEN_SEG_0 0b00111111  //11111100
#define SEVEN_SEG_1 0b00000110  //01100000
#define SEVEN_SEG_2 0b01011011  //11011010
#define SEVEN_SEG_3 0b01001111  //11110010
#define SEVEN_SEG_4 0b01100110  //01100110
#define SEVEN_SEG_5 0b01101101  //10110100
#define SEVEN_SEG_6 0b01111101  //10111110
#define SEVEN_SEG_7 0b00000111  //11100000
#define SEVEN_SEG_8 0b01111111  //11111110
#define SEVEN_SEG_9 0b01101111  //11110110
#define SEVEN_SEG_F 0b01110001  //10001100
#define SEVEN_SEG_BLANK 0x00

// Big Endian
// #define SEVEN_SEG_0 0b11111100
// #define SEVEN_SEG_1 0b01100000
// #define SEVEN_SEG_2 0b11011010
// #define SEVEN_SEG_3 0b11110010
// #define SEVEN_SEG_4 0b01100110
// #define SEVEN_SEG_5 0b10110100
// #define SEVEN_SEG_6 0b10111110
// #define SEVEN_SEG_7 0b11100000
// #define SEVEN_SEG_8 0b11111110
// #define SEVEN_SEG_9 0b11110110
// #define SEVEN_SEG_F 0b10001100

class SevenSeg {
    public:
        SevenSeg(uint8_t spi_rclk_pin = SPI_RCLK_PIN_DEFAULT, uint32_t spi_rate_hz = SPI_RATE_HZ_DEFAULT)
            : _spi_rclk_pin(spi_rclk_pin)
            , _spi_rate_hz(spi_rate_hz) {}
        void init();
        void write(uint8_t value, bool decimal=false);

    private:
        uint8_t _spi_rclk_pin;
        uint32_t _spi_rate_hz;

        uint8_t digit_to_seg(uint8_t digit, bool decimal=false);

};

#endif /* SEVEN_SEG_H */