import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_LDX(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_load_X_positive_value(self):
        self.cpu.reset()
        self.cpu.memory.load_data(0x0000, [OPCODES['LDX']['code'], 0x7F])  # Load immediate value 0x7F

        # Execute LDA instruction
        self.cpu.step()

        self.assertEqual(self.cpu.X.value, 0x7F)
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

    def test_load_X_negative_value(self):
        self.cpu.reset()
        self.cpu.memory.load_data(0x0000, [OPCODES['LDX']['code'], 0x80])  # Load immediate value 0x80

        # Execute LDA instruction
        self.cpu.step()

        self.assertEqual(self.cpu.X.value, 0x80)
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 1)  # Result is negative

    def test_load_X_zero(self):
        self.cpu.reset()
        self.cpu.memory.load_data(0x0000, [OPCODES['LDX']['code'], 0x00])  # Load immediate value 0x00

        # Execute LDA instruction
        self.cpu.step()

        self.assertEqual(self.cpu.X.value, 0x00)
        self.assertEqual(self.cpu.status.Z, 1)  # Result is zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive


if __name__ == "__main__":
    unittest.main()
