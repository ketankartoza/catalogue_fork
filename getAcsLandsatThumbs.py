from catalogue.informix import Informix
myFile = file( "lastlandsat.txt", "rt" )
myLastRecord = myFile.read()
myFile.close()
myI = Informix()
myQuery = 'select count(*) as count from t_landsat_frame'
myRows = myI.runQuery( myQuery )
print "Total number of landsat recs in ACS %s" % myRows[0]['count']
myQuery = 'select FIRST %i * from t_landsat_frame where localization_id > %s' % ( 50000, myLastRecord )
myRows = myI.runQuery( myQuery )
myErrorCount=0
myOkCount=0
for myRow in myRows:
  try:
    myLastRecord = myRow['localization_id']
    myI.thumbForLocalization( myRow['localization_id'] )
    myFile = file( "lastlandsat.txt", "wt" )
    myFile.write( str(myLastRecord) )
    myFile.close()
    myOkCount+=1
  except:
    myErrorCount+=1
    raise
myI.cleanup()
print "Completed: %s imports ok, %s errors" % (myOkCount, myErrorCount)
