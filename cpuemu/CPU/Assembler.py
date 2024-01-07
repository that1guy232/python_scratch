from CPU.opcodes import OPCODES


class Assembler:
    @classmethod
    def assemble(cls, program):
        """Assemble a program into bytecode."""
        bytecode = []
        for line in program:
            parts = line.split(' ', 1)
            instruction = parts[0]
            operand = None if len(parts) == 1 else parts[1]

            opcode_data = OPCODES.get(instruction.upper())
            if opcode_data is None:
                raise ValueError(f"Unknown instruction: {instruction}")

            bytecode.append(opcode_data['code'])

            if operand:
                bytecode.append(int(operand, 16))

        return bytecode
