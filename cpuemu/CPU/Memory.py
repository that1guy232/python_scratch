from CPU.Byte import Byte
from CPU.Word import Word


class Memory:
    def __init__(self, size=1024 * 32):  # max memory is 8bits
        self.total_memory = size
        self._data = [Byte(0) for _ in range(size)]
        # Put a BRK opcode at the end for safety or at the end of the first word size.
        # This should be overwritten by any program.
        if self.total_memory > 65534 - 1:
            self._data[65533] = Byte(0x03)
        else:
            self._data[-1] = Byte(0x03)  # Assuming 0x03 is the opcode for BRK

    def read_byte(self, address):
        if 0 <= address < self.total_memory:
            return self._data[address].value
        else:
            raise ValueError(f"Memory access out of bounds: {address}")

    def write_byte(self, address, value):
        if 0 <= address < self.total_memory:
            self._data[address] = Byte(value)
        else:
            raise ValueError(f"Memory access out of bounds: {address}")

    def load_data(self, start_address, data):
        """Load data into memory starting from the given address."""
        for i, val in enumerate(data):
            self.write_byte(start_address + i, val)

    def dump(self, start_address=0, end_address=None, bytes_per_row=16):
        """Return a formatted string representation of the memory content between start and end addresses."""
        if end_address is None:
            end_address = len(self._data)
        rows = []
        for i in range(start_address, end_address, bytes_per_row):
            row = ' '.join(f"{self.read_byte(addr):02X}" for addr in range(i, min(i + bytes_per_row, end_address)))
            rows.append(row)
        return '\n'.join(rows)

    def read_word(self, address):
        """Read a word (two bytes) from the given address."""
        if 0 <= address < self.total_memory - 1:  # Ensure there is space for a whole word
            low_byte = self.read_byte(address)
            high_byte = self.read_byte(address + 1)
            return Word(Byte(low_byte), Byte(high_byte))
        else:
            raise ValueError(f"Memory access out of bounds: {address}")

    def write_word(self, address, value):
        """Write a word (two bytes) to the given address."""
        if 0 <= address < self.total_memory - 1:  # Ensure there is space for a whole word
            self.write_byte(address, value.low_byte.value)
            self.write_byte(address + 1, value.high_byte.value)
        else:
            raise ValueError(f"Memory access out of bounds: {address}")
