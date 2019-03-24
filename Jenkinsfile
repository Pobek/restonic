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
         image 'cdrx/pyinstaller-linux:python3'
       }
     }
     steps{
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