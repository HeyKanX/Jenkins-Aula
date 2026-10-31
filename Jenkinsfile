pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timeout(time: 45, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        // Separa esta ejecución de los contenedores locales del estudiante.
        COMPOSE_PROJECT_NAME = 'aula-nova-jenkins'
        AULA_NOVA_PORT = '3100'
        TIENDA_DEMO_PORT = '8181'
        SELENIUM_PORT = '4445'
        SELENIUM_VNC_PORT = '7901'
        TESTLINK_URL = 'http://app/lib/api/xmlrpc/v1/xmlrpc.php'
        TESTLINK_PIPELINE_ID = "Jenkins: ${BUILD_URL}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verificar Docker') {
            steps {
                sh '''
                    docker version --format '{{.Server.Version}}'
                    docker compose version
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose --profile tests build'
            }
        }

        stage('Environment') {
            steps {
                sh 'sh ci/prepare-reports.sh'
                sh 'sh ci/start-environment.sh'
            }
        }

        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-unit-tests.sh'
                }
            }
        }

        stage('Selenium') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-selenium.sh'
                }
            }
        }

        stage('Playwright') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-playwright.sh'
                }
            }
        }

        stage('Functional') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-functional.sh'
                }
            }
        }

        stage('Performance') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-k6-suite.sh rendimiento'
                }
            }
        }

        stage('Stress') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-k6-suite.sh estres'
                }
            }
        }

        stage('Security') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh 'sh ci/run-k6-suite.sh seguridad'
                }
            }
        }

        stage('TestLink') {
            steps {
                withCredentials([string(credentialsId: 'testlink-devkey', variable: 'TESTLINK_DEVKEY')]) {
                    sh 'python3 testlink/register_results.py'
                }
            }
        }

        stage('Reports') {
            steps {
                junit allowEmptyResults: true, testResults: 'reports/unit/*.xml,reports/selenium/*.xml,reports/playwright/*.xml,semana9/aula-nova/tests/functional/reports/*.xml'
                archiveArtifacts artifacts: 'reports/**/*,semana8/tienda-demo/evidencias/**/*,semana9/aula-nova/tests/functional/evidencias/**/*', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            sh 'sh ci/cleanup-environment.sh || true'
        }
    }
}
