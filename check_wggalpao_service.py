import datetime
import os
import shutil
import subprocess
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import checkwggalpaoprivate


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Check-WGGalpao'
    _svc_display_name_ = 'Check-WGGalpao'

    logfile = checkwggalpaoprivate.logfile

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nRecebi Stop!\n')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nRecebi Run!\n')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Coloque aqui o código principal do seu serviço
        with open(checkwggalpaoprivate.logfile, 'a') as file:
            file.write(f'\nServiço em execução!\n')
        while self.is_running:
            try:
                if os.path.exists('c:\\Program Files\\WireGuard\\chkwggnew\\chkwgg.exe'):
                    dia = datetime.date.today().strftime("%Y%m%d")

                    with open(checkwggalpaoprivate.logfile, 'a') as file:
                        file.write(f'EXISTE ATUALIZACAO!\n')
                    
                    arquivo_new = "c:\\Program Files\\WireGuard\\chkwggnew\\chkwgg.exe"
                    arquivo_now = "c:\\Program Files\\WireGuard\\chkwgg.exe"
                    arquivo_old = f'c:\\Program Files\\WireGuard\\chkwggnew\\chkwgg-{dia}.exe'

                    # Fazer uma cópia do novo arquivo para um local temporário
                    shutil.move(arquivo_now, arquivo_old)
                    
                    # Substituir o arquivo principal em uso pelo serviço
                    shutil.move(arquivo_new, arquivo_now)
                else:
                    with open(checkwggalpaoprivate.logfile, 'a') as file:
                        file.write(f'NAO EXISTE ATUALIZACAO!\n')

                with open(checkwggalpaoprivate.logfile, 'a') as file:
                    file.write(f'While!\n')
                    subprocess.Popen(['c:\\Program Files\\WireGuard\\chkwgg.exe'])
                    time.sleep(60)
            except Exception as e:
                with open(checkwggalpaoprivate.logfile, 'a') as file:
                    file.write(f'\nFALHA! - Self.Runing - {e}')
            
            pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)
