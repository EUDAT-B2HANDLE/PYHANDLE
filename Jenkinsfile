pipeline {
    agent any
    options {
        checkoutToSubdirectory('PYHANDLE')
    }
    environment {
        PROJECT_DIR="PYHANDLE"
        GH_USER = 'newgrnetci'
        GH_EMAIL = '<argo@grnet.gr>'
    }
    stages {
        stage ('Run tests for each python version') {
            parallel {
                stage ('Test python 2.7') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/Dockerfile"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle"
                            args "-u root:root"
                        }
                    }
                    steps {
                        sh '''
                            cd $WORKSPACE/$PROJECT_DIR/pyhandle/tests
                            ./docker-entrypoint.sh coverage
                        '''
                        cobertura coberturaReportFile: '**/coverage.xml'
                    }
                }
                
                stage ('Test python 3.5') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/Dockerfile-py3.5"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.5"
                            args "-u root:root"
                        }
                    }
                    steps {
                        sh '''
                            cd $WORKSPACE/$PROJECT_DIR/b2handle/tests
                            ./docker-entrypoint.sh coverage
                        '''
                        cobertura coberturaReportFile: '**/coverage.xml'
                    }
                }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
} 
