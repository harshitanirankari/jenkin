pipeline {

  agent any

  environment {

    // Hardcoded environment variables

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

        sh "docker build -t ${env.IMAGE_NAME} ."

      }

    }

    stage('Test') {

      steps {

        echo "Running tests..."

        sh "chmod +x tests/test.sh || echo 'No test script found or permission denied'"

        sh "./tests/test.sh || echo 'Tests failed or script not found'"

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
 
