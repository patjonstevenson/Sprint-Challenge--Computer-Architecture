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
            0b10101000: self.AND,
            0b10101010: self.OR,
            0b10101011: self.XOR,
            0b01101001: self.NOT,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b10100100: self.MOD,


            # Other
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,

            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret,

            0b10100111: self.cmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010100: self.jmp
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

    def cmp(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)

        if operand_a == operand_b:
            self.cpu.set_fl('E')
        elif operand_a > operand_b:
            self.cpu.set_fl('G')
        elif operand_a < operand_b:
            self.cpu.set_fl('L')
        
        self.cpu.increment_pc(3)

    def jmp(self):
        pc = self.cpu.get_pc()
        reg = self.cpu.ram_read(pc + 1)
        addr = self.cpu.reg_read(reg)
        
        diff = pc - addr
        if diff > 0:
            self.cpu.decrement_pc(diff)
        elif diff < 0:
            self.cpu.increment_pc(abs(diff))

    def jeq(self):
        fl = self.cpu.get_fl()
        if fl == 'E':
            self.jmp()
        else:
            self.cpu.increment_pc(2)

    def jne(self):
        fl = self.cpu.get_fl()
        if fl != 'E':
            self.jmp()
        else:
            self.cpu.increment_pc(2)

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


    # TODO
    def AND(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        # print(f"operand_a: {operand_a}")
        # print(f"operand_b: {operand_b}")
        # print(f"reg_a: {reg_a}")
        # print(f"operand_a & operand_b: {operand_a & operand_b}")
        self.cpu.reg_write(operand_a & operand_b, reg_a)
        self.cpu.increment_pc(3)
    
    # TODO
    def OR(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a | operand_b, reg_a)
        self.cpu.increment_pc(3)

    # TODO
    def XOR(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a ^ operand_b, reg_a)
        self.cpu.increment_pc(3)
    

    # TODO
    def NOT(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        operand_a = self.cpu.reg_read(reg_a)
        self.cpu.reg_write(0b11111111 ^ operand_a, reg_a)
        self.cpu.increment_pc(2)
    

    # TODO
    def SHL(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a << operand_b, reg_a)
        self.cpu.increment_pc(3)
    

    # TODO
    def SHR(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a >> operand_b, reg_a)
        self.cpu.increment_pc(3)
    
    # TODO
    def MOD(self):
        pc = self.cpu.get_pc()
        reg_a = self.cpu.ram_read(pc + 1)
        reg_b = self.cpu.ram_read(pc + 2)
        operand_a = self.cpu.reg_read(reg_a)
        operand_b = self.cpu.reg_read(reg_b)
        self.cpu.reg_write(operand_a % operand_b, reg_a)
        self.cpu.increment_pc(3)
    

