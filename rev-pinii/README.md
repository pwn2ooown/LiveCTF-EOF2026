# PINii

- **Tags**: rev, Do Not Try To Reverse It, try to llm this :)
- **Author**: pwn2ooown+asef18766

## Description

I bet your agent can't solve this challenge :)

Flag format: `^FLAG\{\w+\}$`

Once you find the flag, submit correct flag to `nc livectf.9ay.me 30016` and run `./submitter <team_id>`

## Hints

- Don't reverse the VM! Find the flag length first and there will be different `strace` output. Use `pintools` to leak the flag.
- Why the same input has different instruction count? See `strace` output and try to patch the binary to same input always output the same instruction count.
