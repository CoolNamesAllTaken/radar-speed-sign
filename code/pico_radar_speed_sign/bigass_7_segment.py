from machine import Pin, SPI, PWM

class Bigass7SegmentDisplay:
    U16_MAX = 2**16-1
    SEG_DIGIT_DICT = {
        # These values are loaded into the SEG_DIGIT_DICT upon initialization
        # segment order is 0b<HGFEDCBA> (little endian)
        # <num>: 0b<HGFEDCBA> # <ABCDEFGH>

        '0': 0b11111100,
        '1': 0b01100000,
        '2': 0b11011010,
        '3': 0b11110010,
        '4': 0b01100110,
        '5': 0b10110110,
        '6': 0b10111110,
        '7': 0b11100000,
        '8': 0b11111110,
        '9': 0b11110110,
        'A': 0b11101110,
        'B': 0b00111110,
        'C': 0b10011100,
        'D': 0b01111010,
        'E': 0b10011110,
        'F': 0b10001110,
        'G': 0b10111100,
        'H': 0b01101110,
        'I': 0b01100000,
        'J': 0b01111000,
        # K
        'L': 0b00011100,
        # M
        'N': 0b00101010,
        'O': 0b11111100,
        'P': 0b11001110,
        'Q': 0b11100110,
        'R': 0b00001010,
        'S': 0b10110110,
        'T': 0b11100000,
        'U': 0b01111100,
        # V
        # W
        # X
        'Y': 0b01001110,
        'Z': 0b11011010,
        None: 0b00000000 # (blank)
    }


    _brightness = 1.0 # default to max brightness

    def __init__(
            self, 
            num_digits: int,
            spi,
            spi_cs_pin: int,
            digits_rclk_pin: int,
            digits_oe_pin: int
            ):
        """
        Constructor
        """
        self.num_digits = num_digits
        self.digits = [None] * self.num_digits # people interact with this one

        self._digits_buf = bytearray([self.SEG_DIGIT_DICT[ch] for ch in self.digits]) # for writing to segments
        self._spi = spi
        self._spi_srclr_pin = Pin(spi_cs_pin, Pin.OUT)
        self._digits_rclk_pin = Pin(digits_rclk_pin, Pin.OUT)
        self._oe_pin = PWM(Pin(digits_oe_pin))
        self._oe_pin.freq(int(25e3))
        self._oe_pin.duty_u16(0) # turn off until begin() is called
    
    def _reverse_byte(self, byte):
        """
        Utility function for reversing the endianness of a byte. Compensates for having shift registers
        wired up with segment A = output 1. If we want to read binary from left to right, segment A becomes
        the Most Significant Bit.
        """
        reversed = 0x00
        for i in range(8):
            bit = (byte & (0b1<<i))>>i
            reversed |= bit << (7-i)
        return reversed


    def _digit_to_seg(self, digit):
        """
        Private function that converts a character to a byte.
        """
        try: 
            seg = self.SEG_DIGIT_DICT[digit]
        except:
            seg = 0x00 # make unknown characters blank (uPython doesn't support defaultdict)
        
         # reverse from 0<bABCDEFGH> to 0b<HGFEDCBA>
        return int(self._reverse_byte(seg))
    
    def begin(self):
        self.set_brightness(self._brightness)
    
    def set_brightness(self, value: float):
        self._brightness = value
        self._oe_pin.duty_u16(int((1.0-self._brightness) * self.U16_MAX)) # enable digits (active LOW)
    
    def set_digits(self, digits_str):
        """
        Takes a string and puts it into the display buffer.
        """
        digits_str = f"{digits_str:>2}"[0:self.num_digits] # right aligned, max two digits
        for i, ch in enumerate(digits_str):
            self._digits_buf[self.num_digits-i-1] = self._digit_to_seg(ch)
            # if i >= self.num_digits-1: break

    def write(self):
        self._digits_rclk_pin.value(0)
        self._spi_srclr_pin.value(0)
        self._spi_srclr_pin.value(1)
        self._spi.write(self._digits_buf)
        self._digits_rclk_pin.value(1)
