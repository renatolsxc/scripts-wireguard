from pyzabbix import ZabbixSender, ZabbixMetric
import platform
import random

def gerar_numero_aleatorio():
    return random.random()

# Exemplo de uso
numero_aleatorio = gerar_numero_aleatorio()
numero_aleatorio = (int) (numero_aleatorio*10)


# Configurações do servidor Zabbix
zabbix_server = "192.168.100.240"
zabbix_port =  10051

# Dados ue serão enviados
hostname = platform.node()
chave_unica_do_item = 'check_wg'
valor_do_item = 1

# Cria uma lista de métricas ZabbixMetric
metrics = [
    ZabbixMetric(hostname,chave_unica_do_item,numero_aleatorio)
    # Adicione mais métricas se necessário
]

print(f"Hostname: {hostname}")
print(f"\'{hostname}\',\'{chave_unica_do_item}\',{valor_do_item}")
# Cria uma instância do ZabbixSender
sender = ZabbixSender(zabbix_server, zabbix_port)

# Envia as métricas para o servidor Zabbix
try:
    result = sender.send(metrics)
    
    # Exibe os valores
    print(f'\tProcessados: {result.processed}')
    print(f'\tFalhas: {result.failed}')
    print(f'\tTotal: {result.total}')
    print(f'\tTempo: {result.time}')
    print(f'\tChunk: {result.chunk}')

    if result.processed:
        print(f'Métricas enviadas com sucesso. - {result.time}')
    else:
        print(f'Falha ao enviar as métricas. - {result.time}')

except Exception as e:
    print("erro")
    exit(5)



# Desserializa a string JSON em um objeto Python



