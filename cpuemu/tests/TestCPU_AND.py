import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_AND(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_and_operation(self):
        # Given
        self.cpu.reset()
        self.cpu.A.value = 0b10101010  # Load the accumulator with an initial value
        immediate_value = 0b11000011
        expected_result = self.cpu.A.value & immediate_value

        # When
        self.cpu.memory.load_data(0x0000, [OPCODES['AND']['code'], immediate_value])
        self.cpu.step()  # Execute the AND instruction

        # Then
        self.assertEqual(self.cpu.A.value, expected_result)
        self.assertEqual(self.cpu.status.Z, expected_result == 0)
        self.assertEqual(self.cpu.status.N, (expected_result & 0x80) != 0)

    def test_and_zero_flag(self):
        # Given
        self.cpu.reset()
        self.cpu.A.value = 0b10101010
        immediate_value = 0b01010101  # This will result in zero when ANDed with A

        # When
        self.cpu.memory.load_data(0x0000, [OPCODES['AND']['code'], immediate_value])
        self.cpu.step()  # Execute the AND instruction

        # Then
        expected_result = self.cpu.A.value & immediate_value
        self.assertEqual(self.cpu.A.value, 0)
        self.assertEqual(self.cpu.status.Z, int(expected_result == 0))  # Convert boolean to integer
        self.assertEqual(self.cpu.status.N, 0)


if __name__ == "__main__":
    unittest.main()
