# Profile Page

- **Tags**: web
- **Author**: Ching367436

## Description

Just a simple profile page. Flag format: `^EOF\{\d\{8\}\}$`.

## Hints

- There is some oracle to leak the flag one byte at a time but how to reset the server? `package.json` has some interesting packages to help you. The intended solution only needs 1 instance to get the full flag.
- `CVE-2025-7338` can crash the server and force a restart. Combine this with your single byte oracle to get the full flag.
