"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.SP = 7 #stack pointer
        self.pc = 0
        self.fl = False

    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, address, value):
        self.ram[address] = value

#original
    # def load(self):
    #     """Load a program into memory."""
    #     address = 0
    #     # For now, we've just hardcoded a program:
    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]
    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

# loads programmatically
    def load(self):

        if len(sys.argv) < 2:
            print('No program provided')
            exit(2)

        try:
            address = 0
            # fp = open(sys.argv[1], 'r')
            fp = open('sctest.ls8','r')
            for line in fp:
                if line[0] == '#':
                    continue
                instruction = line.split('#')
                instruction = instruction[0].strip()
                if instruction == "":
                    continue
                self.ram[address] = int(instruction, 2)
                address += 1
                # print(line)    

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            exit(2)

        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        # # moving MUL to the correct location
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        # compares reg a to reg b, to see if reg a is less than or equal to reg b TODO: need logic somewhere for greater than
        elif op == "CMP":
           self.reg[reg_a] <= self.reg[reg_b]
           return self.fl == True 
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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
        cpu_running = True
        while cpu_running:
            #HLT
            if self.ram[self.pc] == 0b00000001:
                exit(1)
            #LDI
            elif self.ram[self.pc] == 0b10000010:
                register = self.ram_read(self.pc+1)
                value = self.ram_read(self.pc+2)
                self.reg[register] = value
                self.pc += 3
            #PRN
            elif self.ram[self.pc] == 0b01000111:
                print(self.reg[self.ram_read(self.pc+1)]) #SHOULD PRINT VALUE
                self.pc += 2
            # #MUL
            # elif self.ram[self.pc] == 0b10100010:
            #     register = self.ram_read(self.pc+3)
            #     self.pc +=3 
             #MUL
            elif self.ram[self.pc] == 0b10100010:
                operand_1 = self.reg[self.ram_read(self.pc+1)]
                operand_2 = self.reg[self.ram_read(self.pc+2)]
                self.reg[self.ram_read(self.pc+1)] = operand_1 * operand_2
                self.pc += 3
            # JMP
            elif self.ram[self.pc] == 0b01010100:
                register = self.ram_read(self.pc)
                self.pc = register
            # JEQ
            elif self.ram[self.pc] == 0b01010101:
                self.fl == True
            # JNE
            elif self.ram[self.pc] == 0b01010110:
                self.fl == True
        