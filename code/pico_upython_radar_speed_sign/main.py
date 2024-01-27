from machine import SPI, Pin
from bigass_7_segment import Bigass7SegmentDisplay
from radar_sensor import HB100
from demo_display import DemoDisplay
import utime

SOFTWARE_VERSION = "0.2.0"

DEMO_MODE = False

DIGITS_SPI_PORT = 0
DIGITS_SPI_MOSI_PIN = 19
DIGITS_SPI_SCK_PIN = 18
DIGITS_SPI_SRCLR_PIN = 17
DIGITS_RCLK_PIN = 16
DIGITS_OE_PIN = 21 # active low

DISPLAY_NUM_DIGITS = 2

RADAR_PIN = 28

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

    # Start up the ISR for the HB100 radar.
    hb100 = HB100()
    radar_pin = Pin(RADAR_PIN, mode=Pin.IN)
    def rising_edge_isr_sorter(pin):
        if pin == radar_pin:
            # print("hi")
            hb100.rising_edge_isr()
    radar_pin.irq(trigger=Pin.IRQ_FALLING, handler=rising_edge_isr_sorter)

    brightness_change_pin = Pin(BRIGHTNESS_CHANGE_PIN, Pin.IN, Pin.PULL_UP)
    brightness_change_debounce_timestamp_ms = utime.ticks_ms()
    brightness_index = 0

    demo = DemoDisplay(display, hb100)
    if DEMO_MODE:
        demo.begin()

    # display_value = 0
    while(True):
        if not brightness_change_pin.value() and utime.ticks_ms() > brightness_change_debounce_timestamp_ms:
            brightness_change_debounce_timestamp_ms = utime.ticks_ms() + BRIGHTNESS_CHANGE_DEBOUNCE_MS
            brightness_index += 1
            if brightness_index >= len(BRIGHTNESS_VALUES):
                brightness_index = 0
            display.set_brightness(BRIGHTNESS_VALUES[brightness_index])
        
        if DEMO_MODE:
            demo.update()
            print(f"speed={hb100.get_speed()}")
        else:
            hb100.update()
            speed_str = hb100.get_speed_str()
            display.set_digits(speed_str)
            display.write()

if __name__ == "__main__":
    main()