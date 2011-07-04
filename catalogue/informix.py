import os
import sys
import informixdb  # import the InformixDB module
import traceback
import glob
import Image

class Informix:
  """This class is a helper class to allow you to easily connect
  to the legacy informix database and execute queries there. It 
  is ported from version 1 of the catalogue where this logic was 
  contained in acscatalogue.informix.py"""

  def __init__(self):
    os.environ['INFORMIXSERVER']="catalog2"
    if not os.environ['INFORMIXSERVER']=="catalog2":
      print "We tried to set the INFORMIXSERVER environment variable for you but failed."
      print "You can try to set it manually before running this script from the bash prompt by doing this:"
      print "export INFORMIXSERVER=catalog2"
      sys.exit(0);
    self.mConnection = informixdb.connect('catalogue@catalog2', user='informix', password='')
    self.mCursor = self.mConnection.cursor(rowformat = informixdb.ROW_AS_DICT)
    # this line is needed for blob retrieval to work!
    informixdb.Connection.Sblob(self.mConnection)
    self.mHaltOnError = True
    # set informix output format to 4 (WKT)
    myWktSql="update GeoParam set value = 4 where id=3;"
    self.mCursor.execute(myWktSql)
    print("Constructor called")
    return

  def __del__(self):
    # Dont use logging.* in dtor - it truncates the log file deleting all other messages
    print ("Destructor called")
    # set informix output format to 0 (Geodetic / Informix native)
    myWktSql="update GeoParam set value = 0 where id=3;"
    self.mCursor.execute(myWktSql)
    self.mConnection.close()
    return 

  def haltOnError(self, theFlag):
    self.mHaltOnError = theFlag

  def runQuery(self, theQuery):
    """A helper function that allows you to run any sql statement
    against the informix backend.
    A collection of objects (one for each row) will be returned.
    Note you shouldnt use this for pulling out large recordsets 
    from the database (rather write a dedicated procedure that
    uses a cursor in that case."""
    self.mCursor.execute( theQuery )
    myRows = []
    for myRow in self.mCursor:
      myRows.append(myRow)
    return myRows

  def localization( self, theLocalization ):
    """Fetch a  localization record from the database given its id
       e.g. of what will be returned:
       {'object_supertype': 1, 'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 46), 
         'id': 1219163, 
         'refresh_rate': 0, 
         'geo_time_info': 
         'POLYGON((21.6 -32.76, 22.04 -31.04, 20.05 -30.75, 19.57 -32.46, 21.6 -32.76))'} 
    """
    myQuery = "select * from t_localization where id=%i;" % int( theLocalization )
    myRows = self.runQuery( myQuery )
    # There should only be one record
    if len( myRows ) > 1:
      raise Exception("Localization Rows","Too many localization rows returned for localization (received %s, expected 1)" % len(myRows) )
    if len( myRows ) < 1:
      raise Exception("Localization Rows","No rows returned for localization (received %s, expected 1)" % len(myRows) )

    return myRows[0]

  def frameForLocalization( self, theLocalizationId ):
    """Return a frame record given a localization record. Record returned will 
    look something like this:
           {'ordinal': 20, 
          'ur_lon': 22.040000915527344, 
          'lr_lat': -32.759998321533203, 
          'ul_lat': -30.75, 
          'll_lon': 19.569999694824219, 
          'segment_id': 163777, 
          'frame': 82, 
          'ul_lon': 20.049999237060547, 
          'll_lat': -32.459999084472656, 
          'lr_lon': 21.600000381469727, 
          'begin_time_cod': 21995.346796739504, 
          'localization_id': 1219163, 
          'processable': True, 
          'ur_lat': -31.040000915527344, 
          'cloud_mean': 0, 
          'track_orbit': 174, 
          'end_time_cod': 21995.347094024386, 
          'cloud': '0000****'}"""
    myFrameQuery = "select * from t_frame_common where localization_id=%i;" % int( theLocalizationId )
    myFrameRows = self.runQuery( myFrameQuery )
    # There should only be one record
    if len( myFrameRows ) > 1:
      raise Exception("FrameRows","Too many framerows returned for localization (received %s, expected 1)" % len(myFrameRows) )
    if len( myFrameRows ) < 1:
      raise Exception("FrameRows","Too few framerows returned for localization (received 0, expected 1)" )
    myFrameRow = myFrameRows[0]
    return myFrameRow

  def segmentForFrame( self, theSegmentId ):
    """Return a segment record given a frame id. Return should look 
    something liks this:
    {'sensor_id': 2, 
      'mission': 5, 
      'ascending_flag': False, 
      'satellite_id': 1, 
      'i_lon_max': 28.443050384521484, 
      'displayed_orbit': 138589, 
      'id': 163777, 
      'start_feet': 0, 
      'i_lon_min': 18.360977172851562, 
      'start_block': 0, 
      'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 44), 
      'end_block': 0, 
      'first_address': 20, 
      'insertion_date': 22005.361816053242, 
      'beg_record_date': 21995.341348495371, 
      'station_id': 19, 
      'geo_shape': 'POLYGON((26.733053 -2.30708, 26.2 -4.8, 25.89 -6.24, 25.58 -7.69, 25.26 -9.14, 24.94 -10.58, 24.62 -12.03, 24.3 -13.47, 23.97 -14.91, 23.64 -16.36, 23.31 -17.8, 22.97 -19.24, 22.63 -20.68, 22.28 -22.13, 21.92 -23.57, 21.56 -25, 21.2 -26.44, 20.82 -27.88, 20.44 -29.32, 20.05 -30.75, 19.65 -32.18, 19.24 -33.62, 18.360977 -36.550076, 20.507157 -36.867314, 21.3 -33.92, 21.68 -32.48, 22.04 -31.04, 22.41 -29.6, 22.76 -28.16, 23.11 -26.72, 23.45 -25.28, 23.79 -23.84, 24.13 -22.39, 24.46 -20.95, 24.78 -19.51, 25.1 -18.06, 25.42 -16.62, 25.74 -15.17, 26.06 -13.73, 26.37 -12.28, 26.68 -10.83, 26.99 -9.39, 27.3 -7.94, 27.6 -6.49, 27.91 -5.04, 28.443051 -2.5631083, 26.733053 -2.30708))', 
      'end_feet': 0, 
      'cycle': 138589, 
      'displayed_medium': '1927', 
      'medium_id': 163777, 
      'end_record_date': 21995.347863935185, 
      'i_lat_max': -2.3070800304412842, 
      'i_lat_min': -36.867313385009766, 
      'npass': 1, 
      'orbit': 174, 
      'displayed_track': '174', 
      'second_address': 22}"""


    mySegmentQuery = "select * from t_segment_common where id=%i;" % int( theSegmentId )
    mySegmentRows = self.runQuery( mySegmentQuery )
    # There should only be one record
    if len( mySegmentRows ) > 1:
      raise Exception("SegmentRows","Too many segment rows returned for frame (received %s, expected 1)" % len(mySegmentRows) )
    if len( mySegmentRows ) < 1:
      raise Exception("SegmentRows","Too few segment rows returned for frame (received 0, expected 1)" )
    mySegmentRow = mySegmentRows[0]
    return mySegmentRow



  def auxfileForSegment( self, theSegmentId ):
    """ Return an auxfile for a segment. An auxfile is the thing that 
    actually contains the quicklook blob in it.
    {'visible': False, 
    'file_type': 8, 
    'file_name': 'TM5_T174_S19_20100322_Jpeg', 
    'insertion_date': 22005.361816469907, 
    'file_description': 'Quick look', 
    'file': <_informixdb.Sblob object at 0x23716c0>, 
    'object_supertype': 1, 
    'common_id': 163777, 
    'id': 191795}
 
    The blob will contain the actual segment quicklook.
    
    """
    myAuxFileQuery = "select * from t_aux_files where common_id=%i;" % int( theSegmentId )
    myAuxFileRows = self.runQuery( myAuxFileQuery )
    # There should only be one record
    if len( myAuxFileRows ) > 1:
      raise Exception("AuxFileRows","Too many auxfile rows returned for segment (received %s, expected 1)" % len(myAuxFileRows) )
    if len( myAuxFileRows ) < 1:
      raise Exception("AuxFileRows","Too few auxfile rows returned for segment (received 0, expected 1)" )
    myAuxFileRow = myAuxFileRows[0]
    myBlob = myAuxFileRow['file']
    #try:
    #  myBlob.open()
    #  myStats = myBlob.stat()
    #  #print "Blob stats: size = %s" % str(myStats['size'])
    #except Exception, myException:
    #  print "Sblob open failed (%s)" % str(myException)
    #try:
    #  # First write the whole blob out to a file
    #  myData = myBlob.read(myBlob.stat()['size'])
    #  myFile.write(myData)
    #  #print "Wrote " + myFileName

    #except Exception, myException:
    #  print "Sblob read failed (%s)" % str(myException)
    #  sys.exit(0);
    return myAuxFileRow

  def fileTypeForAuxFile(self, theFileTypeId):
    """Return the file type for a given auxfile
    e.g. {'file_type_name': 'SHOWJPEG', 'id': 8}
    """
    myFileTypeQuery = "select * from t_file_types where id=%i;" % theFileTypeId
    myFileTypeRows = self.runQuery( myFileTypeQuery )
    # There should only be one record
    if len( myFileTypeRows ) > 1:
      raise Exception("FileTypeRows","Too many filetype rows returned for auxfile (received %s, expected 1)" % len(myFileTypeRows) )
    if len( myFileTypeRows ) < 1:
      raise Exception("FileTypeRows","Too few filetype rows returned for auxfile (received 0, expected 1)" )
    myFileTypeRow = myFileTypeRows[0]
    return myFileTypeRow


  def thumbForLocalization(self, theLocalizationId):
    """Given a localization id, return its georeferenced thumbnail as a jpg
    Note: You need to hand build PIL - see install notes for details!
    >>> from catalogue.informix import Informix
    >>> myI = Informix()
    Constructor called
    >>> myI.thumbForLocalization( 1000000 )
    Writing segment image with dimensions x: 1004, y: 17496
    >>>
    """

    #print sys.path.append
    myLocalizationRow = self.localization( theLocalizationId )
    myFrameRow = self.frameForLocalization( theLocalizationId )  
    mySegmentRow = self.segmentForFrame( myFrameRow['segment_id'] )
    myAuxFileRow = self.auxfileForSegment( myFrameRow['segment_id'] )
    myFileTypeRow = self.fileTypeForAuxFile( myAuxFileRow['file_type'] )
    try:
      return self.referencedThumb( myLocalizationRow, myFrameRow, mySegmentRow, myAuxFileRow, myFileTypeRow )
    except:
      raise

  def referencedThumb(self, theLocalizationRow, theFrameRow, theSegmentRow, theAuxFileRow, theFileTypeRow ):
    """Given complete rows of loc, frame, segment, auxfile and file type, return a
    jpg thumbnail which is georeferenced.
    Note: You need to hand build PIL - see install notes for details!
    """
    mySegmentId = theFrameRow['segment_id']
    myBlob = theAuxFileRow['file']
    try:
      mySegmentJpg = self.extractBlobToJpeg( mySegmentId, myBlob )
    except:
      raise

  ########################################################
  # Helper functions for blob extraction to jpgs
  ########################################################

  def getBlockPositionsForBlob(self, theBlob ):
    """In each blob is a series of embedded jpg images. This
       function computes the offset of the start of each
       jpg image by looking for the initial JFIF tag. It
       returns a list of these block offsets"""
    myLength = len( theBlob )
    #print "File Length: %s" % myLength
    myPosition = 0
    myLastPosition = 0
    theFileNo = 0
    myList = []
    while not myPosition < 0:
      theFileNo = theFileNo + 1
      myLastPosition = myPosition
      #print "Searching from : %s" % ( myPosition + 10 )
      myPosition = theBlob.find( "JFIF", myPosition + 10 ) - 6
      #print "JFIF at %s" % (myPosition )
      if myLastPosition > 0 and myPosition > 0:
        myList.append( myPosition )
      elif len( myList ) == 0:
        myList.append( myPosition )
      else:
        myList.append( myLength )
      #print "myPosition: %s " % myPosition
      #print "myLastPosition: %s " % myLastPosition

    return myList

  def blockToData(self, theStart, theEnd, theBlob ):
    """Extracts a block of binary date from a blob"""
    theBlob.seek( theStart )
    myBlockValue = theBlob.read( theEnd - theStart )
    return myBlockValue

  def dataToImage(self, theData, theFile ):
    """Saves a block of binary data as file"""
    #print "Saving %s" % theFile
    myJpg = open( theFile, mode='wb' )
    myJpg.write( theData )
    myJpg.close()

  def createGroupFile(self, theFileList, theOutputFile ):
    """This function will merge 1 or more images into a single file.
       The images will be pasted into incremental positions down the file.
       Note: You need to hand build PIL - see install notes for details!"""
    #print theFileList

    if len( theFileList ) < 1:
      return
    if os.path.exists( theOutputFile ):
      os.remove( theOutputFile )


    # Open the first image to get its dims
    myWidth = 0
    myHeight = 0
    for myFile in theFileList:
      myImage = Image.open( myFile )
      # Get the image metrics nicely so we can paste it into the quad image
      mySize = myImage.size
      myX = mySize[0]
      myY = mySize[1]
      myHeight += myY
      if myX > myWidth:
        myWidth = myX

    print "Writing segment image with dimensions x: %i, y: %i" % (int(myWidth),int(myHeight))
    mySize = ( myWidth, myHeight )
    myOutImage = Image.new( "RGB", mySize )

    myLastY = 0
    for myFile in theFileList:
      myImage = Image.open( myFile )
      mySize = myImage.size
      myX = mySize[0]
      myY = mySize[1]
      #determine the position to paste the block into
      myBox = ( 0, myLastY, myX, myLastY + myY )
      # now paste the blocks in
      try:
        myOutImage.paste( myImage, myBox )
        myLastY += myY
      except IOError as e:
        traceback.print_exc(file=sys.stdout)
        raise
      except ValueError:
        print "Image %s,%s can't go into %s,%s at position 0,%s" % (myX,myY,myWidth,myHeight,myLastY-myY)
        myLastY += myY
        continue
    # save up
    myOutImage.save( theOutputFile )


  def removeBlocks(self, theArray ):
    """This function removes temporary files containing blocks
       (individual jpg sub images)."""
    for myBlockFile in theArray:
      try:
        os.remove( myBlockFile )
      except:
        pass

  def extractBlobToJpeg(self, theSegmentId, theBlob ):
    myBlobFileName = os.path.join( "/tmp/", str( theSegmentId ) + ".blob" )
    myFile = file( myBlobFileName, "wb")
    try:
      theBlob.open()
      myStats = theBlob.stat()
      #print "Blob stats: size = %s" % str(myStats['size'])
    except Exception, myException:
      print "Sblob open failed (%s)" % str(myException)
      raise
    try:
      # First write the whole blob out to a file
      myData = theBlob.read(theBlob.stat()['size'])
      myFile.write(myData)
      myFile.close()
      #print "Wrote " + myFileName

    except Exception, myException:
      print "Sblob read failed (%s)" % str(myException)
      raise


    myBlob = open(myBlobFileName, mode='rb')
    myValue = myBlob.read()
    myArray = self.getBlockPositionsForBlob( myValue )
    #print myArray
    # used to hold filenames that will be combined into a single file
    myGroupFileArray = []
    myBlockTally = 0
    myErrorTally = 0
    #print "%s block(s) in this file" % ( len( myArray ) - 1 )
    for myPosition in range ( 0,len( myArray ) ):
      if myPosition == 0:
        continue # skip the first position marker
      myBlockTally += 1
      myStart = myArray[ myPosition -1 ]
      myEnd = myArray[ myPosition ]
      myData = self.blockToData( myStart, myEnd, myBlob )
      myJpgFile = "/tmp/%sblock%s.jpg" % ( theSegmentId, myBlockTally )
      self.dataToImage( myData, myJpgFile )
      myGroupFileArray.append( myJpgFile )
    # We are accummulating files in blocks of myBlocksInGroup
    # or any remaining at the end of the segment
    # write this group of myBlocksInGroup files into a single file
    # print "Block Tally: %s" % myBlockTally
    myJpegFileName = os.path.join( "/tmp/", str( theSegmentId ) + ".jpg" )
    #print 'Writing %s' % myJpegFileName
    try:
      self.createGroupFile( myGroupFileArray, myJpegFileName )
      self.removeBlocks( myGroupFileArray )
      os.remove( myBlobFileName )
    except IOError as e:
      if e.errno == 28: #out of space exception
        print "Fatal Error - out of disk space!"
        print "Last file processed was: %s" % myFile
        print e
        traceback.print_exc(file=sys.stdout)
        raise
    except Exception as e:
      self.removeBlocks( myGroupFileArray )
      os.remove( myBlobFileName )
      raise


