from CPU.Byte import Byte


class StatusFlags:
    def __init__(self):
        self._value = Byte()  # The byte storing all the flags
        self.reset()

    def reset(self):
        """Reset the status flags to their default values."""
        self._value = Byte()
        # If you want the Zero flag to be 1 on reset:
        self.Z = 1

    # 0: Carry Flag
    @property
    def C(self):
        return (self._value.value >> 0) & 1

    @C.setter
    def C(self, val):
        self._value.value = (self._value.value & ~0b00000001) | (val << 0)

    # 1: Zero Flag
    @property
    def Z(self):
        return (self._value.value >> 1) & 1

    @Z.setter
    def Z(self, val):
        self._value.value = (self._value.value & ~0b00000010) | (val << 1)

    # 2: Break Command
    @property
    def B(self):
        return (self._value.value >> 4) & 1

    @B.setter
    def B(self, val):
        self._value.value = (self._value.value & ~0b00010000) | (val << 4)

    # 6: Overflow
    @property
    def V(self):
        return (self._value.value >> 6) & 1

    @V.setter
    def V(self, val):
        self._value.value = (self._value.value & ~0b01000000) | (val << 6)

    # 7: Negative
    @property
    def N(self):
        return (self._value.value >> 7) & 1

    @N.setter
    def N(self, val):
        self._value.value = (self._value.value & ~0b10000000) | (val << 7)

    # 3: Unused
    @property
    def Unused(self):
        return (self._value.value >> 3) & 1

    @Unused.setter
    def Unused(self, val):
        self._value.value = (self._value.value & ~0b00001000) | (val << 3)

    # 3: Unused
    @property
    def Unused_(self):
        return (self._value.value >> 5) & 1

    @Unused_.setter
    def Unused_(self, val):
        self._value.value = (self._value.value & ~0b00100000) | (val << 5)

    # 2: Unused
    @property
    def Unused__(self):
        return (self._value.value >> 2) & 1

    @Unused__.setter
    def Unused__(self, val):
        self._value.value = (self._value.value & ~0b00000100) | (val << 2)
