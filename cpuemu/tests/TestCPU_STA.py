import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_STA(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_store_A(self):
        self.cpu.reset()
        self.cpu.A.value = 0xF  # Set Accumulator to 0xF
        self.cpu.memory.load_data(0x0000, [OPCODES['STA']['code'], 0x04])  # Store A value at 0x04
        self.cpu.step()
        self.assertEqual(self.cpu.memory.read_byte(0x04), 0xF)


class TestCPU_STX(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_store_X(self):
        self.cpu.reset()
        self.cpu.X.value = 0x7F  # Set X register to 0x7F
        self.cpu.memory.load_data(0x0000, [OPCODES['STX']['code'], 0x04])  # Store X value at 0x04
        self.cpu.step()
        self.assertEqual(self.cpu.memory.read_byte(0x04), 0x7F)


class TestCPU_STY(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_store_Y(self):
        self.cpu.reset()
        self.cpu.Y.value = 0x7F  # Set Y register to 0x7F
        self.cpu.memory.load_data(0x0000, [OPCODES['STY']['code'], 0x05])
        self.cpu.step()
        self.assertEqual((self.cpu.memory.read_byte(0x05)), 0x7f)


if __name__ == "__main__":
    unittest.main()
