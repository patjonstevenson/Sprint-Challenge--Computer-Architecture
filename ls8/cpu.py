"""CPU functionality."""
from dispatch_table import DispatchTable
import sys
from ast import literal_eval
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0, 0, 0, 0, 0, 0, 0, 255]
        self.running = False
        self.pc = 0
        self.program_file = None
        self.dispatch_table = DispatchTable(self)

    def get_pc(self):
        return self.pc

    def get_sp(self):
        return self.reg[7]

    def increment_pc(self, num=1):
        for i in range(num):
            self.pc += 1
    
    def decrement_pc(self, num=1):
        for i in range(num):
            self.pc -= 1

    def increment_sp(self, num=1):
        for i in range(num):
            self.reg[7] += 1
    
    def decrement_sp(self, num=1):
        for i in range(num):
            self.reg[7] -= 1

    def load(self, file=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if file is None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]
        else:
            program = []
            file_text = open(file, "r")
            for f in file_text:
                if f[0] == '#':
                    continue
                elif f[0] == '\n':
                    continue
                elif " " in f:
                    f = f[:f.find(" ")]
                program.append(literal_eval('0b'+f))
            #     print(f"INSTRUCTION: {program[:-1]}")
            # print(f"PROGRAM:\n{program}")

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a+operand_b, reg_a)
        elif op == "SUB":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a-operand_b, reg_a)
        elif op == "MUL":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a*operand_b, reg_a)
        elif op == "DIV":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a/operand_b, reg_a)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        self.pc = 0

        while self.running:
            cmd = self.ram_read(self.pc)
            self.dispatch_table.execute(cmd)
            
    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, data, addr):
        self.ram[addr] = data

    def reg_read(self, addr):
        return self.reg[addr]

    def reg_write(self, data, addr):
        self.reg[addr] = data