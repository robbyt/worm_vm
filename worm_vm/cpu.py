import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class Cpu(object):
    REG = {0: 0,
           1: 0,
           2: 0,
           3: 0,
           4: 0,
           5: 0,}
    PROG_COUNTER = 0

    def __init__(self, debug=False):
        self.debug = debug
        self.name_map = {'a':0,
                         'b':1,
                         'c':2,
                         'd':3,
                         'e':4,
                         's':5,}
        if self.debug:
            logging.info("CPU object created.")

    def __str__(self):
        return str(Cpu.REG)

    def __repr__(self):
        return self.__str__()

    @property
    def register_nums_as_strings(self):
        return [str(k) for k in Cpu.REG.keys()]

    @property
    def human_names(self):
        """ There is a bug here...
        """
        d = {}
        names = [i for i in self.name_map.iterkeys()]
        names.sort()
        for v in Cpu.REG.itervalues():
            d[names.pop(0)] = v

        return d

    def pc_jump(self, jump_to):
        if self.debug:
            logging.info("CPU pc_jump: %s" % jump_to)

        Cpu.PROG_COUNTER = jump_to

    def pc_increment(self, inc_by=1):
        Cpu.PROG_COUNTER += inc_by
        if self.debug:
            logging.info("CPU pc_increment to: %s" % self.get_pc())


    def get_pc(self):
        return Cpu.PROG_COUNTER

    def _reg_name_to_num(self,key):
        """ pass in a human-readable register name, like 'a', and get the 
            re-mapped version as an int.
        """
        if type(key) is str:
            reg_name = self.name_map[key]
            if Cpu.REG.has_key(reg_name):
                return int(reg_name)
            else:
                raise KeyError('Problem with name to register mapping.')
        else:
            raise ValueError

    def _fix_key(self, key):
        """ Converts a '1' to 1, and 'a' to 0
        """
        try:
            key = int(key)
        except ValueError:
            key = self._reg_name_to_num(key)
        return key

    def __getitem__(self, key):
        """ Takes a self[0] and returns data in reg0, or takes self['0'] and
            converts '0' from a str to an int and returns data in reg0, or
            takes self['a'] and tries to convert it to an int, fails and then
            uses an alternative lookup method to return the data in the first 
            register.
        """
        key = self._fix_key(key)
        if type(key) is int or type(key) is str:
            if self.debug:
                logging.info("CPU Register getitem: cpu[%s] = %s" % (key, Cpu.REG[key]))
            return Cpu.REG[key]
        else:
            return ValueError('Key must be an int or string.')

    def __setitem__(self, key, value):
        """ Used for updating existing keys only. No new keys are allowed. If
            you try to create a new key via this method, a ValueError will be
            raised.
        """
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Value must be an int, or int as a string.')

        key = self._fix_key(key)

        if Cpu.REG.has_key(key):
            Cpu.REG[key] = value
            if self.debug:
                logging.info("CPU Register setitem: %s" % str(Cpu.REG))
        else:
            raise ValueError('Only adding data to existing keys is allowed.')

    def __iter__(self):
        return Cpu.REG.iteritems()

