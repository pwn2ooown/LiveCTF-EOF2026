# Hint

If your computer arch is not aarch64, you can try to emulate it with QEMU

`qemu-aarch64 -g 1234 ./ld-musl-aarch64.so.1 ./chal`
Open another terminal run `gdb-multiarch ./chal`
`(gdb) target remote 127.0.0.1:1234`

Challenge is running on ARM GCP instance and the virtual address of memory layout might be different
