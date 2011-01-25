from django.contrib.gis import admin
from models import *



#
# Catalogue lookup tables
#


class DataModeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')}) 

class EllipsoidTypeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('description')})

class ErsCompModeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('description')})

class FileTypeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('fileTypeName')})

class HeaderTypeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})

class SatelliteAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})

class SensorAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})
  
class SpotAcquisitionModeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})

class StationAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})

  
class SuperclassAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})


#
# Main data tables
#
class MediumAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('medium')})
  field = (None, {'fields': ('mediumType')})
  field = (None, {'fields': ('numOfPasses')})
  field = (None, {'fields': ('timeCodeType')})
  field = (None, {'fields': ('storageStation')})
  field = (None, {'fields': ('mediumLoc')})
  field = (None, {'fields': ('density')})
  field = (None, {'fields': ('model')})
  field = (None, {'fields': ('headerType')})

class LocalizationAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('supertype')})
  #geoTimeInfo geoobject,
  field = (None, {'fields': ('refreshRate')})
  field = (None, {'fields': ('timeStamp')})

class SegmentCommonAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('satellite')})
  field = (None, {'fields': ('mission')})
  field = (None, {'fields': ('sensor')})
  field = (None, {'fields': ('medium')})
  field = (None, {'fields': ('ascendingFlag')})
  field = (None, {'fields': ('geoShape')})
  field = (None, {'fields': ('station')})
  field = (None, {'fields': ('insertionDate')})
  field = (None, {'fields': ('begRecordDate')})
  field = (None, {'fields': ('endRecordDate')})
  field = (None, {'fields': ('orbit')})
  field = (None, {'fields': ('cycle')})
  field = (None, {'fields': ('iLatMin')})
  field = (None, {'fields': ('iLonMin')})
  field = (None, {'fields': ('iLatMax')})
  field = (None, {'fields': ('iLonMax')})
  field = (None, {'fields': ('firstAddress')})
  field = (None, {'fields': ('secondAddress')})
  field = (None, {'fields': ('displayedTrack')})
  field = (None, {'fields': ('displayedOrbit')})
  field = (None, {'fields': ('displayedMedium')})
  field = (None, {'fields': ('npass')})
  field = (None, {'fields': ('timeStamp')})
  field = (None, {'fields': ('startBlock')})
  field = (None, {'fields': ('endBlock')})
  field = (None, {'fields': ('startFeet')})
  field = (None, {'fields': ('endFeet')})


class SceneAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('sensor')})
  field = (None, {'fields': ('source')})
  field = (None, {'fields': ('sourceId')})
  field = (None, {'fields': ('aquisitionDate')})
  field = (None, {'fields': ('imagePosition')})
  field = (None, {'fields': ('objects')})


class AuxFileAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('superType')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('fileName')})
  field = (None, {'fields': ('fileType')})
  field = (None, {'fields': ('fileDescription')})
  field = (None, {'fields': ('insertionDate')})
  field = (None, {'fields': ('visible')})
  #file blob  ,
     
    
     

   
  

class SpotSegmentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('segmentNumber')})
  field = (None, {'fields': ('hrvNum')})
  field = (None, {'fields': ('mode')})
  field = (None, {'fields': ('channel')})
  field = (None, {'fields': ('gain')})
  field = (None, {'fields': ('begTimeCod')})
  field = (None, {'fields': ('endTimeCod')})
  field = (None, {'fields': ('begFormat')})
  field = (None, {'fields': ('endFormat')})
  field = (None, {'fields': ('qualityFactor')})
  field = (None, {'fields': ('lookingAngle')})
  field = (None, {'fields': ('firstValidFc')})
  field = (None, {'fields': ('lastValidFc')})
  field = (None, {'fields': ('missingLinesFlag')})
  field = (None, {'fields': ('hrvConf')})
  field = (None, {'fields': ('mirrorStep')})
  field = (None, {'fields': ('triodeQfactor')})
     

class LandsatSegmentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('segmentOrder')})
  field = (None, {'fields': ('begTimeCode')})
  field = (None, {'fields': ('endTimeCode')})
  field = (None, {'fields': ('firstFrameFc')})
  field = (None, {'fields': ('lastFrameFc')})
  field = (None, {'fields': ('ellipsoid')})
  field = (None, {'fields': ('ellipsParam1')})
  field = (None, {'fields': ('ellipsParam2')})
  field = (None, {'fields': ('ellipsParam3')})
  field = (None, {'fields': ('ellipsParam4')})
  field = (None, {'fields': ('channel')})
  field = (None, {'fields': ('metaVersionNo')})
  field = (None, {'fields': ('bandPresent')})

class ErsSegmentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('segmentOrder')})
  field = (None, {'fields': ('rollAngle')})
  field = (None, {'fields': ('begTimeCode')})
  field = (None, {'fields': ('endTimeCode')})
  field = (None, {'fields': ('begFormat')})
  field = (None, {'fields': ('endFormat')})
  field = (None, {'fields': ('icuOnboardBegTime')})
  field = (None, {'fields': ('icuOnboardEndTime')})
  field = (None, {'fields': ('compressionMode')})
  field = (None, {'fields': ('firstFrameNum')})
  field = (None, {'fields': ('lastFrameNum')})
  field = (None, {'fields': ('pulseRepInt')})
  field = (None, {'fields': ('simpleRate')})
  field = (None, {'fields': ('calibSubAtt')})
  field = (None, {'fields': ('receivGain')})
  field = (None, {'fields': ('ellipsoid')})
  field = (None, {'fields': ('ellipsParam1')})
  field = (None, {'fields': ('ellipsParam2')})
  field = (None, {'fields': ('ellipsParam3')})
  field = (None, {'fields': ('ellipsParam4')})
  field = (None, {'fields': ('padFirstFrame')})
  field = (None, {'fields': ('padLastFrame')})
    
class NoaaSegmentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('dataMode')})
  field = (None, {'fields': ('eqcrxTime')})
  field = (None, {'fields': ('eqLon')})
  field = (None, {'fields': ('procLevel')})
  field = (None, {'fields': ('bandMode')})
  field = (None, {'fields': ('pixFormat')})
  field = (None, {'fields': ('arcCenter')})
    
class OrbviewSegmentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('dataMode')})
  field = (None, {'fields': ('eqcrxTime')})
  field = (None, {'fields': ('eqLon')})
  field = (None, {'fields': ('procLevel')})
  field = (None, {'fields': ('bandMod')})
  field = (None, {'fields': ('pixFormat')})
  field = (None, {'fields': ('arcCenter')})
    
class FrameCommonAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentId')})
  field = (None, {'fields': ('cloud')})
  field = (None, {'fields': ('cloudMean')})
  field = (None, {'fields': ('trackOrbit')})
  field = (None, {'fields': ('frame')})
  field = (None, {'fields': ('ordinal')})
  field = (None, {'fields': ('llLat')})
  field = (None, {'fields': ('urLon')})
  field = (None, {'fields': ('urLat')})
  field = (None, {'fields': ('ulLon')})
  field = (None, {'fields': ('ulLat')})
  field = (None, {'fields': ('llLon')})
  field = (None, {'fields': ('lrLat')})
  field = (None, {'fields': ('lrLon')})
  field = (None, {'fields': ('processable')})
  field = (None, {'fields': ('beginTimeCod')})
  field = (None, {'fields': ('endTimeCod')})

class SpotFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('begFormat')})
  field = (None, {'fields': ('endFormat')})
  field = (None, {'fields': ('firstValidFc')})
  field = (None, {'fields': ('lastValidFc')})
  field = (None, {'fields': ('dummySceneFlag')})
  field = (None, {'fields': ('missLines')})
  field = (None, {'fields': ('satMinVal')})
  field = (None, {'fields': ('satMaxVal')})
  field = (None, {'fields': ('centerTimeCod')})
  field = (None, {'fields': ('scLat')})
  field = (None, {'fields': ('scLon')})
  field = (None, {'fields': ('scDevLat')})
  field = (None, {'fields': ('scDevLon')})
  field = (None, {'fields': ('incidence')})
  field = (None, {'fields': ('orientation')})
  field = (None, {'fields': ('sunAz')})
  field = (None, {'fields': ('sunEl')})
    
class LandsatFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('centreLat')})
  field = (None, {'fields': ('centreLon')})
  field = (None, {'fields': ('centreTime')})
  field = (None, {'fields': ('sunAz')})
  field = (None, {'fields': ('sunElev')})
  field = (None, {'fields': ('fopScene')})
  field = (None, {'fields': ('hdShift')})
  field = (None, {'fields': ('sQuality')})
  field = (None, {'fields': ('sbPresent')})
  field = (None, {'fields': ('bGain')})
  field = (None, {'fields': ('bgChange')})
  field = (None, {'fields': ('bslgainchange')})

class ErsFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('frame')})
  field = (None, {'fields': ('meanI')})
  field = (None, {'fields': ('meanQ')})
  field = (None, {'fields': ('sdevI')})
  field = (None, {'fields': ('sdevQ')})
  field = (None, {'fields': ('missLinPerc')})
  field = (None, {'fields': ('dopplerCentroid')})
  field = (None, {'fields': ('blockNumber')})
  field = (None, {'fields': ('lineNumber')})
  field = (None, {'fields': ('maxI')})
  field = (None, {'fields': ('maxQ')})

class NoaaFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})

class OrbviewFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('localization')})

class OtherFrameAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('localization')})
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('dataMode')})
  field = (None, {'fields': ('eqCrxTime')})
  field = (None, {'fields': ('eqLon')})
  field = (None, {'fields': ('procLevel')})
  field = (None, {'fields': ('bandNumber')})
  field = (None, {'fields': ('pixFormat')})
  field = (None, {'fields': ('localization')})

class ErsCalNoiseAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('begNoise1')})
  field = (None, {'fields': ('begNoise2')})
  field = (None, {'fields': ('endNoise1')})
  field = (None, {'fields': ('endNoise2')})
  field = (None, {'fields': ('begCalib1')})
  field = (None, {'fields': ('begCalib2')})
  field = (None, {'fields': ('endCalib1')})
  field = (None, {'fields': ('endCalib2')})
    
class ErsDopCentAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('ordinal')})
  field = (None, {'fields': ('value')})
  field = (None, {'fields': ('format')})

class ErsQualityAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('numberofmlines')})
  field = (None, {'fields': ('overallquality')})
  field = (None, {'fields': ('qualitydensity')})
  field = (None, {'fields': ('missingLines')})
    
class ErsSampTimeAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('ordinal')})
  field = (None, {'fields': ('value')})
  field = (None, {'fields': ('format')})
    
class ErsStateVectorAdmin (admin.GeoModelAdmin):
  field = (None, {'fields': ('segmentCommon')})
  field = (None, {'fields': ('svtype')})
  field = (None, {'fields': ('posX')})
  field = (None, {'fields': ('posY')})
  field = (None, {'fields': ('posZ')})
  field = (None, {'fields': ('velX')})
  field = (None, {'fields': ('velY')})
  field = (None, {'fields': ('velZ')})
  field = (None, {'fields': ('ascNodeJdt')})
  field = (None, {'fields': ('referenceJdt')})
  field = (None, {'fields': ('binaryTime')})
  field = (None, {'fields': ('clockStepLength')})

admin.site.register(DataMode, DataModeAdmin)
admin.site.register(EllipsoidType, EllipsoidTypeAdmin)
admin.site.register(ErsCompMode, ErsCompModeAdmin)
admin.site.register(FileType, FileTypeAdmin)
admin.site.register(HeaderType, HeaderTypeAdmin)
admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SpotAcquisitionMode, SpotAcquisitionModeAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Superclass, SuperclassAdmin)
admin.site.register(SegmentCommon, SegmentCommonAdmin)
admin.site.register(Scene, SceneAdmin)
admin.site.register(AuxFile, AuxFileAdmin)
admin.site.register(Medium, MediumAdmin)
admin.site.register(Localization, LocalizationAdmin)
admin.site.register(SpotSegment, SpotSegmentAdmin)
admin.site.register(LandsatSegment, LandsatSegmentAdmin)
admin.site.register(ErsSegment, ErsSegmentAdmin)
admin.site.register(NoaaSegment, NoaaSegmentAdmin)
admin.site.register(OrbviewSegment, OrbviewSegmentAdmin)
admin.site.register(FrameCommon, FrameCommonAdmin)
admin.site.register(SpotFrame, SpotFrameAdmin)
admin.site.register(LandsatFrame, LandsatFrameAdmin)
admin.site.register(ErsFrame, ErsFrameAdmin)
admin.site.register(NoaaFrame, NoaaFrameAdmin)
admin.site.register(OrbviewFrame, OrbviewFrameAdmin)
admin.site.register(OtherFrame, OtherFrameAdmin)
admin.site.register(ErsCalNoise, ErsCalNoiseAdmin)
admin.site.register(ErsDopCent, ErsDopCentAdmin)
admin.site.register(ErsQuality, ErsQualityAdmin)
admin.site.register(ErsSampTime, ErsSampTimeAdmin)
admin.site.register(ErsStateVector , ErsStateVectorAdmin)
