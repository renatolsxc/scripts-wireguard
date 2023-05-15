import subprocess
import time
import os
import re

host="192.168.100.240"

def verifica_op_atual():
    try:
        #output = subprocess.check_output("wg showconf wggalpao", shell=True)
        output = subprocess.run(["wg","showconf","wggalpao"], capture_output=True, text=True)
        #print(f"{output.stdout}")
        outlines = output.stdout.splitlines()
        for linha in outlines:
            match = re.match(r"\s*(\S+)\s*=\s*(.*)\s*", linha)
            if match:
                key = match.group(1)
                value = match.group(2)
                if key == "Endpoint":
                    endpoint = value
                    #print(f"{value}")
        #print(f"{endpoint}")
        if endpoint == "200.169.14.155:44990":
            return 1
        elif value == "":
            return 0
        else:
            return 2
    except subprocess.CalledProcessError as e:
        date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
        print(date_string, "O comando falhou:", e.output)
        return 5


while True:
    result = os.system(f"ping -n 2 {host} > NUL")
    operadora_atual = verifica_op_atual()
    date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
    print(date_string, "- Operadora Atual:", operadora_atual)
    
    if result == 0:
        date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
        print(date_string, "- Monitoramento OK")
        time.sleep(60)
    else:
        date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
        print(date_string, "- Monitoramento falhou na primeira tentativa. Aguardando 30 segundos.")
        time.sleep(30)
        
        result = os.system(f"ping -n 2 {host} > NUL")
        date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
        print(date_string, "- Operadora Atual:", operadora_atual)
        
        if result == 0:
            date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
            print(date_string, "- Monitoramento OK na segunda tentativa.")
        else:
            date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
            print(date_string, "- Monitoramento falhou na segunda tentativa. Trocar.")
            
            if operadora_atual == 1:
                date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
                print(date_string, "- Trocar para operadora 2")
                cmd_troca = "wg set wggalpao peer 6TYMXmghs5vQZ3B+CoZdvxFwXIDeP+pdPHwvZ+e1ekM= endpoint dleite2.ddns.net:44990"
                subprocess.call(cmd_troca, shell=True)
                time.sleep(10)
            elif operadora_atual == 2:
                date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
                print(date_string, "- Trocar para operadora 1")
                cmd_troca = "wg set wggalpao peer 6TYMXmghs5vQZ3B+CoZdvxFwXIDeP+pdPHwvZ+e1ekM= endpoint dleite.ddns.net:44990"
                subprocess.call(cmd_troca, shell=True)
                time.sleep(10)
            else:
                date_string = time.strftime('%Y-%m-%d_%H:%M:%S')
                print(date_string, "- Comando Falhou")
