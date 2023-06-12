import subprocess
import time
import os
import re
import sys
from datetime import datetime
import checkwggalpaoprivate


def verifica_op_atual():
    endpoint = value = ""
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
        if endpoint == f"{checkwggalpaoprivate.ipwg}:{checkwggalpaoprivate.portawg}":
            return 1
        elif value == "":
            return 0
        else:
            return 2
    except subprocess.CalledProcessError as e:
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nFALHA! - op')
        return 5
    
def install_wggalpao():
    try:
        outp = subprocess.run(('wireguard /installtunnelservice "C:\Program Files\WireGuard\Data\Configurations\wggalpao.conf.dpapi"'), capture_output=True, text=True)
        outlines = outp.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nFALHA! - INSTALLSVC - {e.returncode}')
        return 5

def start_wggalpao():
    try:
        output = subprocess.run(["sc","start","WireGuardTunnel$wggalpao"], capture_output=True, text=True)
        outlines = output.stdout.splitlines()
        outlines = (outlines[0].find("1060"))
        if outlines == "-1":
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nFALHA! - STARTSVC - {e.returncode}')
        return 5

class Logger:
    def __init__(self, filename):
        self.filename = filename
    
    def write(self, message):
        if message != " " and message != "\n":
            timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            formatted_message = f"{timestamp} - {message}\n"
             
            with open(self.filename, 'a') as log_file:
                log_file.write(formatted_message)

    def flush(self):
        pass


def inicio():
    sys.stdout = Logger(checkwggalpaoprivate.logfile)
    
    #while True:

    result = os.system(f"ping -n 2 {checkwggalpaoprivate.host} > NUL")
    operadora_atual = verifica_op_atual()
    #operadora_atual = 2
    print(f"Operadora Atual: {operadora_atual}")
    #print(f"Operadora Atual:")
                
    
    if result == 0:
        print("Monitoramento OK")
        return 1
    else:
        print("Monitoramento falhou na primeira tentativa. Aguardando 30 segundos.")
        time.sleep(30)

        # se a operadora_atual for 0 o comando wg showconf não foi realizado com sucesso
        if operadora_atual == 0:
            # tentar iniciar o serviço wggalpao
            if not start_wggalpao():
                # falhou, preciso instalar o serviço
                install_wggalpao()

        result = os.system(f"ping -n 2 {checkwggalpaoprivate.host} > NUL")
        print(f"Operadora Atual: {operadora_atual}")
        
        if result == 0:
            print("Monitoramento OK na segunda tentativa.")
            return 1
        else:
            print("Monitoramento falhou na segunda tentativa. Trocar.")
            
            operadora_atual = verifica_op_atual()
            
            if operadora_atual == 1:
                print("Trocar para operadora 2")
                cmd_troca = os.system(f"wg set wggalpao peer {checkwggalpaoprivate.pckeywg} endpoint {checkwggalpaoprivate.secdwg}:{checkwggalpaoprivate.portawg}")
                time.sleep(10)
                result = os.system(f"ping -n 2 {checkwggalpaoprivate.host} > NUL")
                if result == 0:
                    print("Monitoramento OK apos a troca")
                    return 1
                else:
                    print("Comando de troca falhou")
                    return 0
                
            elif operadora_atual == 2:
                print("Trocar para operadora 1")
                cmd_troca = os.system(f"wg set wggalpao peer {checkwggalpaoprivate.pckeywg} endpoint {checkwggalpaoprivate.mainwg}:{checkwggalpaoprivate.portawg}")
                time.sleep(10)
                result = os.system(f"ping -n 2 {checkwggalpaoprivate.host} > NUL")
                if result == 0:
                    print("Monitoramento OK apos a troca")
                    return 1
                else:
                    print("Comando de troca falhou")
                    return 0
                
            else:
                print("Comando Falhou")
                return 0