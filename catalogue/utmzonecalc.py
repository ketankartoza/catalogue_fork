
#determine utm zone based on lat,lon
def utmZoneFromLatLon(theLon, theLat, theBuffer = 1):
  """Return the name of the UTM zone given a latitude and longitude.
     @return a tuple e.g. 32734, UTM34S"""
  mySuffix = None
  myPrefix = "326" #all north utm CRS's begin with 327
  myHemisphere = "N"
  if theLat < 0:
    myPrefix = "327"
    myHemisphere = "S"
  myZoneMin = -180
  myZoneIncrement = 6
  myCurrentZone = 1
  try:
    while myZoneMin < 180:
      if theLon >= myZoneMin and theLon < ( myZoneMin + 6 ):
        myResult = []
        mySuffix = "%02d" % myCurrentZone
        myResult.append((myPrefix+mySuffix,"UTM"+mySuffix+myHemisphere))
        #calcualte buffer
        mySuffix = "%02d" % (myCurrentZone+1)
        myResult.append((myPrefix+mySuffix,"UTM"+mySuffix+myHemisphere))
        mySuffix = "%02d" % (myCurrentZone-1)
        myResult.append((myPrefix+mySuffix,"UTM"+mySuffix+myHemisphere))
        
        return myResult
      myZoneMin += myZoneIncrement
      myCurrentZone += 1
    print "Point out of range for UTM zone calculation"
  except Exception, e:
    print "Failed to define a new UTM zone for Lon: %s, Lat: %s" % ( theLon, theLat )
    raise e
  return None
