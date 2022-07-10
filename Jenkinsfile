#!/usr/bin/env groovy
pipeline {
    agent any
    environment {
        EMAIL_RECIPIENTS = 'shashank.dx1992@gmail.com'
    }
    stages {
        stage('Build image and push it to ECR') {
            steps {
                script {
                    echo 'Pulling...' + env.BRANCH_NAME
                    def image = sh "cat values.yaml | tail -2 | head -1 | cut -d ":" -f2"
                    def tag = sh "cat values.yaml | tail -2 | head -1 | cut -d ":" -f3" 
                    sh "docker build -t ${image}:${tag} ."
                }
            }
        }
    }
}