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
# ./runDjangoScript.sh segmentRegistrationWorker.py
#
# If the required data files are present on multiple systems, you 
# can do this accross servers too.
#
# Tim Sutton June, 2010

#######################################################
# Globals
#######################################################

mBasePath = "/mnt/cataloguestorage/segments_out/"
#mBasePath = "segments_out/"



#######################################################
def processFile( theJob ):
  myAuxFile = AuxFile.objects.get(id=theJob.arg)
  #rectifyImage is defined in importutils.py
  return rectifyImage( mBasePath, myAuxFile )

#######################################################

def main(argv):
  #--------------------------------------------
  # Setup gearman worker
  #--------------------------------------------
  worker = GearmanWorker(["127.0.0.1"])
  worker.register_function("processFile", processFile)
  worker.work()

#######################################################

if __name__ == "__main__":
  main(sys.argv)

