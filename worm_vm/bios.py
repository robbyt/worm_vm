import sys
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class Bios(object):
    def __init__(self, cpu, memory, debug=False):
        self.debug = debug
        self.memory = memory
        self.cpu = cpu

        if self.debug:
            logging.info("Bios object created with CPU: %s and Memory: %s" % 
                        (str(self.cpu), str(self.memory)))

    def _run_op(self, op, arg_data):
        op(self, *arg_data)
        self.cpu.pc_increment()

    def run(self, machine_code):
        """ Machine code passed into this function is a list, and will be
            run on the cpu via the _run_op(), which will increment the PC.

            The machine code passed into this function has already been 
            parsed by the os. Each row of the machine code list contains
            a tuple. Index0 of the tuple contains a raw python function,
            and Index1 contains some optional argument data such as the
            constant that should be set on the CPU register.

            All of the raw python functions in Index0 are defined in
        """
        try:
            while not self.cpu.REG[5]:
                current_pc_index = self.cpu.get_pc()

                if self.debug:
                    logging.info("Bios running PC: %s" % current_pc_index)

                self._run_op(machine_code[current_pc_index][0],
                             machine_code[current_pc_index][1])
        except KeyboardInterrupt:
            print "Goodbye."
            sys.exit(0)



