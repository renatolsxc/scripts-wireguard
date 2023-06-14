from pyzabbix import ZabbixSender, ZabbixMetric
import platform
import checkwggalpaoprivate

def send(valor):

    # Configurações do servidor Zabbix
    zabbix_server = checkwggalpaoprivate.zabbix_server
    zabbix_port =  checkwggalpaoprivate.zabbix_port
    

    # Dados ue serão enviados
    hostname = platform.node()
    hostname=hostname.upper()
    chave_unica_do_item = checkwggalpaoprivate.chave_unica_do_item
    chave_operadora = checkwggalpaoprivate.chave_operadora
    

    # Cria uma lista de métricas ZabbixMetric
    metrics = [
        ZabbixMetric(hostname,chave_unica_do_item,valor[0]),
        ZabbixMetric(hostname,chave_operadora,valor[1])
    ]

    #print(f"Hostname: {hostname}")
    #print(f"\'{hostname}\',\'{chave_unica_do_item}\',{valor_do_item}")
    # Cria uma instância do ZabbixSender
    sender = ZabbixSender(zabbix_server, zabbix_port)

    # Envia as métricas para o servidor Zabbix
    try:
        result = sender.send(metrics)
        
        # Exibe os valores
        #print(f'\tProcessados: {result.processed}')
        #print(f'\tFalhas: {result.failed}')
        #print(f'\tTotal: {result.total}')
        #print(f'\tTempo: {result.time}')
        #print(f'\tChunk: {result.chunk}')

        if not result.failed:
            if result.processed:
                return (f'TRUE: {hostname} ; {chave_unica_do_item} ; {valor}')
            #print(f'Métricas enviadas com sucesso. - {result.time}')
            else:
                return (f'FALSE: {hostname} ; {chave_unica_do_item} ; {valor}')
            #print(f'Falha ao enviar as métricas. - {result.time}')
        else:
            return "Falhou ZBX - SEM TIMEOUT"
        
    except Exception as e:
        return "Falhou ZBX - EXCECAO" 
        