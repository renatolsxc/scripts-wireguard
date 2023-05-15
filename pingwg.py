import re
import subprocess
import time
import os
import sys


INTERFACE = "wg0"
hostinspev = "192.168.100.1"
hosttac1305 = "192.168.0.1"


def checar_ping(host):
    if sys.platform.lower() == "win32":
        comando = f"ping -n 2 {host} > NUL"
    else:
        comando = f"ping -c 2 {host} > /dev/null"
    resultado = os.system(comando)
    return resultado
    #if (resultado == 0):
    #    return "OK"
    #else:
    #    return "NOK"

pingi = checar_ping(hostinspev)
pingt = checar_ping(hosttac1305)

if (pingi == 0) and (pingt == 0):
    print (f"{time.ctime()} - ok nas duas localidades")
    exit
elif (pingt == 0):
    print (f"{time.ctime()} - falha na inspev, reiniciando")
    subprocess.run(["systemctl", "restart", "wg-quick@wg0.service"],capture_output=True, text=True)
elif (pingi == 0):
    print (f"{time.ctime()} - falha no tac1305, reiniciando")
    subprocess.run(["systemctl", "restart", "wg-quick@wg0.service"],capture_output=True, text=True)
else:
    print (f"{time.ctime()} - falha nas duas localidades, reiniciando")
    subprocess.run(["systemctl", "restart", "wg-quick@wg0.service"],capture_output=True, text=True)

    #reiniciar wg
#print(f"Ping para {hostinspev}: {ping1}")
#print(f"Ping para {hosttac1305}: {ping2}")

