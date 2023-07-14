def reverse_endianness(byte):
        reversed = 0x00
        for i in range(8):
            bit = (byte & (0b1<<i))>>i
            reversed |= bit << (7-i)
        return reversed

byte = 0b10101110
print(f"{reverse_endianness(byte):b}")