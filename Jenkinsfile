pipeline {
    agent any
    environment {
        VENV = 'venv'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python') {
            steps {
                sh 'python3 -m venv $VENV'
                sh '. $VENV/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. $VENV/bin/activate && pytest'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/screenshots/*.png', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                    publishHTML(target: [allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'reports', reportFiles: 'report.html', reportName: 'Test Report'])
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
