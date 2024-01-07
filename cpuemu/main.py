from CPU.Assembler import Assembler
from CPU.CPU import CPU
from CPU.Memory import Memory
import pygame

if __name__ == "__main__":
    # Create an instance of the CPU.
    asm = Assembler()
    program = [
        'LDA 0x10',
        'STA 0x14',
        'LDX 0x20',
        'STX 0x15',
        'BRK'
    ]
    bytecode = asm.assemble(program)

    memory = Memory()  # Ram
    cpu = CPU(memory)
    cpu.memory.load_data(0x0, bytecode)
    #print(memory.dump())
    cpu.run()
    print(memory.dump())



