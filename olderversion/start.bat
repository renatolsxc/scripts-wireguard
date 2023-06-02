@echo off
set "python=C:\Program Files\Python310\python.exe"
set "script=c:\Program Files\WireGuard\check-wggalpao.py"
start "asdasdasd" /min /b "%python%" -u "%script%" >> "c:\Program Files\WireGuard\loglog.txt"

wmic process where "name='python.exe' and commandline like '%%check-wggalpao.py%%'" get processid | findstr/n ^^|findstr "[2]:" > "c:\Program Files\WireGuard\pid.txt"

rem wmic process where "name='python.exe'" get processid,commandline
rem wmic process where "commandline like '%%%script%%%'" get processid
rem | findstr/n ^^|findstr "[2]:"
rem wmic process where "commandline like '%%[m]check.py%%'" get processid | findstr/n ^^|findstr "[2]:" > "c:\Program Files\WireGuard\pid.txt"