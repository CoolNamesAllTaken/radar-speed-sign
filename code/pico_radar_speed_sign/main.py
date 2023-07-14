from machine import SPI, Pin
from bigass_7_segment import Bigass7SegmentDisplay
from demo_display import DemoDisplay
import utime

SOFTWARE_VERSION = "0.1.0"

DIGITS_SPI_PORT = 0
DIGITS_SPI_MOSI_PIN = 19
DIGITS_SPI_SCK_PIN = 18
DIGITS_SPI_SRCLR_PIN = 17
DIGITS_RCLK_PIN = 16
DIGITS_OE_PIN = 21 # active low

DISPLAY_NUM_DIGITS = 2

BRIGHTNESS_CHANGE_PIN = 0
BRIGHTNESS_CHANGE_DEBOUNCE_MS = 500
BRIGHTNESS_VALUES = [1.0, 0.5, 0.1]

def main():
    print(f"Pico Radar Speed Sign {SOFTWARE_VERSION}")
    print("pantsforbirds.com")

    # Initialize the SPI peripheral to talk to the shift registers.
    digits_spi = SPI(
        DIGITS_SPI_PORT,
        baudrate=57600,
        polarity=1,
        phase=1,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(DIGITS_SPI_SCK_PIN, Pin.OUT),
        mosi=Pin(DIGITS_SPI_MOSI_PIN, Pin.OUT)
    )

    # Start up the 7-segment display driver.
    display = Bigass7SegmentDisplay(DISPLAY_NUM_DIGITS, digits_spi, DIGITS_SPI_SRCLR_PIN, DIGITS_RCLK_PIN, DIGITS_OE_PIN)
    display.begin()

    brightness_change_pin = Pin(BRIGHTNESS_CHANGE_PIN, Pin.IN, Pin.PULL_UP)
    brightness_change_debounce_timestamp_ms = utime.ticks_ms()
    brightness_index = 0

    demo = DemoDisplay(display)
    demo.begin()

    # display_value = 0
    while(True):
        if not brightness_change_pin.value() and utime.ticks_ms() > brightness_change_debounce_timestamp_ms:
            brightness_change_debounce_timestamp_ms = utime.ticks_ms() + BRIGHTNESS_CHANGE_DEBOUNCE_MS
            brightness_index += 1
            if brightness_index >= len(BRIGHTNESS_VALUES):
                brightness_index = 0
            display.set_brightness(BRIGHTNESS_VALUES[brightness_index])
        
        demo.update()

if __name__ == "__main__":
    main()