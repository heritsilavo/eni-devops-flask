
pipeline {
    agent any

    environment {
        IMAGE_REPO = 'heritsilavo/eni-flask-app'
        DOCKER_IMAGE = "heritsilavo/eni-flask-app:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t "$DOCKER_IMAGE" .'
            }
        }

        stage('Python Tests') {
            steps {
                sh '''
                    docker run --rm "$DOCKER_IMAGE" \
                        python -m unittest -v test
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker run --rm "$DOCKER_IMAGE" \
                        python -c "from app import app; c=app.test_client(); assert c.get('/').status_code == 200"
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -eu

                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            -u "$DOCKERHUB_USER" \
                            --password-stdin

                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        docker push "$DOCKER_IMAGE"
                    '''
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubernetes-kubeconfig',
                        variable: 'KUBECONFIG'
                    )
                ]) {
                    sh '''
                        set -eu

                        kubectl set image \
                            deployment/eni-flask \
                            flask="$DOCKER_IMAGE" \
                            -n default

                        kubectl rollout status \
                            deployment/eni-flask \
                            -n default \
                            --timeout=180s

                        kubectl get deployment eni-flask \
                            -n default
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Flask CI/CD + Kubernetes Deployment SUCCESS'
        }

        failure {
            echo 'Flask CI/CD + Kubernetes Deployment FAILED'
        }
    }
}
