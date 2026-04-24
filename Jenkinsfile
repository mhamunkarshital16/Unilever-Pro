pipeline {
    agent any

    environment {
        IMAGE_NAME = "moreshital16/unilever-app"
        TAG = "${BUILD_NUMBER}"
        KUBE_NAMESPACE_DEV = "unilever-dev"
        KUBE_NAMESPACE_QA = "unilever-qa"
        KUBE_NAMESPACE_UAT = "unilever-uat"
        KUBE_NAMESPACE_PROD = "unilever-prod"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/mhamunkarshital16/Unilever-Pro.git'
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
                sh 'docker build -t $IMAGE_NAME:$TAG .'
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:$TAG
                    '''
                }
            }
        }

        // 🔹 DEV Deployment (develop branch)
        stage('Deploy to DEV') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                kubectl set image deployment/unilever-app-dev \
                unilever-app-dev=$IMAGE_NAME:$TAG -n $KUBE_NAMESPACE_DEV
                '''
            }
        }

        // 🔹 QA Deployment (release branch)
        stage('Deploy to QA') {
            when {
                expression { env.BRANCH_NAME.startsWith("release") }
            }
            steps {
                sh '''
                kubectl set image deployment/unilever-app-qa \
                unilever-app-qa=$IMAGE_NAME:$TAG -n $KUBE_NAMESPACE_QA
                '''
            }
        }

        // 🔹 UAT Deployment (manual approval)
        stage('Approve for UAT') {
            when {
                expression { env.BRANCH_NAME.startsWith("release") }
            }
            steps {
                input message: "Approve deployment to UAT?"
            }
        }

        stage('Deploy to UAT') {
            when {
                expression { env.BRANCH_NAME.startsWith("release") }
            }
            steps {
                sh '''
                kubectl set image deployment/unilever-app-uat \
                unilever-app-uat=$IMAGE_NAME:$TAG -n $KUBE_NAMESPACE_UAT
                '''
            }
        }

        // 🔹 PROD Deployment (main branch)
        stage('Approve for PROD') {
            when {
                branch 'main'
            }
            steps {
                input message: "Approve deployment to PROD?"
            }
        }

        stage('Deploy to PROD') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                kubectl set image deployment/unilever-app-prod \
                unilever-app-prod=$IMAGE_NAME:$TAG -n $KUBE_NAMESPACE_PROD
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
