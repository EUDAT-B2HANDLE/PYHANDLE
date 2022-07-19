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
                            filename "pyhandle/tests/testdockers/Dockerfile"
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
                            filename "pyhandle/tests/testdockers/Dockerfile-py3.5"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.5"
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
                stage ('Test python 3.6') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/testdockers/Dockerfile-py3.6"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.6"
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
                stage ('Test python 3.7') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/testdockers/Dockerfile-py3.7"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.7"
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
                 stage ('Test python 3.9') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/testdockers/Dockerfile-py3.9"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.9"
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
                stage ('Test python 3.10') {
                    agent {
                        dockerfile {
                            filename "pyhandle/tests/testdockers/Dockerfile-py3.10"
                            dir "$PROJECT_DIR"
                            additionalBuildArgs "-t eudat-pyhandle:py3.10"
                            args "-u root:root"
                        }
                    }
                    steps {
                        sh '''
                            cd $WORKSPACE/$PROJECT_DIR/pyhandle/tests
                            ./docker-entrypoint-310.sh coverage
                        '''
                        cobertura coberturaReportFile: '**/coverage.xml'
                    }
                }
            }
       }
       stage ('Deploy Docs') {
            when {
                changeset 'docs/source/**'
            }   
            agent {
                docker {
                    image 'eudat-pyhandle:py3.10'
                
                }
            }
            steps {
                echo 'Build Sphinx docs...'
                sh '''
                    cd $WORKSPACE/$PROJECT_DIR
                    cd docs
                    make html
                '''
                echo 'Sending to gh-pages...'
                sshagent (credentials: ['jenkins-master']) {
                    sh '''
                        cd $WORKSPACE/$PROJECT_DIR/build/html
                        mkdir ~/.ssh && ssh-keyscan -H github.com > ~/.ssh/known_hosts
                        git config --global user.email ${GH_EMAIL}
                        git config --global user.name ${GH_USER}
                        GIT_USER=${GH_USER} USE_SSH=true 
                        git checkout gh-pages
                    '''
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
