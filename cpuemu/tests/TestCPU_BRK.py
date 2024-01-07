import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_BRK(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_brk(self):
        # Setting up initial conditions
        self.cpu.reset()
        initial_pc = self.cpu.PC.value
        self.cpu.memory.load_data(0x0000, [OPCODES['BRK']['code']])  # Load BRK instruction, assuming its opcode is 0x03

        # Check the initial status of B flag
        self.assertEqual(self.cpu.status.B, 0)  # Initially B should be 0

        # Execute BRK instruction
        self.cpu.step()
        # Assert that B is now set
        self.assertEqual(self.cpu.status.B, 1)


if __name__ == "__main__":
    unittest.main()
