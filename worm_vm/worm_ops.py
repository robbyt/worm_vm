import sys
import logging
logger = logging.getLogger('ops')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

def op_noop(self):
    logger.debug('op_noop')
    return None

def op_set(self, *args):
    """
    code: 0x1
    arguments: dst register ID (4 bits), 1 short value (24 bits)
    effect: the dst register is set to the given value
    Ex: SET %A, $20 ==> 0x10000014
    """
    dst = args[0]
    val = args[1]
    self.cpu[dst] = int(val)
    logger.debug('op_set: cpu[%s] = %s' % (dst,val))

def op_move(self, *args):
    """
    code: 0x2
    arguments: dst register ID (4 bits), src register ID (4 bits)
    effect: the dst register is set to the value of the src register
    Ex: MOVE %D, %B ==> 0x23100000
    """
    dst = args[0]
    src = args[1]
    self.cpu[dst] = self.cpu[src]
    logger.debug('op_move: cpu[%s] = cpu[%s]' % (dst,src))

def op_load(self, *args):
    """
    code: 0x3
    arguments: dst register ID (4 bits), stack pointer register ID (4 bits)
    effect: the dst register is set to the value of the memory location 
            identified by the value of the stack pointer register
    Ex: LOAD %C, @A ==> 0x32000000. 
    If register A contains the number 8, and the 7th stack (memory) location 
    (0-indexed) contains a 43, then after this instruction, register C 
    should contain a 43

    load memory location @A into reg %C
    """
    cpu_dst = args[0]
    mem_src = args[1]
    self.cpu[cpu_dst] = self.memory[mem_src]
    logger.debug('op_load: cpu[%s] = memory[%s]' % (cpu_dst, mem_src))

def op_store(self, *args):
    """
    code: 0x4
    arguments: stack pointer register ID (4 bits), src register ID (4 bits)
    effect: the memory location identified by the value of the stack pointer 
            register is set to the value of the src register
    Ex: STORE @B, %E ==> 0x41400000. 
    If register B contains the number 0, and register E contains the number 1,
    then after this instruction executes the 1st stack (memory) location 
    (0-indexed) should contain a 1.
    """
    mem_dst = args[0]
    cpu_src = args[1]
    self.memory[mem_dst] = self.cpu[cpu_src]
    logger.debug('op_store: memory[%s] = cpu[%s]' % (mem_dst, cpu_src))

def op_read(self, *args):
    """
    code: 0x5
    arguments: None
    effect: a number from standard input is stored in register A
    Ex: READ ==> 0x50000000. 
    If the next number of standard input is 74, then after this instruction 
    runs, register A should contain 74. The behavior is not defined for the 
    case where there are no more numbers to read from standard input. But 
    unless you've hit EOF (or an input error occurs), then you HAVE to do 
    whatever necessary to put a number into this register, including waiting 
    for more input.
    """
    logger.debug("op_read: reading from stdin...")
    try:
        input_data = int(sys.stdin.readline())
        self.cpu[0] = int(input_data)
        logger.debug('op_read: cpu[0] = %s' % (input_data))
    except KeyboardInterrupt:
        return

def op_write(self, *args):
    """
    code: 0x6
    arguments: None
    effect: the contents of register A are written to stdout
    Ex: WRITE ==> 0x60000000.
    If register A contains 39, then after this instruction executes, 
    "39\n" should be written to stdout.
    """
    logger.debug('op_write')
    print self.cpu[0]

def op_add(self, *args):
    a1 = self.cpu[args[0]]
    a2 = self.cpu[args[1]]
    self.cpu[0] = int(a1) + int(a2)
    logger.debug('op_add: cpu[0] = %s + %s = %s' % 
                (a1, a2, self.cpu[0]))

def op_sub(self, *args):
    a1 = self.cpu[args[0]]
    a2 = self.cpu[args[1]]
    self.cpu[0] = int(a1) - int(a2)
    logger.debug('op_sub: cpu[0] = %s - %s = %s' % 
                (a1, a2, self.cpu[0]))

def op_mul(self, *args):
    a1 = self.cpu[args[0]]
    a2 = self.cpu[args[1]]
    self.cpu[0] = int(a1) * int(a2)
    logger.debug('op_mul: cpu[0] = %s * %s = %s' % 
                (a1, a2, self.cpu[0]))

def op_div(self, *args):
    a1 = self.cpu[args[0]]
    a2 = self.cpu[args[1]]
    self.cpu[0] = int(a1) / int(a2)
    logger.debug('op_mul: cpu[0] = %s / %s = %s' % 
                (a1, a2, self.cpu[0]))

def op_jmp(self, *args):
    """
    code: 0xB
    arguments: instruction location (28 bits, 0-indexed) to execute next
    effect: the next instruction to execute shall be value'th instruction in 
            the program
    Ex: JMP $1 ==> 0xB0000001.
    The next instruction to execute shall be the 2nd instruction of the 
    program, and normally after that (so, unless that instruction is a jmp 
    itself, then the following instruction should be the 3rd one (index 2).
    """
    jmp_to = args[0]
    self.cpu.pc_jump(jmp_to)
    logger.debug("op_jmp: set PC to %s" % jmp_to)

def op_jmp_z(self, *args):
    jmp_to = args[0]

    #if REG['0'] == 0:
    if not self.cpu[0]:
        self.cpu.pc_jump(jmp_to)
        logger.debug("op_jmp_z: set PC to %s" % jmp_to)
    else:
        logger.debug("op_jmp_z: test failed, did not set PC to %s" % jmp_to)

def op_jmp_nz(self, *args):
    jmp_to = args[0]
    if self.cpu[0]:
        self.cpu.pc_jump(jmp_to)
        logger.debug("op_jmp_nz: set PC to %s" % jmp_to)
    else:
        logger.debug("op_jmp_nz: test failed, did not set PC to %s" % jmp_to)

def op_jmp_gt(self, *args):
    jmp_to = args[0]
    if self.cpu[0] >= 1:
        self.cpu.pc_jump(jmp_to)
        logger.debug("op_jmp_gt: set PC to %s" % jmp_to)
    else:
        logger.debug("op_jmp_gt: test failed, did not set PC to %s" % jmp_to)

def op_jmp_lt(self, *args):
    jmp_to = args[0]
    if self.cpu[0] < 0:
        self.cpu.pc_jump(jmp_to)
        logger.debug("op_jmp_lt: set PC to %s" % jmp_to)
    else:
        logger.debug("op_jmp_lt: test failed, did not set PC to %s" % jmp_to)
