from catalogue.informix import Informix
myFile = file( "lastlandsat.txt", "rwt" )
myLastRecord = myFile.read()
myFile.close()
myI = Informix()
myQuery = 'select FIRST %i * from t_landsat_frame where localization_id > %s' % ( 20000, myLastRecord )
myRows = myI.runQuery( myQuery )
myErrorCount=0
myOkCount=0
for myRow in myRows:
  try:
    myLastRecord = myRow['localization_id']
    myI.thumbForLocalization( myRow['localization_id'] )
    myFile = file( "lastlandsat.txt", "rwt" )
    myFile.write( myLastRecord )
    myFile.close()
    myOkCount+=1
  except:
    myErrorCount+=1
    continue
print "Completed: %s imports ok, %s errors" % (myOkCount, myErrorCount)
