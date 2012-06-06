#!/usr/bin/python

#
# Before you run this script, do: export INFORMIXSERVER=catalog2
# Currently the following filetypes exist:
#
# select t.file_type_name, count(*) from t_aux_files f inner join
# t_file_types t on f.file_type=t.id group by t.file_type_name;
#
# file_type_name  SHOWJPEG
# (count(*))      151406
#
# file_type_name  JPEG
# (count(*))      4343
#
# file_type_name  SHOWJPEG_B4
#(count(*))      31233
#
#

import sys
import informixdb  # import the InformixDB module
import struct # for reading binary data into a struct
import os # for creating folders
# ------------------------------------
# open connection to database 'stores'
# ------------------------------------
#myConnection = informixdb.connect('catalogue>informix', user='informix', password='')
myConnection = informixdb.connect('catalogue@catalog2', user='informix', password='')

# ----------------------------------
# allocate cursor and execute select
# ----------------------------------
myCursor = myConnection.cursor(rowformat = informixdb.ROW_AS_DICT)
# this line is needed for blob retrieval to work!
informixdb.Connection.Sblob(myConnection)

# 1 Landsat
# 2 Mos
# 3 J_Ers
# 4 Spot
# 5 E-Ers
# 6 Irs
# 7 Radarsat
# 8 Noaa
# 9 Orbview


myCursor.execute("select first 100 f.id, f.file, t.file_type_name from (t_aux_files f inner join t_file_types t on f.file_type=t.id) inner join t_segment_common s on f.common_id = s.id where f.common_id = s.id and t.file_type_name='JPEG';")
    # and s.satellite_id=5;")
    # or t.file_type_name='JPEG';")

# make a dir for our images
myOutputDir = '/tmp/thumbs'
if not os.path.isdir(myOutputDir):
    try:
        os.makedirs(myOutputDir)
    except OSError:
        print "Failed to make output directory...quitting"
        myConnection.close()
        sys.exit(0);


for myRow in myCursor:

    # -------------------------------------------
    # delete myRow if column 'code' begins with 'C'
    # -------------------------------------------
    print '--'
    print "Writing %s image %s to %s " % (myRow['file_type_name'],myRow['id'], myOutputDir)
    myFileType = myRow['file_type_name']
    myFile = ''
    myFileBase = ''
    myHeaderFile = ''
    #print "Writing image %s to %s " % (str(myRow['file'])), myOutputDir
    if myFileType == 'JPEG':
        myFile = file( myOutputDir + '/id' + str(myRow['id'])  + '.jpg', "wb")
    else:
        myFileBase = myOutputDir + '/id' + str(myRow['id'])
        myFile = file( myFileBase  + '.sjpg', "wb")
        myHeaderFile = file( myFileBase  + '.txt', "wt")

    myBlob = myRow['file']
    try:
        myBlob.open()
        myStats = myBlob.stat()
        #print "Blob stats: size = %s" % str(myStats['size'])
    except Exception, myException:
        print "Sblob open failed (%s)" % str(myException)
    try:
        # First write the whole blob out to a file
        myData = myBlob.read(myBlob.stat()['size'])
        myFile.write(myData)

        #now rewind and read the first 44 bytes which comprise the header for the file
        if myFileType == 'SHOWJPEG':
            myFile.close()
            myFile = file( myOutputDir + '/id' + str(myRow['id'])  + '.sjpg', "rb")
            myFile.seek(0)
            print 'Read to pos: %s' % (myFile.tell())
            myMagicNumber = struct.unpack('>L',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(),myMagicNumber)
            myVideoFormat = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(),myVideoFormat)
            myLineSize = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(),myLineSize)
            myLinesNumber = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(),myLinesNumber)
            myLinesPerJpegBlock = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myLinesPerJpegBlock)
            myJpegBlockNumber = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myJpegBlockNumber)
            myLinesPerLastJpegBlock = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myLinesPerLastJpegBlock)
            myPaddingAtSegmentStart = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myPaddingAtSegmentStart)
            myPaddingAtSegmentEnd = struct.unpack('>l',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myPaddingAtSegmentEnd)
            myPixelSizeX = struct.unpack('>f',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myPixelSizeX)
            myPixelSizeY = struct.unpack('>f',myFile.read(4))[0]
            print 'Read to pos: %s, value %s' % (myFile.tell(), myPixelSizeY)

            myHeaderFile.write( "Unix file Type ")
            myHeaderFile.write( "myMagicNumber          : " + str( myMagicNumber )  + "\n")
            myHeaderFile.write( "Video Format (1=B&W, 3=RGB) ")
            myHeaderFile.write( "myVideoFormat          : " + str( myVideoFormat )  + "\n")
            myHeaderFile.write( "Length in pixels of EBP line ")
            myHeaderFile.write( "myLineSize,            : " + str( myLineSize )  + "\n")
            myHeaderFile.write( "Number of linus in the decompressed EBP file ")
            myHeaderFile.write( "myLinesNumber          : " + str( myLinesNumber )  + "\n")
            myHeaderFile.write( "Number of original lines in each JPEG compressed block ")
            myHeaderFile.write( "myLinesPerJpegBlock    : " + str( myLinesPerJpegBlock )  + "\n")
            myHeaderFile.write( "Number of JPEG blocks ")
            myHeaderFile.write( "myJpegBlockNumber      : " + str( myJpegBlockNumber )  + "\n")
            myHeaderFile.write( "Number of compressed lines for the last JPEG block ")
            myHeaderFile.write( "myLinesPerLastJpegBlock: " + str( myLinesPerLastJpegBlock )  + "\n")
            myHeaderFile.write( "Number of black lines inserted at the beginning of EBP decompressed file ")
            myHeaderFile.write( "myPaddingAtSegmentStart: " + str( myPaddingAtSegmentStart )  + "\n")
            myHeaderFile.write( "Number of black lines inserted at the end of EBP decompressed file ")
            myHeaderFile.write( "myPaddingAtSegmentEnd  : " + str( myPaddingAtSegmentEnd )  + "\n")
            myHeaderFile.write( "Pixel size in x direction (meters) ")
            myHeaderFile.write( "myPixelSizeX           : " + str( myPixelSizeX )  + "\n")
            myHeaderFile.write( "Pixel size in y direction (meters) ")
            myHeaderFile.write( "myPixelSizeY           : " + str( myPixelSizeY )  + "\n")

            # Read the header for each jpeg block
            myBlockDict ={}
            for myBlock in range(1,myJpegBlockNumber):
                #print '------------'
                myBlockStart = struct.unpack('>l',myFile.read(4))[0]
                #print 'Read to pos: %s, first jpeg block starts at: %s' % (myFile.tell(), myBlockStart)
                myBlockLength = struct.unpack('>l',myFile.read(4))[0]
                #print 'Read to pos: %s, first jpeg block length at: %s' % (myFile.tell(), myBlockLength)
                myHeaderFile.write( "Block %s starts at %s, length %s\n" % (myBlock,myBlockStart,myBlockLength))
                myBlockDict[myBlock]=[myBlockStart,myBlockLength]

            # now loop through the blocks extracting their images to jpg files
            for myKey in myBlockDict:
                myFileName = myFileBase + "blk" + str(myKey) + ".jpg"
                myValue = myBlockDict[myKey]
                myBlockStart = myValue[0]
                myBlockLength = myValue[1]
                myFile.seek(myBlockStart)
                myBlockFile = file( myFileName, "wb")
                myBlockFile.write(myFile.read(myBlockLength))
                myBlockFile.close()

    except Exception, myException:
        print "Sblob read failed (%s)" % str(myException)
        myConnection.close()
        sys.exit(0);

    myBlob.close()
    myFile.close()

    if myFileType == 'SHOWJPEG':
        myHeaderFile.close()
# ---------------------------------------
# commit transaction and close connection
# ---------------------------------------
myConnection.close()

sys.exit(0);
