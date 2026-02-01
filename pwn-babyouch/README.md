# Baby Ouch

- **Tags**: pwn, aarch64
- **Author**: pwn2ooown

## Description

Baby Mac is too hard... So I created Baby Ouch :)

## Hints

- `read` doesn't add null byte in the end. If I want to print starting from the 64th byte of buffer, I can input 63 As and it'll keep printing from 64 th byte until reaches a null byte
- Stack layout: `buf[64]/canary/doesn't matter/return address/doesn't matter/libc address`, control input length to leak canary and libc one byte by one byte. ROP gadget: `0x0000000000045e5c : ldr x0, [sp, #0x18] ; ldp x29, x30, [sp], #0x20 ; ret`
