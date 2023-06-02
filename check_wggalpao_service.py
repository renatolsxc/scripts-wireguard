import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import checkwggalpao

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Check-WGGalpao'
    _svc_display_name_ = 'Check-WGGalpao'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        with open('c:\\status.txt', 'a') as file:
            file.write(f'\nRecebi Stop!')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        with open('c:\\status.txt', 'a') as file:
            file.write(f'\nRecebi Run!')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Coloque aqui o código principal do seu serviço
        with open('c:\\status.txt', 'a') as file:
            file.write(f'\nServiço em execução!')
        while self.is_running:
            with open('c:\\status.txt', 'a') as file:
                file.write(f'\nWhile!')
            try:
                checkwggalpao.inicio()
            except Exception as e:
                with open('c:\\status.txt', 'a') as file:
                    file.write(f'\nFALHA! - {e}')
            
            pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)