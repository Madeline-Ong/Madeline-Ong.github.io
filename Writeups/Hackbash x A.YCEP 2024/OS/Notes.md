find location of funct for new return addr 
>> gdb 
>> disass funct (endbr64)


find out len of input & dist btwn input buffer & return addr
$ gdb ./your_program

# Set a breakpoint at the end of main (or funct its in)
# main needs to be runnable by all so chmod 777
(gdb) break main
(gdb) run

# When the program hits the breakpoint, inspect the stack
(gdb) info frame
(gdb) x/20x $rsp   # This will show the memory around the stack pointer

# Find the return address and calculate the offset
