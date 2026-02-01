# Boring Shellcode Game

- **Tags**: pwn, shellcode
- **Author**: naup96321+pwn2ooown

## Description

We don't have any good idea for this challenge so just a typical shellcode game :)

## Hints

- You can use a shorter shellcode to read the second stage shellcode and execute it
- Read shellcode to RWX buffer again to overwrite itself. Notice that some of the registers are 0 already, modify only needed. BTW I use seed 336928 in my solution
