from CPU.Byte import Byte


class Word:
    def __init__(self, low_byte=Byte(0), high_byte=Byte(0)):
        self.low_byte = low_byte
        self.high_byte = high_byte

    def __repr__(self):
        return f"Word({self.low_byte.value}, {self.high_byte.value})"

    @property
    def value(self):
        return (self.high_byte.value << 8) | self.low_byte.value

    @value.setter
    def value(self, new_val):
        if not (0 <= new_val <= 65535):
            raise ValueError("Word value out of range (0-65535)")
        self.low_byte = Byte(new_val & 0xFF)
        self.high_byte = Byte((new_val >> 8) & 0xFF)
