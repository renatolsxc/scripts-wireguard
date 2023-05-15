cd "%programfiles%\WireGuard\"

for /f "tokens=2 delims=:" %%i in (pid.txt) do set pioad=%%i

wmic process where processid=%pioad% call terminate