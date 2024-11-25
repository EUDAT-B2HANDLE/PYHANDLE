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
        stage ('Test python 3.11') {
            agent {
                dockerfile {
                    filename "pyhandle/tests/testdockers/Dockerfile-py3.11"
                    dir "$PROJECT_DIR"
                    additionalBuildArgs "-t eudat-pyhandle:py3.11"
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
        stage ('Test python 3.12') {
            agent {
                dockerfile {
                    filename "pyhandle/tests/testdockers/Dockerfile-py3.12"
                    dir "$PROJECT_DIR"
                    additionalBuildArgs "-t eudat-pyhandle:py3.12"
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
        stage ('Upload to PyPI'){
            when {
                branch 'master'
            }
            agent {
                docker {
                    image 'argo.registry:5000/python3'
                }
            }
            steps {
                echo 'Build python package'
                withCredentials(bindings: [usernamePassword(credentialsId: 'pyhandle-pypi-token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        cd ${WORKSPACE}/$PROJECT_DIR
                        pipenv install --dev
                        pipenv run python setup.py sdist bdist_wheel
                        pipenv run python -m twine upload -u $USERNAME -p $PASSWORD dist/*
                    '''
                }
            }
            post {
                always {
                    cleanWs()
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
            
                echo 'Sending to gh-pages...'
                sshagent (credentials: ['jenkins-master']) {
                    sh '''
                         
                        ls ~/
                        mkdir ~/.ssh && ssh-keyscan -H github.com > ~/.ssh/known_hosts
                        git config --global user.email ${GH_EMAIL}
                        git config --global user.name ${GH_USER}
                        GIT_USER=${GH_USER} 
                        USE_SSH=true 
                        cd $WORKSPACE/$PROJECT_DIR
                        cd docs
                        make html
                        cd $WORKSPACE/$PROJECT_DIR/docs/build/html
                        touch .nojekyll
                        rm -rf .git   
                        git init
                        git remote add deploy git@github.com:EUDAT-B2HANDLE/PYHANDLE
                        git checkout -b gh-pages
                        git add .
                        git commit -am "docs update"
                        git push deploy gh-pages --force
                        rm -rf .git                        
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
