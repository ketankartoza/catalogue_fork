from PIL import Image
import os, sys
import traceback
from acscatalogue.models import *
from subprocess import call
from gearman import * 
from importutils import * #make sure the scripts dir is in your path!

# This is a gearman worker instance. A gearman worker is 
# a piece of python code designed to be called via the gearman 
# messaging queue. It is designed to be  parallised
# To use this worker (with multiple instances), open several tty's 
# in a screen session and run this command:
#
# ./runDjangoScript.sh sceneRegistrationWorker.py
#
# If the required data files are present on multiple systems, you 
# can do this accross servers too.
#
# Tim Sutton June, 2010

#######################################################
# Globals
#######################################################

mSegmentsPath = "/mnt/cataloguestorage/segments_out/"
mScenesPath = "/mnt/cataloguestorage/scenes_out_projected/"
#mSegmentsPath = "segments_out/"
#mScenesPath = "scenes_out_projected/"


#######################################################
def processScenes( theJob ):
  """Used by gearman"""
  myId = theJob.arg
  return processScenesUsingId( myId )


#######################################################
def processScenesUsingId( theId ):
  myAuxFile = AuxFile.objects.get( original_id=theId )
  mySegment = myAuxFile.segmentCommon
  myFrames = FrameCommon.objects.filter( segment=mySegment )
  for myFrame in myFrames:
    #clipImage is defined in importutils.py
    clipImage( mScenesPath, mSegmentsPath, myAuxFile, myFrame )
  return

#######################################################

def main(argv):
  # For testing you can pass a single id
  if len(argv) > 1:
    print "Running in test mode"
    processScenesUsingId( sys.argv[1] )
  else:
    print "Running as gearman worker"
    #--------------------------------------------
    # Setup gearman worker
    #--------------------------------------------
    worker = GearmanWorker( ["127.0.0.1"] )
    worker.register_function( "processScenes", processScenes )
    worker.work()

#######################################################

if __name__ == "__main__":
  main(sys.argv)

