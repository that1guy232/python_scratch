import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_ADC(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_adc_no_flags(self):
        self.cpu.reset()
        self.cpu.A.value = 0x02
        self.cpu.memory.load_data(0x0000, [OPCODES['LDA']['code'], 0x05])  # Load immediate value 0x03 to be added
        # Execute ADC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x05)
        self.assertEqual(self.cpu.status.C, 0)  # No carry
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

    def test_adc_with_carry(self):
        self.cpu.reset()
        self.cpu.A.value = 0xFF
        self.cpu.status.C = 1  # Set carry
        self.cpu.memory.load_data(0x0000, [OPCODES['LDA']['code'], 0x01])  # Load immediate value 0x01 to be added

        # Execute ADC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x01)
        self.assertEqual(self.cpu.status.C, 1)  # There should be a carry
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

    def test_adc_with_overflow(self):
        self.cpu.reset()
        self.cpu.A.value = 0x7F
        self.cpu.memory.load_data(0x0000, [OPCODES['ADC']['code'], 0x02])  # Load immediate value 0x02 to be added

        # Execute ADC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x81)
        self.assertEqual(self.cpu.status.C, 0)  # No carry
        self.assertEqual(self.cpu.status.V, 1)  # Overflow occurred
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 1)  # Result is negative

    def test_adc_zero_result(self):
        self.cpu.reset()
        self.cpu.A.value = 0x02
        self.cpu.memory.load_data(0x0000, [OPCODES['ADC']['code'], 0xFE])

        # Execute ADC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x00)
        self.assertEqual(self.cpu.status.C, 1)  # Expecting a carry
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 1)  # Result is zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive


if __name__ == "__main__":
    unittest.main()
