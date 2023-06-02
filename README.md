# Scripts for WireGuard

this project aims to create service scripts that can monitor your vpn wireguard.
in my scenario I have a central wireguard vpn server, with two internet links in addition to approximately 70 clients that connect to this server through the wireguard vpn.
this repository contains a module and a script that generates a service that can be installed on the remote computer to monitor the local vpn service and always be connected with my main office

## Instalation

- To install this script, just install the following libraries:
    - python -m pip install pyinstaller
    - python -m pip install pywin32-ctypes

- after installed, you need to clone the repository and make changes to the variables:
    - host= < remote host to monitor >
    - ipwg= < main wan public ip >
    - mainwg= < main wan dns name >
    - secdwg= < secondary wan dns name >
    - portawg= < port you use for your WireGuard >
    - pckeywg= < public key >
    - logfile= < path to log file >

- to generate the exe:
    - python -m PyInstaller --onefile ---hidden-import=win32timezone check_wggalpao_service.py

## Usage

after generating the exe file, it must be copied to the machines that close the vpn with the wireguard server and installed as follows.

- copy the file to the folder you want
- open cmd with administrative permissions
- walk to the folder where the exe is
- file.exe install
- file.exe start


## About me

- linkedin: https://www.linkedin.com/in/silvarenatolopes/

