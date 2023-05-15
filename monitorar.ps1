# Função para verificar a operadora atual
Start-Transcript -Path "C:\Program Files\WireGuard\log.txt" -Append

function verificaopatual() {
	try {
		$output = Invoke-Expression "wg showconf wggalpao" | Select-String -Pattern "endpoint"
		if ($output) {
            $parts = ($output.Line -split ":")[0]
            $parts = ($parts -split "= ")[1] 
			switch ($parts) {
				"200.169.14.155" { return 1 }
				default {
					if ($parts -ne "") {
						return 2
					} else {
						return 0
					}
				}
			}
        }
        else {
            return 0
        }
    }
    catch {
        $dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
		Write-Host $dateString "O comando falhou: $($_.Exception.Message)" -ForegroundColor Red
        return 5
    }
	
    
}

# Inicia o monitoramento do endereço IP 192.168.100.240
while ($true) {
    $result = Test-NetConnection -ComputerName 192.168.100.240 -InformationLevel Quiet
    $operadoraAtual = verificaopatual
	$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
	write-host $dateString "- Operadora Atual: " $operadoraAtual
	if ($result -eq $true) {
		$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
        Write-Host $dateString "- Monitoramento OK"
        Start-Sleep -Seconds 60
    } else {
        $dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
		Write-Host $dateString "- Monitoramento falhou na primeira tentativa. Aguardando 30 segundos."
		Start-Sleep -Seconds 30
		
		$result = Test-NetConnection -ComputerName 192.168.100.240 -InformationLevel Quiet
		$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
		write-host $dateString "- Operadora Atual: " $operadoraAtual
		if ($result -eq $true) {
			$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
			Write-Host $dateString "- Monitoramento OK na segunda tentativa."
		} else {
			
			$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
			Write-Host $dateString "- Monitoramento falhou na segunda tentativa. Trocar."
		
		
			switch ($operadoraAtual) {
				1 {
					$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
					Write-Host $dateString "- Trocar para operadora 2"
					$cmdTroca = "wg set wggalpao peer 6TYMXmghs5vQZ3B+CoZdvxFwXIDeP+pdPHwvZ+e1ekM= endpoint dleite2.ddns.net:44990"
					Invoke-Expression $cmdTroca
					Start-Sleep -Seconds 10
				}
				2 {
					$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
					Write-Host $dateString "- Trocar para operadora 1"
					$cmdTroca = "wg set wggalpao peer 6TYMXmghs5vQZ3B+CoZdvxFwXIDeP+pdPHwvZ+e1ekM= endpoint dleite.ddns.net:44990"
					Invoke-Expression $cmdTroca
					Start-Sleep -Seconds 10
				}
				default {
					$dateString = Get-Date -Format 'yyyy-MM-dd_HH:mm:ss'
					Write-Host $dateString "- Comando falhou"
					break
				}
			}
		}
    }
}
