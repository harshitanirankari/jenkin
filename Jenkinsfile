pipeline {
  agent any
  
  environment {
    IMAGE_NAME = 'jenkin:latest'
    CONTAINER_PORT = '8080'
    DEPLOY_PORT = '80'
    REPO_URL = 'https://github.com/harshitanirankari/jenkin.git'
    REPO_BRANCH = 'main'
  }

  stages {
    stage('Initial Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Project Checkout') {
      steps {
        echo "Checking out from ${env.REPO_URL}, branch: ${env.REPO_BRANCH}"
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${env.REPO_BRANCH}"]],
          doGenerateSubmoduleConfigurations: false,
          extensions: [],
          submoduleCfg: [],
          userRemoteConfigs: [[
            credentialsId: 'github-credentials-2',
            url: "${env.REPO_URL}"
          ]]
        ])
      }
    }

    stage('Build') {
      steps {
        echo "Building Docker image: ${env.IMAGE_NAME}"
        bat "docker build -t ${env.IMAGE_NAME} ."
      }
    }

    stage('Test') {
      steps {
        echo "Running tests..."
        bat 'if exist tests\\test.bat (call tests\\test.bat) else (echo No test script found)'
      }
    }

    stage('Deploy') {
      steps {
        echo "Deploying the website..."
        bat "docker rm -f website || exit 0"
        bat "docker run -d --name website -p ${env.DEPLOY_PORT}:${env.CONTAINER_PORT} ${env.IMAGE_NAME}"
      }
    }

    stage('Deploy to Render') {
      steps {
        bat 'curl -X POST https://api.render.com/deploy/srv-cvvtqi49c44c73f9uud0?key=8XmRVPBC1fs'
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded."
    }
    failure {
      echo "Pipeline failed."
    }
    always {
      echo "Pipeline execution completed."
    }
  }
}
