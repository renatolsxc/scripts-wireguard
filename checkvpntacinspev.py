#import subprocess
import datetime
import os
import textwrap

host = "192.168.0.1"

# Função para verificar o ping
def verificar_ping():
    
    result = os.system(f"ping -n 4 {host} > NUL")
    #subprocess.run(["ping", "-n", "1", hostname], capture_output=True)
    #print(result)
    return result == 0
    #.returncode == 0

# Função para modificar o arquivo
def modificar_arquivo(resultado):
    arquivo = "c:\\inetpub\\wwwroot\\checkvpntacinspev.html"  # Substitua pelo caminho do arquivo que deseja modificar
    texto_ok = '''
    <html>
        <head>
        <meta charset="utf-8">
        </head>
        <body>
                <h1>OK</h1>
        </body>
    </html>
    '''
    texto_nok = '''
    <html>
        <head>
        <meta charset="utf-8">
        </head>
        <body>
                <h1>FALHA</h1>
        </body>
    </html>
    '''    
    with open(arquivo, "w") as f:
        if resultado:
            f.write(texto_ok)
        else:
            f.write(texto_nok)

# Função para registrar no arquivo de log
def registrar_log(mensagem):
    arquivo_log = "c:\\scripts\\log_checkvpntacinspev.txt"  # Substitua pelo caminho do arquivo de log
    data_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mensagem_formatada = f"[{data_hora}] {mensagem}\n"

    with open(arquivo_log, "a") as f:
        f.write(mensagem_formatada)

# Loop principal
#while True:
ping = verificar_ping()
modificar_arquivo(ping)
#print(ping)
if ping:
    registrar_log("Ping OK")
else:
    registrar_log("Ping FALHA")
