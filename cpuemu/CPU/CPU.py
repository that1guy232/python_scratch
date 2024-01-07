from CPU.Byte import Byte
from CPU.Memory import Memory
from CPU.StatusFlags import StatusFlags
from CPU.Word import Word
from .opcodes import OPCODES


# Collapse Ctrl + Shift + NumPad *, 1.
class CPU:
    """
    A CPU simulation, interprets & executes instructions for a simple CPU.
    """

    def __init__(self, memory):
        """
        Initializes the CPU with memory and default register values.
        Args:
            :param memory: An instance of the Memory Class, over all Systems RAM/Memory
        """

        self.memory = memory
        self.status = StatusFlags()
        self.PC = Word()  # Program Counter
        self.SP = Word()  # Stack Pointer
        self.SP.value = self.memory.total_memory

        # Registers
        self.A = Byte()
        self.X = Byte()
        self.Y = Byte()

        # Decode opcode mappings to their respective instructions.
        self.INSTRUCTIONS = {v['code']: getattr(self, v['method']) for k, v in OPCODES.items()}

    def reset(self):
        """
        Resets the CPU state, including memory, registers, program counter,
        stack pointer, and status flags.
        """

        self.memory = Memory()

        # Reset registers
        self.A = Byte()
        self.X = Byte()
        self.Y = Byte()

        # Reset Program Counter and Stack Pointer
        self.PC.value = 0x0000  # Default startup address
        self.SP.value = self.memory.total_memory
        self.status.reset()

    def run(self):
        """
        Runs the CPU, executing instructions until the break (BRK) instruction is encountered.
        """
        while not self.status.B:
            self.step()

    def step(self):
        """Perform one CPU cycle"""
        """
        Performs a single instruction cycle: fetch, decode, and execute.
        """
        opcode = self._fetch()
        self._decode_and_execute(opcode)

    def _fetch(self):
        """
        Fetches the next instruction byte from memory.

        :return: The opcode at the current program counter location.
        """
        opcode = self.memory.read_byte(self.PC.value)
        self.PC.value += 1  # Increase the program counter
        return opcode

    def _decode_and_execute(self, opcode):
        """
        Decodes the fetched opcode and executes the corresponding instruction.

        :param opcode: The opcode to decode and execute.
        """
        if opcode in self.INSTRUCTIONS:
            instruction = self.INSTRUCTIONS[opcode]
            instruction()
        else:
            if opcode != 0x00:
                print(f"Unknown opcode: {opcode:02x}")

    def _update_zero_and_negative_flags(self, value):
        """
        Updates the zero and negative flags based on the given value.

        :param value: The result of the last operation to check for zero and negative status.
        """
        self.status.Z = 1 if value == 0 else 0
        self.status.N = 1 if (value & 0x80) != 0 else 0

    def _fetch_next_byte(self):
        """
        Fetches the next byte following the current program counter-value.

        :return: The next byte value from memory.
        """
        value = self.memory.read_byte(self.PC.value)
        self.PC.value += 1
        return value

    def _fetch_next_word(self):
        """
        Fetches the next word (two bytes) following the current program counter-value.

        :return: The next word value from memory.
        """
        value = self.memory.read_word(self.PC.value)
        self.PC += 2
        return value

    ###
    ## CPU INSTRUCTIONS
    ###

    ## LOADS`
    def _load_register(self, register):
        """
        Loads the given register with the next byte from memory.

        :param register: The CPU register to load the value into.
        """
        register.value = self._fetch_next_byte()
        self._update_zero_and_negative_flags(register.value)

    def _LDA(self):
        """ Loads the Accumulator (A) with the next byte from memory. """
        self._load_register(self.A)

    def _LDX(self):
        """ Loads the X index register with the next byte from memory. """
        self._load_register(self.X)

    def _LDY(self):
        """ Loads the Y index register with the next byte from memory. """
        self._load_register(self.Y)

    ## Stores

    def _store_value(self, register_value):
        """Stores a value from a register into memory at a location specified by the next byte in the program counter."""
        self.memory.write_byte(self._fetch_next_byte(), register_value)

    def _STA(self):
        """Store Accumulator: Stores the value in the accumulator into memory."""
        self._store_value(self.A.value)

    def _STX(self):
        """Store X Register: Stores the value in the X register into memory."""
        self._store_value(self.X.value)

    def _STY(self):
        """Store Y Register: Stores the value in the Y register into memory."""
        self._store_value(self.Y.value)

    def _transfer_values(self, from_register, to_register):
        """Transfers the value from one register to another and updates zero and negative flags."""
        to_register.value = from_register.value
        self._update_zero_and_negative_flags(to_register.value)

    def _TAX(self):
        """Transfer Accumulator to X: Copies the current value of the accumulator to the X register."""
        self._transfer_values(self.A, self.X)

    def _TAY(self):
        """Transfer Accumulator to Y: Copies the current value of the accumulator to the Y register."""
        self._transfer_values(self.A, self.Y)

    def _TXA(self):
        """Transfer X to Accumulator: Copies the current value of the X register to the accumulator."""
        self._transfer_values(self.X, self.A)

    def _TYA(self):
        """Transfer Y to Accumulator: Copies the current value of the Y register to the accumulator."""
        self._transfer_values(self.Y, self.A)

    def _ADC(self):
        """Add with Carry: Adds a value to the accumulator along with the carry flag."""
        immediate_value = self._fetch_next_byte()
        temp = self.A.value + immediate_value + self.status.C
        self.status.V = 1 if ((self.A.value ^ temp) & (immediate_value ^ temp) & 0x80) != 0 else 0
        self.status.C = 1 if temp > 0xFF else 0
        self.A.value = temp & 0xFF
        self._update_zero_and_negative_flags(self.A.value)

    def _SBC(self):
        """Subtract with Borrow: Subtracts a value from the accumulator with the borrow determined by the carry flag."""
        immediate_value = self._fetch_next_byte()

        # Invert the bits of the immediate value when performing the subtraction, as 6502 considers carry flag as "no borrow" when set.
        value_with_carry = (immediate_value ^ 0xFF) + self.status.C

        # Store the original value of the accumulator before the subtraction
        original_a = self.A.value

        # Perform the subtraction using unsigned values
        result = original_a + value_with_carry

        # The & 0xFF ensures the result is within 0x00-0xFF, simulating an 8-bit wraparound
        self.A.value = result & 0xFF

        # Set the zero flag if the result is zero
        self.status.Z = 1 if self.A.value == 0 else 0

        # The negative flag is set if the result's most significant bit is 1
        self.status.N = 1 if (self.A.value & 0x80) != 0 else 0

        # The overflow flag (V) is set if the sign of the result is different from the sign of A
        # This happens when subtracting a positive number from a negative number or vice versa.
        # XOR the original and immediate values, and then XOR that with the result. If the 7th bit is set, then overflow occurred.
        self.status.V = 1 if ((original_a ^ value_with_carry) & (original_a ^ self.A.value) & 0x80) != 0 else 0

        # Carry flag is set if there is no borrow (i.e., if the unsigned result is 0 or positive)
        self.status.C = 1 if result < 0x100 else 0

    def _INC(self):
        """Increment Memory: Increments a memory location by one."""
        address = self._fetch_next_word()
        value = self.memory.read_byte(address)
        value = (value + 1) & 0xFF
        self.memory.write_byte(address, value)
        self._update_zero_and_negative_flags(value)

    def _DEC(self):
        """Decrement Memory: Decrements a memory location by one."""
        address = self._fetch_next_word()
        value = self.memory.read_byte(address)
        value = (value - 1) & 0xFF
        self.memory.write_byte(address, value)
        self._update_zero_and_negative_flags(value)

    def _BRK(self):
        """Break: Triggers a software interrupt."""
        self.status.B = 1

    def _AND(self):
        """Logical AND: Performs a bitwise AND operation on the accumulator and the next byte in memory."""
        value = self._fetch_next_byte()  # Fetch the immediate value
        self.A.value &= value  # Perform the AND operation
        self._update_zero_and_negative_flags(self.A.value)  # Update the flags

    #### TODO WIP BELOW HERE
    def _ORA(self):
        """Logical OR: Performs a bitwise OR operation on the accumulator and the next byte in memory."""
        value = self._fetch_next_byte()
        self.A.value |= value
        self._update_zero_and_negative_flags(self.A.value)

    def _EOR(self):
        """Logical XOR: Performs a bitwise XOR operation on the accumulator and the next byte in memory."""
        value = self._fetch_next_byte()
        self.A.value ^= value
        self._update_zero_and_negative_flags(self.A.value)

    def _CMP(self):
        """Compare: Compares the accumulator with the next byte in memory."""
        value = self._fetch_next_byte()
        self._compare(self.A.value, value)

    def _CPX(self):
        """Compare X Register: Compares the X register with the next byte in memory."""
        value = self._fetch_next_byte()
        self._compare(self.X.value, value)

    def _CPY(self):
        """Compare Y Register: Compares the Y register with the next byte in memory."""
        value = self._fetch_next_byte()
        self._compare(self.Y.value, value)

    def _compare(self, registry, address):
        """Compares the registry with the address and sets the zero, negative and carry flags accordingly."""
        result = registry - address
        self.status.C = 1 if result >= 0 else 0
        self._update_zero_and_negative_flags(result)
        pass

    # Control Instructions
    ## Jmp, JSR, RTS, Branching
    def _JMP(self):
        """Jump: Jumps to a new location in memory."""
        self.PC.value = self._fetch_next_word()

    def _JSR(self):
        """Jump to Subroutine: Jumps to a subroutine and saves the return address."""
        self._push_word(self.PC.value - 1)
        self.PC.value = self._fetch_next_word()

    def _RTS(self):
        """Return from Subroutine: Returns from a subroutine."""
        self.PC.value = self._pop_word() + 1

    def _branch_if(self, condition):
        """Branches if the condition is true."""
        address = self._fetch_next_byte()
        if condition:
            self.PC.value = address

    def _BCC(self):
        """Branch if Carry Clear: Branches if the carry flag is clear."""
        self._branch_if(not self.status.C)

    def _BCS(self):
        """Branch if Carry Set: Branches if the carry flag is set."""
        self._branch_if(self.status.C)

    def _BEQ(self):
        """Branch if Equal: Branches if the zero flag is set."""
        self._branch_if(self.status.Z)

    def _BNS(self):
        """Branch if Negative: Branches if the negative flag is set."""
        self._branch_if(self.status.N)

    def _BNE(self):
        """Branch if Not Equal: Branches if the zero flag is clear."""
        self._branch_if(not self.status.Z)

    def _BPL(self):
        """Branch if Positive: Branches if the negative flag is clear."""
        self._branch_if(not self.status.N)

    def _BVC(self):
        """Branch if Overflow Clear: Branches if the overflow flag is clear."""
        self._branch_if(not self.status.V)

    def _BVS(self):
        """Branch if Overflow Set: Branches if the overflow flag is set."""
        self._branch_if(self.status.V)

    ## Flag Instructions, sets and clears flags
    ## StatusFlags:
    #   .C Carry flag
    #   .Z Zero flag
    #   .B Break flag
    #   .V Overflow flag
    #   .N Negative flag
    def _CLC(self):
        """Clear Carry Flag: Clears the carry flag."""
        self.status.C = 0

    def _SEC(self):
        """Set Carry Flag: Sets the carry flag."""
        self.status.C = 1

    def _CLZ(self):
        """Clear Zero Flag: Clears the zero flag."""
        self.status.Z = 0

    def _SEZ(self):
        """Set Zero Flag: Sets the zero flag."""
        self.status.Z = 1

    def _CLB(self):
        """Clear Break Flag: Clears the break flag."""
        self.status.B = 0

    def _SEB(self):
        """Set Break Flag: Sets the break flag."""
        self.status.B = 1

    def _CLV(self):
        """Clear Overflow Flag: Clears the overflow flag."""
        self.status.V = 0

    def _SEV(self):
        """Set Overflow Flag: Sets the overflow flag."""
        self.status.V = 1

    def _CLN(self):
        """Clear Negative Flag: Clears the negative flag."""
        self.status.N = 0

    def _SEN(self):
        """Set Negative Flag: Sets the negative flag."""
        self.status.N = 1

    # Math Instructions (ASL, LSR, ROL, ROR)
    def _ASL(self):
        """Arithmetic Shift Left: Shifts all bits left one, shifting a 0 in on the right."""
        self._shift_left(self.A)

    def _LSR(self):
        """Logical Shift Right: Shifts all bits right one, shifting a 0 in on the left."""
        self._shift_right(self.A)

    def _ROL(self):
        """Rotate Left: Shifts all bits left one, shifting the carry flag in on the right."""
        self._rotate_left(self.A)

    def _ROR(self):
        """Rotate Right: Shifts all bits right one, shifting the carry flag in on the left."""
        self._rotate_right(self.A)

    def _shift_left(self, registry):
        """Shifts all bits left one, shifting a 0 in on the right."""
        self.status.C = registry.value & 0x80
        registry.value <<= 1
        self._update_zero_and_negative_flags(registry.value)

    def _shift_right(self, registry):
        """Shifts all bits right one, shifting a 0 in on the left."""
        self.status.C = registry.value & 0x01
        registry.value >>= 1
        self._update_zero_and_negative_flags(registry.value)

    def _rotate_left(self, registry):
        """Shifts all bits left one, shifting the carry flag in on the right."""
        carry = self.status.C
        self.status.C = registry.value & 0x80
        registry.value <<= 1
        registry.value |= carry
        self._update_zero_and_negative_flags(registry.value)

    def _rotate_right(self, registry):
        """Shifts all bits right one, shifting the carry flag in on the left."""
        carry = self.status.C
        self.status.C = registry.value & 0x01
        registry.value >>= 1
        registry.value |= carry << 7
        self._update_zero_and_negative_flags(registry.value)

    # Stack Instructions

    def _push_byte(self, byte):
        """Pushes a byte onto the stack."""
        self.memory.write(self.SP.value, byte)
        self.SP.value -= 1

    def _push_word(self, word):
        """Pushes a word onto the stack."""
        self._push_byte(word >> 8)
        self._push_byte(word & 0xFF)

    def _pop_byte(self):
        """Pops a byte off the stack."""
        self.SP.value += 1
        return self.memory.read(self.SP.value)

    def _pop_word(self):
        """Pops a word off the stack."""
        low_byte = self._pop_byte()
        high_byte = self._pop_byte()
        return (high_byte << 8) | low_byte

    def _PHA(self):
        """Push Accumulator: Pushes the accumulator onto the stack."""
        self._push_byte(self.A.value)

    def _PHP(self):
        """Push Processor Status: Pushes the processor status onto the stack."""
        self._push_byte(self.status)

    def _PLA(self):
        """Pull Accumulator: Pulls the accumulator from the stack."""
        self.A.value = self._pop_byte()
        self._update_zero_and_negative_flags(self.A.value)

    def _PLP(self):
        """Pull Processor Status: Pulls the processor status from the stack."""
        self.status = self._pop_byte()
