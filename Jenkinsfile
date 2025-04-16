pipeline {

  agent any

  environment {

    IMAGE_NAME = ''

    CONTAINER_PORT = ''

    DEPLOY_PORT = ''

  }

  stages {

    stage('Initial Checkout') {

      steps {

        checkout scm

      }

    }

    stage('Load Environment Variables') {

      steps {

        script {

          def envFile = fileExists('.env') ? readFile('.env') : ''

          if (envFile) {

            echo "Loading environment variables from .env file"

            def envVars = envFile.split('\n')

            envVars.each { line ->

              if (line.trim() && !line.startsWith('#')) {

                def parts = line.split('=', 2)

                if (parts.size() == 2) {

                  def key = parts[0].trim()

                  def value = parts[1].trim()

                  env.setProperty(key, value)

                  echo "Set ${key}=${value}"

                }

              }

            }

          } else {

            echo "Warning: .env file not found"

          }

        }

      }

    }

    stage('Project Checkout') {

      steps {

        script {

          if (env.REPO_URL?.trim() && env.REPO_BRANCH?.trim()) {

            echo "Checking out from ${env.REPO_URL}, branch: ${env.REPO_BRANCH}"

            // Use the same credential ID used in the initial checkout

            checkout([

              $class: 'GitSCM',

              branches: [[name: "*/${env.REPO_BRANCH}"]],

              doGenerateSubmoduleConfigurations: false,

              extensions: [],

              submoduleCfg: [],

              userRemoteConfigs: [[

                credentialsId: 'github-credentials-2',  // Important: Use your GitHub credentials ID here

                url: "${env.REPO_URL}"

              ]]

            ])

          } else {

            echo "Skipping additional checkout - using files from initial checkout"

          }

        }

      }

    }

    stage('Build') {

      steps {

        script {

          if (env.IMAGE_NAME?.trim()) {

            echo "Building Docker image..."

            sh "docker build -t ${env.IMAGE_NAME} ."

          } else {

            error "IMAGE_NAME environment variable is not set"

          }

        }

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

        script {

          if (env.DEPLOY_PORT?.trim() && env.CONTAINER_PORT?.trim() && env.IMAGE_NAME?.trim()) {

            echo "Deploying the website..."

            sh "docker rm -f website || true"

            sh "docker run -d --name website -p ${env.DEPLOY_PORT}:${env.CONTAINER_PORT} ${env.IMAGE_NAME}"

          } else {

            error "Required environment variables for deployment are not set"

          }

        }

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
 