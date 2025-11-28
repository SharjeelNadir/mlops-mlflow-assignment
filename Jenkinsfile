pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Pipeline Compilation (Run MLflow Pipeline)') {
            steps {
                echo 'Running pipeline.py to validate workflow...'
                bat '''
                    call venv\\Scripts\\activate
                    python pipeline.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving artifacts...'
            archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
        }
        success {
            echo 'Jenkins Pipeline completed successfully!'
        }
        failure {
            echo 'Jenkins Pipeline failed.'
        }
    }
}
