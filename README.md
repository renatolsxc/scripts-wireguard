# Scripts de wireGuard

this project aims to create service scripts that can monitor your vpn wireguard.
in my scenario I have a central wireguard vpn server, with two internet links in addition to approximately 70 clients that connect to this server through the wireguard vpn.
this repository contains a module and a script that generates a service that can be installed on the remote computer to monitor the local vpn service and always be connected with my main office

## Instalação

To install this script, just install the following libraries:
- python -m pip install pyinstaller
- python -m pip install pywin32-ctypes
after installed, you need to clone the repository and make changes to the variables:
-host=<remote host to monitor>
-ipwg=<main wan public ip>
-mainwg=<main wan dns name>
-secdwg=<secondary wan dns name>
-portawg=<port you use for your WireGuard>
- pckeywg=<public key>
- logfile="C:\Program Files\WireGuard\log_check-wggalpao.txt"
to generate the exe:
python -m PyInstaller --onefile ---hidden-import=win32timezone check_wggalpao_service.py

## Uso

Forneça exemplos e instruções claras sobre como usar o projeto. Inclua exemplos de código, capturas de tela ou gifs animados para demonstrar o uso em ação.

## Recursos

- Liste os principais recursos e funcionalidades do projeto.
- Destaque pontos fortes e diferenciais do projeto em relação a outros.
- Inclua uma tabela ou uma lista para facilitar a leitura e compreensão.

## Contribuição

Explique como outros desenvolvedores podem contribuir com o projeto. Forneça instruções sobre como fazer um fork, como configurar o ambiente de desenvolvimento local, quais ferramentas e padrões de codificação devem ser seguidos, como submeter alterações e como reportar problemas ou solicitar novos recursos.

## Licença

Informe sobre a licença do projeto e inclua um link para o arquivo LICENSE.md, onde os detalhes da licença podem ser encontrados.

## Contato

Inclua informações de contato, como e-mail ou links para redes sociais, para que os usuários possam entrar em contato com você para fornecer feedback, fazer perguntas ou colaborar em potencial.

## Agradecimentos

Agradeça às pessoas, organizações ou recursos que foram úteis para o projeto. Reconheça e dê crédito a contribuições de terceiros.

## Status do Projeto

Descreva brevemente o status atual do projeto - se está em desenvolvimento ativo, se é um projeto concluído ou se está em fase de manutenção. Inclua informações sobre a estabilidade e possíveis riscos.

## Exemplos Adicionais

Se necessário, você pode adicionar seções adicionais ao README para atender às necessidades específicas do seu projeto. Por exemplo, se o projeto possui APIs ou documentação técnica, você pode criar seções separadas para esses tópicos.




# Welcome!

 

## I'm (SEU NOME)!

 

:computer: I'm Front-End Developer!

:house_with_garden: I’m from Brazil.

:books: I’m currently learning everything.

:outbox_tray: 2021 Goals: create a new project and find a new job.

 

## About me

[![Github Badge](https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=LINK_GIT)](LINK_GIT)

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link= LINK_LINKEDIN)]( LINK_LINKEDIN)


# Índice 

* [Título e Imagem de capa](#Título-e-Imagem-de-capa)
* [Badges](#badges)
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Status do Projeto](#status-do-Projeto)
* [Funcionalidades e Demonstração da Aplicação](#funcionalidades-e-demonstração-da-aplicação)
* [Acesso ao Projeto](#acesso-ao-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Pessoas Contribuidoras](#pessoas-contribuidoras)
* [Pessoas Desenvolvedoras do Projeto](#pessoas-desenvolvedoras)
* [Licença](#licença)
* [Conclusão](#conclusão)

- Thanks for visiting.

- Enjoy it!! o/

o arquivo call.bat está configuado para chamar o arquivo monitorar.ps1

o arquivo check-wggalpao.py foi feito para monitorar a vpn usando o linguagem python e trocar de endpoint caso o primeiro falhe

o arquivo checkwg.py foi feito em python para testar o arquivo wg0.conf dentro da pasta /etc e monitorar o latest-handshake

o arquivo desligar.bat e desligar.vbs foram feitos para desligar o monitoramento da vpn wireguard

o arquivo monitorar.ps1 foi feito em powershell para monitorar a vpn wireguard e trocar de endpoint caso o primeiro falhe

o arquivo pingwg.py está configurado no cron do servidor ubuntu 22.04 proxy zabbix instalado na loja 1 para monitorar outros sites ele está monitorando as duas vpns e reinicia o serviço de wireguard caso o ping falhe. não há mudanças de endpoint. apenas reinicio de serviço caso falhe.

o arquivo start.bat foi feito para chamar em background e salvar o arquivo de log do monitoramento check-wggalpao.py


próximas versões
- preciso fazer criar um serviço para monitorar o tunnel service, abandonar a opção de scripts de inicialização e desligamento
- criando um serviço que se inicia de forma dependente do tcp/ip do windows
- ele vai monitorar o serviço da seguinte forma:
C:\Users\Usuario>sc query WireGuardTunnel$wggalpao

NOME_DO_SERVIÇO: WireGuardTunnel$wggalpao
    TIPO                       : 10  WIN32_OWN_PROCESS
    ESTADO                     : 4  RUNNING
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
    CÓDIGO_DE_SAÍDA_DO_WIN32   : 0  (0x0)
    CÓDIGO_DE_SAÍDA_DO_SERVIÇO : 0  (0x0)
    PONTO_DE_VERIFICAÇÃO       : 0x0
    AGUARDAR_DICA              : 0x0

se estiver running e não estiver pingando tomar alguma ação, trocar de operadora, por exemplo.
se não estiver running executar
wireguard /installtunnelservice "c:\Program Files\WireGuard\Data\Configurations\wggalpao.conf.dpapi"
para instalar o tunnel interface service

se tentar trocar a operadora com o seguinte comando
C:\Users\Usuario>wg set wggalpao peer 6TYMXmghs5vQZ3B+hashhash+pdPHwvZ+e1ekM= endpoint ippublico.ddns.net:51028
Unable to modify interface: No such file or directory
o serviço não está ligado ou não existe um servico do tipo WireGuardTunnel$
então preciso criar o serviço.

preciso decidir o que monitorar primeiro e como fazer esse monitoramento virar um serviço
"c:\Program Files\Python310\python.exe" -m PyInstaller --onefile --hidden-import=win32timezone check.py
- preciso melhorar o script que monitora o wg por ping para validar se o computador que roda o script possui internet. pois se ele nao tem internet ele não consegue fechar a vpn. testar ping, testar dns, testar velocidade, jitter e atraso.
