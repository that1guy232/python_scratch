class Byte:
    def __init__(self, value=0):
        if not (0 <= value <= 255):
            raise ValueError("Byte value out of range (0-255)")
        self._value = value

    def __repr__(self):
        return f"Byte({self._value})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        if not (0 <= new_val <= 255):
            raise ValueError("Byte value out of range (0-255)")
        self._value = new_val
