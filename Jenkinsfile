pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "moreshital16/unilever-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'feature/login', url: 'https://github.com/mhamunkarshital16/Unilever-Pro.git'
            }
        }

        stage('Build Application') {
            steps {
                sh 'echo "Building application..."'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Running tests..."'
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to DEV') {
            steps {
                sh 'echo "Deploying to DEV..."'
            }
        }

        stage('Deploy to QA') {
            steps {
                input message: 'Approve deployment to QA?', ok: 'Deploy'
                sh 'echo "Deploying to QA..."'
            }
        }

        stage('Deploy to UAT') {
            steps {
                input message: 'Approve deployment to UAT?', ok: 'Deploy'
                sh 'echo "Deploying to UAT..."'
            }
        }

        stage('Deploy to PROD') {
            steps {
                input message: 'Approve deployment to PROD?', ok: 'Deploy'
                sh 'echo "Deploying to PROD..."'
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
