import sys
import struct # for reading binary data into a struct
import os # for creating folders
import shutil # for moving files
import glob # file glob for iterating dir
import traceback
import re # regexp
from acscatalogue.models import *

##########################################################
#
# Before running this script either do this:
#
# export DJANGO_SETTINGS_MODULE=settings
# export PYTHONPATH=../
#
# then run the script from in the sac dir:
#
# python 3_organise_thumbs.py
#
# Or use the convenience bash django script launcher I wrote
# e.g.
#
# scripts/runDjangoScript.sh 3_organise_thumbs.py
#
##########################################################


mInputDir = '/mnt/cataloguestorage/scenes_out_projected/'
def main(argv):
    myCount = 0
    if not os.path.isdir(mInputDir):
        try:
            os.makedirs(mInputDir)
        except OSError:
            print "Failed to make output directory...quitting"
            sys.exit(0);

    for myDir in glob.glob(os.path.join(mInputDir, '*')):
        for myFile in glob.glob(os.path.join(mInputDir, myDir, '*')):

            #run the appropriate function from our functionlist:
            print "Processing: " + myFile
            try:
                myFileBase = os.path.split(myFile)[1]
                myFileBase = os.path.splitext(myFileBase)[0]
                myRegexp = re.compile( '^[0-9]*' )
                myFileId = myRegexp.search( myFileBase ).group()
                myRegexp = re.compile( 'scn[0-9]*' )
                mySceneId = myRegexp.search( myFileBase ).group()
                print "copying file::  %s , scene %s" % ( myFileId, mySceneId )
            except:
                print "Regex found no match, skipping"
                continue
            myCount = myCount +1
            #
            # Find a matching auxfile and from there work out what
            # the segment and sensor were. The original blob extract
            # script saves thumbs using the auxfile id + scn + scn counter
            # and now we are going to save them as segment_id + scn + scn counter
            #
            try:
                myAuxFile = AuxFile.objects.get( original_id = myFileId )
                if myAuxFile:
                    mySegment = myAuxFile.segmentCommon
                    print "Sensor for this segment is:" + str( mySegment.sensor )
                    myDate = mySegment.begRecordDate
                    myOutputDir = "thumbs_out" + "/" + str(mySegment.sensor.name).replace(" ","_").replace(",","_")
                    if not os.path.isdir( myOutputDir ):
                        try:
                            os.makedirs( myOutputDir )
                        except OSError:
                            print "Failed to make output directory...quitting"
                            sys.exit(0);
                    myNewFile = myOutputDir + "/" + str(mySegment.id) + mySceneId + ".jpg"
                    print "Moving " + myFile + " to " + myNewFile
                    shutil.move(myFile,myNewFile)
            except:
                print "No matching auxfile original id found !"
                sys.exit(0)

            # we do this because we need to run multiple times due to mem overflow
            #if myCount > 100:
            #  sys.exit(0)
    print "-------------------------"
    print "----- ALL DONE ----------"
    print "-------------------------"

if __name__ == "__main__":
    main(sys.argv)
