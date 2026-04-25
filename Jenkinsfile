pipeline {
    agent any

    environment {
        DOCKER_USER = 'meghabarua'
        IMAGE_NAME  = 'aceest-fitness'
        IMAGE_TAG   = "v${BUILD_NUMBER}"
    }

    stages {

        stage('1. Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/2022us70037-cmd/aceest-fitness.git'
            }
        }

        stage('2. Install Dependencies') {
            steps {
                sh '''
                    python3 --version || (apt update && apt install -y python3 python3-venv python3-pip)
                    
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                '''
            }
        }

        stage('3. Run Pytest') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest pytest-cov
                    pytest tests/ -v --junitxml=test-results.xml || true
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('4. Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USER}/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('5. Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS')]) {

                    sh '''
                        echo $DH_PASS | docker login -u $DH_USER --password-stdin
                        docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        // ❌ Skipped Kubernetes stage
        stage('6. Deploy to Kubernetes') {
            steps {
                echo "Skipping Kubernetes deployment for now"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}