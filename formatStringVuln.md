# Format string vuln
per maggiori info `man 3 printf`
esempio:
`% 12 $ lx` stampa il dodicesimo valore degli argomenti in hex 
esempio:
`% 3 $ 20 c` stampa il terzo valore degli argomenti come carattere, ma aggiungendo 19 spazi. In totale 20 caratteri

Nota: in un exploit fai in modo che se ci sono degli 0 (ad esempio negli indirizzi) questi siano in ultima posizione del payload, altrimeni la printf viene interrotta a meta e non si triggera il `%n`
