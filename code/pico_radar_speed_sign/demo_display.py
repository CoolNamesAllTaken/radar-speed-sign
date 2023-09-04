from bigass_7_segment import Bigass7SegmentDisplay
from radar_sensor import HB100
import utime

class DemoDisplay:
    DISPLAY_MODE_CHANGE_INTERVAL_SEC = 30

    COUNTER_MAX_VALUE = 99
    COUNTER_SPEED_SEC = 0.1

    SCROLL_TEXT_MESSAGE = "OPEN SAUCE BAYBEEE LESGO "
    SCROLL_TEXT_SPEED_SEC = 0.5 # seconds per digit

    MS_PER_SEC = 1000

    class DisplayMode:
        COUNT_UP = 0
        SCROLL_TEXT = 1
        RADAR_SIGN = 2

    counter_value = 0

    def __init__(self, display: Bigass7SegmentDisplay, hb100: HB100):
        self.display = display

        self.display_mode = self.DisplayMode.COUNT_UP
        self.next_display_mode_change_timestamp_ms = utime.ticks_ms() + self.DISPLAY_MODE_CHANGE_INTERVAL_SEC

        self.scroll_text_message = self.SCROLL_TEXT_MESSAGE + ('').join([' ' for i in range(self.display.num_digits)]) # pad with tail to enable scrolling to the last character

        self.hb100 = hb100
    
    def reset(self):
        """
        Resets all timers, counters, etc.
        """
        self.counter_value = 0
        self.counter_next_update_ms = utime.ticks_ms() + self.COUNTER_SPEED_SEC * self.MS_PER_SEC

        self.scroll_text_index = 0
        self.scroll_text_next_update_ms = utime.ticks_ms() + self.SCROLL_TEXT_SPEED_SEC * self.MS_PER_SEC
    
    def begin(self):
        """
        Alias for reset(). Call during startup.
        """
        self.reset()
        self.display.set_brightness(0.1) # spare us
    
    def update(self):
        if utime.ticks_ms() >= self.next_display_mode_change_timestamp_ms:
            self.next_display_mode_change_timestamp_ms = utime.ticks_ms() + self.DISPLAY_MODE_CHANGE_INTERVAL_SEC * self.MS_PER_SEC
            self.display_mode += 1 # if we jump into an invalid mode it will get sorted out next time around
            self.reset()

        display_text = "ER"
        if self.display_mode == self.DisplayMode.COUNT_UP:
            if utime.ticks_ms() >= self.counter_next_update_ms:
                # Time to increment the counter.
                self.counter_next_update_ms = utime.ticks_ms() + self.COUNTER_SPEED_SEC * self.MS_PER_SEC
                self.counter_value += 1
                # Wrap counter value if needed.
                if self.counter_value >= self.COUNTER_MAX_VALUE:
                    self.counter_value = 0
            display_text = str(self.counter_value)
        elif self.display_mode == self.DisplayMode.SCROLL_TEXT:
            if utime.ticks_ms() >= self.scroll_text_next_update_ms:
                # Time to shift the text.
                self.scroll_text_next_update_ms = utime.ticks_ms() + self.SCROLL_TEXT_SPEED_SEC * self.MS_PER_SEC
                self.scroll_text_index += 1
                if self.scroll_text_index >= len(self.SCROLL_TEXT_MESSAGE):
                    self.scroll_text_index = 0

            display_text = self.scroll_text_message[self.scroll_text_index:self.scroll_text_index+self.display.num_digits]
        elif self.display_mode == self.DisplayMode.RADAR_SIGN:
            self.hb100.update()
            display_text = self.hb100.get_speed_str()
        else: # invalid display mode, reset
            self.display_mode = self.DisplayMode.COUNT_UP
            display_text = "  " # blanking during transition
        
        self.display.set_digits(str(display_text))
        self.display.write()