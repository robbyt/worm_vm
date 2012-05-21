from lepl import Any, Literal, Literals, Newline, Optional, Or

# start a cpu instance and find out what our registers are called
from cpu import Cpu
_cpu = Cpu()
_REG_NAMES = _cpu.register_nums_as_strings

def my_flat(d):
    """ takes input like '00006' and returns a flat int like 6
        or, it will take a hex'd number like 0001C and return 28
    """
    return int("".join(tuple(d)), 16)

reg = Literals(*_REG_NAMES)
five_digits = Any() & Any() & Any() & Any() & Any() > my_flat
six_digits = Any() & Any() & Any() & Any() & Any() & Any() > my_flat
seven_digits = Any() & Any() & Any() & Any() & Any() & Any() & Any() > my_flat

# newline: if there's a newline (optionally) drop it off the end of a line (~)
nl = ~Optional(Newline())

# noop
op_noop = Literal('0') & ~seven_digits & nl

# reg target => data
op_set = Literal('1') & reg & six_digits & nl

# reg source => reg dest 
op_move = Literal('2') & reg & reg & ~five_digits & nl

# reg target => stack pointer
op_load = Literal('3') & reg & Any() & ~five_digits & nl

# stack pointer => reg target
op_store = Literal('4') & Any() & reg & ~five_digits & nl

# read from stdin
op_read = Literal('5') & ~seven_digits & nl

# just print reg[0]
op_write = Literal('6') & ~seven_digits & nl

# operate on dst, src
op_base = reg & reg & ~five_digits & nl
op_add = Literal('7') & op_base
op_sub = Literal('8') & op_base
op_mul = Literal('9') & op_base
op_div = Literal('A') & op_base

# jump to index num
op_jmp_base = seven_digits & nl
op_jmp = Literal('B') & op_jmp_base
op_jmp_z = Literal('C') & op_jmp_base
op_jmp_nz = Literal('D') & op_jmp_base
op_jmp_gt = Literal('E') & op_jmp_base
op_jmp_lt = Literal('F') & op_jmp_base


parser = Or(op_noop, op_set, op_move, op_load, op_store, op_read, op_write, 
                 op_add, op_sub, op_mul, op_div, op_jmp, op_jmp_z, op_jmp_nz,
                 op_jmp_gt, op_jmp_lt)
