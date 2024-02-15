pipeline {
    agent any
    environment {
        USER_CAUSE = "${currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause')}"
        BUILD_RESULT = "${currentBuild.result}"
    }
    stages {
        stage('Extract User Info') {
            steps {
                script {
                    // Parse the USER_CAUSE string to extract userName
                    def match = USER_CAUSE =~ /userName:(\w+)/

                    if (match) {
                        USER_NAME = match[0][1]
                    }
                    
                    env.USER_NAME = "${USER_NAME}"
                    echo "User Name: ${USER_NAME}"
                }
            }
        }
        stage ('user_meta') {
            agent any
            steps {
                script {
                    def durationString = currentBuild.durationString
                    def match = durationString =~ /(\d+\.\d+)/
                    def extractedValue = match ? match[0][0] : null
                    echo "Stage 2 Duration: ${extractedValue} milliseconds"
                    env.BUILD_DURATION = extractedValue
                }
            }   
        }
    }
    post { 
        always { 
            script {
                withCredentials([string(credentialsId: 'e2fe5270-046a-4aee-b1e6-657f705a7489', variable: 'APPLICATIONINSIGHTS_CONNECTION_STRING')]) {
                sh 'python3 user_meta.py'
                sh "echo $USER_NAME"
                }
            }
        }
    }
}
