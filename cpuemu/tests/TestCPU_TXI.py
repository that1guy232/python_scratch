import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory


class TestCPU_TXI(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU and Memory for each test."""
        self.cpu = CPU(Memory())
        self.cpu.reset()

    def test_TAX_transfers_A_to_X_with_non_zero_value(self):
        # Load A with a non-zero value and execute TAX instruction
        self.cpu.A.value = 0x20
        self.cpu._TAX()

        # Assert X register has the value of A and status flags are correct
        self.assertEqual(self.cpu.X.value, 0x20)
        self.assertEqual(self.cpu.status.Z, 0)  # Not Zero
        self.assertEqual(self.cpu.status.N, 0)  # Positive value

    def test_TAY_transfers_A_to_Y_with_zero_value(self):
        # Load A with zero and execute TAY instruction
        self.cpu.A.value = 0x00
        self.cpu._TAY()

        # Assert Y register has the value of A and status flags are correct
        self.assertEqual(self.cpu.Y.value, 0x00)
        self.assertEqual(self.cpu.status.Z, 1)  # Zero
        self.assertEqual(self.cpu.status.N, 0)  # Positive value

    def test_TXA_transfers_X_to_A_with_negative_value(self):
        # Load X with a negative value (0x80 or higher) and execute TXA instruction
        self.cpu.X.value = 0x80
        self.cpu._TXA()

        # Assert A register has the value of X and status flags are correct
        self.assertEqual(self.cpu.A.value, 0x80)
        self.assertEqual(self.cpu.status.Z, 0)  # Not Zero
        self.assertEqual(self.cpu.status.N, 1)  # Negative value

    def test_TYA_transfers_Y_to_A_with_non_zero_value(self):
        # Load Y with a non-zero value and execute TYA instruction
        self.cpu.Y.value = 0x01
        self.cpu._TYA()

        # Assert A register has the value of Y and status flags are correct
        self.assertEqual(self.cpu.A.value, 0x01)
        self.assertEqual(self.cpu.status.Z, 0)  # Not Zero
        self.assertEqual(self.cpu.status.N, 0)  # Positive value


if __name__ == "__main__":
    unittest.main()
