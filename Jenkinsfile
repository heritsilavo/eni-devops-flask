
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'eni-flask-app'
        IMAGE_TAG = '1.0'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Python Tests') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$IMAGE_TAG \
                        python -m unittest -v test
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$IMAGE_TAG \
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

                        IMAGE="$DOCKERHUB_USER/eni-flask-app:$IMAGE_TAG"

                        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE"

                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            -u "$DOCKERHUB_USER" \
                            --password-stdin

                        docker push "$IMAGE"
                        docker logout
                    '''
                }
            }
        }

        
    stage('Kubernetes Connection') {
        steps {
            withCredentials([
                file(
                    credentialsId: 'kubernetes-kubeconfig',
                    variable: 'KUBECONFIG'
                )
            ]) {
                sh '''
                    kubectl get deployment eni-flask -n default
                    kubectl auth can-i patch deployment/eni-flask -n default
                '''
            }
        }
    }

    }

    post {
        success {
            echo 'Flask CI/CD Pipeline SUCCESS'
        }

        failure {
            echo 'Flask CI/CD Pipeline FAILED'
        }
    }
}
