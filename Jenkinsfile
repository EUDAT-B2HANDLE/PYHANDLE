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
                branch 'devel'
            }      
            agent {
               // dockerfile {
               //     filename "docs/Dockerfile"
                //    dir "$PROJECT_DIR"
//                    additionalBuildArgs "-t eudat-pyhandle:docs"
                 //   args "-u root:root"
                docker {
                    image 'eudat-pyhandle:py3.10'
                
                }
            }
            steps {
                echo 'Publish Sphinx docs...'
                sh '''
                    cd $WORKSPACE/$PROJECT_DIR
                    cd docs
                    make html
                '''
            }
       }
    }
    post {
        always {
            cleanWs()
        }
    }
} 
