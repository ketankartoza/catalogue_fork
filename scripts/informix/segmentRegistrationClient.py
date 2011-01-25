from acscatalogue.models import *
from gearman import * 
import sys

# This is a gearman client for registering segment preview so 
# that we can clip out georeferenced thumbs. It will call 
# one or more gearman worker instances to do the processing. 
# A gearman worker is  a piece of python code designed to be 
# called via the gearman messaging queue. It is designed to be  
# parallised.
# To use this client, see first the notes in the worker 
# companion file and then do in a screen session:
#
# ./runDjangoScript.sh segmentRegistrationClient.py
#
# Tim Sutton June, 2010

def main(argv):
  mySuccesses = 0
  myRectifyErrors = 0

  ###################################
  # Gearman stuff
  ###################################
  myClient = GearmanClient(["127.0.0.1"])
  #myAuxFiles = AuxFile.objects.filter(original_id=262) # for testing
  #myAuxFiles = AuxFile.objects.all()[0:10] #for testing
  myAuxFiles = AuxFile.objects.all()
  #Process in blocks of 1000
  myLastJob = 0
  myTotalJobs = len( myAuxFiles )
  while myLastJob <= myTotalJobs:
    myRemainingJobs = myTotalJobs - myLastJob
    mySlice = None
    if myRemainingJobs < 1000:
      mySlice = myAuxFiles[myLastJob:myRemainingJobs]
    else:
      mySlice = myAuxFiles[myLastJob:myLastJob+1000]
    myLastJob+=1000

    myTasks = []
    for myAuxFile in mySlice:
      myTasks.append( myClient.dispatch_background_task( 'processFile', myAuxFile.id ) )
    for myTask in myTasks:
      #print myTask.result
      mySuccesses += 1
  print "Processed successfully: %s" % mySuccesses
  print "Errors: %s" % myRectifyErrors

#######################################################

if __name__ == "__main__":
  main(sys.argv)

