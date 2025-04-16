pipeline {
  agent any
  environment {
    // Default values (can be overridden by .env file)
    IMAGE_NAME = ''
    CONTAINER_PORT = ''
    DEPLOY_PORT = ''
    REPO_URL = ''
    REPO_BRANCH = ''
  }
  stages {
    stage('Load Environment Variables') {
      steps {
        script {
          // Read the .env file and set environment variables
          def envVars = readFile('.env').split('\n')
          envVars.each { line ->
            if (line.trim() && !line.startsWith('#')) {
              def parts = line.split('=')
              if (parts.size() == 2) {
                // Fix: Use env.setProperty instead of direct array access
                env.setProperty(parts[0].trim(), parts[1].trim())
              }
            }
          }
        }
      }
    }
    stage('Checkout') {
      steps {
        git branch: "${env.REPO_BRANCH}", url: "${env.REPO_URL}"
      }
    }
    stage('Build') {
      steps {
        echo "Building Docker image..."
        sh "docker build -t ${env.IMAGE_NAME} ."
      }
    }
    stage('Test') {
      steps {
        echo "Running tests..."
        sh "chmod +x tests/test.sh"
        sh "./tests/test.sh"
      }
    }
    stage('Deploy') {
      steps {
        echo "Deploying the website..."
        sh "docker rm -f website || true"
        sh "docker run -d --name website -p ${env.DEPLOY_PORT}:${env.CONTAINER_PORT} ${env.IMAGE_NAME}"
      }
    }
    stage('Deploy to Render') {
      steps {
        withCredentials([string(credentialsId: 'render-api-key', variable: 'RENDER_API_KEY')]) {
          script {
            def serviceId = "srv-cvvtqi49c44c73f9uud0"
            def deployUrl = "https://api.render.com/deploy/${serviceId}?key=${RENDER_API_KEY}"
            sh "curl -X POST ${deployUrl}"
          }
        }
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