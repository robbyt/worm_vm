#!/usr/bin/env python
from cpu import Cpu
from memory import Memory
from bios import Bios
from wormos import WormOS


def main(args):
    import os
    debug_envar = os.environ.get('WORM_DEBUG')
    debug_mode = True if debug_envar is 'true' else False

    # create cpu and ram
    cpu = Cpu(debug=debug_mode)
    memory = Memory(debug=debug_mode)

    # plug the cpu and ram into the bios
    bios = Bios(cpu, memory, debug=debug_mode)

    # boot the worm os
    wormos = WormOS(debug=debug_mode)


    # first check if a bytecode file was sent as a 1st arg
    if len(args) == 2:
        
        # then read the data from the file
        input_data= open(args[1], 'r').readlines()
        
        # load the raw bytecode string into the wormos, build and "exe"
        exe = wormos.build_exe(input_data)

        # turn the exe into machine code for the cpu
        machine_code = wormos.build_machine_code(exe)

        # run the machine code on the cpu
        bios.run(machine_code)

    else:
        print "Error: bytecode file needed as 1st argument."

if __name__ == "__main__":
    import sys
    main(sys.argv)
