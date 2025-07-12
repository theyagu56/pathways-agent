pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = "0"  // Disable buildkit to avoid hang
        PATH = "/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/sbin:$PATH"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git checkout main'
            }
        }

        stage('Build and Deploy') {
            steps {
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5'
                sh '''
                set -e
                echo "🔄 Checking backend API (Cloudflare)..."
                curl -X POST https://api.jeffandsons.us/symptoms \
                    -H 'Content-Type: application/json' \
                    -d '{"symptoms": "test"}'
                echo "✅ Backend API healthy"

                echo "🔄 Checking frontend (Cloudflare)..."
                curl https://patient.jeffandsons.us
                echo "✅ Frontend healthy"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ PatientCopilot pipeline executed successfully.'
        }
        failure {
            echo '❌ Pipeline failed. Please check logs.'
        }
    }
}
