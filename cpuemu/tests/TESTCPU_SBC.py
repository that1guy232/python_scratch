import unittest
from CPU.CPU import CPU
from CPU.Memory import Memory
from CPU.opcodes import OPCODES


class TestCPU_SBC(unittest.TestCase):

    def setUp(self):
        """Initialize the CPU for each test."""
        self.cpu = CPU(Memory())

    def test_sbc_no_borrow(self):
        # Test SBC where no borrow is expected
        self.cpu.reset()
        self.cpu.A.value = 0x05
        self.cpu.status.C = 1  # Set carry (which means no borrow in the SBC instruction)
        self.cpu.memory.load_data(0x0000, [OPCODES['SBC']['code'], 0x02])

        # Execute SBC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x03)
        self.assertEqual(self.cpu.status.C, 1)  # Expecting no borrow
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

    def test_sbc_borrow(self):
        # Test SBC where a borrow is expected
        self.cpu.reset()
        self.cpu.A.value = 0x00
        self.cpu.status.C = 0  # Clear carry (which means borrow in the SBC instruction)
        self.cpu.memory.load_data(0x0000, [OPCODES['SBC']['code'], 0x01])

        # Execute SBC instruction
        self.cpu.step()

        # 0x00 - 0x01 - borrow (since C flag is 0) should give us 0xFF after the wraparound
        self.assertEqual(self.cpu.A.value, 0xFF)  # 0xFF is the correct result after the borrow
        self.assertEqual(self.cpu.status.C, 0)  # Borrow occurred
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 1)  # Result is negative due to sign bit being set

    def test_sbc_overflow(self):
        # Test SBC with overflow
        self.cpu.reset()
        self.cpu.A.value = 0x80
        self.cpu.status.C = 1  # Set carry (no borrow)
        self.cpu.memory.load_data(0x0000, [OPCODES['SBC']['code'], 0x01])

        # Execute SBC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x7F)
        self.assertEqual(self.cpu.status.C, 1)  # No borrow
        self.assertEqual(self.cpu.status.V, 1)  # Overflow occurred (from negative to positive)
        self.assertEqual(self.cpu.status.Z, 0)  # Result is not zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

    def test_sbc_zero_result(self):
        # Test SBC resulting in zero
        self.cpu.reset()
        self.cpu.A.value = 0x01
        self.cpu.status.C = 1  # Set carry (no borrow)
        self.cpu.memory.load_data(0x0000, [OPCODES['SBC']['code'], 0x01])

        # Execute SBC instruction
        self.cpu.step()

        self.assertEqual(self.cpu.A.value, 0x00)
        self.assertEqual(self.cpu.status.C, 1)  # No borrow
        self.assertEqual(self.cpu.status.V, 0)  # No overflow
        self.assertEqual(self.cpu.status.Z, 1)  # Result is zero
        self.assertEqual(self.cpu.status.N, 0)  # Result is positive

# The rest of the test cases can follow similar logic, considering various edge cases.
