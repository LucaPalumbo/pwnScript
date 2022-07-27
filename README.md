# pwnScript
Collezione di script utili per ctf. Da riempire man mano che li scrivo


## Avvia binario con libc diversa
usa pwninit

## Attaccati a un programma 
```gdb -p $(pidof canvas_dbg) -ex "br *main+175" ```
