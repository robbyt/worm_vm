import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class Memory(object):
    STACK = {}

    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            logging.info("Memory object created.")

    def __str__(self):
        return str(Memory.STACK)

    def __getitem__(self, key):
        return Memory.STACK.get(key, 0)

    def __setitem__(self, key, value):
        Memory.STACK[key] = int(value)
        if self.debug:
            logging.info("Memory Updated: %s" % (Memory.STACK[key]))
            logging.info("Memory Currently Set to: %s" % str(Memory.STACK))

    def __iter__(self):
        return Memory.STACK.iteritems()

