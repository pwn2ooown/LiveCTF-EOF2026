import ctypes
import struct
import mmap

print("SUDDEN DEATH !!! Just double it!!!")

doubles = []

while True:
    try:
        data = input()
        if data == "EOF":
            break
        doubles.append(float(data))
    except:
        print("????")
        exit()

buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_void_p)
fpointer = ctypes.c_void_p.from_buffer(buf)
f = ftype(ctypes.addressof(fpointer))

buf.write(b''.join(struct.pack('<d', d) for d in doubles))

f()

del fpointer
buf.close()