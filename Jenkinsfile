pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        CI = 'true'
        CHROME_BIN = '/usr/bin/chromium'
    }

    stages {
        stage('Verificar herramientas') {
            steps {
                sh '''
                    node --version
                    npm --version
                    python3 --version
                    chromium --version
                    k6 version
                '''
            }
        }

        stage('Preparar dependencias funcionales') {
            steps {
                sh '''
                    rm -rf .venv tests/functional/reports
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r tests/functional/requirements.txt
                    mkdir -p tests/functional/reports
                '''
            }
        }

        stage('Pruebas unitarias de backend') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'npm test'
                }
            }
        }

        stage('Iniciar Aula Nova') {
            steps {
                sh '''
                    if [ -f .jenkins-server.pid ] && kill -0 "$(cat .jenkins-server.pid)" 2>/dev/null; then
                        echo 'Ya existe un servidor de Aula Nova en este workspace.'
                        exit 1
                    fi

                    nohup node backend/server.js > jenkins-server.log 2> jenkins-server-error.log &
                    echo $! > .jenkins-server.pid

                    for attempt in $(seq 1 30); do
                        if curl --fail --silent http://127.0.0.1:3000/ > /dev/null; then
                            exit 0
                        fi
                        sleep 1
                    done

                    echo 'Aula Nova no inició en http://127.0.0.1:3000.'
                    exit 1
                '''
            }
        }

        stage('Pruebas funcionales') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '.venv/bin/behave tests/functional/features --junit --junit-directory tests/functional/reports'
                }
            }
        }

        stage('Pruebas no funcionales con k6') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        status=0
                        for group in rendimiento estres seguridad; do
                            for script in k6/"$group"/*.js; do
                                echo "Ejecutando $script"
                                k6 run "$script" || status=1
                            done
                        done
                        exit "$status"
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'tests/functional/reports/*.xml'
            archiveArtifacts artifacts: 'tests/functional/evidencias/**/*.png,tests/functional/reports/**/*.xml,jenkins-server*.log', allowEmptyArchive: true
            sh '''
                if [ -f .jenkins-server.pid ]; then
                    kill "$(cat .jenkins-server.pid)" 2>/dev/null || true
                    rm -f .jenkins-server.pid
                fi
            '''
        }
    }
}
