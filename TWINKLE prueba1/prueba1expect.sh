#!/usr/bin/expect -f
set timeout 40
# Inicia Twinkle-console
spawn twinkle-console
# Espera 2 segundos
sleep 3
# Envía la orden "call 101"
send "call 101\r"
sleep 15
# Espera a que se complete la llamada
#expect "200 OK"
#spleep 20
#send "quit"
send "exit\r"
send "\x03"
pkill twinkle-console
