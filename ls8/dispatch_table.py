class DispatchTable:
    '''
    Contains a mapping of binary instructions to functions
    Initialized with a CPU instance
    '''
    def __init__(self, cpu):
        self.cpu = cpu
        self.table = {
            # ALU Operations
            0b10100000: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,

            # Other
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,

            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret
        }

    def execute(self, cmd):
        if cmd not in self.table:
            raise Exception(f"Unsupported Operation: {cmd}")
        else:
            instruction = self.table[cmd]
            instruction()

    def ldi(self):
        pc = self.cpu.get_pc()
        reg = self.cpu.ram_read(pc + 1)
        data = self.cpu.ram_read(pc + 2)
        self.cpu.reg_write(data, reg)
        self.cpu.increment_pc(3)
    
    def prn(self):
        pc = self.cpu.get_pc()
        reg = self.cpu.ram_read(pc + 1)
        data = self.cpu.reg_read(reg)
        print(data)
        self.cpu.increment_pc(2)
    
    def hlt(self):
        self.cpu.running = False
        self.cpu.increment_pc()

    def push(self):
        pc = self.cpu.get_pc()
        reg = self.cpu.ram_read(pc + 1)
        val = self.cpu.reg_read(reg)
        self.cpu.decrement_sp(1)
        sp = self.cpu.get_sp()
        self.cpu.ram_write(val, sp)
        self.cpu.increment_pc(2)
        
    def pop(self):
        pc = self.cpu.get_pc()
        sp = self.cpu.get_sp()
        reg = self.cpu.ram_read(pc + 1)
        stack_val = self.cpu.ram_read(sp)
        self.cpu.increment_sp(1)
        self.cpu.reg_write(stack_val, reg)
        self.cpu.increment_pc(2)
        
    def call(self):
        pc = self.cpu.get_pc()
        
        # Push return address to the stack
        self.cpu.decrement_sp()
        sp = self.cpu.get_sp()
        self.cpu.ram_write(pc + 2, sp)
        
        # Get the address of the subroutine
        reg = self.cpu.ram_read(pc + 1)
        rout_addr = self.cpu.reg_read(reg)

        # Set pc to address of subroutine
        diff = pc - rout_addr
        if diff > 0:
            self.cpu.decrement_pc(diff)
        elif diff < 0:
            self.cpu.increment_pc(abs(diff))
        else:
            raise ProcessLookupError(f'The subroutine at address {rout_addr} is the current address.')
        
    def ret(self):
        sp = self.cpu.get_sp()
        ret_addr = self.cpu.ram_read(sp)
        self.cpu.increment_sp()
        pc = self.cpu.get_pc()
        diff = pc - ret_addr
        if diff > 0:
            self.cpu.decrement_pc(diff)
        elif diff < 0:
            self.cpu.increment_pc(abs(diff))

    # ALU Operations
    def add(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a + operand_b, reg_a)
        self.cpu.increment_pc(3)

    def sub(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a - operand_b, reg_a)
        self.cpu.increment_pc(3)

    def mul(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a * operand_b, reg_a)
        self.cpu.increment_pc(3)

    def div(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a/operand_b, reg_a)
        self.cpu.increment_pc(3)