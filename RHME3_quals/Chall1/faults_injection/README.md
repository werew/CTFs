`faults.py` is a gdb script which insert faults into the execution
of the program and prints out the faulty results. The faulty result
are prepended with a ~ so they can be easily "greped".

`tracefile` contains already a collection of faulty outputs, ready
to be used with JeanGrey. The first line is the original (not faulty)
output.
