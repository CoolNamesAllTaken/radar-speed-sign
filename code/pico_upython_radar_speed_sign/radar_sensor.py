from machine import Pin
import utime

class HB100:
    LOW_PASS_FILTER_WEIGHT = 1.0 # 1.0 = no filtering
    HOLD_INTERVAL_MS = 500
    SPEED_BUFFER_SIZE = 10
    SPEED_BUFFER_SAMPLE_INTERVAL_MS = 10

    class SpeedFilterMode:
        LOW_PASS = 0
        BUFFER_MAX = 1

    def __init__(self):
        self.last_rising_edge_timestamp_us = utime.ticks_us()
        self.last_pulse_period_us = 1000000 # default to very low speed
        self.speed = 0
        self.hold_end_timestamp_ms = utime.ticks_ms()

        self.speed_filter_mode = self.SpeedFilterMode.BUFFER_MAX
        self.speed_buffer = [0.0]*self.SPEED_BUFFER_SIZE
        self.speed_buffer_index = 0
        self.speed_buffer_prev_index = self.SPEED_BUFFER_SIZE-1
        self.speed_buffer_next_sample_timestamp_ms = 0
    
    def increment_speed_buffer_index(self, index):
        """
        Helper function for wrapping indices on the speed buffer.
        """
        if index >= len(self.speed_buffer)-1:
            return 0
        return index + 1

    def rising_edge_isr(self):
        """
        Interrupt service routine for rising edge on radar pin.
        """
        timestamp_us = utime.ticks_us()
        self.last_pulse_period_us = timestamp_us - self.last_rising_edge_timestamp_us
        self.last_rising_edge_timestamp_us = timestamp_us

        self.hold_end_timestamp_ms = utime.ticks_ms() + self.HOLD_INTERVAL_MS # fresh signal delays blank

        if self.last_pulse_period_us == 0:
            self.speed = 0 # prevent divide by zero
        else:
            new_speed = 31360 / self.last_pulse_period_us # V = Fd / 31.36, Fd = 1 / last_pulse_period[s]
            if self.speed_filter_mode == self.SpeedFilterMode.LOW_PASS:
                self.speed = new_speed * self.LOW_PASS_FILTER_WEIGHT + (1 - self.LOW_PASS_FILTER_WEIGHT)*self.speed    
            elif self.speed_filter_mode == self.SpeedFilterMode.BUFFER_MAX:
                sample_timestamp = utime.ticks_ms()
                if sample_timestamp < self.speed_buffer_next_sample_timestamp_ms:
                    return # limit buffer updates so that faster speeds don't fall out of the buffer too quickly
                self.speed_buffer[self.speed_buffer_index] = new_speed * self.LOW_PASS_FILTER_WEIGHT + (1 - self.LOW_PASS_FILTER_WEIGHT)*self.speed_buffer[self.speed_buffer_prev_index]
                self.speed_buffer_next_sample_timestamp_ms = sample_timestamp + self.SPEED_BUFFER_SAMPLE_INTERVAL_MS
                self.speed_buffer_index = self.increment_speed_buffer_index(self.speed_buffer_index)
                self.speed_buffer_prev_index = self.increment_speed_buffer_index(self.speed_buffer_prev_index)

                self.speed = max(self.speed_buffer)

    def update(self):
        """
        Called frequently to update filters and holds.
        """
        if utime.ticks_ms() >= self.hold_end_timestamp_ms:
            self.speed = 0
            self.speed_buffer = [0] * self.SPEED_BUFFER_SIZE


    def get_speed(self):
        return self.speed
    
    def get_speed_str(self):
        """
        Return a nicely formatted string with an integer speed value in mph, with blanking
        for zero values.
        """
        speed = round(self.get_speed())
        if speed == 0:
            return "  "
        else:
            return str(speed)


