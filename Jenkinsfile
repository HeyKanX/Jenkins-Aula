pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Preparar dependencias funcionales') {
            steps {
                powershell '''
                    py -3 -m venv .venv
                    & .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
                    & .\\.venv\\Scripts\\python.exe -m pip install -r tests\\functional\\requirements.txt
                    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                '''
            }
        }

        stage('Pruebas unitarias de backend') {
            steps {
                bat 'npm test'
            }
        }

        stage('Iniciar Aula Nova') {
            steps {
                powershell '''
                    if (Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue) {
                        throw 'El puerto 3000 ya está en uso en el agente Jenkins.'
                    }

                    $server = Start-Process -FilePath 'node' -ArgumentList 'backend/server.js' -PassThru -RedirectStandardOutput 'jenkins-server.log' -RedirectStandardError 'jenkins-server-error.log'
                    $server.Id | Set-Content -Path '.jenkins-server.pid'

                    $ready = $false
                    for ($attempt = 1; $attempt -le 30; $attempt++) {
                        try {
                            $response = Invoke-WebRequest -Uri 'http://127.0.0.1:3000/' -UseBasicParsing -TimeoutSec 1
                            if ($response.StatusCode -eq 200) {
                                $ready = $true
                                break
                            }
                        } catch {
                            Start-Sleep -Seconds 1
                        }
                    }

                    if (-not $ready) {
                        throw 'Aula Nova no inició en http://127.0.0.1:3000.'
                    }
                '''
            }
        }

        stage('Pruebas funcionales') {
            steps {
                powershell '''
                    New-Item -ItemType Directory -Force tests\\functional\\reports | Out-Null
                    & .\\.venv\\Scripts\\behave.exe tests\\functional\\features --junit --junit-directory tests\\functional\\reports
                    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                '''
            }
        }

        stage('Pruebas no funcionales con k6') {
            steps {
                powershell '''
                    $groups = @('rendimiento', 'estres', 'seguridad')
                    foreach ($group in $groups) {
                        Get-ChildItem -Path (Join-Path 'k6' $group) -Filter '*.js' | Sort-Object Name | ForEach-Object {
                            Write-Host "Ejecutando $($_.FullName)"
                            & k6 run $_.FullName
                            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                        }
                    }
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'tests/functional/reports/*.xml'
            archiveArtifacts artifacts: 'tests/functional/evidencias/**/*.png,tests/functional/reports/**/*.xml,jenkins-server*.log', allowEmptyArchive: true
            powershell '''
                if (Test-Path -LiteralPath '.jenkins-server.pid') {
                    $serverPid = [int](Get-Content -LiteralPath '.jenkins-server.pid')
                    $server = Get-Process -Id $serverPid -ErrorAction SilentlyContinue
                    if ($server) {
                        Stop-Process -Id $serverPid -Force
                    }
                    Remove-Item -LiteralPath '.jenkins-server.pid' -Force
                }
            '''
        }
    }
}
