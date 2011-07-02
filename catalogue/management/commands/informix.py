import os
import sys
import informixdb  # import the InformixDB module
import traceback

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

