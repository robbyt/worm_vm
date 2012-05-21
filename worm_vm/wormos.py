import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

import lepl

import worm_ops as ops
import wormos_bc_parser

class WormOS(object):
    """ Provides a meta-program for mapping opcode to python functions,
        and storage for the program stack
    """

    def __init__(self, debug=False):
        self.debug = debug
        self.literals = []
        self.op_codes = {}
#        self.op_names_to_func = {}
        self.op_codes_to_func = {}

        self.exe = None
        self.machine_code = None

        self.op_names = {"NOOP":  '0',
                         "SET":   '1',
                         "MOVE":  '2',
                         "LOAD":  '3',
                         "STORE": '4',
                         "READ":  '5',
                         "WRITE": '6',
                         "ADD":   '7',
                         "SUB":   '8',
                         "MUL":   '9',
                         "DIV":   'A',
                         "JMP":   'B',
                         "JMP_Z": 'C',
                         "JMP_NZ":'D',
                         "JMP_GT":'E',
                         "JMP_LT":'F'}

        # load up the op names
        for op_name, op_code in self.op_names.iteritems():
            self.__setitem__(op_name, op_code)

    def build_exe(self, txt):
        """ Turns the raw bytecode string into parsed data, builds a psuedo exe
        """
        self.exe = []
        for i in txt:
            try:
                li = wormos_bc_parser.parser.parse(i)
                self.exe.append(li)
            except lepl.stream.maxdepth.FullFirstMatchException:
                # to handle parse errors
                logging.error("Error parsing byte code on line %s!!!" %
                             (str(len(self.exe) + 1)))

                logging.error("Parsed instructions so far:")
                logging.error(str(self.exe))
                raise

        return self.exe

    def build_machine_code(self, exe):
        self.machine_code = []
        for row in exe:
            opcode = row[0] # the opcode number
            arg_data = row[1:] # the optional data for the operation

            # builds a list of tuples, that contain the raw function object
            # and some optional args, if they exist
            self.machine_code.append((self.op_codes_to_func[opcode],arg_data))

        # add an exit to the end of the stack, so if the PC runs off the stack
        # the program will just exit
        self.machine_code.append((ops.op_set,(5,1)))

        return self.machine_code


    def __setitem__(self, op_name, op_code):
        """ provides a standard python api for adding entries like 
            self[key]=value. in this case, key=op_name, and value=op_code
        """
        if self.debug:
            logging.info("WormOS: loading operation %s, with opcode %s" % 
                        (op_name, op_code))

        # create an inverse dict
        self.op_codes[op_code] = op_name

        # this builds a list of all op_codes, which is used for the op_parser
        self.literals.append(op_code)

        # these two will attach a matching function object to the op_name, 
        # assuming that a matching function name exists in the ops module.
#        self.op_names_to_func[op_name] = getattr(ops, "op_" + op_name.lower())
        self.op_codes_to_func[op_code] = getattr(ops, "op_" + op_name.lower())

