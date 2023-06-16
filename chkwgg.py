import checkwggalpao
import zbxwggalpao
import checkwggalpaoprivate


status=checkwggalpao.inicio()
zbx = zbxwggalpao.send(status)
with open(checkwggalpaoprivate.logfile, 'a') as file:
    file.write(f'ZBX: {zbx}\n')