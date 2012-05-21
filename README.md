Worm VM
=============

This is a "simple" virtual machine implemented in python, used for
interpreting and executing "worm" bytecode.

Working with this VM
--------------------

First, this vm requires the lepl python parser, so install that from pip.
```bash
$ pip install lepl
```

Once lepl is installed, you can run the VM with a simple example bytecode file
```bash
$ worm_vm/vm.py programs/print_expression.wormbc
```

Running the VM in debug mode
----------------------------

```bash
$ export WORM_DEBUG=true
$ worm_vm/vm.py programs/print_expression.wormbc
```





