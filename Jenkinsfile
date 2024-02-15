pipeline {
    agent any
    environment {
        USER_CAUSE = "${currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause')}"
        BUILD_RESULT = "${currentBuild.currentResult}"
    }
    stages {
        stage('Stage1') {
            steps {
                script {
                    sh "echo ${JOB_NAME}"
                    env.GIT_BRANCH = env.BRANCH_NAME
                    echo env.BRANCH_NAME
                    // Extracting Pipeline Trigger User
                    def match = USER_CAUSE =~ /userName:(\w+)/

                    if (match) {
                        USER_NAME = match[0][1]
                    }
                    
                    env.USER_NAME = "${USER_NAME}"
                    echo env.USER_NAME
                }
                script {
                    // Extracting Stage 1 Duration
                    def duration1String = currentBuild.durationString
                    def match1 = duration1String =~ /(\d+\.\d+)/
                    def extractedValue1 = match1 ? match1[0][0] : null
                    echo "Stage 1 Duration: ${extractedValue1} milliseconds"
                    env.Stage1Duration = extractedValue1
                }
                script {
                    def check = BUILD_RESULT
                    env.Stage1Status = check
                    sh "echo ${Stage1Status}"
                }
            }
        }
        stage ('Stage2') {
            agent any
            steps {
                script {
                    sh "echo ${JOB_NAME}"
                }
                script {
                    // Extracting Stage2 Duration
                    def duration2String = currentBuild.durationString
                    def match2 = duration2String =~ /(\d+\.\d+)/
                    def extractedValue2 = match2 ? match2[0][0] : null
                    echo "Stage 2 Duration: ${extractedValue2} milliseconds"
                    env.Stage2Duration = extractedValue2
                }
                script {
                    def check2 = BUILD_RESULT
                    env.Stage2Status = check2
                    sh "echo ${Stage2Status}"
                }
            }   
        }
    }
    post { 
        always { 
            script {
                withCredentials([string(credentialsId: 'e2fe5270-046a-4aee-b1e6-657f705a7489', variable: 'APPLICATIONINSIGHTS_CONNECTION_STRING')]) {
                sh 'python3 user_meta.py'
                }
            }
        }
    }
}
