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
       stage ('Deploy Docs') {
          //  when {
            //    branch 'devel'
            //}
            agent {
                dockerfile {
                    filename "docs/Dockerfile"
                    dir "$PROJECT_DIR"
                    additionalBuildArgs "-t eudat-pyhandle:docs"
                    args "-u root:root"
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
