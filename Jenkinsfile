pipeline{
 agent none
 stages {
   stage('Test'){
     agent{
       docker{
         image 'qnib/pytest'
       }
     }
     steps{
       sh 'py.test --verbose --junit-xml test-reports/results.xml tests/test_mpgw_commands.py'
     }
     post{
       always{
         junit 'test-reports/results.xml'
       }
     }
   }
   stage('Deliver'){
     agent{
       docker{
         image 'python:3.7.2'
       }
     }
     steps{
       sh 'pip install --upgrade setuptools'
       sh 'pip install -v -r requirements.txt'
       sh 'pip install pyinstaller --trusted-host=pypi.python.org'
       sh 'done'
       sh 'pyinstaller --onefile restonic.py'
     }
     post{
       success{
         archiveArtifacts 'dist/restonic'
       }
     }
   }
 } 
}